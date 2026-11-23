---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# FTS5 Overview: 검색 대상과 SQL 모델

## What

FTS5는 SQLite virtual table module이다. 문서를 tokenizer로 분해하고 token sequence를 기준으로 검색한다. query 안의 string도 tokenizer를 거쳐 zero or more tokens가 되며, phrase는 하나 이상의 token이 순서대로 연결된 표현이다.

```text
문서 → tokenizer → token 기반 index
검색 string → tokenizer → phrase / query → 일치 문서 → 정렬·강조
```

## Why

| 검색 의도 | FTS5 표현 |
|---|---|
| 여러 단어가 문서 어디에나 함께 존재 | implicit 또는 명시적 AND |
| 단어가 정해진 순서로 연속 | phrase |
| 표현들이 일정 거리 안에 존재 | NEAR |
| 제목으로 제한하거나 특정 조건 제외 | column filter, NOT |
| 결과를 관련도순으로 보고 일치 부분 표시 | ORDER BY rank, highlight() |

문서에 어떤 문자열이 보인다는 사실만으로 검색 일치를 보장할 수 없다. 구두점, 대소문자, 접두어에 대한 기대를 tokenizer의 동작과 맞춰야 한다. 기본 검색은 대소문자를 구분하지 않는다.

## Virtual table과 문서 식별

```sql
CREATE VIRTUAL TABLE email USING fts5(sender, title, body);
```

- `rowid`는 암묵적인 INTEGER PRIMARY KEY다.
- 일반 table처럼 `INSERT`, `UPDATE`, `DELETE`를 사용할 수 있다.
- column에 type, constraint, `PRIMARY KEY`를 선언하면 오류다.
- `rowid`, `rank`, 해당 table 이름은 column 이름으로 사용할 수 없다.
- 제공 본문에서 인정된 column option은 `UNINDEXED`다. 알 수 없는 option은 오류이며, `UNINDEXED` 세부 동작은 제공 범위 밖이다.

관계형 schema를 그대로 복사하기보다 문서 식별과 검색 column 구성을 별도로 설계한다.

## 검색과 결과 표현

`MATCH`, table 이름에 대한 `=`, table-valued function 형태는 같은 full-text 검색을 수행한다. 결과 순서는 `ORDER BY`가 없으면 임의적이다. 자료는 `ORDER BY rank`를 가장 관련 있는 결과부터 반환하는 예제로 제시한다.

Auxiliary function은 첫 인수로 FTS5 table 이름을 받는다. `highlight(email, 2, '<b>', '</b>')`는 세 번째 column인 body의 일치 부분을 감싼 복사본을 반환한다. 사용자 정의 auxiliary function과 tokenizer는 C 확장 지점이다.

## 배포와 설계 경계

FTS5는 SQLite 3.9.0부터 amalgamation에 포함되었다. `--enable-fts5`, `SQLITE_ENABLE_FTS5`, loadable extension 경로가 제시된다. **소스 포함과 실제 빌드 활성화는 구분**하며 빌드 기본값을 가정하지 않는다.

설정으로 tokenizer 변경, prefix query용 추가 disk index, 다른 곳에 저장된 content를 대상으로 한 index 구성이 가능하다. 구체 설정값·동기화·성능은 추가 확인이 필요하다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
