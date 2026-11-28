---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 합성 signature 검색

## 목표와 준비

Python 3 표준 라이브러리만 사용해 cosine similarity와 Top-K를 확인한다. 아래 숫자와 ID는 모두 가상이며 생물학적 의미가 없다. 입력은 이미 생성된 signature로 가정하므로 control 대비 signature 생성 과정은 포함하지 않는다.

먼저 데이터 사전에 query, candidate, context, relevance를 적는다. 이 예제는 같은 context의 **실험 행**을 candidate로 삼아 query와 같은 방향의 반응을 찾는다. Compound·target 단위 검색은 별도 매핑과 집계 규칙이 필요하다.

## 실행 예제

```python
from math import sqrt

query = [1.0, 0.0, 0.0]
rows = [
    {"id": "exp-A", "compound": "cmp-A", "context": "ctx-1",
     "signature": [1.0, 0.0, 0.0], "target": None},
    {"id": "exp-B", "compound": "cmp-B", "context": "ctx-1",
     "signature": [0.8, 0.6, 0.0], "target": None},
    {"id": "exp-C", "compound": "cmp-C", "context": "ctx-1",
     "signature": [-1.0, 0.0, 0.0], "target": None},
    {"id": "exp-D", "compound": "cmp-D", "context": "ctx-2",
     "signature": [1.0, 0.0, 0.0], "target": None},
]

def cosine(a, b):
    if len(a) != len(b):
        raise ValueError("Dimension mismatch")
    na = sqrt(sum(x*x for x in a))
    nb = sqrt(sum(x*x for x in b))
    if not na or not nb:
        raise ValueError("Zero vector has no cosine similarity")
    return sum(x*y for x, y in zip(a, b)) / (na * nb)

ranked = sorted(
    [(cosine(query, r["signature"]), r) for r in rows
     if r["context"] == "ctx-1"],
    key=lambda item: (-item[0], item[1]["id"]),
)
for score, row in ranked[:2]:
    print(row["id"], row["compound"], row["context"],
          f"{score:.3f}", row["target"] or "미확인")
```

예상 결과:

```text
exp-A cmp-A ctx-1 1.000 미확인
exp-B cmp-B ctx-1 0.800 미확인
```

## 관찰 과제

- exp-D는 signature가 같아도 context 필터 때문에 제외된다.
- exp-C는 반대 방향이다. 반대 반응 검색을 원하면 relevance와 순위 방향을 별도로 정의한다.
- 동점은 ID로 정렬해 재현성을 확보한다. 0 벡터는 임의의 점수로 대체하지 않는다.
- 점수 1.000은 벡터 방향의 일치를 뜻한다. target 일치나 약효 확률을 뜻하지 않는다.
- 실제 데이터에서는 차원·특징 순서·결측·비정상 수치·정규화를 추가로 검증해야 한다.

## 완료 기준

- [ ] 같은 입력으로 같은 순위가 나온다.
- [ ] 필터와 점수의 계산 근거를 설명할 수 있다.
- [ ] 관측값, 알려진 연결, 추론을 구분한다.

## 연결

[[tech/ai/perturbation-signature-retrieval/04-learning/02-deep-dive|다음: 평가와 일반화]] · [[tech/ai/perturbation-signature-retrieval/README|학습 지도]]

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
