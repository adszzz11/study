---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
  - tools
  - mcp
status: studying
---

# 05. Tools & MCP Integrations — 심화

> 이 문서는 **Tool 시스템의 설계 원리**와 **MCP(Model Context Protocol)** 통합 패턴을 다룹니다.

---

## 1. Tool — 설계 원리

Mastra Tool은 4가지 구성 요소를 가진 작은 단위다:

| 구성 요소 | 역할 | 누가 봄 |
|-----------|------|---------|
| `id` | 식별자 | 사람·로그 |
| `description` | 모델이 도구 선택할 때 읽는 텍스트 | LLM |
| `inputSchema` | 모델이 보내는 인자의 형태 (JSON Schema) | LLM + 런타임 |
| `outputSchema` | execute의 반환값 검증 | 런타임 |
| `execute` | 실제 로직 | Node 런타임 |

> **핵심 통찰**: Tool은 **함수 호출의 타입 안전성** + **모델 친화적 description**의 결합이다. Zod 스키마가 양쪽 역할을 한다.

### 1.1. 기본 패턴 — `createTool`

```typescript
import { createTool } from '@mastra/core/tools'
import { z } from 'zod'

export const weatherTool = createTool({
  id: 'weather-tool',
  description: 'Fetches weather for a location',
  inputSchema: z.object({
    location: z.string(),
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

### 1.2. Standard Schema — Zod / Valibot / ArkType

스키마는 **Standard JSON Schema** 호환이면 무엇이든 OK.

```typescript
// Valibot
import * as v from 'valibot'
import { toStandardJsonSchema } from '@valibot/to-json-schema'

createTool({
  inputSchema: toStandardJsonSchema(v.object({ location: v.string() })),
  ...
})

// ArkType
import { type } from 'arktype'
createTool({
  inputSchema: type({ location: 'string' }),
  ...
})
```

### 1.3. `toModelOutput` — 컨텍스트 절약

도구가 큰 객체를 반환하는데 모델에게는 요약만 주고 싶을 때:

```typescript
createTool({
  execute: async ({ location }) => {
    const data = await fetchWeather(location)
    return {
      location,
      temperature: data.temp,
      condition: data.condition,
      weatherIconUrl: data.iconUrl,
      source: data,  // 풀 데이터 (앱에서 쓸 용도)
    }
  },
  toModelOutput: output => ({
    type: 'content',
    value: [
      { type: 'text', text: `${output.location}: ${output.temperature}°F, ${output.condition}` },
      { type: 'image-url', url: output.weatherIconUrl },
    ],
  }),
})
```

모델에는 짧은 텍스트 + 이미지만, 앱에는 풀 페이로드 반환.

### 1.4. `transform` — UI/transcript용 변형

브라우저 스트림이나 사용자 가시 transcript에 **민감 데이터를 마스킹** 또는 **축약**:

```typescript
createTool({
  ...,
  transform: {
    output: ({ payload, target }) => {
      if (target === 'display') {
        const { internalToken, ...rest } = payload
        return rest
      }
      return payload
    },
  },
})
```

> `toModelOutput`은 **모델용**, `transform`은 **UI/로그용** — 둘은 서로 독립.

### 1.5. 런타임 제어

```typescript
await agent.generate('Check the forecast', {
  toolChoice: 'required',           // 'auto' | 'required' | 'none'
  activeTools: ['weatherTool'],
  clientTools: { /* 브라우저에서 실행할 툴 */ },
  prepareStep: async ({ step }) => { /* step 전 후처리 */ },
})
```

### 1.6. Tool Naming 규칙 (Stream 응답)

`tools: { weatherTool }` 처럼 객체 키 이름이 stream의 `toolName`이 된다:

```typescript
// 옵션 A: 변수명을 키로
tools: { weatherTool }              // toolName: "weatherTool"

// 옵션 B: tool의 id를 키로
tools: { [weatherTool.id]: weatherTool }   // toolName: "weather-tool"

// 옵션 C: 커스텀 이름
tools: { 'my-weather': weatherTool }       // toolName: "my-weather"
```

서브에이전트와 워크플로우는 **prefix가 자동 부여**된다:

| 종류 | Prefix | 키 | 결과 toolName |
|------|--------|----|----|
| `agents` | `agent-` | `weather` | `agent-weather` |
| `workflows` | `workflow-` | `research` | `workflow-research` |

---

## 2. MCP — Model Context Protocol

MCP는 **도구를 표준 프로토콜로 외부 프로세스에 분리**하는 사양이다. Mastra는 양방향 지원:

- **MCPClient** — 외부 MCP 서버의 도구를 가져와 Mastra Agent에 주입
- **MCPServer** — Mastra의 도구/에이전트/워크플로우를 MCP 프로토콜로 노출

```
                    MCP Protocol (stdio / SSE / HTTP)
                              ▲
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
   ┌────▼────┐                                ┌────▼─────┐
   │ Mastra  │                                │ External │
   │ Agent   │  ◄── tools from external ───► │ MCP      │
   │         │                                │ Server   │
   │ Mastra  │  ─── tools to external ────►  │ (any     │
   │ MCPServer│                               │  client) │
   └─────────┘                                └──────────┘
```

### 2.1. MCPClient — 외부 MCP 도구 가져오기

```typescript
import { MCPClient } from '@mastra/mcp'
import { Agent } from '@mastra/core/agent'

const mcp = new MCPClient({
  servers: {
    filesystem: {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-filesystem', '/Users/me/Downloads'],
    },
    github: {
      command: 'npx',
      args: ['-y', '@modelcontextprotocol/server-github'],
      env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN! },
    },
  },
})

export const agent = new Agent({
  id: 'mcp-agent',
  instructions: 'You can use filesystem and GitHub tools.',
  model: 'openai/gpt-5.4',
  tools: await mcp.getTools(),    // ← 외부 도구를 한 번에 주입
})
```

`MCPClient`는 stdio / SSE / Streamable HTTP transport를 모두 지원한다.

#### 동적 toolsets (요청별 다른 도구)

```typescript
await agent.generate('Help me', {
  toolsets: await mcp.getToolsets(),  // 매 요청 새로 구성
})
```

세션 별로 다른 MCP 서버에 접속하고 싶을 때 유용.

### 2.2. MCPServer — Mastra 도구를 외부에 노출

```typescript
import { MCPServer } from '@mastra/mcp'
import { weatherTool } from './tools/weather-tool'
import { researchAgent } from './agents/research-agent'
import { contentWorkflow } from './workflows/content-workflow'

const server = new MCPServer({
  name: 'mastra-internal',
  version: '1.0.0',
  tools: { weatherTool },
  agents: { researchAgent },         // 자동으로 ask_researchAgent 같은 툴이 됨
  workflows: { contentWorkflow },    // 자동으로 run_contentWorkflow 같은 툴이 됨
})

await server.startStdio()
// 또는 await server.startSSE({ port: 3001 })
```

→ Claude Desktop, Cursor, 다른 Mastra Agent, 또는 임의의 MCP 클라이언트가 이 도구들을 호출 가능.

### 2.3. 실전 통합 사례

| 통합처 | 패턴 |
|--------|------|
| **Apify Actors** | RAG Web Browser + TikTok Extractor를 Apify MCP 서버로 노출, Mastra Agent가 클라이언트로 소비 |
| **Arcade.dev** | OAuth가 필요한 SaaS(Gmail, Slack, Notion)를 Arcade MCP로 위임 |
| **Elasticsearch** | Elastic이 제공하는 MCP 서버를 통해 RAG 에이전트 구축 |
| **Filesystem / Git / GitHub** | Anthropic 공식 MCP servers를 직접 spawn |

---

## 3. Tools 설계 베스트 프랙티스

### 3.1. Description은 모델 관점에서

❌ **나쁜 예** (개발자 관점):
```typescript
description: 'Calls /api/v2/weather endpoint'
```

✅ **좋은 예** (모델 관점):
```typescript
description: 'Get the current weather for a specific city. Returns temperature in Fahrenheit and a short condition string.'
```

### 3.2. 단일 책임

도구 하나에 너무 많은 일을 시키면 LLM이 사용법을 혼동한다. 하나의 도구 = 하나의 명확한 명사형 동작.

### 3.3. 입력 스키마는 LLM에게 친절하게

`z.string().describe('City name in English, e.g. "Seoul"')` 처럼 **`.describe()` 활용**. 모델은 description을 읽고 인자를 채운다.

### 3.4. 출력은 결정적으로

스트링 자유 형식보다 **enum / 객체 구조**가 후속 처리에 유리:

```typescript
outputSchema: z.object({
  status: z.enum(['ok', 'not_found', 'rate_limited']),
  data: z.object({ ... }).nullable(),
})
```

### 3.5. 큰 결과는 `toModelOutput` 로 압축

API가 큰 JSON을 반환하면 그대로 두지 말고 모델에게는 요약만, 앱에는 풀 데이터를 분리.

### 3.6. 위험한 동작은 Approval

자금 이체, 메일 발송 같은 위험한 도구는 [`agent-approval`](https://mastra.ai/docs/agents/agent-approval) 패턴으로 사람 승인 게이팅.

---

## 다음 문서

- [[06-evals-observability]] — Scorer와 Tracing으로 운영하기
- [[cheatsheet]] — 빠른 API 참조
