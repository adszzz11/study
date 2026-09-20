---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5

> **한 줄 정의**: ELI5는 여러 Machine Learning 모델의 **global feature importance**와 **개별 prediction의 feature contribution**을 통합 API로 설명·시각화하는 Python XAI/debugging 라이브러리다.

## Overview

ELI5는 모델을 새로 학습하는 framework가 아니라, 이미 학습한 estimator가 **무엇을 보고 판단했는지** 검사하는 도구다. `explain_weights()`와 `explain_prediction()`은 구조화된 `Explanation`을 만들고, `show_weights()`와 `show_prediction()`은 이를 notebook에서 바로 시각화한다.

```text
Estimator + Input
       │
       ▼
explain_weights() / explain_prediction()
       │ estimator type에 따른 dispatch
       ▼
Explanation intermediate object
       ├── HTML / IPython
       ├── plain text
       ├── dict / JSON
       ├── pandas.DataFrame
       └── PIL image
```

초기 강점은 `scikit-learn`의 `CountVectorizer`, `TfidfVectorizer`, `HashingVectorizer`, `Pipeline`, `FeatureUnion`을 이해하고 text feature를 원문에 highlighting하는 기능이었다. 최신 `0.16.0`은 Keras 3.x Grad-CAM과 OpenAI token logprobs 시각화까지 범위를 넓혔다.

> [!info] 조사 기준
> 2026-08-23 기준 PyPI 최신판은 `0.16.0`이며 artifact 업로드일은 2025-04-20이다. PyPI 본문의 `0.16.0 (2024-04-20)` 표기는 release history와 달라 문서상 오기로 판단한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, global·local explanation, 지원 방식 이해
- [ ] [[02-ecosystem|Ecosystem]] — scikit-learn inspection, SHAP, LIME, InterpretML, Captum과 비교
- [ ] [[03-references|References]] — 공식 API, tutorial, 제약 문서 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — linear text classifier를 학습하고 weights/prediction 설명
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — Permutation Importance, LIME, formatter, 검증 전략 학습
- [ ] [[05-projects|Projects]] — dataset artifact audit와 model explanation report 제작
- [ ] [[cheatsheet|Cheatsheet]] — API, 선택 기준, 함정 빠른 참조

## When To Use

- 전통적인 `scikit-learn` linear/tree model을 빠르게 debugging할 때
- text classifier가 의미 있는 token 대신 dataset artifact를 학습했는지 확인할 때
- `Pipeline`과 vectorizer를 거친 feature name을 coefficient에 연결할 때
- 한 sample의 prediction에 어떤 feature가 양·음의 기여를 했는지 notebook에서 볼 때
- estimator 내부를 몰라도 held-out data에서 model-agnostic importance를 추정할 때
- 설명 결과를 HTML, text, dict/JSON, DataFrame 등으로 report pipeline에 전달할 때

## When Not To Use

- feature attribution을 현실 세계의 **causality**로 해석하려 할 때
- 대규모 tree model에서 정교하고 일관된 Shapley attribution이 핵심일 때
- PyTorch layer/neuron 수준의 deep attribution이 필요할 때
- XGBoost `>=2.0.0`의 local prediction 설명을 검증 없이 그대로 사용할 때
- correlated features가 많은 data에서 permutation score를 단일한 진실로 해석할 때
- OpenAI token logprobs로 model reasoning이나 factual correctness를 설명하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/ai-ecosystem/01-overview]] — AI/XAI 도구를 더 넓은 ecosystem에서 비교
- [[tech/ai/model-context-protocol-mcp/README]] — explanation 결과를 tool/resource로 노출할 때의 integration 맥락

## Sources

- https://eli5.readthedocs.io/en/stable/
- https://eli5.readthedocs.io/en/stable/overview.html
- https://eli5.readthedocs.io/en/stable/libraries/index.html
- https://github.com/eli5-org/eli5
- https://pypi.org/project/eli5/
- https://scikit-learn.org/stable/modules/permutation_importance.html

