---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - references
  - prompt-governance
type: tech-tool-study
parent: "[[README]]"
---

# Claude System Prompts Release Notes - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. 핵심 공식 문서

| 우선순위 | 문서 | URL | 읽을 포인트 |
|----------|------|-----|-------------|
| 1 | Anthropic Claude API Docs, System Prompts | https://platform.claude.com/docs/en/release-notes/system-prompts | `claude.ai`/mobile core system prompt release notes, API 미적용 범위 |
| 2 | Anthropic, Model IDs and versioning | https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | Claude 4.6+ dateless ID가 pinned snapshot이라는 semantics |
| 3 | Anthropic, Prompting best practices | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts | API `system` parameter로 role/context 지정하는 방식 |
| 4 | Anthropic, What's new in Claude Opus 4.8 | https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8 | mid-conversation system messages, prompt cache 보존 |
| 5 | Anthropic, Introducing Claude Fable 5 and Claude Mythos 5 | https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5 | safety classifier와 `stop_reason: "refusal"` |
| 6 | Anthropic, Reduce prompt leak | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak | prompt leak 완전 방지 불가, mitigation pattern |
| 7 | OpenAI, Text generation guide | https://platform.openai.com/docs/guides/text?api-mode=responses | `instructions`, `developer` message, prompt lifecycle guidance |
| 8 | Google Gemini, Text generation docs | https://ai.google.dev/gemini-api/docs/text-generation | `system_instruction` / `systemInstruction` usage |

## 2. Anthropic 문서별 메모

### System Prompts release notes

- `claude.ai` web/mobile app에서 주입되는 core system prompt의 public changelog다.
- Claude API에는 적용되지 않는다.
- 2026-06-20 기준 최신 항목은 **Claude Fable 5, June 9, 2026**이다.
- 2025-2026 구간에 Sonnet 3.7, Claude 4, Opus 4.1, Sonnet/Haiku/Opus 4.5, Opus/Sonnet 4.6, Opus 4.7, Opus 4.8, Fable 5가 포함된다.

### Model IDs and versioning

- Claude 4.6 이후 dateless ID는 alias가 아니라 pinned snapshot이다.
- Anthropic은 기존 model ID의 weights/config를 업데이트하지 않고, 새 버전은 새 model ID로 출시한다고 설명한다.
- 다만 serving infrastructure는 바뀔 수 있다.

### Opus 4.8

- mid-conversation system messages를 지원한다.
- 긴 대화 중 user turn 직후 `role: "system"` message를 추가할 수 있다.
- full system prompt를 반복하지 않고 prompt cache hit를 보존하는 목적이 있다.

### Fable 5 / Mythos 5

- safety classifiers가 요청을 거절할 수 있다.
- refusal은 HTTP error가 아니라 성공 응답 안의 `stop_reason: "refusal"` 형태로 반환될 수 있다.

### Reduce prompt leak

- prompt leak 완전 방지는 어렵다.
- system prompt로 context/query를 분리하되 post-processing, audits, proprietary detail 제거를 병행해야 한다.

## 3. 확인 질문 체크리스트

| 질문 | 확인 문서 |
|------|-----------|
| 이 prompt가 API에 자동 적용되는가? | System Prompts release notes |
| 내가 쓰는 model ID는 pinned snapshot인가? | Model IDs and versioning |
| 긴 대화 중 system instruction을 갱신할 수 있는가? | What's new in Claude Opus 4.8 |
| refusal을 error handling으로 잡아야 하는가? | Fable 5 / Mythos 5 |
| system prompt에 secret policy를 넣어도 되는가? | Reduce prompt leak |
| OpenAI equivalent는 무엇인가? | OpenAI Text generation guide |
| Gemini equivalent는 무엇인가? | Gemini text generation docs |

## 4. 연구/운영에 남길 메타데이터

```yaml
source_url: https://platform.claude.com/docs/en/release-notes/system-prompts
observed_at: 2026-06-20
latest_entry:
  model: Claude Fable 5
  date: 2026-06-09
scope: claude.ai web/mobile
api_applies: false
risk_tags:
  - reproducibility
  - prompt-governance
  - prompt-leak
  - serving-layer-change
```

## 관련 노트

- [[study/tech/ai/ai-ecosystem/01-overview]] - provider 공식 문서 비교
- [[study/tech/ai/litellm]] - production prompt와 model routing reference로 연결
- [[study/tech/ai/model-context-protocol-mcp]] - runtime context 문서와 함께 읽기
