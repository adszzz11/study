---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 Ecosystem

> [[01-overview|이전: Overview]] | [[README|목차로 돌아가기]] | [[03-references|다음: References]]

## Positioning

ELI5는 XAI 전체를 대체하기보다 **전통적 scikit-learn/text workflow의 빠른 debugging**에 강한 도구다. 선택 기준은 “가장 유명한 도구인가?”보다 모델 종류, 필요한 설명 범위, 계산비용, 사용자가 받아들일 수 있는 가정에 두어야 한다.

## Comparison

| 도구 | 주력 영역 | Global / Local | 장점 | ELI5 대비 선택 기준 |
|---|---|---:|---|---|
| **ELI5** | scikit-learn, text, tree debugging | 둘 다 | 간단한 API, Pipeline·vectorizer 이해, text highlighting, formatter 분리 | 전통적 sklearn/NLP 모델을 빠르게 검사할 때 |
| **scikit-learn inspection** | sklearn-native model inspection | 주로 Global | 별도 의존성 없이 permutation importance, PDP 등 제공 | ELI5 rendering이 필요 없고 표준 API만 원할 때 |
| **SHAP** | Shapley-value attribution | 둘 다 | Tree/Linear 최적화, model-agnostic API, 풍부한 plot | 정교한 local attribution과 대규모 tree 분석이 핵심일 때 |
| **LIME** | local surrogate explanation | Local | text/tabular/image black-box 지원 | sample 주변의 근사 decision boundary가 필요할 때 |
| **InterpretML** | glassbox + blackbox XAI | 둘 다 | Explainable Boosting Machine, dashboard, 통합 workflow | 설명 가능한 모델 자체를 학습하거나 통합 XAI 환경이 필요할 때 |
| **Captum** | PyTorch deep learning attribution | Local 중심 | Integrated Gradients, layer/neuron, multimodal attribution | PyTorch network 내부 분석이 필요할 때 |

## ELI5 vs scikit-learn Inspection

둘 다 Permutation Importance를 제공할 수 있지만 초점이 다르다.

| 질문 | 선택 |
|---|---|
| sklearn만으로 dependency를 최소화할까? | `sklearn.inspection.permutation_importance` |
| 기존 ELI5 explanation/formatter와 함께 보여줄까? | `eli5.sklearn.PermutationImportance` |
| Partial Dependence나 ICE가 핵심인가? | scikit-learn inspection |
| text token highlighting이 필요한가? | ELI5 |

Permutation Importance의 통계적 함정은 어느 API를 쓰든 같다. 먼저 held-out score를 확인하고, 반복 shuffle의 평균과 분산을 함께 보며, correlated features를 점검해야 한다.

## ELI5 vs SHAP

ELI5의 linear contribution과 tree path contribution을 곧바로 SHAP value와 동일시하면 안 된다. SHAP은 Shapley-value framework와 background/reference distribution에 기반한 attribution을 제공한다. ELI5는 모델별로 더 직접적이고 가벼운 설명을 제공하는 경우가 많다.

- 빠른 coefficient/token 확인: ELI5
- tree ensemble의 풍부한 local/global plot: SHAP
- attribution의 additive consistency가 중요한 분석: SHAP의 가정과 explainer 선택 검토
- 결과를 이해관계자에게 전달: 둘 중 하나를 고르기 전에 baseline/reference 의미부터 명시

## ELI5 TextExplainer vs LIME

`TextExplainer`는 LIME 계열 아이디어를 ELI5의 text workflow와 presentation에 통합한다. 원 모델을 black box로 호출해 주변 text를 perturb하고 local surrogate를 학습한다.

```text
target document
   └─ token perturbations
       └─ black-box predictions
           └─ weighted sparse surrogate
               └─ local feature contributions
```

설명은 target document 주변에서만 유효한 **근사치**다. `random_state`, sampling 설정, tokenization과 surrogate fidelity를 기록해야 재현하고 비판할 수 있다.

## Deep Learning Choice

| Stack | 우선 검토 도구 | 이유 |
|---|---|---|
| Keras image classifier | ELI5 Grad-CAM 또는 Keras visualization | class localization heatmap을 빠르게 확인 |
| PyTorch model | Captum | framework-native attribution 범위가 넓음 |
| tree-based tabular model | SHAP + native importance | optimized explainer와 다양한 plot |
| mixed black-box API | LIME, SHAP model-agnostic, permutation | prediction function만으로 접근 가능 |

ELI5 Grad-CAM은 image classification 중심이고 한 번에 하나의 target class를 다루는 등 범위가 제한적이다.

## Recommended Decision Flow

```text
설명 대상은?
├─ sklearn linear/text ───────────────> ELI5 우선
├─ sklearn model의 global inspection ─> sklearn inspection 또는 ELI5
├─ tree local attribution ────────────> SHAP 우선, ELI5는 교차검증
├─ black-box의 한 sample ─────────────> LIME/TextExplainer
├─ PyTorch neural network ────────────> Captum
└─ 설명 가능한 모델 자체 ────────────> InterpretML
```

## Sources

- https://eli5.readthedocs.io/en/stable/libraries/index.html
- https://scikit-learn.org/stable/modules/permutation_importance.html
- https://shap.readthedocs.io/en/latest/
- https://lime-ml.readthedocs.io/en/latest/
- https://interpret.ml/
- https://captum.ai/docs/introduction

