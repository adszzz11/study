---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: SQLite 로컬 기록

## 역할 구분

| 질문 | 답 |
|---|---|
| 누가 음성을 텍스트로 바꾸는가? | 음성 인식·Whisper |
| SQLite는 무엇을 하는가? | 생성된 기록을 로컬에 저장 |
| 표시된 파형·시간도 저장되는가? | 자료만으로 확인 불가 |
| 오디오 외부 미전송이면 텍스트도 같은가? | 텍스트 전송 여부는 미확인 |
| 로컬이면 암호화되어 있는가? | 자료에 암호화 설명 없음 |

## 실습 명령

[[tech/data/sqlite-local-history/04-learning/01-getting-started|시작하기]]의 schema를 먼저 생성한다. 아래 쓰기 명령은 실습 DB의 내용을 바꾼다.

```sh
sqlite3 history-demo.db
```

```sql
.tables
.schema recognition_history
.headers on
.mode column
SELECT id, created_at, transcript FROM recognition_history ORDER BY id DESC;
INSERT INTO recognition_history (transcript) VALUES ('확정 텍스트');
UPDATE recognition_history SET transcript = '수정 텍스트' WHERE id = 1;
DELETE FROM recognition_history WHERE id = 1;
.quit
```

앱 코드에서는 parameter binding을 사용한다. UPDATE·DELETE 대상 id는 먼저 조회하고 확인한다.

## 설계 점검

- [ ] 중간 결과와 최종 기록을 구분했다.
- [ ] 저장 시점과 성공·실패 표시를 정했다.
- [ ] 재실행 조회와 재시도 중복을 확인했다.
- [ ] 처리·저장·전송 경계를 데이터별로 적었다.
- [ ] 보관 기간·삭제·백업·복구 정책을 별도로 정했다.
- [ ] 학습용 schema를 제품 실제 구현으로 표현하지 않았다.

## 관련 노트

[[tech/data/sqlite-local-history/04-learning/02-deep-dive|심화 정책]] · [[tech/data/sqlite-local-history/03-references|출처의 확인 범위]] · [[tech/data/sqlite-local-history/README|학습 경로]]

## Sources

- 사례의 확인 범위: 제공 dossier, URL 미제공.
- CLI 명령: https://www.sqlite.org/cli.html
- SQL: https://www.sqlite.org/lang.html
