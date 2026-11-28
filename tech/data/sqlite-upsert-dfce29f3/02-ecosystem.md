---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# UPSERT와 대안 비교

## 정책별 선택

| 선택지 | 동작·차이 | 적합한 상황 / 주의점 |
|---|---|---|
| SQLite UPSERT | PostgreSQL에서 출발, 여러 충돌 절과 마지막 target 생략 지원 | unique constraint별 정책 표현 |
| PostgreSQL UPSERT | 구문의 출발점. 원문 counter 예제는 PostgreSQL에서 기존 값의 table qualifier 필요성을 언급 | 전체 호환성은 이 자료만으로 단정하지 않는다 |
| `DO NOTHING` | 충돌 삽입을 no-op으로 처리 | 기존 데이터 보존 |
| `DO UPDATE` | 충돌 행의 값 갱신 | 누적 또는 교체 |
| `DO UPDATE ... WHERE` | 조건을 만족할 때만 갱신 | 날짜 등 기존·신규 값 비교 |
| 일반 `INSERT` | UPSERT 절 없는 삽입 | 중복 처리의 모든 대안은 이 자료 범위 밖 |

## 결정 순서

1. schema에 입력의 식별 기준을 `PRIMARY KEY` 또는 unique constraint로 표현한다.
2. 중복 시 보존·누적·교체·조건부 교체 중 하나를 고른다.
3. 여러 unique constraint가 있으면 충돌 절의 우선순위를 정한다.
4. 배포 SQLite 버전과 `DO UPDATE` 실패 시 문장 rollback을 확인한다.

다른 DBMS의 동작이나 성능 우열, 모든 conflict resolution algorithm의 비교는 제공 자료로 판단할 수 없다.

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
