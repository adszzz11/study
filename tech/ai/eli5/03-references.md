---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: Getting Started]]

## Official Resources

| 자료 | URL | 읽을 포인트 |
|---|---|---|
| Stable documentation | https://eli5.readthedocs.io/en/stable/ | 현재 문서 진입점 |
| Architecture overview | https://eli5.readthedocs.io/en/stable/overview.html | explanation/presentation 분리, dispatch |
| Top-level API | https://eli5.readthedocs.io/en/stable/autodocs/eli5.html | `explain_*`, `show_*`, formatter |
| Supported libraries | https://eli5.readthedocs.io/en/stable/libraries/index.html | estimator/library별 integration |
| GitHub repository | https://github.com/eli5-org/eli5 | source, issue, release tag |
| PyPI | https://pypi.org/project/eli5/ | version, Python 요구사항, release history |

## Tutorials

| 자료 | URL | 읽을 포인트 |
|---|---|---|
| scikit-learn text debugging | https://eli5.readthedocs.io/en/0.16.0/tutorials/sklearn-text.html | vectorizer, feature name, text highlighting |
| LLM token logprobs | https://eli5.readthedocs.io/en/0.16.0/tutorials/explain_llm_logprobs.html | token confidence visualization의 범위 |
| Black-box text classifier | https://eli5.readthedocs.io/en/stable/tutorials/black-box-text-classifiers.html | `TextExplainer`, local surrogate |
| Keras integration | https://eli5.readthedocs.io/en/latest/libraries/keras.html | Grad-CAM 대상과 제한 |
| XGBoost integration | https://eli5.readthedocs.io/en/stable/libraries/xgboost.html | local explanation version warning |

## Method References

| 주제 | URL | 확인할 것 |
|---|---|---|
| scikit-learn Permutation Importance | https://scikit-learn.org/stable/modules/permutation_importance.html | validation score, correlation, 반복 측정 |
| SHAP documentation | https://shap.readthedocs.io/en/latest/ | Shapley attribution과 explainer 선택 |
| LIME documentation | https://lime-ml.readthedocs.io/en/latest/ | perturbation과 local surrogate |
| InterpretML | https://interpret.ml/ | glassbox와 blackbox workflow |
| Captum | https://captum.ai/docs/introduction | PyTorch attribution algorithms |

## Version Notes

```yaml
checked_at: 2026-08-23
package: eli5
latest_version: 0.16.0
uploaded_at: 2025-04-20
requirements:
  python: ">=3.9"
  scikit_learn: ">=1.6"
```

| Version | Release date | Change |
|---|---:|---|
| `0.14.0` | 2025-03-26 | scikit-learn 1.6+, Python 3.11–3.13 지원 |
| `0.15.0` | 2025-04-06 | OpenAI client token logprobs 시각화 |
| `0.16.0` | 2025-04-20 | Keras 3.x / TensorFlow 2.x Grad-CAM |

> [!note] 날짜 불일치
> PyPI 본문의 changelog는 `0.16.0 (2024-04-20)`로 표시하지만 artifact upload와 release history는 2025-04-20을 기록한다. 이 노트는 후자를 사용하며 본문 표기는 오기로 판단한다.

## Reading Order

1. Architecture overview에서 `Explanation`과 formatter의 분리를 이해한다.
2. scikit-learn text tutorial로 global/local API를 실행한다.
3. Permutation Importance 문서에서 validation과 correlation 함정을 읽는다.
4. 사용할 estimator의 integration 문서와 known limitation을 확인한다.
5. SHAP/LIME/Captum과 비교해 explanation method의 가정을 명시한다.

## Evidence Checklist

- [ ] version과 확인 날짜를 함께 기록했는가?
- [ ] model score를 held-out set에서 먼저 확인했는가?
- [ ] global과 local explanation을 구분했는가?
- [ ] feature value, coefficient, contribution, importance를 혼용하지 않았는가?
- [ ] explanation을 causality로 표현하지 않았는가?
- [ ] XGBoost 2.x local explanation을 다른 방법으로 교차 확인했는가?
- [ ] LLM logprobs를 reasoning이나 factuality로 과장하지 않았는가?

## Sources

- https://eli5.readthedocs.io/en/stable/
- https://github.com/eli5-org/eli5
- https://pypi.org/project/eli5/
- https://scikit-learn.org/stable/modules/permutation_importance.html
