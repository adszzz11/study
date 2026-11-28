---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — What / Why / 특징

> 범위: 특정 CodeWiki 제품의 검증된 사양이 아닌 개념 분석이다.

## What

| 지식 종류 | 답하려는 질문 | 확인할 근거 |
|---|---|---|
| 구조 | 어떤 module·symbol·dependency가 있는가? | 선언, import, reference |
| 동작 | 요청·데이터·상태가 어디로 이동하는가? | 구현, 테스트, 설정, 실행 관찰 |
| 설계 의도 | 왜 이 구조를 선택했는가? | ADR, issue, PR, 작성자 설명 |

코드에서 구조를 찾았다는 이유만으로 설계 의도까지 확정할 수는 없다. 의도에 근거가 없으면 ‘추정’ 또는 ‘확인 필요’로 남긴다.

## Why

수동 Wiki는 설명에 강하지만 구현 변경을 따라가는 데 비용이 든다. Code search는 위치를 찾는 데 강하지만 전체 흐름은 사용자가 종합해야 한다. CodeWiki형 접근은 설명과 원본을 연결하는 지식 계층을 구상한다.

## Reference architecture

아래 계층의 실제 제품 채택 여부는 모두 **확인 필요**다.

| 계층 | 역할 | 평가 질문 |
|---|---|---|
| Source ingestion | 코드·문서·테스트 수집 | repository·branch·commit·권한 범위가 명시되는가? |
| Structure extraction | 파일·symbol·import·reference 추출 | parser 지원 범위와 분석 한계를 밝히는가? |
| Knowledge indexing | full-text·semantic·관계 검색 | 질문에 필요한 설정·호출자도 찾는가? |
| Documentation generation | module 설명·흐름·Q&A | 사실과 추론을 구분하는가? |
| Presentation | Wiki·검색·코드 링크 | 원본 근거로 바로 이동할 수 있는가? |
| Update management | 변경 감지·관련 설명 갱신 | 설명 대상 commit과 최신성 상태가 보이는가? |

## 핵심 주의점

- AST·symbol analysis는 정적 구조를 돕는다. Reflection, dynamic dispatch, dependency injection, runtime configuration이 있으면 실제 호출 경로는 추가 검증이 필요하다.
- RAG는 검색한 근거를 모델에 제공하는 방식이다. 핵심 설정이나 호출자를 검색하지 못하면 설명도 불완전하다.
- Provenance에는 repository, commit SHA, path, symbol을 함께 기록한다. Line number만으로는 변경 뒤 같은 내용을 가리킨다고 보장할 수 없다.
- 공통 interface 변경은 다른 module 설명에도 영향을 준다. 갱신 범위와 비용을 함께 평가한다.
- 요약·embedding·검색 결과에도 원본 접근 권한을 반영해야 한다.

## 다음 학습

[[tech/devtools/codewiki-analysis/02-ecosystem|접근 방식 비교]] → [[tech/devtools/codewiki-analysis/04-learning/01-getting-started|작은 repository 실습]] · [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
