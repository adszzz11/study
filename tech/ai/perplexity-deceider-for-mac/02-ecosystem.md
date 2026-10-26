---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and alternatives

## 비교

| 선택지 | 강점 | 한계 | 적합한 경우 |
|---|---|---|---|
| **Decider for Mac** | local privacy, API key/사용료 없음, text+image probability API | Apple silicon 전용, 4B Flash 품질 한계, 단일 Mac 처리량 | 민감한 로컬 파일 분류, 개발/검증, Mac automation |
| **Perplexity hosted `pplx-decider-v1.2`** | 27B, 256K context, 관련 question의 joint inference | API key·입력 token 비용, 데이터 전송 | 높은 정확도, 장문 평가, 운영 대량 처리 |
| **OpenAI Structured Outputs** | JSON Schema 준수, 생성·추출·agent 작업에 범용적 | decision 전용 probability 계약이나 완전 local Mac 실행이 중심은 아님 | 분류와 설명·추론·생성이 함께 필요한 workflow |
| **Claude Structured Outputs** | schema-constrained JSON, strict tool use | cloud 중심, schema-valid가 calibrated decision을 보장하지 않음 | typed output/tool call agent workflow |
| **Gemini Structured Outputs** | JSON Schema 기반 structured classification | decision-specialized local API가 아닌 범용 LLM output | Google stack에서 extraction/classification 통합 |
| **자체 local model + custom classifier** | 모델·데이터·운영을 완전히 통제 | 학습·평가·serving·calibration 책임 | 대규모·특수 도메인, 지속적인 자체 model 운영 |

## 핵심 구분

**Structured Output**은 “형식 보장”에 초점이 있다. JSON Schema에 맞는 output을 얻어도 label의 확률이 calibration됐거나 threshold가 적절하다는 뜻은 아니다.

**Decider**는 정의한 후보 또는 ordered scale에 대한 probability를 중심 계약으로 삼는다. 따라서 routing, scoring, blocking 같은 후속 code를 단순하게 만들지만, semantic accuracy와 threshold calibration은 여전히 labeled data로 평가해야 한다.

## 선택 흐름

1. data가 Mac 밖으로 나갈 수 없는가? 그러면 Decider for Mac부터 평가한다.
2. 출력이 단일 decision이며 확률 threshold가 핵심인가? Decider를 우선한다.
3. explanation, extraction, generation을 결합해야 하는가? Structured Outputs를 포함한 범용 LLM을 검토한다.
4. context, 정확도, 처리량이 Flash의 범위를 넘는가? hosted 27B를 candidate로 두고 재평가한다.

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- https://ai.google.dev/gemini-api/docs/structured-output
