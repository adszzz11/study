---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# 실습 프로젝트: WAL 정책 검증

아래는 제안 실험이며 측정값이나 성능 향상을 미리 가정하지 않는다. 모두 폐기 가능한 로컬 database에서 수행한다.

## 프로젝트 1. Snapshot 수명 관찰

- 두 connection으로 [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/01-getting-started|시작 실습]]을 재현한다.
- reader transaction 시작·종료, writer COMMIT, 각 SELECT 결과를 시간순으로 기록한다.
- 완료 기준: 같은 read transaction에서는 관찰 값이 유지되고, 종료 후 새 읽기에서 변경이 보임을 설명한다.

## 프로젝트 2. Checkpoint와 COMMIT 지연

| 조건 | 측정 항목 |
|---|---|
| 기본 자동 checkpoint | COMMIT p50/p95/p99, 처리량 |
| 자동 checkpoint 해제 + 별도 실행 | 동일 지연 지표, checkpoint 실행 시간·진행 상태 |
| 긴 reader 유지/종료 | WAL 크기 추이, 반영 진행, 읽기 지연 |

- SQLite 버전, page size, storage, transaction 크기와 reader 수를 고정·기록한다.
- 자동 checkpoint를 해제하면 실험 harness가 반드시 checkpoint 실행을 책임진다.
- 완료 기준: 느린 COMMIT과 checkpoint 실행의 관계를 설명하고, WAL 크기와 미반영 상태를 구분한다.

## 프로젝트 3. FULL과 NORMAL의 선택 문서

- 동일 workload에서 각 connection의 `synchronous`를 명시하고 처리량·지연을 비교한다.
- 전원 장애 후 최근 transaction 유실을 업무가 허용하는지 문서화한다.
- 단순 process 종료를 전원 장애와 동일시하거나, 성능 실험을 내구성 증명으로 해석하지 않는다.
- 완료 기준: 선택한 정책, 허용 가능한 유실, checkpoint 실행 책임과 관찰 지표를 한 표로 정리한다.

## 제출 산출물

환경 정보, 재현 SQL, 측정 표, 관찰과 해석을 분리한 보고서. 결과는 이 노트 폴더 안에서만 관리하고 vault 관리 파일은 수정하지 않는다.

## 연결

[[tech/backend/sqlite-wal-architecture-d6f43ae0/cheatsheet|운영 체크]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
