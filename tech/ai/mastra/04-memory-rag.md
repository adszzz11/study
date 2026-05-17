---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
  - memory
  - rag
status: studying
---

# 04. Memory & RAG — 심화

> 이 문서는 Mastra의 **Memory 4계층 시스템**과 **RAG 파이프라인**을 다룹니다.

---

## 1. Memory — 4계층 모델

LLM은 stateless하므로 멀티턴 대화에 컨텍스트가 필요하다. Mastra의 Memory는 **네 가지 레이어**를 합성해 컨텍스트를 만든다.

```
┌──────────────────────────────────────────────────────┐
│                Final System Context                  │
├──────────────────────────────────────────────────────┤
│  ① Message History     → 최근 N개의 raw message      │
│  ② Working Memory      → 사용자 프로필 / 선호도       │
│  ③ Semantic Recall     → 의미 유사 과거 메시지        │
│  ④ Observational Memory→ LLM이 압축한 관찰 로그       │
└──────────────────────────────────────────────────────┘
                       ▲
                       │ resourceId + threadId로 스코핑
                       │
                  ┌────────────┐
                  │  Storage   │ ← LibSQL / Postgres / D1 / ...
                  └────────────┘
```

### 1.1. 가장 단순한 메모리

```typescript
import { Mastra } from '@mastra/core'
import { LibSQLStore } from '@mastra/libsql'

export const mastra = new Mastra({
  storage: new LibSQLStore({ id: 'storage', url: ':memory:' }),
})
```

```typescript
import { Agent } from '@mastra/core/agent'
import { Memory } from '@mastra/memory'

export const memoryAgent = new Agent({
  id: 'memory-agent',
  name: 'Memory Agent',
  model: 'openai/gpt-5.4',
  memory: new Memory({
    options: { lastMessages: 20 },   // ← Message History 길이
  }),
})
```

### 1.2. resourceId / threadId — 스코핑 규칙

| 식별자 | 의미 | 변경 가능? |
|--------|------|------------|
| `resource` | 사용자/엔티티의 안정적 ID (`user-123`, `project-42`) | 한번 정해지면 thread의 owner로 고정 |
| `thread`   | 한 세션/대화 ID (`conversation-2026-05-17`) | 새 대화마다 새 ID |

```typescript
await memoryAgent.generate('My favorite color is blue.', {
  memory: { resource: 'user-123', thread: 'chat-1' },
})

await memoryAgent.generate("What's my favorite color?", {
  memory: { resource: 'user-123', thread: 'chat-1' },
})
// → "Your favorite color is blue."
```

> **주의**: 같은 `thread`에 다른 `resource`를 쓰면 오류. thread는 한 resource에 종속된다.

### 1.3. ① Message History — 가장 기본

`options.lastMessages: N` 만큼의 raw 메시지를 컨텍스트에 끼워 넣는다. **단순/빠름**, 하지만 길어지면 컨텍스트 윈도우를 빠르게 잡아먹는다.

### 1.4. ② Working Memory — 사용자 메타데이터

이름, 선호도, 진행 중인 목표 등 **세션 전반에서 유용한 구조화 데이터**.

```typescript
new Memory({
  options: {
    workingMemory: {
      enabled: true,
      template: `
- User Name:
- Timezone:
- Preferences:
      `,
    },
  },
})
```

LLM이 자체적으로 이 템플릿을 채우고 업데이트한다. `scope: 'resource'`가 기본이므로 **여러 thread에 걸쳐 공유**된다.

### 1.5. ③ Semantic Recall — 의미 기반 회상

과거 메시지를 임베딩해 두고, 현재 질문과 유사한 메시지를 가져온다.

```typescript
new Memory({
  options: {
    semanticRecall: {
      topK: 3,
      messageRange: { before: 2, after: 1 },  // 매치된 메시지 주변 컨텍스트
      scope: 'resource',  // 'thread'면 같은 대화 안에서만
    },
  },
})
```

> 키워드 매칭이 아니라 **의미** 매칭이므로 "그때 말한 그 회사" 같은 모호한 회상이 가능하다.

### 1.6. ④ Observational Memory — 긴 대화 대응 (권장)

긴 대화에서 메시지 히스토리가 컨텍스트를 잠식하는 문제를 해결.

```typescript
new Memory({
  options: {
    observationalMemory: true,
  },
})
```

작동 방식:
1. **백그라운드 에이전트**가 주기적으로 오래된 메시지를 읽고
2. 핵심 사실/관찰만 **dense observation log**로 압축
3. 압축된 observation이 raw history를 대체

**관찰만 남기므로 컨텍스트 윈도우가 일정하게 유지됨**. 1.0에서 공식 권장.

### 1.7. 멀티에이전트 메모리

```typescript
// 같은 resource, 다른 thread → working memory + semantic embedding 공유
await researcher.generate('Find info about quantum computing.', {
  memory: { resource: 'project-42', thread: 'research-session' },
})

await writer.generate('Summarize from research notes.', {
  memory: { resource: 'project-42', thread: 'writing-session' },
})
```

| 공유 종류 | 설정 | 효과 |
|-----------|------|------|
| **Resource-scoped** (기본) | 같은 `resource`, 다른 `thread` | Working memory + Semantic embedding 공유, message history는 격리 |
| **Thread-scoped** | 같은 `resource`, 같은 `thread` | 전체 메시지 히스토리 공유 (Observational memory 기본) |
| **Supervisor 위임** | 자동 | 새 thread, deterministic `{parent}-{agentName}` resource. 부모 컨텍스트는 messageFilter로 제어 |

### 1.8. Memory Processors — 컨텍스트 압축/필터

컨텍스트가 모델 한도를 넘으면 동작하는 후처리:

```typescript
new Memory({
  processors: [
    new TokenLimiter({ limit: 8000 }),
    new ToolCallFilter({ exclude: ['debugTool'] }),
  ],
})
```

---

## 2. RAG — Retrieval Augmented Generation

Mastra RAG는 **5단계 표준 파이프라인**이다.

```
[Raw Docs]
   │
   ▼  ① MDocument.fromText / .fromMarkdown / .fromHtml / .fromPdf
[MDocument]
   │
   ▼  ② doc.chunk({ strategy, size, overlap })
[Chunks]
   │
   ▼  ③ embedMany({ values, model })
[Embeddings]
   │
   ▼  ④ vectorStore.upsert({ indexName, vectors, metadata })
[Vector DB]
   │
   ▼  ⑤ vectorStore.query({ queryVector, topK })
[Relevant Chunks → 프롬프트로 주입]
```

### 2.1. 풀 예제

```typescript
import { embedMany } from 'ai'
import { PgVector } from '@mastra/pg'
import { MDocument } from '@mastra/rag'
import { ModelRouterEmbeddingModel } from '@mastra/core/llm'

// ① Document 로드
const doc = MDocument.fromText(`Your document text here...`)

// ② Chunking
const chunks = await doc.chunk({
  strategy: 'recursive',
  size: 512,
  overlap: 50,
})

// ③ Embedding
const { embeddings } = await embedMany({
  values: chunks.map(c => c.text),
  model: new ModelRouterEmbeddingModel('openai/text-embedding-3-small'),
})

// ④ Vector store
const pgVector = new PgVector({
  id: 'pg-vector',
  connectionString: process.env.POSTGRES_CONNECTION_STRING!,
})

await pgVector.upsert({
  indexName: 'docs',
  vectors: embeddings,
  metadata: chunks.map((c, i) => ({ text: c.text, chunkIndex: i })),
})

// ⑤ Query
const queryVector = /* embed the user query the same way */
const results = await pgVector.query({
  indexName: 'docs',
  queryVector,
  topK: 3,
})
console.log(results)
```

### 2.2. Chunking 전략

| `strategy` | 설명 | 적합한 문서 |
|------------|------|--------------|
| `recursive` | 재귀적으로 큰 구분자 → 작은 구분자로 분할 | 일반 텍스트 (기본 권장) |
| `character` | 문자 수 기반 단순 분할 | 정형 텍스트 |
| `markdown` | Markdown 구조(헤딩) 기반 | 마크다운 문서 |
| `html` | HTML 시멘틱 분할 | 웹 페이지 |
| `token` | 토큰 단위 분할 | 모델 입력 한도 정확히 맞출 때 |

### 2.3. 지원 Vector Store

`@mastra/pg` (pgvector), `@mastra/pinecone`, `@mastra/qdrant`, `@mastra/mongodb`, `@mastra/chroma`, `@mastra/upstash`, `@mastra/turbopuffer` 등. **공통 인터페이스**: `upsert`, `query`, `createIndex`, `deleteIndex`, `listIndexes`.

### 2.4. RAG를 도구로 노출 — `createVectorQueryTool`

가장 흔한 패턴은 RAG를 **Agent의 도구**로 감싸는 것:

```typescript
import { createVectorQueryTool } from '@mastra/rag'

const docsRag = createVectorQueryTool({
  vectorStoreName: 'pg-vector',     // mastra에 등록된 store id
  indexName: 'docs',
  model: new ModelRouterEmbeddingModel('openai/text-embedding-3-small'),
})

export const supportAgent = new Agent({
  id: 'support-agent',
  instructions: `Answer with grounded facts from docsRag.`,
  model: 'openai/gpt-5.4',
  tools: { docsRag },
})
```

→ LLM이 필요할 때 알아서 도구를 호출 → 임베딩 → 유사 청크 인출 → 답변 생성.

### 2.5. GraphRAG — 관계 기반 검색

문서 사이의 **의미적 관계 그래프**를 만들어, 단순 top-k 코사인보다 풍부한 컨텍스트를 검색.

```typescript
import { createGraphRAGTool } from '@mastra/rag'

const graphRag = createGraphRAGTool({
  vectorStoreName: 'pg-vector',
  indexName: 'docs',
  model: new ModelRouterEmbeddingModel('openai/text-embedding-3-small'),
  graphOptions: { dimension: 1536, threshold: 0.7 },
})
```

`docs A` 와 `docs B`가 의미적으로 강하게 연결돼 있으면, A를 인출했을 때 B도 자동으로 함께 가져온다. 한 청크가 다른 청크의 컨텍스트를 보강해 답변 품질이 올라간다.

### 2.6. RAG 평가

Mastra Evals 패키지에 **RAG-specific scorer**가 있다:
- **Faithfulness** — 답변이 검색된 컨텍스트에 충실한지
- **Context Relevancy** — 검색된 컨텍스트가 질문과 관련 있는지
- **Context Recall** — 정답이 들어있어야 할 컨텍스트가 인출됐는지

[[06-evals-observability]] 에서 자세히.

---

## 3. Memory ↔ RAG 차이 정리

| 항목 | Memory | RAG |
|------|--------|-----|
| 무엇을 저장 | 대화 메시지, 사용자 메타 | 외부 문서 |
| 누가 씀 | Agent 자동 | Agent가 도구로 호출 |
| 인덱싱 단위 | 메시지 | 청크 |
| 스코프 키 | `resourceId` / `threadId` | `indexName` |
| 갱신 빈도 | 매 turn | 문서 변경 시 |

> 실무 시스템은 **둘 다** 함께 쓴다. Memory는 "사용자가 누구인지", RAG는 "회사 지식".

---

## 다음 문서

- [[05-tools-mcp]] — Tools와 MCP 통합 패턴
- [[06-evals-observability]] — Scorer와 Tracing
