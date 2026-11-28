---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — 코드 지식화 검토표

## 먼저 구분할 것

| 항목 | 원칙 |
|---|---|
| 특정 제품 | 공식 URL·버전부터 식별. 현재 확인 필요 |
| 구조 | 선언·import·reference로 확인 |
| 동작 | 구현·테스트·설정·필요한 실행 근거로 확인 |
| 설계 의도 | ADR·issue·PR이 없으면 추정 |
| RAG | 검색 품질과 생성 품질을 나눠 검토 |
| 최신성 | 설명 대상 commit과 현재 snapshot 비교 |

## 설명 검토 체크리스트

- [ ] repository·branch·commit SHA 범위가 명확하다.
- [ ] 중요한 주장마다 path·symbol 근거가 연결되어 있다.
- [ ] 링크의 내용이 실제 주장을 지지한다.
- [ ] dynamic dispatch·DI·runtime configuration의 한계를 표시했다.
- [ ] 코드에서 확인한 사실과 추론·미확인 사항을 구분했다.
- [ ] 변경된 파일 외 관련 module 설명도 검토했다.
- [ ] 요약·embedding·검색 결과의 접근 권한을 확인했다.
- [ ] 생성 문서의 원본 근거를 유지했다.

## 답변 양식

```text
질문:
답변 / 답변 유보 이유:
확인한 사실:
추론·확인 필요:
repository / branch / commit SHA:
path / symbol / 보조 line number:
테스트·설정·ADR 근거:
최신성 확인 날짜:
```

## 빠른 탐색

- 제품 식별 → [[tech/devtools/codewiki-analysis/03-references|References]]
- 수동 기준 답안 → [[tech/devtools/codewiki-analysis/04-learning/01-getting-started|시작하기]]
- 검색·변경·권한 평가 → [[tech/devtools/codewiki-analysis/04-learning/02-deep-dive|심화 학습]]
- 학습 순서 → [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
