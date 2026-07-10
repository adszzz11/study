---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - getting-started
  - system-prompt
type: tech-tool-study
parent: "[[../README]]"
---

# 시작하기 - Claude System Prompts Release Notes 읽기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 목표

이 단계의 목표는 release notes를 "복사할 prompt 모음"이 아니라 **제품 runtime policy의 변경 로그**로 읽는 습관을 만드는 것이다.

완료하면 다음을 구분할 수 있어야 한다.

- `claude.ai`/mobile app prompt와 Claude API `system` parameter
- model snapshot 변화와 app prompt 변화
- refusal/error handling과 safety classifier
- prompt transparency와 prompt leak risk

## 1. 범위 먼저 확인

System Prompts release notes를 읽을 때 첫 질문은 이것이다.

```text
이 문서는 어떤 runtime에 적용되는가?
```

정답은 `claude.ai` 웹 앱과 iOS/Android 앱이다. API에는 자동 적용되지 않는다.

| 관찰 대상 | 적용 여부 | 설명 |
|-----------|-----------|------|
| `claude.ai` web | 적용 | app-level core system prompt가 대화 시작 시 주입됨 |
| Claude mobile | 적용 | iOS/Android app에서도 같은 범주의 prompt 사용 |
| Claude API | 미적용 | API caller가 `system` parameter를 직접 제공 |
| 다른 provider API | 미적용 | OpenAI/Gemini는 별도 instruction primitive 사용 |

## 2. 최신 항목 기록

2026-06-20 기준 dossier에서 확인한 최신 항목은 다음과 같다.

```yaml
latest_system_prompt_release:
  model: Claude Fable 5
  release_date: 2026-06-09
  checked_at: 2026-06-20
  scope:
    - claude.ai
    - iOS app
    - Android app
  applies_to_api: false
```

노트나 실험 로그에는 항상 `checked_at`을 남긴다. release notes는 시간에 따라 바뀌는 문서이므로 "최신"이라고만 쓰면 재현성이 떨어진다.

## 3. API에서는 직접 system prompt 작성

Anthropic API에서는 다음처럼 application-specific instruction을 넣는다.

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1200,
    system=(
        "You are a technical study-note assistant. "
        "Write in Korean, preserve English technical terms, "
        "and distinguish source facts from inference."
    ),
    messages=[
        {
            "role": "user",
            "content": "Explain Claude System Prompts release notes."
        }
    ],
)
```

이때 release notes의 public prompt는 참고 자료일 뿐이다. 내 application의 domain, safety boundary, output format, tool policy는 별도 versioning 대상이다.

## 4. 간단 비교 실험

웹 Claude와 API를 비교하려면 다음처럼 실험 조건을 분리한다.

| 실험 | 고정할 것 | 관찰할 것 |
|------|-----------|-----------|
| Web app | 같은 계정, 같은 대화 시작, 같은 user prompt | app prompt가 만드는 formatting/behavior |
| API no system | 같은 model ID, 같은 user prompt | base behavior에 가까운 응답 |
| API custom system | 같은 model ID, 명시 system prompt | instruction에 따른 behavior 변화 |
| API repeated | temperature/sampling 설정 | serving/sampling variability |

실험 로그 예시:

```yaml
experiment:
  date: 2026-06-20
  prompt: "Explain how to read Claude system prompt release notes."
  surfaces:
    - claude.ai
    - anthropic_api_without_system
    - anthropic_api_with_custom_system
  model_id: claude-sonnet-4-6
  notes:
    - "Do not attribute all differences to model weights."
    - "Check app prompt, serving layer, safety classifier separately."
```

## 5. 초보자가 자주 하는 실수

| 실수 | 왜 문제인가 | 교정 |
|------|-------------|------|
| 웹 Claude prompt를 API 기본값으로 가정 | API에는 적용되지 않음 | API `system` field를 직접 작성 |
| model ID만 같으면 결과가 같다고 가정 | app prompt와 serving layer가 다름 | surface와 runtime을 로그에 기록 |
| system prompt에 secret policy를 넣음 | prompt leak 완전 방지는 불가 | proprietary detail 최소화, post-processing |
| refusal을 HTTP error로만 처리 | success response의 `stop_reason`일 수 있음 | response body의 stop reason 확인 |
| 최신 항목 날짜를 안 남김 | release notes가 바뀌면 문맥 손실 | `checked_at` 저장 |

## 6. 완료 체크리스트

- [ ] System Prompts release notes의 적용 범위를 설명할 수 있다.
- [ ] Claude API `system` parameter와 app core system prompt를 구분할 수 있다.
- [ ] 최신 항목을 `model`, `release_date`, `checked_at`으로 기록했다.
- [ ] 웹/API 비교 실험에서 app prompt, model ID, serving layer를 분리했다.
- [ ] prompt leak mitigation 원칙을 3개 이상 말할 수 있다.

---

## 관련 노트

- [[study/tech/ai/litellm]] - API 호출면에서 system prompt를 관리하는 gateway 패턴
- [[study/tech/ai/model-context-protocol-mcp]] - runtime tool/context 주입과 system instruction 경계
- [[study/tech/ai/ai-ecosystem/01-overview]] - provider별 API surface 비교
