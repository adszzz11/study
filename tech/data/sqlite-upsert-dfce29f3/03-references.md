---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 공식 문서

| 자료 | URL | 읽을 지점 |
|---|---|---|
| SQLite UPSERT | https://www.sqlite.org/lang_upsert.html | Description, Examples, Parsing Ambiguity, Limitations, History |

## 읽기 질문

- conflict target은 어떤 uniqueness constraint에 반응하는가?
- 여러 절 중 몇 개가 한 행에 실행되는가?
- 기존 값과 `excluded` 값은 어떻게 다른가?
- `DO UPDATE`의 `WHERE`가 거짓이면 어떻게 되는가?
- `ABORT`가 되돌리는 범위는 문장인가 transaction 전체인가?

## 근거와 범위

이 노트는 제공 dossier와 그 안의 공식 문서 설명을 바탕으로 구성했다. 문서 갱신일 기준은 2024-04-11이며 현재 사이트의 최신 변경을 재검토한 기록은 아니다. conflict target 쪽 `WHERE`의 상세 규칙이나 DBMS 간 성능 비교는 확장해서 단정하지 않는다.

실습의 예상 결과와 로컬 SQLite 실행 검증은 구분한다. 실행 검증 기록은 시작하기와 심화 학습 노트에 적는다.

## Sources

- https://www.sqlite.org/lang_upsert.html
- 내용 기준: 제공 dossier가 인용한 문서 갱신일 **2024-04-11**. 이후 변경은 이 노트의 검토 범위 밖이다.
