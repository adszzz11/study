---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) Projects

[[tech/scraping/egolite-agent-browser/README|README]] · [[tech/scraping/egolite-agent-browser/04-learning/02-deep-dive|심화]]

## 실전 과제

| 프로젝트 | 목표 | 안전 경계 |
|---|---|---|
| Logged-in research assistant | SaaS, GitHub, CRM, analytics의 read-only 데이터를 citation/URL 포함 보고서로 정리 | private data를 필요한 범위로 제한하고 source tab을 보존 |
| QA copilot | local dev server UI를 Snapshot으로 확인하고 수정→reload→재검증 | production environment에서는 실행하지 않음 |
| Back-office export automation | 주문/정산 dashboard filter와 CSV download 자동화 | export·submit 직전 user confirmation |
| Web operations runbook | console 확인, support queue triage, issue creation 절차를 learning으로 축적 | issue 생성은 template·승인 규칙 적용 |
| Multi-agent browser work | Space별 병렬 조사·검증 | 같은 account의 write는 직렬화 |

## 권장 구현 순서

1. read-only workflow 하나를 정하고 허용 URL·계정·산출물을 문서화한다.
2. Task Space에서 navigation → Snapshot → extraction을 구현한다.
3. 결과에 URL, 수집 시각, tab 이름을 넣어 audit 가능하게 한다.
4. human handoff가 필요한 지점과 실패 조건을 명시한다.
5. 반복 성공한 workflow만 site learning으로 승격한다.

## Done 기준

- Snapshot ref를 재사용하지 않고 상태 변화 뒤 re-snapshot한다.
- 생성물에 source URL이 있다.
- export·submit·delete 같은 write action은 사용자 승인 없이는 실행되지 않는다.
- 사람이 종료 후 작업 tab과 결과를 검토할 수 있다.

## Sources

- https://www.egolite.app/document/en/docs/space
- https://github.com/citrolabs/ego-lite/blob/main/AGENTS.md

