---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon Projects

## 1. AR / Invoice Operations

**흐름**: billing mailbox에서 미납 invoice 추출 → tracker App record 갱신 → 담당자별 follow-up draft 생성 → 승인 후 발송.

| 설계 항목 | 권장안 |
| --- | --- |
| Connection | read-only mailbox부터 시작, tracker의 제한된 field만 write |
| record | invoice ID, due date, owner, status, evidence link, draft 상태 |
| 승인 | customer email은 사람이 검토하고 Send |
| 점검 | 중복 invoice, 잘못된 고객 매칭, credit 사용량 |

## 2. Sales Research Cockpit

**흐름**: Apollo/Ahrefs 등 데이터와 CRM 연결 → target account 조사 → qualification record 작성 → 영업 담당자 briefing과 follow-up draft 제공.

처음에는 research 결과를 draft record로 만들고, CRM의 공식 field 갱신은 담당자가 검토한 뒤 승인한다. 출처 URL과 조사 시각을 record에 남겨 업데이트 가능한 intelligence로 만든다.

## 3. Field Operations Input App

**흐름**: warehouse count, 점검, 공급사 이슈를 모바일 form으로 접수 → record 변화가 agent를 trigger → 이상치 요약 → ops Room escalation.

핵심은 form validation과 escalation threshold다. agent가 수량을 자동 수정하지 않게 하고, 원본 제출 record와 agent의 해석을 분리한다.

## 4. Agency Client Workspace

고객사별 별도 Workspace로 data, member, Connection을 격리한다. 재사용 가능한 agent/workflow pattern은 만들되, 고객 A의 Connection이나 Room 맥락이 고객 B로 넘어가지 않는지 검토한다.

## 5. Engineering-to-Business Handoff

Codex 또는 Claude Code가 코드·분석 결과를 Room에 남기면 비개발 팀은 같은 맥락에서 App 요구사항, 배포 승인, 운영 이슈를 이어간다.

```text
IDE / terminal agent → Kylon Room → product/ops review → App or workflow change
```

secret, private repository 내용, 고객 식별 정보는 Room에 공유할 수 있는 범위를 먼저 정한다.

## Project Definition of Done

- [ ] 업무 입력·출력·소유자가 명시되어 있다.
- [ ] Connection별 최소 권한과 실제 계정을 검토했다.
- [ ] 위험 action의 승인자와 draft-first 규칙이 정해져 있다.
- [ ] 실패·중복·예외 처리 결과가 Room 또는 record에 남는다.
- [ ] run history에서 비용과 실패율을 검토한다.
- [ ] 필요 시 workflow를 중지하거나 Connection을 취소하는 rollback 절차가 있다.

## Related Notes

- [[04-learning/01-getting-started|Getting started]]
- [[04-learning/02-deep-dive|Deep dive]]
