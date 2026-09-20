---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Instinct AI: Getting Started

## Goal

낮은 위험의 read/draft task로 action quality와 approval behavior를 관찰한 뒤, 필요한 integration만 단계적으로 추가한다.

## 1. Connect Least Privilege

- 처음부터 mailbox, location, payment, password를 모두 연결하지 않는다.
- 첫 task에 필요한 integration 하나만 부여한다.
- Workspace를 연결했다면 access revoke, indexed data deletion, training opt-out의 위치를 먼저 확인한다.

## 2. Start With Read or Draft

```text
오늘 calendar를 요약해줘.
겹치는 일정과 준비가 필요한 항목은 별도 bullet로 표시해줘.
외부 변경은 하지 마.
```

```text
이 email thread의 follow-up 초안을 만들어줘.
수신자·날짜·보낼 내용은 실행 전에 나에게 보여주고, 보내지는 마.
```

관찰 항목은 정확성, 누락, context 해석, 외부 변경 여부, 결과의 검증 가능성이다.

## 3. Plan Before Act

예약·구매·대외 메시지는 다음 정보를 request에 넣는다.

| 필드 | 예시 |
|---|---|
| 대상 | 어느 업체/recipient인지 |
| 조건 | 날짜, 시간, 장소, 인원 |
| 제약 | 최대 예산, cancellation/refund 조건 |
| 승인 | “후보만 제시”, “최종 실행 전 재확인” |

```text
서울역 근처에서 10월 5일 19:00, 2명 저녁 식사 후보를 찾아줘.
1인 5만원 이하, 취소 조건을 표로 비교해줘.
예약은 하지 말고 내가 '예약 진행'이라고 답할 때만 실행해.
```

## 4. Review Result

- [ ] 대상과 동명이인이 없는가?
- [ ] 날짜·시간·timezone·예산이 request와 일치하는가?
- [ ] 취소·환불·수수료를 확인했는가?
- [ ] 실제 action이 있었으면 독립적인 service record도 확인했는가?

## Sources

- https://instinct.com/
- https://instinct.com/privacy-policy
- https://instinct.com/terms

