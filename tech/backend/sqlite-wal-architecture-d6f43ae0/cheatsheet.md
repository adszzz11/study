---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite WAL Cheatsheet

## 설정·조회

```sql
SELECT sqlite_version();
PRAGMA journal_mode=WAL;  -- 반환값 wal 확인, database에 지속
PRAGMA journal_mode;
PRAGMA synchronous=FULL; -- COMMIT마다 WAL sync
PRAGMA synchronous;      -- connection 설정 확인
PRAGMA wal_autocheckpoint; -- 기본 1000 pages
PRAGMA wal_checkpoint;   -- 호출과 완료는 구분
```

`NORMAL`과 자동 checkpoint 해제는 정책 선택이다. 설정 예시를 그대로 적용하기 전에 유실 허용 범위와 checkpoint 실행 책임을 정한다.

## 기억할 구분

| 오해 | 올바른 해석 |
|---|---|
| WAL은 여러 writer가 동시에 쓴다 | writer는 하나, reader–writer가 공존한다 |
| COMMIT이면 원본 파일이 최신이다 | 변경은 아직 WAL에만 있을 수 있다 |
| checkpoint 호출이면 완료다 | reader 때문에 일부만 진행될 수 있다 |
| checkpoint 완료면 파일이 줄어든다 | 보통 truncate하지 않고 공간을 재사용한다 |
| 기본 임계값은 4MB다 | 1000 pages이며 byte 크기는 page size에 의존한다 |
| NORMAL이면 corruption을 허용한다 | 최근 transaction 유실 가능성과 corruption 방지 순서를 구분한다 |
| WAL 잔존은 오류다 | 비정상 종료·PERSIST_WAL 등으로 남을 수 있다 |
| WAL은 임시 파일이니 삭제 가능하다 | persistent state의 일부이므로 수동 삭제하지 않는다 |

## 도입 전 체크

- [ ] 모든 process가 같은 host에서 접근한다.
- [ ] 긴 reader transaction과 checkpoint 진행을 관찰한다.
- [ ] WAL 전환 반환값과 사용 SQLite 버전을 확인한다.
- [ ] WAL mode에서 `page_size` 변경을 시도하지 않는다.
- [ ] 여러 ATTACH database 집합의 atomicity를 가정하지 않는다.
- [ ] read-only 조건과 DELETE mode 배포 권고를 확인한다.
- [ ] database 파일만 복사하는 절차를 안전한 복사로 가정하지 않는다.

## 연결

[[tech/backend/sqlite-wal-architecture-d6f43ae0/04-learning/02-deep-dive|설계 근거]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/03-references|근거 범위]] · [[tech/backend/sqlite-wal-architecture-d6f43ae0/README|학습 경로]]

## Sources

- https://www.sqlite.org/wal.html — 제공된 dossier의 본문 범위(§6 checkpoint starvation 설명 도중까지)를 근거로 정리.
