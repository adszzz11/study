---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite WAL의 동시성·Checkpoint·내구성 설계 분석

> **한 줄 정의**: SQLite WAL(Write-Ahead Logging)은 변경 내용을 별도 log에 append하여 COMMIT하고, 이후 checkpoint로 원본 database에 반영하는 transaction 처리 방식이다.

## Overview

WAL은 COMMIT과 원본 database 반영을 분리해 reader와 writer의 동시 실행을 가능하게 한다. 단, **writer는 동시에 하나**이며 checkpoint와 durability 정책을 함께 설계해야 한다.

- reader는 transaction 시작 시 정한 end mark를 기준으로 일관된 snapshot을 읽는다.
- `-wal`은 COMMIT된 변경을 포함할 수 있는 persistent state다. 수동 삭제하지 않는다.
- 기본 자동 checkpoint 임계값은 **1000 pages**이며 고정 4MB가 아니다.
- `synchronous=NORMAL`은 전원 장애 이후 최근 transaction의 유실 가능성을 허용한다.

이 노트는 제공된 dossier 범위의 분석이다. 목차에만 등장한 WAL-reset bug나 `SQLITE_BUSY`의 상세 조건은 다루지 않는다.

## Learning Path

- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/01-overview|Overview]] — 구성 요소와 읽기·쓰기 흐름 이해
- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/02-ecosystem|비교]] — rollback journal과 선택 기준 비교
- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/01-getting-started|시작하기]] — WAL 전환과 두 connection 실습
- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/02-deep-dive|심화 학습]] — checkpoint·snapshot·내구성 설계
- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/05-projects|실습 프로젝트]] — 측정으로 정책 검증
- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/cheatsheet|Cheatsheet]] — 설정 및 운영 주의점 확인
- [ ] [[tech/backend/sqlite-wal-architecture-d6f43ae0/03-references|References]] — 출처와 버전별 근거 확인

## When To Use

- 같은 host의 여러 connection에서 읽기와 쓰기가 겹치는 embedded application.
- 쓰기를 직렬화할 수 있고, reader transaction 수명과 checkpoint 실행을 관리할 수 있는 경우.
- 순차 I/O와 sync 호출 감소의 효과를 실제 workload에서 검증할 수 있는 경우.

## When Not To Use

- 서로 다른 host가 network filesystem의 database를 공유해야 하는 경우.
- 다중 writer의 병렬 실행이나 여러 ATTACH database 전체의 atomic commit이 필요한 경우.
- read-only media 배포: 원문은 `journal_mode=DELETE` 전환을 권장한다.
- 대부분 읽기인 workload: rollback journal 대비 약 1~2% 느릴 수 있으므로 측정 후 선택한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Backend]]
- [[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/02-deep-dive|SQLite WAL의 snapshot·checkpoint 상세 분석]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
