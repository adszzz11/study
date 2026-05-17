---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
  - agents
  - workflows
status: studying
---

# 03. Agents & Workflows — 심화

> 이 문서는 Mastra의 두 핵심 추상화인 **Agent (비결정적 LLM 루프)** 와 **Workflow (결정적 그래프 엔진)** 를 코드와 함께 깊이 다룹니다.

---

## 1. Agent

### 1.1. 가장 단순한 Agent

```typescript
// src/mastra/agents/test-agent.ts
import { Agent } from '@mastra/core/agent'

export const testAgent = new Agent({
  id: 'test-agent',
  name: 'Test Agent',
  instructions: 'You are a helpful assistant.',
  model: 'openai/gpt-5.4',  // ← Model Router 문자열
})
```

```typescript
// src/mastra/index.ts
import { Mastra } from '@mastra/core'
import { testAgent } from './agents/test-agent'

export const mastra = new Mastra({
  agents: { testAgent },
})
```

### 1.2. 호출 — `.generate()` vs `.stream()`

```typescript
const agent = mastra.getAgentById('test-agent')

// 한 번에 결과 받기 (모든 tool call 완료 후)
const response = await agent.generate('Help me organize my day')
console.log(response.text)
console.log(response.toolCalls)   // [{ name, args, ... }]
console.log(response.toolResults) // 각 toolCall에 대응
console.log(response.steps)       // LLM ↔ tool 라운드별 정보
console.log(response.usage)       // 토큰 사용량

// 토큰 스트리밍
const stream = await agent.stream('Tell me a story')
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk)
}
```

### 1.3. Tool을 가진 Agent

```typescript
// src/mastra/tools/weather-tool.ts
import { createTool } from '@mastra/core/tools'
import { z } from 'zod'

export const weatherTool = createTool({
  id: 'weather-tool',
  description: 'Fetches current weather for a given city',
  inputSchema: z.object({
    location: z.string().describe('City name, e.g. "Seoul"'),
  }),
  outputSchema: z.object({
    weather: z.string(),
  }),
  execute: async ({ inputData }) => {
    const res = await fetch(`https://wttr.in/${inputData.location}?format=3`)
    return { weather: await res.text() }
  },
})
```

```typescript
// src/mastra/agents/weather-agent.ts
import { Agent } from '@mastra/core/agent'
import { weatherTool } from '../tools/weather-tool'

export const weatherAgent = new Agent({
  id: 'weather-agent',
  name: 'Weather Agent',
  instructions: `
    You are a helpful weather assistant.
    Use weatherTool to fetch current weather data.
  `,
  model: 'openai/gpt-5.4',
  tools: { weatherTool },
})
```

> **포인트**: `description`은 모델이 도구 선택에 쓰는 텍스트다. **모델 입장에서 무엇을 위한 도구인지** 명확하게 쓰는 게 가장 큰 성능 지렛대.

### 1.4. Agent를 도구처럼 (Supervisor 패턴)

```typescript
const writer = new Agent({
  id: 'writer',
  name: 'Writer',
  description: 'Drafts and edits written content',  // ← supervisor가 위임 판단에 사용
  instructions: 'You are a skilled writer.',
  model: 'openai/gpt-5.4',
})

const researcher = new Agent({
  id: 'researcher',
  name: 'Researcher',
  description: 'Researches topics deeply',
  instructions: 'You are a research expert.',
  model: 'openai/gpt-5.4',
})

export const supervisor = new Agent({
  id: 'supervisor',
  name: 'Supervisor',
  instructions: 'Coordinate writer and researcher to produce a report.',
  model: 'openai/gpt-5.4',
  agents: { writer, researcher },   // ← 서브에이전트
})
```

Mastra가 자동으로 `agent-writer`, `agent-researcher`라는 **툴**로 변환해서 supervisor의 컨텍스트에 주입한다.

### 1.5. Workflow를 도구처럼

```typescript
import { Agent } from '@mastra/core/agent'
import { researchWorkflow } from '../workflows/research-workflow'

export const researchAgent = new Agent({
  id: 'research-agent',
  name: 'Research Agent',
  instructions: 'You are a research assistant.',
  model: 'openai/gpt-5.4',
  workflows: { researchWorkflow },  // ← workflow-researchWorkflow 라는 툴이 됨
})
```

### 1.6. 구조화 출력 (Structured Output)

```typescript
import { z } from 'zod'

const InvoiceSchema = z.object({
  invoiceNumber: z.string(),
  total: z.number(),
  lineItems: z.array(z.object({ description: z.string(), amount: z.number() })),
})

const response = await agent.generate('Extract invoice from this image', {
  output: InvoiceSchema,
})

// response.object is typed as z.infer<typeof InvoiceSchema>
console.log(response.object.invoiceNumber)
```

### 1.7. 런타임 도구 제어

```typescript
await agent.generate('Check the forecast', {
  toolChoice: 'required',          // 반드시 도구 호출
  activeTools: ['weatherTool'],    // 이번 호출에서는 이 툴만 활성화
})
```

이 외에 런타임에 전달 가능한 옵션: `toolsets`(여러 툴 묶음), `clientTools`(브라우저에서 실행될 툴), `prepareStep`(각 step 전 후처리).

### 1.8. 동적 설정 — RequestContext

요청별로 다른 모델/메모리/instructions를 쓰고 싶을 때:

```typescript
export const dynamicAgent = new Agent({
  id: 'dynamic-agent',
  model: ({ requestContext }) => {
    const tier = requestContext.get('user-tier')
    return tier === 'enterprise' ? 'anthropic/claude-5' : 'openai/gpt-5-mini'
  },
  memory: ({ requestContext }) => {
    const tier = requestContext.get('user-tier')
    return tier === 'enterprise' ? premiumMemory : standardMemory
  },
})
```

---

## 2. Workflow

### 2.1. Step과 Workflow의 분리

Mastra Workflow는 **두 단계**로 만든다:

1. `createStep()` — 입력/출력 스키마 + execute 함수
2. `createWorkflow()` — step들을 `.then()`, `.branch()`, `.parallel()`로 조합

### 2.2. 가장 단순한 Workflow

```typescript
// src/mastra/workflows/test-workflow.ts
import { createStep, createWorkflow } from '@mastra/core/workflows'
import { z } from 'zod'

const upperStep = createStep({
  id: 'upper',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ formatted: z.string() }),
  execute: async ({ inputData }) => {
    return { formatted: inputData.message.toUpperCase() }
  },
})

const emphasizeStep = createStep({
  id: 'emphasize',
  inputSchema: z.object({ formatted: z.string() }),
  outputSchema: z.object({ emphasized: z.string() }),
  execute: async ({ inputData }) => {
    return { emphasized: `${inputData.formatted}!!!` }
  },
})

export const testWorkflow = createWorkflow({
  id: 'test-workflow',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ emphasized: z.string() }),
})
  .then(upperStep)
  .then(emphasizeStep)
  .commit()                  // ← 잊지 말 것
```

### 2.3. 실행

```typescript
const wf = mastra.getWorkflow('testWorkflow')
const run = await wf.createRun()

const result = await run.start({
  inputData: { message: 'hello world' },
})

if (result.status === 'success') {
  console.log(result.result.emphasized)  // "HELLO WORLD!!!"
}
```

### 2.4. 결과 타입 (Discriminated Union)

```typescript
type WorkflowResult =
  | { status: 'success'; result: TOutput; steps: ...; input: TInput }
  | { status: 'failed'; error: Error; steps: ...; input: TInput }
  | { status: 'suspended'; suspendPayload: ...; suspended: string[]; ... }
  | { status: 'tripwire'; tripwire: { reason, retry?, metadata? }; ... }
  | { status: 'paused'; ... }
```

`status`로 분기 후 unique property에 접근하는 게 안전한 패턴.

### 2.5. 제어 흐름 — `.branch()`, `.parallel()`, `.map()`

```typescript
import { z } from 'zod'

export const routerWorkflow = createWorkflow({
  id: 'router',
  inputSchema: z.object({ tier: z.enum(['free', 'pro']) }),
  outputSchema: z.object({ result: z.string() }),
})
  .branch([
    [({ inputData }) => inputData.tier === 'pro', proStep],
    [({ inputData }) => inputData.tier === 'free', freeStep],
  ])
  .commit()
```

```typescript
// 병렬 실행
.parallel([fetchEmails, fetchSlack, fetchCalendar])
.then(mergeResults)
```

```typescript
// 데이터 변환
.map(async ({ inputData }) => ({
  message: inputData.userText.trim().toLowerCase(),
}))
.then(upperStep)
```

### 2.6. Workflow State — step 간 누적 값

매 step의 inputSchema/outputSchema에 끼워 넣기 부담스러운 값을 위해:

```typescript
const step1 = createStep({
  id: 'step-1',
  inputSchema: z.object({ message: z.string() }),
  outputSchema: z.object({ formatted: z.string() }),
  stateSchema: z.object({ counter: z.number() }),
  execute: async ({ inputData, state, setState }) => {
    setState({ ...state, counter: state.counter + 1 })
    return { formatted: inputData.message.toUpperCase() }
  },
})
```

### 2.7. Suspend & Resume (Human-in-the-loop)

```typescript
const approvalStep = createStep({
  id: 'await-approval',
  inputSchema: z.object({ draft: z.string() }),
  outputSchema: z.object({ approved: z.boolean() }),
  suspendSchema: z.object({ draft: z.string() }),  // 외부에 노출할 payload
  resumeSchema: z.object({ approved: z.boolean() }),
  execute: async ({ inputData, suspend, resumeData }) => {
    if (!resumeData) {
      await suspend({ draft: inputData.draft })
      return { approved: false }  // 도달 안 함
    }
    return { approved: resumeData.approved }
  },
})

// --- 외부에서 ---
const run = await wf.createRun()
const r1 = await run.start({ inputData: { draft: 'Hello' } })
if (r1.status === 'suspended') {
  // r1.suspendPayload.draft 를 사람이 검토하고...
  const r2 = await run.resume({
    step: 'await-approval',
    resumeData: { approved: true },
  })
}
```

### 2.8. Workflow 안에서 Agent 호출

```typescript
const writeStep = createStep({
  id: 'write',
  inputSchema: z.object({ topic: z.string() }),
  outputSchema: z.object({ draft: z.string() }),
  execute: async ({ inputData, mastra }) => {  // ← mastra 인스턴스 주입
    const writer = mastra.getAgentById('writer')
    const res = await writer.generate(`Write about: ${inputData.topic}`)
    return { draft: res.text }
  },
})
```

### 2.9. Workflow를 step으로 (Composition)

```typescript
const childWorkflow = createWorkflow({...})
  .then(stepA).then(stepB)
  .commit()

export const parentWorkflow = createWorkflow({...})
  .then(childWorkflow)        // 다른 workflow를 step처럼
  .then(stepC)
  .commit()
```

`cloneWorkflow(wf, { id: 'cloned' })`로 같은 로직을 **별도 ID로 추적**할 수도 있다.

### 2.10. 스트리밍 실행

```typescript
const stream = await run.stream({ inputData: { message: 'hi' } })

for await (const event of stream) {
  // event: 'step-start' | 'step-finish' | 'workflow-finish' | ...
  console.log(event.type, event.payload)
}

const final = await stream.result   // 동일한 discriminated union
```

---

## 3. Agent vs Workflow — 결정 가이드

| 시나리오 | 선택 | 이유 |
|----------|------|------|
| "사용자 질문에 맞춰 도구를 골라가며 답변" | **Agent** | 단계가 예측 불가 |
| "PDF → 추출 → 요약 → 슬랙 전송" 파이프라인 | **Workflow** | 단계가 결정적 |
| "고객 응대: 분류 후 부서별 다른 처리" | **Workflow + Agent step** | 분류는 그래프, 처리는 LLM |
| "코드 리뷰: 변경사항 모두에 대해 LLM 코멘트" | **Workflow + Agent step** (또는 supervisor) | 반복은 그래프가 안전 |
| Long-running, human approval 끼움 | **Workflow** (suspend/resume) | Agent로는 어려움 |

> **하이브리드가 가장 흔하다.** Workflow의 step 안에서 Agent를 호출하고, Agent의 도구로 다른 Workflow를 노출한다.

---

## 다음 문서

- [[04-memory-rag]] — Memory 4계층과 RAG 파이프라인
- [[05-tools-mcp]] — Tools와 MCP
