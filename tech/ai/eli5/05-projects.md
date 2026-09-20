---
date: 2026-08-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ELI5 Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: Cheatsheet]]

## Project 1: Text Classifier Artifact Audit

news, review, support-ticket classifier가 실제 의미 대신 dataset artifact를 학습했는지 감사한다.

| 항목 | 내용 |
|---|---|
| 입력 | trained Pipeline, train/validation split, raw text |
| Global 검사 | class별 top positive/negative weights |
| Local 검사 | 정답·오답·low-confidence sample의 token contribution |
| 산출물 | suspicious feature 목록과 data remediation plan |

감사할 artifact 예시:

- author/user ID, source domain, template footer
- label을 암시하는 prefix나 folder name
- train/test 기간을 구분하는 timestamp pattern
- 특정 class에서만 발생한 spelling/encoding 문제

성공 기준:

- suspicious token을 제거하고 split을 다시 만든다.
- model score 변화와 explanation 변화가 함께 기록된다.
- 성능이 떨어지더라도 leakage 제거 후 score를 진짜 baseline으로 채택한다.

## Project 2: Model Card Explanation Appendix

모델 카드에 재현 가능한 explanation appendix를 붙인다.

```yaml
explanation_run:
  model_version: ticket-router-v3
  eli5_version: 0.16.0
  data_split: validation-2026-08
  checked_at: 2026-08-23
  methods:
    - linear_weights
    - linear_contribution
    - permutation_importance
  limitations:
    - non_causal
    - correlated_features
```

appendix 구성:

1. held-out metric과 dataset provenance
2. global top features
3. 대표 true positive/negative와 failure case
4. permutation mean/variance
5. known limitation과 사람이 검토할 escalation rule

## Project 3: Explanation Regression Test

model release마다 prediction뿐 아니라 설명의 큰 변화도 추적한다.

```python
def suspicious_features(explanation_dict, denylist):
    rendered = str(explanation_dict).lower()
    return [token for token in denylist if token.lower() in rendered]
```

검사 항목:

- gold sample의 predicted class가 바뀌었는가?
- contribution 상위 feature가 갑자기 ID/leakage feature로 바뀌었는가?
- global top features의 rank가 허용 범위 이상 이동했는가?
- explanation formatter schema가 dependency update로 바뀌었는가?

설명 순위는 data와 regularization 변화에 민감하므로 exact snapshot보다 의미 있는 invariant와 threshold를 test한다.

## Project 4: Correlated Feature Lab

서로 거의 같은 두 feature를 만들고 permutation importance의 함정을 재현한다.

```text
X1 ───────────────┐
                  ├─ same signal ─> model
X2 = X1 + noise ──┘
```

실험 순서:

1. X1, X2가 모두 있는 model을 학습한다.
2. 개별 permutation importance를 계산한다.
3. X1과 X2를 한 그룹으로 함께 shuffle한다.
4. 한 feature를 제거하고 재학습한다.
5. 결과 차이를 “importance가 feature의 고유 속성이 아니다”라는 관점으로 기록한다.

## Project 5: XGBoost Local Explanation Cross-check

현대 XGBoost model에서 ELI5 결과를 검증하는 작은 compatibility suite를 만든다.

| 검증 | 목적 |
|---|---|
| fixed synthetic samples | contribution 방향을 사람이 계산 가능하게 함 |
| native margin/prediction | base prediction과 일치 확인 |
| SHAP TreeExplainer | feature별 attribution 교차 확인 |
| version matrix | XGBoost/ELI5 조합별 known result 기록 |

공식 경고 때문에 이 프로젝트의 목표는 ELI5 결과를 “증명”하는 것이 아니라, 잘못된 결과를 production에서 차단하는 것이다.

## Project 6: Token Confidence Viewer

OpenAI token logprobs를 문장별로 highlight하고 uncertainty 구간을 탐색하는 viewer를 만든다.

UI에는 다음 disclaimer를 고정 표시한다.

> Token confidence는 factual correctness나 hidden reasoning의 증거가 아니다.

추가로 기록할 값:

- model ID와 sampling parameters
- prompt/context hash
- token, logprob, top alternatives
- request timestamp
- factuality evaluation은 별도 pipeline 결과로 분리

## Project Selection

| 난이도 | 추천 프로젝트 | 학습 포인트 |
|---|---|---|
| 입문 | Text Classifier Artifact Audit | global/local explanation |
| 중급 | Model Card Appendix | provenance와 전달 |
| 중급 | Correlated Feature Lab | permutation 함정 |
| 심화 | Explanation Regression Test | 운영·versioning |
| 심화 | XGBoost Cross-check | integration 검증 |
| 심화 | Token Confidence Viewer | logprobs의 올바른 범위 |

## Sources

- https://eli5.readthedocs.io/en/0.16.0/tutorials/sklearn-text.html
- https://scikit-learn.org/stable/modules/permutation_importance.html
- https://eli5.readthedocs.io/en/stable/libraries/xgboost.html
- https://eli5.readthedocs.io/en/0.16.0/tutorials/explain_llm_logprobs.html

