---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
  - architecture
status: studying
---

# 02. Architecture — 내부 구조와 실행 흐름

> 이 문서는 Mastra의 **컴포넌트 토폴로지**와 **요청 → 응답까지의 실행 흐름**을 설명합니다.

---

## 1. 컴포넌트 토폴로지

```
                ┌────────────────────────────────────┐
                │      Your TS Application           │
                │  (Next.js / Express / Hono / etc.) │
                └──────────────┬─────────────────────┘
                               │  imports
                               ▼
        ┌──────────────────────────────────────────────────────┐
        │            Mastra Instance  (src/mastra/index.ts)     │
        │  new Mastra({ agents, workflows, storage, scorers })  │
        │                                                       │
        │   Shared services:                                    │
        │     - Logger                                          │
        │     - Storage (LibSQL / Postgres / D1 / ...)          │
        │     - Vector Store (pgvector / Pinecone / Qdrant)     │
        │     - Telemetry (OTEL exporter or bridge)             │
        │     - Agent / Workflow / Scorer registry              │
        └─────┬──────────────┬──────────────┬─────────────┬─────┘
              │              │              │             │
              ▼              ▼              ▼             ▼
        ┌─────────┐   ┌────────────┐  ┌──────────┐   ┌─────────┐
        │ Agents  │   │ Workflows  │  │  Tools   │   │ Memory  │
        │         │   │            │  │  (MCP)   │   │  / RAG  │
        └────┬────┘   └─────┬──────┘  └────┬─────┘   └────┬────┘
             │              │              │              │
             └──────────────┴──────┬───────┴──────────────┘
                                   ▼
                    ┌────────────────────────────┐
                    │     Vercel AI SDK Core     │
                    │  generateText / streamText │
                    │  generateObject / tool()   │
                    └────────────┬───────────────┘
                                 ▼
                    ┌────────────────────────────┐
                    │   Model Router             │
                    │   "openai/gpt-5.4"         │
                    │   "anthropic/claude-5"     │
                    │   "google/gemini-3-pro"    │
                    └────────────────────────────┘
```

### 핵심 통찰

- **`Mastra` 인스턴스는 DI 컨테이너**다. Agent/Workflow를 직접 import해서도 쓸 수 있지만, `mastra.getAgentById()` / `mastra.getWorkflow()`로 가져와야 storage·logger·telemetry 같은 **공유 리소스에 자동 연결**된다.
- **Vercel AI SDK가 LLM 호출 레이어**다. Mastra는 그 위에 "에이전트 루프 / 메모리 주입 / 도구 변환 / 트레이싱"을 얹는다.
- **Model Router**는 `"provider/model"` 문자열로 모델을 추상화. 코드 한 줄로 OpenAI ↔ Anthropic ↔ Google ↔ Bedrock 등을 스왑.

---

## 2. 디렉토리 구조 (관용)

`npm create mastra@latest` 가 만드는 기본 구조:

```
src/
└── mastra/
    ├── index.ts              ← Mastra 인스턴스 (DI 컨테이너)
    ├── agents/
    │   └── weather-agent.ts  ← Agent 정의
    ├── workflows/
    │   └── content-flow.ts   ← Workflow 정의
    ├── tools/
    │   └── weather-tool.ts   ← Tool 정의
    └── scorers/
        └── relevancy.ts      ← 커스텀 Scorer
```

### Mastra 인스턴스 (index.ts)

```typescript
import { Mastra } from '@mastra/core'
import { LibSQLStore } from '@mastra/libsql'
import { weatherAgent } from './agents/weather-agent'
import { contentWorkflow } from './workflows/content-flow'

export const mastra = new Mastra({
  agents: { weatherAgent },
  workflows: { contentWorkflow },
  storage: new LibSQLStore({
    id: 'mastra-storage',
    url: process.env.DATABASE_URL ?? ':memory:',
  }),
})
```

`agents`, `workflows`, `scorers`는 **객체의 키 이름이 곧 식별자**가 된다. (`mastra.getAgentById('weatherAgent')`)

---

## 3. 요청 → 응답 실행 흐름 (Agent의 경우)

`agent.generate('서울 날씨 알려줘')` 를 호출했을 때 내부적으로 일어나는 일:

```
[User Input]
    │
    ▼
[Agent.generate() / .stream() 호출]
    │
    ▼
┌───────────────────────────────────┐
│ 1. 시스템 프롬프트 빌드           │
│   - agent.instructions            │
│   - + memory.getMessages()        │  ← thread/resource 기반 조회
│   - + observational memory 요약   │
│   - + semantic recall 결과        │  ← 질문 임베딩 → 유사 메시지
│   - + working memory 스냅샷       │
└───────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────┐
│ 2. Tool 설명 주입                 │
│   - createTool들의 description    │
│   - inputSchema → JSON Schema     │
│   - agents/workflows도 자동 변환  │
│     → "agent-foo", "workflow-bar" │
└───────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────┐
│ 3. LLM 호출 (Vercel AI SDK)       │
│   - streamText / generateText     │
│   - model router로 provider 선택  │
└───────────────────────────────────┘
    │
    ▼ (LLM이 tool_call을 반환하면)
┌───────────────────────────────────┐
│ 4. Tool 실행 루프                 │
│   - inputSchema로 인자 파싱       │
│   - tool.execute() 호출           │
│   - outputSchema로 결과 검증      │
│   - 결과를 메시지로 추가          │
│   → 3번으로 다시                  │
└───────────────────────────────────┘
    │
    ▼ (LLM이 최종 텍스트 반환하면)
┌───────────────────────────────────┐
│ 5. Memory에 저장                  │
│   - 메시지 history 누적           │
│   - observational memory 업데이트 │
│   - working memory 갱신           │
└───────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────┐
│ 6. Scorer 비동기 평가             │
│   - sampling rate 기반            │
│   - 별도 trace로 기록             │
└───────────────────────────────────┘
    │
    ▼
[Response (text + toolCalls + steps + usage)]
```

> **모든 단계가 OTEL trace span으로 자동 기록됨.** Studio의 Observability 탭에서 단계별로 들여다볼 수 있다.

---

## 4. Workflow의 실행 모델 (Agent와 어떻게 다른가)

| 항목 | Agent | Workflow |
|------|-------|----------|
| 실행 순서 결정자 | LLM (비결정적) | 코드의 그래프 (결정적) |
| 입출력 보장 | 모델 출력 신뢰 | 각 step의 `inputSchema`/`outputSchema`로 강제 |
| 사용 시점 | 사용자가 "뭘 할지" 못 정함 | 다단계 파이프라인이 명확 |
| 중단/재개 | 어렵다 | `suspend()`/`resume()` 1급 지원 |
| 관찰 | trace 1개 묶음 | step별 노드/엣지 시각화 |

### Workflow 실행 모델

```
createRun()
   │
   ▼
.start({ inputData })  ─── 또는  ──▶  .stream({ inputData })
   │                                   │
   ▼                                   ▼
[Step 1 execute]                  [emit "step-start"]
   │                                   │
   ▼ (스키마 검증)                      ▼ (실행)
[Step 2 execute]                  [emit "step-finish"]
   │                                   │
   ▼ ... .then() / .branch() ...      ▼ ... 반복 ...
[Step N execute]                  [emit "workflow-finish"]
   │                                   │
   ▼                                   ▼
{ status: "success" | "failed" |  "suspended" | "tripwire" | "paused",
  result, steps, state, input }
```

**중요한 4가지 종료 상태**:
- `success` — 정상 완료. `result`에 최종 출력.
- `failed` — 에러 발생. `error`에 사유.
- `suspended` — `step.suspend()` 호출됨. 외부 이벤트로 `.resume()` 필요. (human-in-the-loop)
- `tripwire` — Guardrail/Processor가 차단. `reason` 포함.

---

## 5. 저장소 레이어 (Storage)

Mastra는 **세 종류의 저장소**를 사용:

| 종류 | 무엇을 저장 | 구현체 |
|------|--------------|--------|
| **Key-Value / Relational Storage** | message history, threads, scorer 결과, workflow snapshots | `LibSQLStore`, `PostgresStore`, `D1Store`, `UpstashStore` |
| **Vector Store** | RAG 임베딩 | `PgVector`, `PineconeVector`, `QdrantVector`, `MongoVector` |
| **Trace Sink** | OTEL spans | `OtelExporter` (Datadog/SigNoz/Langfuse/...), `OtelBridge` |

**`Mastra({ storage })`** 로 등록한 storage는 메모리·workflow snapshot·scorer 결과 등 **모든 영속화 필요한 컴포넌트가 공유**한다.

---

## 6. 통합 진입점 (Integration Surface)

Mastra는 **세 가지 방식**으로 호출 가능:

| 방식 | 어디서 쓰나 | API |
|------|-------------|-----|
| **직접 import + getAgentById** | 같은 Node 프로세스 내 (Next.js Route Handler, Express) | `mastra.getAgentById('x').generate(...)` |
| **Mastra Server** | 별도 서비스로 띄움 | `mastra dev` / `mastra start` — HTTP/SSE |
| **Mastra Client (`@mastra/client-js`)** | 다른 서비스/프론트엔드에서 원격 호출 | `mastraClient.getAgent('x').stream(...)` |

> Studio는 **로컬 dev server에 자동 연결**되어 그래프, 트레이스, 메모리, 스코어를 실시간 시각화.

---

## 7. 핵심 의존성 트리

```
@mastra/core           ← Agent, Workflow, Tool, Mastra 클래스
  ├─ ai (Vercel AI SDK) ← LLM 호출, 스트리밍, tool calling
  └─ standard-schema   ← Zod/Valibot/ArkType 통합

@mastra/memory         ← Memory 클래스
  └─ @mastra/libsql    ← (또는 @mastra/pg 등) 영속화

@mastra/rag            ← MDocument, chunking strategies
  └─ @mastra/pg        ← PgVector 등 vector store

@mastra/evals          ← Scorer 빌트인 + custom 헬퍼
@mastra/mcp            ← MCPClient, MCPServer
@mastra/deployer-*     ← Vercel/Cloudflare/Netlify 배포 어댑터
```

---

## 다음 문서

- [[03-agents-workflows]] — Agent와 Workflow를 실제 코드로 깊이 이해
- [[04-memory-rag]] — Memory 4계층과 RAG 파이프라인
