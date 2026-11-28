---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

| 용어 | 학습용 정의 | 주의점 |
|---|---|---|
| Perturbation | 세포에 가한 개입 | 유전자 조작·화합물 처리 등 구체적 종류 미확인 |
| Signature | 개입 후 변화의 표현 | gene expression·morphology·protein abundance 중 무엇인지 미확인 |
| Target | 검색하려는 생물학적 대상 | 유전자 또는 단백질 등 범위 미확인 |
| Compound | 검색하려는 화합물 | identity와 처리 조건을 연결해야 함 |
| Context | 세포 유형·농도·시간 등 조건 | 제공되지 않은 조건은 결측으로 유지 |
| Relevance | 검색 결과가 적절하다는 기준 | 유사 반응·반대 반응·알려진 연결을 구분 |

**Cell-level을 single-cell과 동의어로 가정하지 않는다.** 세포 실험의 집계 표현인지 단일 세포 측정인지 알 수 없다.

## Why

원하는 반응에 가까운 화합물을 순위화하거나 관찰 반응에 연결되는 target 후보를 좁히는 데 활용할 수 있다. 이는 제목으로부터 해석한 가능한 활용이며 검증된 성과가 아니다.

## 검색 계약

| 항목 | 먼저 정할 질문 |
|---|---|
| Query | 관찰 signature인가, 원하는 변화 패턴인가? |
| Candidate | 실험 행인가, compound인가, target인가? |
| Relevance | 같은 방향·반대 방향·알려진 연결 중 무엇인가? |
| Context | 어떤 조건 안에서 비교할 수 있는가? |
| Output | 순위와 함께 어떤 실험 근거·불확실성을 표시할 것인가? |

Signature→target 검색에는 별도의 관측 또는 annotation 연결이 필요하다. Compound 검색에도 identity와 실험 조건의 매핑이 필요하다. 두 검색을 자동으로 같은 문제로 취급하지 않는다.

## 검토용 참조 아키텍처

```text
관측 데이터 + 실험 metadata
  → 품질 관리 및 control·replicate 확인
  → signature 생성
  → 검색 표현
  → context 필터 및 후보 순위화
  → 근거 실험·조건·불확실성 제시
```

Control 대비 변화량을 쓰려면 control 정의와 비교 가능성을 먼저 확인한다. 원시 관측값·변화량 벡터·학습 embedding은 서로 다른 선택지다. 점수는 검증된 확률이나 작용 강도가 아니다.

## 다음 학습

[[tech/ai/perturbation-signature-retrieval/04-learning/01-getting-started|합성 데이터로 검색 시작하기]] · [[tech/ai/perturbation-signature-retrieval/README|학습 지도]]

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
