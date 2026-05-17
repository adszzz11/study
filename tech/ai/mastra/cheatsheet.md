---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
  - cheatsheet
status: studying
---

# Mastra Cheatsheet — 빠른 API 참조

---

## 0. 설치 & 부트스트랩

```bash
# 새 프로젝트
npm create mastra@latest

# 기존 프로젝트에 추가
npm install @mastra/core @mastra/libsql zod

# 메모리/RAG/Evals/MCP를 추가
npm install @mastra/memory @mastra/rag @mastra/pg @mastra/evals @mastra/mcp
```

```typescript
// src/mastra/index.ts
import { Mastra } from '@mastra/core'
import { LibSQLStore } from '@mastra/libsql'

export const mastra = new Mastra({
  storage: new LibSQLStore({ id: 'storage', url: ':memory:' }),
  agents: { /* ... */ },
  workflows: { /* ... */ },
  scorers: { /* ... */ },
})
```

---

## 1. Agent

```typescript
import { Agent } from '@mastra/core/agent'

new Agent({
  id: 'x',
  name: 'X',
  description: 'short desc, used as tool when nested',
  instructions: 'system prompt',
  model: 'openai/gpt-5.4',                  // or fn returning string
  tools: { ... },
  agents: { ... },                          // subagents → agent-<key>
  workflows: { ... },                       // → workflow-<key>
  memory: new Memory({ ... }),
  scorers: { ... },
})
```

```typescript
const agent = mastra.getAgentById('x')

await agent.generate('hi', {
  memory: { resource: 'user-1', thread: 't-1' },
  toolChoice: 'auto',     // 'required' | 'none'
  activeTools: ['weatherTool'],
  output: ZodSchema,      // structured output
})

for await (const c of (await agent.stream('hi')).textStream) {
  process.stdout.write(c)
}
```

---

## 2. Tool

```typescript
import { createTool } from '@mastra/core/tools'
import { z } from 'zod'

createTool({
  id: 'weather-tool',
  description: 'Get current weather for a city',
  inputSchema: z.object({ location: z.string() }),
  outputSchema: z.object({ weather: z.string() }),
  execute: async ({ inputData, requestContext, mastra }) => ({ weather: '...' }),
  toModelOutput: out => ({ type: 'content', value: [...] }),    // 모델용 변형
  transform: { output: ({ payload, target }) => payload },      // UI용 변형
})
```

---

## 3. Workflow

```typescript
import { createStep, createWorkflow, cloneWorkflow } from '@mastra/core/workflows'
import { z } from 'zod'

const s1 = createStep({
  id: 's1',
  inputSchema: z.object({ x: z.string() }),
  outputSchema: z.object({ y: z.string() }),
  stateSchema: z.object({ counter: z.number() }),
  execute: async ({ inputData, state, setState, mastra, requestContext, suspend, resumeData }) => {
    return { y: inputData.x.toUpperCase() }
  },
})

const wf = createWorkflow({
  id: 'wf',
  inputSchema: z.object({ x: z.string() }),
  outputSchema: z.object({ y: z.string() }),
})
  .then(s1)
  .branch([
    [({ inputData }) => inputData.x === 'a', sA],
    [({ inputData }) => true, sDefault],
  ])
  .parallel([sP1, sP2])
  .map(async ({ inputData }) => ({ ... }))
  .commit()
```

```typescript
const run = await wf.createRun()

// 한 번에
const res = await run.start({ inputData: { x: 'hi' } })

// 스트리밍
const stream = await run.stream({ inputData: { x: 'hi' } })
for await (const ev of stream) console.log(ev.type)
const final = await stream.result

// suspend/resume
if (res.status === 'suspended') {
  await run.resume({ step: 'await-approval', resumeData: { ok: true } })
}

// 복구
await run.restart()
await wf.restartAllActiveWorkflowRuns()
```

**Result discriminated union**:
```typescript
type R =
  | { status: 'success', result, steps, input }
  | { status: 'failed', error, steps, input }
  | { status: 'suspended', suspendPayload, suspended, steps, input }
  | { status: 'tripwire', tripwire: { reason, retry?, metadata? } }
  | { status: 'paused' }
```

---

## 4. Memory

```typescript
import { Memory } from '@mastra/memory'

new Memory({
  options: {
    lastMessages: 20,                                          // ①
    workingMemory: { enabled: true, template: '- Name:\n- ...' }, // ②
    semanticRecall: { topK: 3, messageRange: { before: 2, after: 1 }, scope: 'resource' }, // ③
    observationalMemory: true,                                 // ④ (권장)
  },
  processors: [
    new TokenLimiter({ limit: 8000 }),
    new ToolCallFilter({ exclude: ['debugTool'] }),
  ],
})
```

```typescript
await agent.generate('msg', {
  memory: { resource: 'user-123', thread: 'thread-1' },
})
```

| 키 | 의미 | 변경 |
|----|------|------|
| `resource` | 사용자/엔티티 ID, thread owner | 한번 정해지면 고정 |
| `thread`   | 한 대화 세션 ID | 자유 |

---

## 5. RAG

```typescript
import { MDocument } from '@mastra/rag'
import { PgVector } from '@mastra/pg'
import { embedMany } from 'ai'
import { ModelRouterEmbeddingModel } from '@mastra/core/llm'

const doc = MDocument.fromText('...')
const chunks = await doc.chunk({ strategy: 'recursive', size: 512, overlap: 50 })

const { embeddings } = await embedMany({
  values: chunks.map(c => c.text),
  model: new ModelRouterEmbeddingModel('openai/text-embedding-3-small'),
})

const pg = new PgVector({ id: 'pg', connectionString: process.env.PG! })
await pg.upsert({ indexName: 'docs', vectors: embeddings, metadata: chunks.map(c => ({ text: c.text })) })
const hits = await pg.query({ indexName: 'docs', queryVector, topK: 3 })
```

```typescript
// Agent의 도구로 노출
import { createVectorQueryTool, createGraphRAGTool } from '@mastra/rag'

const rag = createVectorQueryTool({
  vectorStoreName: 'pg',
  indexName: 'docs',
  model: new ModelRouterEmbeddingModel('openai/text-embedding-3-small'),
})
```

**Chunking strategies**: `recursive`, `character`, `markdown`, `html`, `token`.

---

## 6. MCP

```typescript
import { MCPClient, MCPServer } from '@mastra/mcp'

// 클라이언트
const mcp = new MCPClient({
  servers: {
    fs: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-filesystem', '/path'] },
    gh: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-github'], env: { GITHUB_TOKEN: '...' } },
  },
})
new Agent({ ..., tools: await mcp.getTools() })

// 서버
const server = new MCPServer({
  name: 'mastra-internal',
  version: '1.0.0',
  tools: { weatherTool },
  agents: { researchAgent },
  workflows: { contentWorkflow },
})
await server.startStdio()    // or .startSSE({ port: 3001 })
```

---

## 7. Evals (Scorers)

```typescript
import { createAnswerRelevancyScorer, createToxicityScorer } from '@mastra/evals/scorers/prebuilt'
import { createScorer } from '@mastra/evals'

new Agent({
  ...,
  scorers: {
    rel:    { scorer: createAnswerRelevancyScorer({ model: 'openai/gpt-5-mini' }), sampling: { type: 'ratio', rate: 0.2 } },
    safety: { scorer: createToxicityScorer({ model: 'openai/gpt-5-mini' }),        sampling: { type: 'ratio', rate: 1 } },
  },
})
```

```typescript
// Custom
createScorer({
  name: 'brand-tone',
  model: 'openai/gpt-5-mini',
  judgePrompt: ({ input, output }) => `...`,
})
```

**Prebuilt**: `answerRelevancy`, `faithfulness`, `toxicity`, `bias`, `hallucination`, `contextRelevancy`, `contextRecall`, `summarization`, `classification`, `bleu`, `rouge`, `cosineSimilarity`.

---

## 8. Observability

```typescript
import { OtelExporter, OtelBridge } from '@mastra/core/observability'

new Mastra({
  observability: {
    exporter: new OtelExporter({
      endpoint: process.env.OTEL_ENDPOINT,
      headers: { 'api-key': process.env.OTEL_API_KEY },
    }),
    // 또는
    bridge: new OtelBridge({ tracer: trace.getTracer('my-app') }),
  },
})
```

**호환 백엔드**: Datadog, New Relic, SigNoz, MLflow, Dash0, Traceloop, Laminar, LangSmith/LangFuse/Braintrust (OTEL 모드).

---

## 9. 자주 쓰는 Mastra 인스턴스 API

```typescript
mastra.getAgentById('id')
mastra.getWorkflow('key')              // 등록 키 — 타입 추론 더 강력
mastra.getWorkflowById('id')           // 약한 타입
mastra.getStorage()
mastra.getLogger()
mastra.getVector('vectorStoreName')
```

---

## 10. 모델 라우터 (Model Router)

`"<provider>/<model>"` 문자열:

```
openai/gpt-5.4
openai/gpt-5-mini
openai/text-embedding-3-small
anthropic/claude-5
google/gemini-3-pro
bedrock/claude-5
groq/llama-4-70b
ollama/llama4
```

환경변수에서 키 자동 로드: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_GENERATIVE_AI_API_KEY`, ...

---

## 11. 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| Memory에서 "thread already owned by another resource" | 같은 thread ID에 다른 resource | thread ID를 resource별로 분리 |
| Workflow `.commit()` 누락 → execute 안 됨 | 마지막 commit 잊음 | 체이닝 끝에 `.commit()` |
| Tool description이 길어 prompt가 폭주 | description에 사용 가이드까지 다 담음 | 한 줄 요약만, 상세는 agent instructions로 |
| Scorer가 응답을 느리게 함 | `sampling.rate` 누락(기본 1) | 운영은 0.05~0.2 |
| `getWorkflow()` 타입 추론 안 됨 | `getWorkflowById()`를 씀 | 등록 키로 `getWorkflow()` 사용 |
| OTEL exporter 데이터 안 도착 | endpoint/headers 누락 | `process.env` 확인, `mastra dev`로 trace 먼저 확인 |
