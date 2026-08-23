---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 Overview

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: Ecosystem]]

## What

ELI5는 Python 기반 Machine Learning explainability 라이브러리다. 여러 estimator에 흩어진 coefficient, feature importance, decision path를 비슷한 API로 꺼내고 사람이 읽기 좋은 형태로 표현한다.

| 관점 | 주요 API | 답하려는 질문 |
|---|---|---|
| Global explanation | `show_weights()`, `explain_weights()` | 모델 전체가 어떤 feature에 의존하는가? |
| Local explanation | `show_prediction()`, `explain_prediction()` | 이 sample을 왜 이 class로 예측했는가? |

`show_*()`는 notebook에서 즉시 살펴볼 때 편하고, `explain_*()`는 결과를 저장하거나 custom frontend로 전달할 때 적합하다.

## Why

모델의 score만으로는 다음 문제를 발견하기 어렵다.

- text classifier가 주제어가 아니라 작성자 이름이나 formatting artifact를 학습했다.
- preprocessing 뒤의 feature name과 linear coefficient를 연결할 수 없다.
- 특정 오분류를 만든 positive/negative contribution을 알고 싶다.
- black-box estimator가 validation data에서 어떤 column에 실제로 의존하는지 알고 싶다.
- 모델 설명을 notebook뿐 아니라 dashboard나 정적 report에 재사용하고 싶다.

ELI5는 설명 생성과 presentation을 분리해 이 문제를 한 인터페이스에서 다룬다.

## Architecture

```text
                         ┌─ linear model adapter
Estimator + optional X ──┼─ tree model adapter
                         ├─ external library adapter
                         └─ model-agnostic explainer
                                    │
                                    ▼
                           Explanation object
                                    │
            ┌──────────┬────────────┼───────────┬──────────┐
            ▼          ▼            ▼           ▼          ▼
          HTML       text       dict/JSON   DataFrame   PIL image
```

estimator type에 따라 등록된 구현으로 dispatch하는 구조이므로, 사용자는 모델마다 완전히 다른 출력 API를 외울 필요가 없다. 동시에 intermediate object를 formatter와 분리해 presentation layer를 교체할 수 있다.

## Explanation Methods

| 방식 | 범위 | 핵심 동작 | 주의점 |
|---|---|---|---|
| Linear weights | Global | coefficient와 feature name 연결 | scale과 regularization의 영향을 받음 |
| Linear contribution | Local | 대체로 `feature value × coefficient`와 bias 표시 | probability 자체의 인과 분해가 아님 |
| Tree importance | Global | split gain, usage, coverage 또는 estimator importance | method별 의미가 다름 |
| Tree path contribution | Local | root→leaf node score 변화량을 feature별 합산 | library/version별 구현 검증 필요 |
| Permutation Importance | Global, dataset-specific | feature를 shuffle한 뒤 score 감소 측정 | held-out data와 correlated feature 주의 |
| LIME / `TextExplainer` | Local, model-agnostic | 주변 sample perturbation 후 sparse surrogate 학습 | seed, sampling, distance, fidelity에 민감 |
| Grad-CAM | Local, image | activation과 gradient로 class heatmap 생성 | Keras image classification 중심 |
| Token logprobs | Local, LLM output | token log probability로 confidence highlighting | reasoning·사실성 설명이 아님 |

## Supported Ecosystem

- `scikit-learn`
- XGBoost, LightGBM, CatBoost
- lightning, `sklearn-crfsuite`
- Keras
- OpenAI Python client
- 일반 black-box estimator용 Permutation Importance
- text classifier용 LIME 기반 `TextExplainer`

## Release Snapshot

| Version | Date | 주요 변화 |
|---|---:|---|
| `0.14.0` | 2025-03-26 | scikit-learn 1.6+, Python 3.11–3.13 지원 |
| `0.15.0` | 2025-04-06 | OpenAI client token logprobs 시각화 |
| `0.16.0` | 2025-04-20 | Keras 3.x / TensorFlow 2.x Grad-CAM |

현재 요구 환경은 Python 3.9+와 scikit-learn 1.6+다. 2026-08-23 기준 2026년에 배포된 후속 release는 확인되지 않았다.

## Interpretation Boundaries

> [!warning] Explanation is not causality
> 높은 weight나 importance는 **현재 모델이 현재 data에서 prediction을 만드는 방식**을 설명한다. feature를 현실에서 바꾸면 결과가 반드시 그만큼 변한다는 인과 주장이 아니다.

- training-set importance는 overfitting된 feature까지 높게 보일 수 있다.
- score가 낮은 모델을 설명해도 유용한 예측 근거가 생기지는 않는다.
- correlated feature는 서로 대체 가능해 permutation importance가 모두 낮게 보일 수 있다.
- LIME 설명에는 local surrogate가 원 모델을 얼마나 잘 근사했는지 확인이 필요하다.
- XGBoost `>=2.0.0`의 `explain_prediction()`은 공식 문서가 잘못된 결과 가능성을 경고한다.

## Sources

- https://eli5.readthedocs.io/en/stable/overview.html
- https://eli5.readthedocs.io/en/stable/autodocs/eli5.html
- https://eli5.readthedocs.io/en/stable/libraries/index.html
- https://pypi.org/project/eli5/
- https://eli5.readthedocs.io/en/stable/libraries/xgboost.html

