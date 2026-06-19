---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - deep-dive
  - prompt-governance
type: tech-tool-study
parent: "[[../README]]"
---

# 심화 - Versioning, Serving Layer, Prompt Governance

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Mental model

Claude product behavior는 한 개의 model ID만으로 설명되지 않는다.

```text
Observed response
  = model snapshot
  + app/system prompt
  + conversation context
  + tool/product state
  + serving infrastructure
  + safety classifiers
  + sampling settings
```

System prompt release notes는 이 중 **app/system prompt** 변화를 추적하는 문서다. 다른 층의 변화까지 모두 설명하지는 않는다.

## 2. Model ID와 reproducibility

Anthropic은 Claude 4.6 이후 dateless model ID가 alias가 아니라 pinned snapshot이라고 설명한다. 즉 기존 model ID의 weights/config를 조용히 업데이트하지 않고, 새 버전은 새 model ID로 출시한다는 의미다.

| 항목 | 의미 |
|------|------|
| Pinned snapshot | 특정 model ID가 고정된 weights/config를 가리킴 |
| New model ID | 새 weights/config가 필요할 때 새 ID로 출시 |
| Reproducibility 도움 | "어떤 model을 썼는가" 기록이 더 명확해짐 |
| 남는 변수 | serving infrastructure, safety classifiers, sampling logic |

실험 로그에는 최소한 다음을 남긴다.

```yaml
run:
  date: 2026-06-20
  surface: anthropic_api
  model_id: claude-sonnet-4-6
  system_prompt_version: app-study-v3
  temperature: 0.2
  release_note_checked_at: 2026-06-20
```

## 3. Serving layer 변수

model weights가 고정되어도 다음 layer는 변할 수 있다.

| 변수 | 예시 영향 |
|------|-----------|
| Request router | region, load, model backend 선택 |
| Safety classifier | refusal 여부, unsafe content handling |
| Sampling logic | response diversity, stop behavior |
| Product feature flags | artifact/tool behavior, formatting behavior |
| Prompt assembly | hidden context, file/project metadata 포함 여부 |

따라서 behavior regression을 분석할 때는 "model이 변했다"만으로 결론내리지 않는다.

## 4. Mid-conversation system messages

Opus 4.8은 mid-conversation system messages를 지원한다. 긴 대화 중 user turn 직후 `role: "system"` message를 추가해 full system prompt를 반복하지 않고도 새 instruction을 넣을 수 있다. 목적 중 하나는 prompt cache hit를 보존하는 것이다.

개념 예시:

```json
{
  "model": "claude-opus-4-8",
  "messages": [
    {
      "role": "user",
      "content": "Analyze this long document."
    },
    {
      "role": "assistant",
      "content": "Initial analysis..."
    },
    {
      "role": "user",
      "content": "Now convert it into a Korean study note."
    },
    {
      "role": "system",
      "content": "For the next answer, use Korean explanations, preserve English technical terms, and include tables."
    }
  ]
}
```

운영상 이 기능은 다음 상황에 유용하다.

- 긴 context를 유지하면서 output mode만 바꿀 때
- full system prompt 재전송을 줄이고 cache hit를 보존할 때
- multi-step workflow에서 phase-specific instruction을 추가할 때

## 5. Refusal handling

Fable 5 문서 흐름에서 중요한 점은 refusal이 HTTP error가 아니라 성공 응답 안의 `stop_reason: "refusal"`로 반환될 수 있다는 것이다.

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [],
  "stop_reason": "refusal"
}
```

API client는 다음처럼 처리해야 한다.

| 처리 | 이유 |
|------|------|
| HTTP status만 보지 않기 | refusal은 successful response일 수 있음 |
| `stop_reason` 기록 | eval과 audit에서 refusal rate 추적 |
| user-facing message 분리 | provider raw refusal을 제품 UX로 변환 |
| retry 남발 금지 | safety classifier refusal은 단순 transient error가 아님 |

## 6. Prompt leak 대응

Anthropic은 prompt leak 완전 방지는 어렵다고 본다. 따라서 system prompt를 secret vault처럼 쓰는 방식은 피한다.

| 위험 | 대응 |
|------|------|
| Proprietary detail leak | prompt에 불필요한 내부 정책/비밀 제거 |
| Instruction extraction | system prompt와 user query/context 분리 |
| Sensitive output | post-processing, redaction, allowlist |
| Silent drift | prompt audits, eval set, release diff |
| Debug leakage | logs와 traces에서 prompt 접근권한 제한 |

Prompt governance 원칙:

```text
1. Secrets do not belong in prompts.
2. Prompts need versions, diffs, evals, and owners.
3. Public product prompts are references, not production policy.
4. Serving-layer behavior must be monitored separately.
```

## 7. 운영 체크리스트

- [ ] app prompt, API system prompt, model ID를 별도 필드로 기록한다.
- [ ] release notes의 `checked_at` 날짜를 남긴다.
- [ ] system prompt 변경은 code review와 eval을 통과시킨다.
- [ ] prompt leak을 가정하고 proprietary detail을 줄인다.
- [ ] refusal은 `stop_reason` 기반으로 계측한다.
- [ ] model snapshot과 serving layer 변화를 분리해서 사고 분석한다.

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - agent runtime의 phase-specific instruction 운영
- [[study/tech/ai/litellm]] - model gateway에서 versioning과 audit를 붙이는 방식
- [[study/tech/ai/model-context-protocol-mcp]] - tool/resource 호출과 instruction authority 경계
