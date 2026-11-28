---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화 학습 — 정확성·갱신·권한 평가

아래 절차와 지표는 평가 제안이며 특정 제품의 측정 결과가 아니다.

## 검색과 생성 분리하기

1. 시작하기에서 만든 동일 질문·commit을 유지한다.
2. 검색 근거에 호출자, 설정, 테스트가 포함되는지 살핀다.
3. 정답 근거가 검색되지 않은 실패와, 근거가 있어도 설명을 잘못한 실패를 구분한다.
4. 동적 호출이나 환경별 설정은 정적 분석으로 확정 가능한 범위를 기록한다.

## 변경 실험

승인된 실습 repository에서만 별도 변경을 만든다. 이 노트는 실행 결과를 주장하지 않는다.

| 변경 | 관찰할 문제 | 확인 대상 |
|---|---|---|
| 함수 이름 변경 | 낡은 symbol·링크 잔존 | 원본 위치·문서 링크 |
| 공통 interface 수정 | 다른 module의 설명 누락 | dependency를 따라간 영향 범위 |
| retry 설정 변경 | 동작 설명이 그대로 남음 | 설정과 구현·테스트의 관계 |

변경된 파일만 갱신하는 방식과 관련 dependency까지 검토하는 방식을 비교한다. 넓은 갱신은 비용이 증가하고, 좁은 갱신은 설명 누락 위험이 커질 수 있다.

## 평가 지표

| 지표 | 계산·기록 방식 | 해석 시 주의 |
|---|---|---|
| 질문 해결 시간 | 질문 시작부터 원본 검증 완료까지 | 같은 질문·범위에서 비교 |
| 근거 보유 비율 | 근거가 붙은 중요 주장 / 전체 중요 주장 | 링크 존재가 정확성을 뜻하지 않음 |
| 근거 일치도 | 실제 근거가 지지하는 주장 / 검토한 주장 | 부분 지지는 별도 기록 |
| 갱신 지연 | 변경 확정부터 관련 설명 검증 완료까지 | 감지·생성·검토 시간 구분 |
| 영향 후보 품질 | 실제 영향 대상의 누락·불필요 후보 수 | 사람이 정한 기준 집합 필요 |

분모가 0이면 비율을 산출하지 않고 ‘해당 없음’으로 기록한다. 제품 간 성능 수치로 일반화하지 않는다.

## Provenance와 권한 검토

- repository·commit SHA·path·symbol을 보존하고 line number는 보조 정보로 사용한다.
- 설명 대상 commit이 현재 branch와 다르면 차이를 표시한다.
- 허가된 테스트 계정으로 원본 접근 제한이 요약·검색·embedding 기반 응답에도 적용되는지 확인한다.
- 접근 철회 뒤 파생 결과와 캐시 처리도 점검한다. 공개 vault에는 민감한 실험 결과를 기록하지 않는다.
- 설계 의도는 ADR·PR 근거가 없으면 추정으로 표시한다.

## 연결

[[tech/devtools/codewiki-analysis/05-projects|평가를 프로젝트로 확장]] · [[tech/devtools/codewiki-analysis/cheatsheet|검토표]] · [[tech/devtools/codewiki-analysis/README|진입점]]

## Sources

- 사용자 제공 dossier: 제품을 식별할 URL과 수집 자료 없음.
- 아래 URL은 일반 개념의 추가 참고자료이며, 특정 CodeWiki의 사양을 입증하지 않는다. 이번 작성에서는 웹 페이지를 열어 검증하지 않았다.
- Git revision 지정: https://git-scm.com/docs/gitrevisions
- Tree-sitter 소개: https://tree-sitter.github.io/tree-sitter/
- Retrieval-Augmented Generation 논문: https://arxiv.org/abs/2005.11401
- ADR 개념: https://adr.github.io/
