---
date: 2026-11-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 검색 문법과 인덱스 설계 경계

## 두 문법 계층: SQL과 FTS5

```sql
SELECT * FROM email WHERE email MATCH '"one two three"';
```

SQL의 single quote는 SQL 문자열을 만들고, 그 안의 double quote는 FTS5 phrase를 만든다. FTS5 string 안의 double quote는 두 번 써서 escape한다. bareword 허용 문자는 제한되어 있으므로 특수문자 입력을 그대로 query에 연결하지 않는다.

애플리케이션에서는 SQL 값을 parameter binding으로 전달하고, 별도로 FTS5 query의 quoting·operator 정책을 정한다. SQL binding이 검색 문법의 오류나 의도하지 않은 Boolean 조합까지 해결해 주는 것은 아니다.

## 연산별 의미

| 표현 | 의미·경계 |
|---|---|
| `thr*` | thr로 시작하는 token |
| `one + two + thr*` | 연속 phrase의 마지막 token이 prefix |
| `title : ^one` | title의 첫 token에서 시작 |
| `NEAR("one two" "three four", 10)` | phrase들이 거리 조건을 만족하는 묶음에 존재 |
| `{title body} : fts5` | 지정 column 집합에서 검색 |
| `- sender : fts5` | sender를 제외한 column에서 검색 |
| `(one OR two) NOT three` | 대안 조건에서 three 일치 문서를 제외 |

Prefix의 `*`는 FTS5 string 바깥에 둔다. `"one two thr*"`는 `*`까지 tokenizer에 전달하므로 기대한 prefix 연산이 되지 않을 수 있다. `^`는 phrase 중간이나 `NEAR` 내부에 쓸 수 없다.

## NEAR의 거리와 순서

기본 N은 10이다. 각 phrase가 한 번 이상 포함된 token 묶음이 있고, 첫 phrase의 끝과 마지막 phrase의 시작 사이 token 수가 N 이하여야 한다. **인수에 적은 phrase 순서를 요구하는 연산이 아니다.** 순서와 연속성이 필요하면 phrase로 표현한다.

실습에서는 phrase 순서를 뒤집은 문서, 간격이 N인 문서, N+1인 문서를 만들어 경계를 비교한다. 여러 phrase가 겹치는 복잡한 사례는 원문과 실제 실행으로 별도 확인한다.

## Boolean precedence와 query builder

우선순위는 implicit `AND` → `NOT` → 명시적 `AND` → `OR`다. `NOT`는 `query1 NOT query2`인 이항 연산자다.

```text
one NOT two three   → one NOT (two AND three)
one OR two NOT three → one OR (two NOT three)

(one OR two) three       -- Syntax error
(one OR two) AND three   -- 올바른 명시적 연결
```

괄호 expression 앞뒤에 implicit AND는 삽입되지 않는다. UI의 조건 조합은 공백 연결보다 명시적 operator와 괄호로 생성하면 검토하기 쉽다.

## Column filter는 교집합처럼 좁아진다

```sql
SELECT rowid FROM email
WHERE email MATCH '{title body} : (title : one OR body : two)';
```

중첩 filter는 검색 가능한 column 집합을 더 좁힌다. 바깥에서 제외한 column을 안쪽에서 다시 활성화할 수 없다. UI에서 filter를 중첩한다면 유효 column 집합을 먼저 점검한다.

## 인덱스 설계에서 남은 검증

- prefix index: prefix 빈도, 저장 크기, 지연을 측정한 뒤 판단한다. 제공 범위에는 구체 설정 문법이 없다.
- 외부 content: 저장 위치 설계는 가능하지만 동기화·복구 절차는 추가 문서 확인이 필요하다.
- custom tokenizer: 실제 언어 corpus로 품질을 확인하고 API를 별도로 학습한다.
- ranking·저장 구조: `bm25()` 공식, segment 병합, 압축 비용은 본문 확인 범위 밖이다.

## Navigation

[[tech/data/sqlite-fts5-search-90b57f7d/README|학습 가이드]]

## Sources

- https://www.sqlite.org/fts5.html
