---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite WAL 개요

## What

rollback journal은 수정 전 page를 보관한 뒤 원본 database를 변경한다. dossier는 journal 삭제를 COMMIT 시점으로 설명한다. WAL은 원본을 유지하면서 변경된 page와 commit record를 append한다.

| 요소 | 역할 | 설계상 의미 |
|---|---|---|
| 원본 database | checkpoint로 반영된 page 저장 | COMMIT 직후 최신 상태가 모두 담겨 있지는 않을 수 있다 |
| `-wal` | 변경 page와 commit record 저장 | COMMIT된 변경도 WAL에만 존재할 수 있다 |
| wal-index / `-shm` | page 위치와 checkpoint 진행 정보 관리 | 전체 WAL 검색 비용을 줄인다 |
| checkpoint | WAL 내용을 원본으로 복사 | 읽기·쓰기 외의 세 번째 동작이다 |

## Why

읽기·쓰기의 상호 차단과 쓰기 I/O, 잦은 `fsync()` 비용을 줄이기 위한 설계다. 대부분의 시나리오에서 빠르고 I/O가 더 순차적이지만 성능은 workload와 checkpoint 정책에 달려 있다.

## 읽기 snapshot

1. read transaction이 마지막 유효 commit record 위치인 end mark를 기억한다.
2. end mark 이전 WAL에서 필요한 page의 최신 사본을 찾는다.
3. 있으면 그 사본을, 없으면 원본 database page를 읽는다.

end mark는 transaction 종료까지 고정된다. 다른 writer가 COMMIT해도 기존 reader의 관찰 시점은 변하지 않는다. reader마다 다른 시점을 볼 수 있다.

## 특징과 한계

- reader–writer 동시성은 개선되지만 writer는 하나다.
- 일반적인 WAL은 shared memory를 사용하므로 같은 host에서 동작해야 한다.
- 오래 열린 reader가 checkpoint 진행을 제한할 수 있다.
- WAL 재사용과 물리적 파일 축소는 다르다.

## 버전 구분

| 버전 | 변화 |
|---|---|
| 3.7.0 | WAL 도입 |
| 3.11.0 | 대용량 transaction도 rollback mode와 동등한 효율로 개선 |
| 3.22.0 | 조건을 만족하면 read-only WAL database 접근 가능 |

과거의 100MB·1GB 관련 경고를 현재의 보편적 제한으로 사용하지 않는다.

## 다음 단계

[[tech/backend/sqlite-wal-architecture-d6f43ae0/02-ecosystem|Rollback journal과 비교]] → [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/01-getting-started|실습]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
