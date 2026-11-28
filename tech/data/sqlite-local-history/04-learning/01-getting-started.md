---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 최소 로컬 기록함

## 실습 범위

이 실습은 직접 만든 텍스트로 저장·재조회를 확인한다. 음성 인식 엔진 설치는 포함하지 않으며, SQL과 schema는 Sokki 실제 구현이 아니다. SQLite CLI가 설치되어 있어야 한다.

## 1. 저장 단위 정하기

- 한 번의 받아쓰기에서 사용자가 확정한 텍스트를 한 기록으로 저장한다.
- 중간 인식 결과는 이 실습에서는 저장하지 않는다.
- 후보 필드는 식별자, 생성 시각, 인식 텍스트다. 경과 시간·오디오 연결 정보는 필요할 때 추가한다.

## 2. Database 만들기

빈 실습 디렉터리에서 실행한다. 명령 실행 시 해당 경로에 DB 파일이 생성된다.

```sh
sqlite3 history-demo.db
```

SQLite prompt에서 실행한다.

```sql
CREATE TABLE IF NOT EXISTS recognition_history (
  id INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  transcript TEXT NOT NULL CHECK(length(trim(transcript)) > 0)
);
INSERT INTO recognition_history (transcript)
VALUES ('로컬 기록 저장을 실습합니다.');
SELECT id, created_at, transcript
FROM recognition_history ORDER BY id DESC;
.quit
```

시각은 UTC 문자열로 기록한다. 위 INSERT는 호출할 때마다 새 행을 만든다. 실제 앱에서는 텍스트를 SQL 문자열에 이어 붙이지 않고 parameter binding을 사용한다.

## 3. 재실행 후 확인

```sh
sqlite3 history-demo.db 'SELECT id, created_at, transcript FROM recognition_history ORDER BY id DESC;'
```

- [ ] 종료 전 저장한 텍스트가 다시 보인다.
- [ ] 공백 텍스트를 넣으면 CHECK 제약으로 실패한다.
- [ ] 같은 저장 요청을 두 번 실행하면 두 행이 생기는 것을 확인한다.
- [ ] 화면 표시 시점과 저장 완료 시점을 따로 설명할 수 있다.

중복 요청에 대한 정책은 심화에서 다룬다. 이 실습은 로컬 오디오 파일을 만들지 않는다.

## 다음 학습

[[tech/data/sqlite-local-history/04-learning/02-deep-dive|저장 완료와 생애주기]] · [[tech/data/sqlite-local-history/cheatsheet|명령 요약]] · [[tech/data/sqlite-local-history/README|학습 경로]]

## Sources

- 실습 설계의 출발점: 제공 dossier, URL 미제공.
- CLI: https://www.sqlite.org/cli.html
- CREATE TABLE: https://www.sqlite.org/lang_createtable.html
- 날짜 함수: https://www.sqlite.org/lang_datefunc.html
- Parameter binding: https://www.sqlite.org/c3ref/bind_blob.html
