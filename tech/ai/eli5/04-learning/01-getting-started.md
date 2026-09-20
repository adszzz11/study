---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 Getting Started

> [[../03-references|이전: References]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep Dive]]

## Goal

작은 text classifier를 학습하고 다음 질문에 답한다.

- 전체 모델에서 어떤 단어가 각 class를 밀어주는가?
- 한 문서가 왜 positive 또는 negative로 분류됐는가?
- notebook rendering과 구조화된 explanation은 어떻게 다른가?

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install "eli5==0.16.0" "scikit-learn>=1.6"
```

Python 3.9+가 필요하다. 실무에서는 package version과 실행 환경을 lock file에 고정한다.

## Train a Text Classifier

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

texts = [
    "clear explanation and useful examples",
    "excellent guide and reliable result",
    "confusing explanation and broken example",
    "poor guide with unreliable result",
]
labels = ["positive", "positive", "negative", "negative"]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
classifier = LogisticRegression(random_state=42)
pipeline = make_pipeline(vectorizer, classifier)
pipeline.fit(texts, labels)

print(pipeline.predict(["clear and reliable guide"]))
```

이 toy data는 API 흐름을 익히기 위한 것이며, explanation 품질을 평가할 만큼 충분한 dataset은 아니다.

## Global Explanation

pipeline에서 vectorizer와 classifier를 꺼내 feature name을 연결한다.

```python
import eli5

eli5.show_weights(
    classifier,
    vec=vectorizer,
    target_names=classifier.classes_,
    top=10,
)
```

읽는 순서:

1. 어느 class에 대한 weight인지 확인한다.
2. bias와 실제 feature를 구분한다.
3. positive/negative sign이 class decision 방향에서 무엇을 뜻하는지 확인한다.
4. 의미 없는 token, 이름, formatting artifact가 상위에 있는지 찾는다.

`TfidfVectorizer`를 쓰면 coefficient 크기만 보지 말고 feature scaling과 document별 TF-IDF value도 함께 고려한다.

## Local Explanation

```python
document = "clear and reliable guide"

eli5.show_prediction(
    classifier,
    document,
    vec=vectorizer,
    target_names=classifier.classes_,
)
```

linear model의 local contribution은 대체로 다음 관계로 이해할 수 있다.

```text
decision score ≈ bias + Σ(feature value × coefficient)
```

highlighting은 어떤 token이 target class score를 올리거나 내렸는지 보여준다. 이는 단어의 일반적 의미가 아니라 **학습된 모델 안에서의 역할**이다.

## Explanation vs Rendering

```python
explanation = eli5.explain_prediction(
    classifier,
    document,
    vec=vectorizer,
    target_names=classifier.classes_,
)

plain_text = eli5.format_as_text(explanation)
structured = eli5.format_as_dict(explanation)

print(plain_text)
print(structured.keys())
```

| 목적 | API |
|---|---|
| notebook에서 즉시 확인 | `show_weights()`, `show_prediction()` |
| test/report에서 재사용 | `explain_weights()`, `explain_prediction()` |
| terminal/log | `format_as_text()` |
| JSON pipeline/custom UI | `format_as_dict()` |

## First Audit

다음처럼 의도적으로 artifact를 넣은 data를 만들어 모델이 그것을 상위 feature로 잡는지 확인해 본다.

```python
audit_texts = [
    "POS clear tutorial",
    "POS useful documentation",
    "NEG confusing tutorial",
    "NEG broken documentation",
]
```

`POS`, `NEG`가 label을 직접 누설하므로 높은 accuracy가 나와도 모델은 유용하지 않다. ELI5의 목적은 예쁜 explanation이 아니라 이런 shortcut을 빨리 발견하는 데 있다.

## Troubleshooting

| 문제 | 원인 후보 | 해결 |
|---|---|---|
| feature name이 `x0`, `x1`처럼 보임 | vectorizer/feature names 미전달 | `vec=` 또는 `feature_names=` 연결 |
| notebook HTML이 표시되지 않음 | notebook renderer가 아닌 환경 | `format_as_text()` 사용 |
| contribution 방향이 혼란스러움 | target class 또는 class order 착각 | `classifier.classes_`와 target 확인 |
| 상위 feature가 이상함 | leakage, artifact, preprocessing 오류 | raw sample과 split pipeline 감사 |
| explanation이 매번 다름 | stochastic estimator/explainer | `random_state` 고정, version 기록 |

## Checklist

- [ ] isolated environment에 `eli5==0.16.0` 설치
- [ ] classifier의 held-out score 확인
- [ ] `show_weights()`로 global feature 검사
- [ ] 정답·오답 sample 각각 `show_prediction()` 확인
- [ ] `explain_prediction()`을 text/dict로 변환
- [ ] suspicious token과 data source를 추적

## Sources

- https://eli5.readthedocs.io/en/0.16.0/tutorials/sklearn-text.html
- https://eli5.readthedocs.io/en/stable/autodocs/eli5.html
- https://pypi.org/project/eli5/

