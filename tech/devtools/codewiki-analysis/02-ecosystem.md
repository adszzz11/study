---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 대안과 조합

특정 CodeWiki와의 기능 우열·성능 비교는 확인할 수 없다. 아래는 접근 방식의 비교다.

| 접근 | 강점 | 한계 | 적합한 용도 |
|---|---|---|---|
| 수동 Wiki·README·ADR | 배경과 판단 근거를 명시 | 유지보수 부담·노후화 | 운영 절차·설계 결정 |
| API documentation generator | 주석·선언을 일관된 reference로 변환 | 서비스 간 흐름·의도 설명 제한 | library·SDK reference |
| IDE navigation·code search | 구현·reference 직접 확인 | 결과 종합은 사용자의 몫 | debugging·정밀 탐색 |
| Repository 기반 AI assistant | 자연어 질문·상황별 설명 | 검색 누락·잘못된 추론 | 초기 탐색·이해 보조 |
| CodeWiki형 지식 계층 | 코드와 설명의 지속적 연결 구상 | 정확성·갱신·권한 구현 검증 필요 | onboarding·시스템 지도 |

## 선택 기준

- 정확한 함수 위치가 필요하면 code search·symbol navigation부터 시작한다.
- 공개 API의 계약은 API reference와 테스트에서 확인한다.
- 설계 배경은 ADR·PR을 찾고 현재 구현과 대조한다.
- 넓은 흐름은 Wiki·AI 설명으로 탐색하되 중요한 주장을 원본으로 검토한다.

## 조합 예시

ADR → 관련 구현·테스트 링크 → API reference → 읽기 쉬운 Wiki 설명을 연결한다. 생성 문서 자체를 새 사실의 원천으로 반복 사용하면 초기 오류가 누적될 수 있으므로 원본 근거를 유지한다.

## 다음 학습

[[tech/devtools/codewiki-analysis/04-learning/02-deep-dive|동일 질문으로 비교 평가]] · [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
