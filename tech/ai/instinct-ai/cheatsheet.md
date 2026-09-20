---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Instinct AI: Cheatsheet

## Mental Model

```text
LLM answer bot: 질문 → 답변
Instinct-style agent: 요청 + personal context → plan → tool/device action → 결과
```

## Safe Prompt Pattern

```text
[목표]를 처리해줘.
조건: [날짜/장소/예산/대상].
먼저 [조사/초안/후보]만 보여줘.
[예약/구매/발송]은 내가 명시적으로 승인한 뒤에만 실행해.
실행 후 confirmation과 취소·환불 조건을 요약해줘.
```

## Pre-Action Checklist

- [ ] 필요한 integration만 연결했는가?
- [ ] recipient, 날짜, timezone, 예산, cancellation 조건이 명시됐는가?
- [ ] plan과 final action 사이에 review gate가 있는가?
- [ ] payment·계약·외부 message에 explicit approval이 필요한가?
- [ ] action 후 독립적인 confirmation을 확인할 수 있는가?

## Data Checklist

- [ ] model-training opt-out을 확인했는가?
- [ ] Vault data와 일반 material의 training 경계를 이해했는가?
- [ ] disconnect와 indexed data deletion이 별개임을 확인했는가?
- [ ] 사용 종료 시 deletion request 절차를 기록했는가?

## Publicly Confirmed vs Unknown

| 확인됨 | 공개 자료에서 확인되지 않음 |
|---|---|
| text/call UX, connected context, device-oriented action, Google Workspace access | underlying model, orchestration runtime, MCP/API, 전체 connector catalog |

## Sources

- https://instinct.com/
- https://instinct.com/privacy-policy
- https://instinct.com/terms
