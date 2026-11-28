---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# WAL과 Rollback Journal 비교

## 비교 범위

제공 자료가 직접 비교하는 대안은 SQLite 내부의 rollback journal 계열이다. 다른 database 제품의 우열이나 benchmark를 주장할 근거는 없다.

| 항목 | WAL | Rollback journal |
|---|---|---|
| 변경 기록 | 새 page를 WAL에 append | 이전 page를 journal에 보관 후 원본 수정 |
| COMMIT | commit record append | dossier에서는 journal 삭제로 설명 |
| 읽기·쓰기 | reader와 writer 공존 가능 | 쓰기와 읽기의 상호 차단 발생 가능 |
| writer | 동시에 하나 | WAL 전환이 다중 writer 병렬화를 제공하지 않음 |
| 원본 반영 | checkpoint로 별도 수행 | transaction 중 원본 수정 |
| I/O | 더 순차적이며 sync 호출 감소 가능 | workload별 비교 필요 |
| 읽기 위주 성능 | 약 1~2% 느릴 수도 있음 | 읽기 위주 비교 기준 |
| 운영 파일 | database + WAL + shared-memory 파일 | database와 rollback journal 관리 |
| ATTACH 집합 atomicity | 각 database 내부만 atomic | WAL 선택 시 집합 atomicity 차이를 확인해야 함 |

## 선택 질문

- 읽기·쓰기 중첩이 실제 병목인가? WAL이 직접 개선하는 부분이다.
- 쓰기 병렬화가 필요한가? WAL만으로 해결되지 않는다.
- application이 checkpoint 주기와 긴 read transaction을 관리할 수 있는가?
- 최근 COMMIT의 전원 장애 내구성이 필요한가? `synchronous` 설정까지 결정한다.
- read-only 배포인가? `DELETE` mode 전환 권고를 먼저 검토한다.

## 연결

[[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/02-deep-dive|정책과 trade-off]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
