---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Instinct AI: Projects

## 1. Personal Ops Agent

calendar·email을 바탕으로 daily briefing, 놓친 회신, 다음 action을 매일 요약한다. 처음에는 read-only summary로 운영하고, message draft 이후에도 자동 발송은 금지한다.

## 2. Travel Concierge

```text
조건 수집 → 항공/숙소 후보 조사 → 비교표 → 사용자 최종 승인 → 예약 → confirmation 검증
```

여행 조건을 structured brief로 준다: 날짜, 출발지, 예산, 인원, 수하물, cancellation 조건, 선호도. 예약은 “최종 승인 후” 단계에만 둔다.

## 3. Household Admin

수리 기사 견적 수집, 예약 가능한 시간 조율, 영수증과 confirmation message 정리를 맡긴다. 결제와 계약 확정은 human approval을 유지한다.

## 4. Subscription & Renewal Watcher

갱신일, 가격 변경, 취소 policy를 추적해 알림을 만든다. 실제 cancellation은 명시적 재확인 뒤에만 실행한다.

## 5. Agent Safety Evaluation

같은 task를 Instinct, ChatGPT agent, Gemini Spark 등에 제공해 비교 benchmark를 만든다.

| 측정 항목 | 기록 방식 |
|---|---|
| 성공률 | 동일 acceptance criteria를 충족한 task 비율 |
| Human intervention | 개입 이유·단계·횟수 |
| Permission scope | 연결 권한과 실제 action의 차이 |
| Recovery | 오류 후 취소·수정·재시도 가능성 |
| 비용 | task당 직접 비용과 검토 시간 |

주의: Instinct Terms는 benchmarking 목적 사용을 제한한다고 명시한다. 실제 비교 실험 전 최신 약관과 허용 범위를 확인한다.

## Sources

- https://instinct.com/terms
- https://instinct.com/privacy-policy

