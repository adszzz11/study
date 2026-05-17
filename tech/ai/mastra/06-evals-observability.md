---
date: 2026-05-17
tags:
  - tech
  - ai
  - mastra
  - evals
  - observability
status: studying
---

# 06. Evals & Observability — 심화

> 이 문서는 **Scorers (Evals)** 와 **Tracing (Observability)** 를 다룹니다. Mastra의 운영 레이어다.

---

## 1. Why — 왜 별도 시스템이 필요한가

전통 소프트웨어 테스트는 입력 → 결정적 출력 → pass/fail이다. **LLM 출력은 같은 입력에도 매번 다르다.** 따라서:

- 단위 테스트 대신 → **점수**로 수렴
- 한 번의 PR 검증 대신 → **지속적 모니터링**
- 한 가지 척도 대신 → **여러 차원** (관련성, 안전성, 사실성, 어조...)

이를 위한 Mastra의 답이 **Scorer + AI Tracing** 한 쌍.

---

## 2. Scorers — Mastra의 평가 단위

### 2.1. 정의

> Scorer = AI 출력을 자동으로 채점해 0~1 사이 수치를 반환하는 함수.

**세 종류**:
- **Model-graded** — LLM을 judge로 사용 (예: 답변 관련성, 독성)
- **Rule-based** — 정규식·문자열 매칭 (예: 형식 검증)
- **Statistical** — BLEU, ROUGE, embedding similarity 등

### 2.2. 설치

```bash
npm install @mastra/evals@latest
```

### 2.3. Built-in Scorer 적용 — Agent에

```typescript
import { Agent } from '@mastra/core/agent'
import {
  createAnswerRelevancyScorer,
  createToxicityScorer,
} from '@mastra/evals/scorers/prebuilt'

export const evaluatedAgent = new Agent({
  id: 'evaluated-agent',
  model: 'openai/gpt-5.4',
  scorers: {
    relevancy: {
      scorer: createAnswerRelevancyScorer({ model: 'openai/gpt-5-mini' }),
      sampling: { type: 'ratio', rate: 0.5 },   // 50%만 채점
    },
    safety: {
      scorer: createToxicityScorer({ model: 'openai/gpt-5-mini' }),
      sampling: { type: 'ratio', rate: 1 },     // 100% 채점
    },
  },
})
```

**Sampling**:
- `rate: 1.0` → 모든 응답 채점
- `rate: 0.1` → 10%만 (운영 비용 절감)
- `rate: 0` → 비활성

### 2.4. Built-in Scorer 목록 (주요)

| 카테고리 | Scorer | 측정 대상 |
|----------|--------|------------|
| Textual | `answerRelevancy` | 답변이 질문과 관련 있는가 |
| Textual | `faithfulness` | RAG 답변이 인용 컨텍스트에 충실한가 |
| Textual | `summarization` | 요약 품질 |
| Safety | `toxicity` | 유해/독성 표현 여부 |
| Safety | `bias` | 편향성 |
| Safety | `hallucination` | 환각 |
| RAG | `contextRelevancy` | 검색된 컨텍스트가 관련 있는가 |
| RAG | `contextRecall` | 정답이 컨텍스트에 들어있나 |
| Classification | `classification` | 라벨 일치 |
| Statistical | `bleu`, `rouge`, `cosineSimilarity` | 정답 텍스트 대비 유사도 |

### 2.5. Workflow Step에 Scorer 붙이기

```typescript
const contentStep = createStep({
  id: 'generate-content',
  inputSchema: z.object({ topic: z.string() }),
  outputSchema: z.object({ draft: z.string() }),
  scorers: {
    qualityScore: {
      scorer: customStepScorer(),
      sampling: { type: 'ratio', rate: 1 },
    },
  },
  execute: async ({ inputData, mastra }) => {
    const writer = mastra.getAgentById('writer')
    const res = await writer.generate(`Write about ${inputData.topic}`)
    return { draft: res.text }
  },
})
```

### 2.6. Custom Scorer

```typescript
import { createScorer } from '@mastra/evals'
import { z } from 'zod'

export const lengthScorer = createScorer({
  name: 'length-bounds',
  description: 'Score 1 if 100-500 chars, else lower',
  judge: async ({ output }) => {
    const len = (output.text ?? '').length
    if (len < 100) return { score: len / 100, reason: 'Too short' }
    if (len > 500) return { score: Math.max(0, 1 - (len - 500) / 500), reason: 'Too long' }
    return { score: 1, reason: 'Within bounds' }
  },
})
```

LLM judge를 사용하는 커스텀 scorer:

```typescript
export const brandToneScorer = createScorer({
  name: 'brand-tone',
  model: 'openai/gpt-5-mini',
  judgePrompt: ({ output, input }) => `
    Rate how well this response matches our brand tone
    (friendly, concise, professional). 0-1 score.

    Input: ${input}
    Output: ${output.text}

    Return JSON: { "score": number, "reason": string }
  `,
})
```

### 2.7. 비동기 실행 + 자동 저장

- 응답 직후 채점하지 않고 **백그라운드**로 실행 → 사용자 응답 지연 0
- 결과는 `mastra_scorers` 테이블에 자동 저장
- Studio Observability 탭에서 시계열 추이/필터링

### 2.8. CI에서 Scorer 돌리기

```typescript
// tests/relevancy.test.ts
import { describe, it, expect } from 'vitest'
import { createAnswerRelevancyScorer } from '@mastra/evals/scorers/prebuilt'
import { evaluatedAgent } from '../src/mastra/agents/evaluated-agent'

const scorer = createAnswerRelevancyScorer({ model: 'openai/gpt-5-mini' })

describe('relevancy regression', () => {
  it('answers stay relevant', async () => {
    const res = await evaluatedAgent.generate('What is the capital of France?')
    const { score } = await scorer.run({
      input: 'What is the capital of France?',
      output: { text: res.text },
    })
    expect(score).toBeGreaterThan(0.8)
  })
})
```

### 2.9. Datasets — 회귀 방지 정답셋

Studio에 dataset을 등록해 두면 새 모델/프롬프트로 **일괄 재평가**가 가능. 모델 교체나 instructions 수정 후 회귀를 잡는 표준 패턴.

---

## 3. Observability — Tracing

### 3.1. 무엇이 트레이싱 되나

Telemetry가 켜져 있으면 Mastra는 **모든 핵심 프리미티브**에 자동으로 OTEL span을 생성:

- Agent 호출 (`.generate`, `.stream`)
- LLM 호출 (provider, 모델, 토큰 사용량)
- Tool 실행 (입력, 출력, 에러)
- Workflow step (status, payload)
- Memory operations (read/write)
- RAG retrieval (쿼리, top-k 결과)
- Storage / DB

```
Agent.generate (span)
├─ LLM call (child span: provider=openai, model=gpt-5.4, tokens=...)
├─ Tool: weatherTool (child span: location="Seoul", output=...)
└─ LLM call (child span: 후속 응답 생성)
```

### 3.2. AI Tracing — Mastra의 1급 시스템

`@mastra/core` 안에 **AI-aware tracing**이 내장. 일반 OTEL과 다르게:
- LLM 메시지/도구 호출 페이로드를 **온전한 형태**로 보존
- 토큰 단위 스트리밍을 span 안에 기록
- Studio에서 **timeline + chat view + JSON inspector**로 동시 표시

### 3.3. OTEL Exporter — 외부 백엔드로 보내기

```typescript
import { Mastra } from '@mastra/core'
import { OtelExporter } from '@mastra/core/observability'

export const mastra = new Mastra({
  observability: {
    exporter: new OtelExporter({
      endpoint: process.env.OTEL_ENDPOINT,
      headers: { 'api-key': process.env.OTEL_API_KEY },
    }),
  },
})
```

호환 백엔드: **Datadog, New Relic, SigNoz, MLflow, Dash0, Traceloop, Laminar**, 그리고 LangSmith/LangFuse/Braintrust도 OTEL 형식으로 export 가능.

### 3.4. OTEL Bridge — 기존 OTEL 시스템에 native span 통합

Exporter는 **별도 전송**, Bridge는 **같은 trace context 안에 native span**을 생성:

```typescript
import { OtelBridge } from '@mastra/core/observability'
import { trace } from '@opentelemetry/api'

export const mastra = new Mastra({
  observability: {
    bridge: new OtelBridge({
      tracer: trace.getTracer('my-app'),
    }),
  },
})
```

→ 기존 백엔드(Express request 등)의 trace에 Mastra span이 **자식으로** 붙는다. 분산 트레이싱이 자연스럽게 이어진다.

### 3.5. Studio Observability 탭

로컬 dev server를 띄우면 (`npm run dev`) Studio에서:
- **Traces** — 시간순 요청 리스트
- **Trace detail** — 단계별 timeline, 각 span 안의 입출력 / 도구 호출 / LLM 응답
- **Score overlay** — 해당 trace에 붙은 scorer 결과
- **Replay** — 같은 입력으로 재실행 (디버깅)

### 3.6. Trace 기반 Scorer 적용 (사후 평가)

이미 일어난 trace에 새 scorer를 돌릴 수 있다. 새 평가 척도를 도입했을 때 과거 데이터를 **재평가**하는 시나리오.

---

## 4. 운영 패턴 — 한 줄 정리

| 단계 | 도구 | 무엇을 보는가 |
|------|------|---------------|
| 개발 | Studio (로컬) | trace, replay, dataset 평가 |
| CI | `@mastra/evals` + vitest | 회귀 차단 |
| 프로덕션 모니터링 | Scorer (sampling rate 0.05~0.2) | 추세 |
| 인시던트 디버그 | OTEL Bridge로 통합된 trace | 분산 시스템 맥락에서 root cause |
| 모델/프롬프트 교체 | Studio Dataset Experiment | A/B 점수 비교 |

---

## 5. 흔한 함정

1. **Sampling 100%로 두기** — 운영 비용이 LLM 호출만큼 든다. judge LLM이 비싸면 더더욱.
2. **단일 Scorer로 충분하다 착각** — 안전성·관련성·정확성을 동시에 봐야 함.
3. **Trace를 안 켜고 Scorer만 돌림** — trace 없이는 "왜 낮은 점수인지" 알기 어렵다.
4. **Custom Scorer judge 프롬프트가 모호** — 채점자 LLM에게 명확한 rubric 제공.
5. **Dataset 없이 모델 교체** — 회귀가 보이지 않는다.

---

## 다음 문서

- [[cheatsheet]] — API 빠른 참조
- [[99-references]] — 공식 문서 링크
