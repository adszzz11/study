---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: Checkpoint·Snapshot·Durability 설계

## COMMIT과 원본 반영의 분리

```text
writer: 변경 page append → commit record append → COMMIT 완료
checkpoint: WAL sync → 원본으로 page 복사 → 원본 sync → 조건 충족 시 WAL reset
reader: 시작 시 end mark 고정 → 그 시점까지의 page 읽기 → transaction 종료
```

COMMIT된 데이터는 아직 WAL에만 있을 수 있다. database 파일만 복사하거나 WAL을 분리하는 방식은 이미 확정된 transaction의 유실이나 손상을 일으킬 수 있다.

## Checkpoint의 세 단계

| 구분 | 조건과 의미 |
|---|---|
| 진행 | reader가 필요한 범위를 침범하지 않는 page까지 원본 반영 |
| 완료 | WAL 전체 반영 및 필요한 sync 완료 |
| 재사용 | 완료 후 WAL을 사용하는 reader가 없으면 writer가 처음부터 기록 가능 |

오래된 reader에 필요한 원본 page를 checkpoint가 덮어쓰면 snapshot이 깨진다. 따라서 reader의 end mark가 진행을 제한한다. 중단된 진행 위치는 wal-index에 남아 다음 호출에서 이어갈 수 있다.

일반 checkpoint는 truncate 대신 기존 공간을 재사용한다. **WAL 파일 크기만으로 checkpoint 실패를 판정하지 않는다.**

## 자동 Checkpoint와 지연 분포

기본 임계값은 1000 pages다. 임계값에 도달하게 한 COMMIT thread가 checkpoint를 수행하므로 일부 COMMIT에 지연이 집중될 수 있다.

| 정책 | 기대 효과 | 비용·책임 |
|---|---|---|
| 잦은 checkpoint | WAL을 작게 유지, 읽기에 유리 | sync·seek 비용 증가 |
| 드문 checkpoint | 여러 쓰기에 비용 분산 | WAL 공간 및 읽기 비용 증가 |
| 별도 thread/process | COMMIT thread 부담 완화 | 주기·진행·완료 관리 필요 |

자동 checkpoint를 끄는 connection에서는 다음과 같이 설정할 수 있다. 실제 적용 범위를 확인하고 별도 실행 주체를 마련한 뒤 사용한다.

```sql
PRAGMA wal_autocheckpoint=0;
-- 별도 실행 주체에서 주기적으로 수행
PRAGMA wal_checkpoint;
```

실행 누락이나 긴 reader로 진행이 계속 제한되면 WAL이 커질 수 있다. dossier의 starvation 설명은 중간에 끝나므로 상세 회피 알고리즘까지 확정하지 않는다.

## Durability 선택

| 설정 | COMMIT 시 WAL sync | 장애 이후 의미 |
|---|---|---|
| FULL | 매 transaction 수행 | COMMIT 경로에 sync 비용 포함 |
| NORMAL | 매 COMMIT sync 생략 | 전원 장애·hard reset 후 transaction rollback 가능 |

```sql
PRAGMA synchronous=FULL;
-- 유실 허용 정책과 성능 측정을 전제로 선택하는 대안
-- PRAGMA synchronous=NORMAL;
```

dossier에 따르면 NORMAL에서는 checkpoint가 sync를 수행하는 유일한 동작이다. 이를 별도 실행 주체로 옮기면 주 query/update 경로가 직접 sync에 막히는 상황을 줄일 수 있다.

**최근 transaction 유실과 database corruption을 구분한다.** checkpoint의 WAL 선행 sync와 reset 전 원본 sync 순서는 corruption 방지를 위한 것이다. 이는 NORMAL의 최근 COMMIT 유실 가능성을 없애는 설명이 아니다.

## 파일 수명

마지막 connection을 정상 종료하면 보통 최종 checkpoint 후 WAL·SHM이 삭제된다. 비정상 종료나 `SQLITE_FCNTL_PERSIST_WAL` 때문에 남을 수도 있다. 잔존 자체는 오류의 증거가 아니다. 원문이 제시하는 WAL 제거 절차는 SQLite open interface로 열고 닫는 방법이며 수동 삭제가 아니다.

## 연결

[[tech/backend/sqlite-wal-architecture-d6f43ae0/05-projects|정책 검증 프로젝트]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
