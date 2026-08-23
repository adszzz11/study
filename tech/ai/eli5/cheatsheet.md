---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 Cheatsheet

> [[README|목차로 돌아가기]]

## Install

```bash
python -m pip install "eli5==0.16.0" "scikit-learn>=1.6"
```

```yaml
checked_at: 2026-08-23
eli5: 0.16.0
python: ">=3.9"
scikit_learn: ">=1.6"
```

## Core API

| 질문 | 즉시 표시 | 구조화된 결과 |
|---|---|---|
| 모델 전체가 무엇을 보는가? | `show_weights()` | `explain_weights()` |
| 이 prediction은 왜 나왔나? | `show_prediction()` | `explain_prediction()` |

```python
import eli5

eli5.show_weights(model, feature_names=feature_names, top=20)
eli5.show_prediction(model, sample, feature_names=feature_names)

exp = eli5.explain_prediction(model, sample, feature_names=feature_names)
print(eli5.format_as_text(exp))
payload = eli5.format_as_dict(exp)
```

text vectorizer를 쓸 때:

```python
eli5.show_weights(classifier, vec=vectorizer, top=20)
eli5.show_prediction(classifier, document, vec=vectorizer)
```

## Method Map

| Model / 질문 | 방법 |
|---|---|
| linear model global | coefficient/weights |
| linear model local | feature value × coefficient + bias |
| tree global | native tree importance 또는 permutation |
| tree local | path contribution; SHAP 교차 검토 |
| arbitrary estimator global | Permutation Importance |
| black-box text local | `TextExplainer` / LIME |
| Keras image local | Grad-CAM |
| OpenAI output uncertainty | token logprobs highlighting |

## Permutation Importance

```python
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(
    model,
    scoring="accuracy",
    n_iter=10,
    random_state=42,
).fit(X_valid, y_valid)

eli5.show_weights(perm, feature_names=feature_names)
```

```text
importance = baseline validation score - shuffled validation score
```

- validation score를 먼저 확인한다.
- 가능하면 held-out set에서 계산한다.
- 평균과 분산을 함께 본다.
- correlated features는 grouped permutation/removal로 추가 검사한다.

## TextExplainer

```python
from eli5.lime import TextExplainer

te = TextExplainer(random_state=42)
te.fit(document, pipeline.predict_proba)
te.show_prediction(target_names=pipeline.classes_)
```

- local surrogate일 뿐 전체 model 설명이 아니다.
- seed, perturbation, sampling, fidelity를 기록한다.
- seed를 바꿔 feature ranking stability를 확인한다.

## Quick Decision

| 상황 | 우선 선택 |
|---|---|
| sklearn/text를 빠르게 debug | ELI5 |
| sklearn 표준 inspection만 필요 | scikit-learn inspection |
| tree의 정교한 local attribution | SHAP |
| black-box sample 주변 근사 | LIME / `TextExplainer` |
| 설명 가능한 model 자체를 학습 | InterpretML |
| PyTorch 내부 attribution | Captum |

## Red Flags

| 보이면 멈출 것 | 이유 |
|---|---|
| “이 feature가 결과의 원인이다” | attribution은 causality가 아님 |
| training set에서만 importance 계산 | overfitting feature가 높게 보일 수 있음 |
| 낮은-score model의 importance 해석 | 설명할 predictive signal 자체가 약함 |
| correlated feature를 개별 순위로 단정 | 서로 정보를 대체함 |
| LIME 1회 결과만 보고 결론 | sampling/seed에 민감함 |
| XGBoost 2.x local ELI5 결과 단독 사용 | 공식 문서가 오류 가능성을 경고함 |
| 높은 token logprob를 사실성으로 해석 | confidence와 factuality는 다름 |

## Report Metadata

```yaml
explanation:
  model_version: your-model-v1
  data_split: validation
  method: eli5-permutation-importance
  scoring: roc_auc
  random_state: 42
  library_versions:
    eli5: 0.16.0
  limitations:
    - non_causal
    - correlated_features
```

## Sources

- https://eli5.readthedocs.io/en/stable/autodocs/eli5.html
- https://eli5.readthedocs.io/en/0.16.0/tutorials/sklearn-text.html
- https://scikit-learn.org/stable/modules/permutation_importance.html
- https://eli5.readthedocs.io/en/stable/libraries/xgboost.html
