---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - cheatsheet
  - system-prompt
type: tech-tool-study
parent: "[[README]]"
---

# Claude System Prompts Release Notes - 치트시트

> [[README|목차로 돌아가기]]

---

## 한 줄 구분

| 용어 | 기억할 문장 |
|------|-------------|
| Claude System Prompts release notes | `claude.ai`/mobile core system prompt 공개 변경 로그 |
| Claude API `system` | API caller가 직접 넣는 developer-controlled instruction |
| Model ID | model weights/config snapshot을 식별하는 ID |
| Serving layer | router, safety classifier, sampling logic 등 model 외부 실행 계층 |
| Prompt governance | prompt를 versioned policy artifact로 관리하는 운영 규율 |
| Prompt leak | system prompt나 hidden instruction이 사용자에게 노출되는 리스크 |

## 최신 기준

```yaml
checked_at: 2026-06-20
latest_entry:
  model: Claude Fable 5
  date: 2026-06-09
scope:
  - claude.ai
  - iOS app
  - Android app
applies_to_api: false
```

## Claude API 기본 형태

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a careful technical assistant.",
    messages=[
        {"role": "user", "content": "Explain prompt governance."}
    ],
)
```

## Provider별 instruction field

| Provider | API primitive | 비고 |
|----------|---------------|------|
| Anthropic Claude | `system` | app release notes와 별개 |
| OpenAI | `instructions`, `developer` message | user보다 높은 authority |
| Google Gemini | `system_instruction` / `systemInstruction` | config 기반 behavior guide |

## 재현성 체크

| 기록할 것 | 예시 |
|-----------|------|
| Surface | `claude.ai`, `anthropic_api`, `openai_responses` |
| Model ID | `claude-sonnet-4-6` |
| Prompt version | `study-note-v3` |
| Release note checked_at | `2026-06-20` |
| Sampling | temperature, top_p 등 |
| Safety result | `stop_reason`, refusal 여부 |
| Product state | project, file, tool, conversation context |

## Behavior 분석 공식

```text
observed behavior
  != model weights only

observed behavior
  = model snapshot
  + app/API system prompt
  + context
  + serving infrastructure
  + safety classifier
  + sampling
```

## Prompt leak 방어

| 원칙 | 실행 |
|------|------|
| Secrets out of prompts | API key, private URL, internal policy 제거 |
| Minimize proprietary detail | 공개되어도 되는 수준으로 instruction 작성 |
| Separate context/query | system prompt와 user data를 분리 |
| Post-process outputs | redaction, allowlist, sensitive field filtering |
| Audit regularly | prompt extraction 시도와 diff review |
| Version everything | prompt, model ID, eval result, owner 기록 |

## Refusal handling

```json
{
  "stop_reason": "refusal"
}
```

| 하지 말 것 | 할 것 |
|------------|-------|
| HTTP error만 refusal로 간주 | response body의 `stop_reason` 확인 |
| 무조건 retry | safety refusal과 transient error 분리 |
| raw provider message 그대로 노출 | product UX에 맞게 변환 |
| refusal rate 미계측 | eval/audit metric으로 기록 |

## 빠른 판단

| 질문 | 답 |
|------|----|
| Claude web prompt가 API에 자동 적용되나? | 아니오 |
| release notes는 왜 유용한가? | product-level prompt transparency와 behavior change 추적 |
| Claude 4.6+ dateless ID는 alias인가? | dossier 기준 alias가 아니라 pinned snapshot |
| model ID가 고정되면 behavior가 완전히 고정되나? | 아니오, serving layer가 남는다 |
| system prompt로 leak을 완전히 막을 수 있나? | 아니오, mitigation과 audit가 필요 |

## 관련 노트

- [[study/tech/ai/litellm]] - multi-provider prompt/routing 관리
- [[study/tech/ai/model-context-protocol-mcp]] - runtime context와 tool boundary
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent instruction governance
