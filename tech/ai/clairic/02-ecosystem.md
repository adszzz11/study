---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and comparison

| 대안/계층 | 주 역할 | 출력 방식 | Clairic보다 적합한 경우 |
| --- | --- | --- | --- |
| **Clairic** | extraction·간단 계산·estimate·forecast | bounded typed value, confidence, span | 대량 문서에서 검증 가능한 field 추출 |
| **Cloudflare Clef / Jev** | decision/classification | 정해진 option의 probability | refund 여부, 담당 팀 routing처럼 선택지가 정의됨 |
| **GPT / Claude / Gemini 등 LLM** | reasoning·설명·문서 작성 | free-form generated text | 복합 reasoning, 정책 해석, 사용자 응답 생성 |
| OCR + regex + rules | 고정 양식 extraction | deterministic field | 형식이 안정적이고 예외율이 낮음 |
| 전용 time-series model | 시계열 예측 | 수치 forecast | metric별 학습·검증이 필요한 고정밀 예측 |

## 권장 cascade

```text
raw email / PDF / OCR / image
            │
            ▼
     Clairic: facts + span + uncertainty
            │
            ▼
       Clef: policy decision / routing
            │
            ▼
 LLM: 사용자용 설명·응답 생성
```

이 분리는 각 모델에 맞는 일을 배정한다. 예를 들어 claim ticket에서 Clairic이 order ID·damage·amount를 뽑고, Clef가 refund/repair/escalation을 분류하며, LLM이 고객 응답을 작성한다.

Cloudflare의 예시 benchmark는 이 cascade가 all-LLM pipeline보다 latency와 비용이 낮았다고 보고한다. 이는 공급사 실험 결과이므로, 실제 채택 전에는 자사 문서·오류 비용·review 시간을 포함한 corpus 평가가 필요하다.

## 선택 질문

1. 결과가 미리 정의된 typed field인가, 열린 문장인가?
2. 값의 원문 근거(span)를 운영자가 즉시 확인해야 하는가?
3. failure가 비용·법무·고객 피해로 이어지는가? 그렇다면 deterministic validation과 human review는 어디에 둘 것인가?
4. forecast가 실제 시계열 학습 문제인가? 그렇다면 Clairic output을 보조 신호로만 두고 별도 backtest를 하는가?

## Sources

- https://blog.cloudflare.com/clairic-extraction-model/
- https://developers.cloudflare.com/workers-ai/models/clef/
- https://developers.cloudflare.com/workers-ai/models/clairic/
