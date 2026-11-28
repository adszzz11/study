---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 문서 입력부터 결과 강조까지

## 목표와 준비

SQLite 실행 환경에서 FTS5가 실제로 활성화되어 있는지 확인하고 검색 결과 집합과 정렬을 구분한다. 다음 예제는 임시 in-memory DB에서 순서대로 실행한다.

```sh
sqlite3 :memory:
```

```sql
SELECT sqlite_version();
CREATE VIRTUAL TABLE email USING fts5(sender, title, body);
INSERT INTO email(rowid, sender, title, body) VALUES
  (1, 'alice', 'FTS5 intro', 'one two three'),
  (2, 'bob', 'Search notes', 'one gap two three'),
  (3, 'carol', 'FTS5 design', 'three two one');
```

`no such module: fts5` 오류가 나면 해당 실행 환경의 빌드 활성화를 점검한다. SQLite 버전만으로 활성화를 보장하지 않는다.

## 같은 검색을 세 가지 방식으로 실행

```sql
SELECT rowid, title FROM email WHERE email MATCH 'fts5';
SELECT rowid, title FROM email WHERE email = 'fts5';
SELECT rowid, title FROM email('fts5');
```

세 쿼리는 rowid 1, 3을 선택한다. `ORDER BY`가 없으므로 반환 순서는 가정하지 않는다.

```sql
SELECT rowid, title FROM email('fts5') ORDER BY rank;
SELECT rowid, highlight(email, 2, '<b>', '</b>')
FROM email('one') ORDER BY rowid;
```

첫 쿼리는 관련도순 정렬 예제다. 둘째 쿼리의 column 번호는 `sender=0`, `title=1`, `body=2`다. 반환값은 강조된 복사본이다.

## Phrase와 AND를 구분

```sql
SELECT rowid FROM email('"one two three"') ORDER BY rowid;
SELECT rowid FROM email('one + two + three') ORDER BY rowid;
SELECT rowid FROM email('one two three') ORDER BY rowid;
```

- 첫 두 쿼리: 연속된 token sequence를 요구하므로 rowid 1.
- 마지막 쿼리: implicit AND이므로 rowid 1, 2, 3.

## 문서 변경 확인

```sql
UPDATE email SET body = 'one two three' WHERE rowid = 2;
SELECT rowid FROM email('"one two three"') ORDER BY rowid;
-- 1, 2
DELETE FROM email WHERE rowid = 1;
SELECT rowid FROM email('"one two three"') ORDER BY rowid;
-- 2
```

## 완료 조건

- [ ] type·constraint 없는 FTS5 table을 생성한다.
- [ ] 세 검색 경로의 결과 집합이 같음을 확인한다.
- [ ] phrase와 implicit AND의 결과 차이를 설명한다.
- [ ] `rank` 정렬과 `highlight()`의 역할을 구분한다.
- [ ] 수정·삭제 뒤 검색 결과 변화를 확인한다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
