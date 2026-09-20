---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 Deep Dive

> [[01-getting-started|이전: Getting Started]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: Projects]]

## Goal

native model explanation을 넘어 model-agnostic 방법을 사용하고, explanation이 틀리거나 불안정해지는 조건을 실험한다.

## Permutation Importance

Permutation Importance는 한 feature column을 shuffle해 model score가 얼마나 감소하는지 측정한다.

```text
importance(feature j)
  = baseline score
  - score after shuffling feature j
```

```python
import eli5
from eli5.sklearn import PermutationImportance
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data,
    data.target,
    test_size=0.25,
    random_state=42,
    stratify=data.target,
)

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)
print("held-out score:", model.score(X_test, y_test))

perm = PermutationImportance(
    model,
    scoring="accuracy",
    n_iter=10,
    random_state=42,
).fit(X_test, y_test)

eli5.show_weights(perm, feature_names=data.feature_names.tolist())
```

### Interpretation protocol

1. **먼저 baseline score**: validation set에서 predictive power가 없으면 importance도 해석하지 않는다.
2. **held-out data 사용**: training set은 overfit된 feature를 중요하게 보이게 할 수 있다.
3. **반복과 분산 확인**: shuffle 결과는 random하므로 mean만 보지 않는다.
4. **scoring 명시**: accuracy, ROC AUC, loss는 서로 다른 질문이다.
5. **correlation 검사**: 대체 가능한 correlated features는 양쪽 importance가 낮게 보일 수 있다.

> [!warning] 낮은 importance ≠ 쓸모없는 feature
> feature A와 B가 같은 정보를 담으면 A를 shuffle해도 B가 대신한다. 두 feature를 함께 제거하거나 grouped permutation을 실험해야 한다.

## Local Black-box Explanation with TextExplainer

`TextExplainer`는 target text 주변의 perturbation을 만들고 원 classifier의 prediction을 query한 뒤 sparse local surrogate를 학습한다.

```python
from eli5.lime import TextExplainer

document = "clear explanation but unreliable result"
explainer = TextExplainer(random_state=42)
explainer.fit(document, pipeline.predict_proba)
explainer.show_prediction(target_names=pipeline.classes_)
```

반드시 기록할 것:

- target document와 target class
- tokenizer/perturbation 정의
- number of samples와 distance/kernel 설정
- `random_state`
- local surrogate fidelity
- 원 model prediction과 surrogate prediction의 차이

LIME 계열 설명은 전체 decision boundary가 아니라 한 sample 주변의 근사 모델이다. seed나 sampling을 바꿨을 때 상위 feature가 크게 바뀐다면 결론의 안정성도 낮다.

## Native vs Model-agnostic Cross-check

같은 model에 여러 설명을 적용해 질문과 가정이 다른지 확인한다.

| 결과 | 가능한 해석 | 다음 검사 |
|---|---|---|
| coefficient 높음, permutation도 높음 | 큰 weight이며 held-out score에도 영향 | scale, leakage 확인 |
| coefficient 높음, permutation 낮음 | rare feature 또는 correlated 대체 feature | frequency, correlation 확인 |
| tree native importance 높음, permutation 낮음 | training split에 많이 쓰였지만 validation 기여는 작음 | overfitting 확인 |
| LIME 결과가 seed마다 변함 | local approximation 불안정 | sampling 확대, SHAP/ablation 교차 확인 |

## XGBoost Version Trap

공식 ELI5 문서는 XGBoost `>=2.0.0`에서 `explain_prediction()`이 잘못된 결과를 만들 가능성을 경고한다.

```text
XGBoost >= 2.0.0 local explanation
    ├─ ELI5 결과 단독 사용 금지
    ├─ native prediction/contribution 확인
    ├─ SHAP TreeExplainer와 교차 확인
    └─ known test case에서 합계·방향 검증
```

global `explain_weights()`와 local `explain_prediction()`은 서로 다른 구현 경로일 수 있으므로 한쪽의 정상 동작이 다른 쪽까지 보장하지 않는다.

## Keras Grad-CAM

ELI5 `0.16.0`은 Keras 3.x / TensorFlow 2.x image classification용 Grad-CAM을 지원한다. heatmap은 target class에 민감한 spatial region을 보여주지만 다음을 증명하지 않는다.

- 해당 pixel이 현실에서 원인이라는 것
- 모델이 object를 인간과 같은 개념으로 이해한다는 것
- heatmap이 adversarial하거나 shortcut-based 판단을 배제한다는 것

한 번에 하나의 target class를 다루는 범위와 지원 layer/model 구조를 공식 integration 문서에서 확인한다.

## OpenAI Token Logprobs

`0.15.0`에 추가된 기능은 completion token의 log probability를 highlighting한다.

| 말할 수 있는 것 | 말할 수 없는 것 |
|---|---|
| 생성 시 특정 token의 상대적 confidence | 숨겨진 chain-of-thought |
| 어느 구간의 token uncertainty가 높은지 | 문장의 factual correctness |
| alternative token 분포를 이용한 debugging | 모델 내부의 인과적 reasoning process |

logprob는 model과 decoding context에 조건부인 확률 신호다. 낮은 confidence가 오류를 뜻하지 않고, 높은 confidence가 사실임을 보장하지도 않는다.

## Production Report Pattern

```python
import json
import eli5

explanation = eli5.explain_prediction(
    classifier,
    document,
    vec=vectorizer,
    target_names=classifier.classes_,
)

payload = {
    "model_version": "text-clf-v3",
    "data_split": "validation-2026-08",
    "explanation_method": "eli5-linear-contribution",
    "warning": "Feature attribution is not a causal explanation.",
    "explanation": eli5.format_as_dict(explanation),
}

print(json.dumps(payload, ensure_ascii=False, default=str))
```

report에는 model/data/method version, target, score, limitation을 explanation과 함께 묶는다. explanation payload만 떼어 전달하면 사용자가 범위를 과장하기 쉽다.

## Deep-dive Checklist

- [ ] held-out set에서 Permutation Importance 계산
- [ ] scoring과 반복 횟수 기록
- [ ] correlation matrix 또는 feature grouping 검사
- [ ] `TextExplainer` seed를 바꿔 stability 확인
- [ ] native explanation과 model-agnostic result 비교
- [ ] XGBoost 2.x local result는 SHAP/native method로 교차 확인
- [ ] LLM logprob와 factuality를 명확히 분리
- [ ] report에 non-causal warning과 provenance 포함

## Sources

- https://eli5.readthedocs.io/en/stable/blackbox/permutation_importance.html
- https://scikit-learn.org/stable/modules/permutation_importance.html
- https://eli5.readthedocs.io/en/stable/tutorials/black-box-text-classifiers.html
- https://eli5.readthedocs.io/en/stable/libraries/xgboost.html
- https://eli5.readthedocs.io/en/latest/libraries/keras.html
- https://eli5.readthedocs.io/en/0.16.0/tutorials/explain_llm_logprobs.html

