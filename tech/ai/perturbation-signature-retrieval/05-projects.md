---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 검색과 근거를 구현하기

아래 프로젝트는 합성 데이터 중심의 학습 제안이다. 실제 데이터 선정·논문 재현·효능 판단에는 별도 자료와 검증이 필요하다.

## 1. Signature retrieval 최소 프로토타입

- 입력: 가상 signature, candidate identity, context, 선택적 annotation.
- 구현: query 입력 → 조건 필터 → cosine Top-K → 근거 행 조회.
- 산출물: 실행 스크립트, 고정 입력, 순위표, 설정 기록.
- 완료 기준: 같은 입력·설정에서 순위가 재현되며 모든 결과의 계산 근거를 추적할 수 있다. 높은 생물학적 성능은 목표가 아니다.

## 2. 검색 평가 설계 비교

- 같은 합성 데이터에 identity별 replicate와 여러 context를 구성한다.
- 행 무작위·perturbation identity·조건 분할을 각각 적용한다.
- 합성 relevance label의 생성 규칙을 공개한다. 이 label은 생물학적 정답이 아니다.
- 산출물: split별 corpus 정의, 검색 지표, 순위 변화 및 대표 사용 상황의 평가표.
- 완료 기준: 가장 높은 점수보다 각 분할이 무엇을 일반화하는지 설명할 수 있다.

| 분할 | Query / corpus 정의 | Relevance | 지표 | 대표 사용 상황 | 제한 |
|---|---|---|---|---|---|
| 행 / identity / 조건 | 실험에서 작성 | 생성 규칙 기록 | P@K·R@K·MRR 중 선택 | 질문을 명시 | 누수·결측 기록 |

## 3. Target·compound 근거 탐색 도구

- Signature, 실험 조건, target annotation, compound identity를 별도 객체로 연결한다.
- 후보마다 근거 실험과 annotation 출처를 조회할 수 있게 한다.
- 연결 정보가 없으면 ‘미확인’을 표시하고, 유사도만으로 target 관계를 확정하지 않는다.
- 산출물: 데이터 스키마, 후보 상세 화면 또는 CLI 출력, 결측 처리 예시.
- 완료 기준: 관측과 알려진 연결 및 추론이 결과에서 구분된다.

## 연결

[[tech/ai/perturbation-signature-retrieval/04-learning/01-getting-started|최소 코드]] · [[tech/ai/perturbation-signature-retrieval/04-learning/02-deep-dive|평가 설계]] · [[tech/ai/perturbation-signature-retrieval/README|학습 지도]]

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
