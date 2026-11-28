---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# SQLite FTS5 Cheatsheet

## 생성·검색·표시

```sql
CREATE VIRTUAL TABLE email USING fts5(sender, title, body);
INSERT INTO email(sender, title, body) VALUES ('alice', 'FTS5', 'one two three');
SELECT * FROM email WHERE email MATCH 'fts5';
SELECT * FROM email WHERE email = 'fts5';
SELECT * FROM email('fts5');
SELECT rowid, title FROM email('fts5') ORDER BY rank;
SELECT highlight(email, 2, '<b>', '</b>') FROM email('one');
UPDATE email SET title = 'Search' WHERE rowid = 1;
DELETE FROM email WHERE rowid = 1;
```

세 검색 경로는 동일한 full-text 검색이다. `ORDER BY`가 없으면 순서는 임의적이다. `highlight()` column 번호는 0부터 시작한다.

## MATCH 오른쪽의 FTS5 query

| 의도 | Query |
|---|---|
| 연속 phrase | `"one two three"` 또는 `one + two + three` |
| 모두 포함 | `one two three` |
| token prefix | `thr*` |
| phrase 끝의 prefix | `one + two + thr*` |
| column 첫 token | `title : ^one` |
| proximity | `NEAR("one two" "three four", 10)` |
| column 집합 | `{title body} : fts5` |
| column 제외 | `- sender : fts5` |
| Boolean | `(one OR two) NOT three` |

## 자주 틀리는 규칙

- token 검색과 원문 substring 검색은 다르다.
- `"one two thr*"`에서 별표는 prefix operator가 아니라 tokenizer 입력이 된다.
- `^`는 phrase 중간·NEAR 내부에 사용할 수 없다.
- NEAR는 인수 순서를 강제하지 않는다. 기본 N은 10이다.
- 우선순위: implicit AND > NOT > 명시적 AND > OR.
- `(one OR two) three`는 오류. `(one OR two) AND three`로 쓴다.
- NOT는 이항 연산자다. 중첩 column filter는 검색 범위를 넓히지 않는다.
- FTS5 string 내부 double quote는 두 번 쓴다. SQL quoting과 별개다.
- column에 type·constraint·PRIMARY KEY 선언을 넣지 않는다.
- column 이름으로 `rowid`, `rank`, table 이름을 쓰지 않는다.

## 추가 확인이 필요한 항목

`bm25()` 공식, 기본 rank 연결, prefix index 설정값, 외부 content 동기화, tokenizer 세부 옵션, Segment B-Tree 비용은 제공 범위에서 확정하지 않는다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
