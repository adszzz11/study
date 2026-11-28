---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 적용 과제

아래 과제는 구현 제안이다. 특정 CodeWiki가 지원하는 기능이나 완료된 실험이 아니다.

| 프로젝트 | 최소 구현 범위 | 완료 기준 |
|---|---|---|
| Onboarding repository atlas | 주요 module·entry point·테스트 위치 연결 | 신규 개발자가 대표 기능의 구현·테스트 위치를 찾음 |
| 변경 영향 문서 도우미 | 변경 symbol에서 설명 페이지로 연결·검토 후보 표시 | 실제 영향 대상 누락과 불필요 후보를 평가 가능 |
| 근거 기반 코드 Q&A | 주요 주장에 commit·path·symbol 연결 | 근거 부족 시 답변 유보·원본 확인 가능 |
| ADR 연결 지도 | 설계 결정과 관련 구현·테스트 연결 | 결정 배경과 현재 구현의 차이 추적 가능 |

## 추천 첫 과제: repository atlas

1. 작은 repository와 기준 commit 하나를 선택한다.
2. 대표 기능 하나의 entry point → 핵심 로직 → 저장소·외부 호출 → 테스트를 연결한다.
3. 페이지마다 설명 대상 commit과 근거를 기록한다.
4. 다른 개발자가 대표 질문에 답하도록 하고 시간·막힌 위치·틀린 설명을 기록한다.
5. 이름 또는 설정 변경 뒤 검토가 필요한 페이지를 다시 확인한다.

## 산출물과 범위

- 읽기 전용 탐색 문서, 근거 목록, 미확인 사항, 평가 기록을 만든다.
- 자동 갱신은 수동 검토로 검색·근거 품질을 확인한 뒤 확대한다.
- 생성 문서를 다시 요약할 때도 원본 provenance를 유지한다.
- 실행 전 임의의 성과 수치나 완료 판정을 적지 않는다.

## 구현 후보 스택

Git snapshot → 언어별 parser/AST·symbol 추출 → full-text search·선택적 vector retrieval → 선택적 RAG/LLM → Wiki presentation을 조합할 수 있다. 실제 CodeWiki의 언어·framework·database·hosting·라이선스는 확인 필요다.

## 연결

[[tech/devtools/codewiki-analysis/04-learning/02-deep-dive|평가 지표]] · [[tech/devtools/codewiki-analysis/cheatsheet|반복 검토]] · [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
