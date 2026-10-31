---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - anthropic
  - system-prompt
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# Claude System Prompts Release Notes - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - 무엇인가?

Claude System Prompts release notes는 Anthropic이 `claude.ai` 웹 앱과 iOS/Android 앱에서 Claude에 주입하는 **core system prompt**의 공개 변경 로그다. 여기에는 현재 날짜, 응답 형식, Markdown/code block 사용 방식, 안전/행동 지침, 제품 UX와 연결된 기본 behavior가 포함된다.

```text
User in claude.ai
  -> Claude web/mobile app
    -> App-level core system prompt
    -> User message
    -> Model + serving layer
    -> Assistant response
```

중요한 경계는 이 release notes가 **Claude API의 `system` parameter와 별개**라는 점이다. API 사용자는 Messages API에서 직접 `system` field를 제공해야 하며, 웹 Claude와 동일한 runtime prompt가 자동으로 적용된다고 가정하면 안 된다.

## 2. Why - 왜 중요한가?

### Transparency

Claude 같은 hosted AI product는 model weights만으로 동작하지 않는다. 제품이 주입하는 system prompt, safety policy, formatting instruction, tool policy가 사용자가 관찰하는 behavior를 만든다. 공개 release notes는 이 숨은 product behavior 일부를 시간축으로 추적하게 해준다.

### Reproducibility 한계

웹 Claude에서 보이는 응답을 API에서 재현하려 할 때 다음 변수가 함께 작동한다.

| 변수 | 의미 |
|------|------|
| App prompt | `claude.ai`/mobile이 대화 시작 시 넣는 core system prompt |
| Model snapshot | 특정 model ID가 가리키는 weights/config |
| Serving infrastructure | request router, safety classifiers, sampling logic |
| User context | project, artifact, file, tool, conversation history |
| Product policy | refusal, formatting, tool behavior, privacy UX |

따라서 "Claude가 이렇게 답했다"는 관찰은 API model의 순수 성능 평가와 분리해야 한다.

### Prompt governance

System prompt는 이제 단순 prompt engineering 산출물이 아니라 runtime policy artifact다. 제품 정책, UX convention, safety boundary, formatting rule, tool 사용 기준을 한 파일 또는 prompt bundle에 넣고 versioning해야 한다.

## 3. 핵심 특징

| 특징 | 설명 |
|------|------|
| Scope 분리 | release notes의 system prompt는 `claude.ai`와 모바일 앱용이며 API에는 적용되지 않음 |
| Model generation별 log | 2025-2026 구간에 Sonnet 3.7, Claude 4, Opus/Sonnet/Haiku 4.x, Fable 5 항목 포함 |
| Model ID 안정성 | Claude 4.6 이후 dateless ID는 alias가 아니라 pinned snapshot |
| Serving layer 변수 | model weights가 고정되어도 router/classifier/sampling은 바뀔 수 있음 |
| Safety 결합 | refusal이 HTTP error가 아니라 successful response의 `stop_reason: "refusal"`로 올 수 있음 |
| Prompt leak 리스크 | system prompt leak 완전 방지는 어렵고 후처리와 audits가 필요 |

## 4. 최신 항목 기준

2026-06-20 기준 dossier에 따르면 해당 release notes의 최신 항목은 다음과 같다.

| 항목 | 값 |
|------|----|
| 최신 release note | Claude Fable 5 |
| 날짜 | 2026-06-09 |
| 범위 | `claude.ai` web/mobile core system prompt |
| API 적용 여부 | 적용 안 됨 |

2025-2026 구간에는 Sonnet 3.7, Claude 4, Opus 4.1, Sonnet/Haiku/Opus 4.5, Opus/Sonnet 4.6, Opus 4.7, Opus 4.8, Fable 5가 순차적으로 포함된다.

## 5. API와의 구분 예시

웹 Claude의 core system prompt가 API에 자동 적용되는 것이 아니므로 API에서는 명시적으로 role과 context를 지정한다.

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a careful Korean technical study-note assistant.",
    messages=[
        {"role": "user", "content": "Summarize the release notes implications."}
    ],
)
```

## 6. 읽을 때의 기준

- **제품 prompt인가, API instruction인가?**: `claude.ai`/mobile prompt와 API `system` field를 분리한다.
- **model ID가 snapshot인가, alias인가?**: Claude 4.6 이후 semantics를 확인한다.
- **behavior 변화 원인이 prompt인가?**: serving layer, safety classifier, product UI도 함께 의심한다.
- **내 앱에 복사할 수 있는가?**: 공개 prompt는 참고 자료이지 내 domain policy의 대체물이 아니다.
- **leak되어도 되는가?**: proprietary detail은 system prompt에 넣지 않는 설계가 필요하다.

---

## 관련 노트

- [[study/tech/ai/litellm]] - API gateway에서 provider별 system prompt와 routing을 다루는 맥락
- [[study/tech/ai/model-context-protocol-mcp]] - runtime context/tool 주입과 prompt boundary 비교
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent CLI의 system prompt와 tool policy 운영

## References

- [Anthropic Claude API Docs, System Prompts](https://platform.claude.com/docs/en/release-notes/system-prompts)
- [Anthropic, Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)
- [Anthropic, Prompting best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)
