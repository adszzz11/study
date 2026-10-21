---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Harness² ecosystem and alternatives

| 도구/연구 | 주 최적화 대상 | 피드백 전제 | Harness²와의 차이 |
|---|---|---|---|
| **Harness²** | agent의 8개 harness component | verifier 없이 execution contrast 활용 가능 | task별 개선과 cross-task lesson 축적을 함께 제공 |
| [Meta-Harness](https://arxiv.org/abs/2603.28052) | application harness source code | score·trace·기존 후보 이력 | offline/outer-loop code search에 더 가깝고, Harness²는 unseen task의 online adaptation에 초점 |
| [DSPy](https://dspy.ai/) | declarative LM program의 prompt/demo/module | metric 및 optimization workflow | 구조화된 LM pipeline 개발·최적화에 강점; Harness²는 agent runtime 전체의 self-improving harness에 초점 |
| [Reflexion](https://arxiv.org/abs/2303.11366) | agent reflection memory | 환경의 scalar/text feedback | 실패 feedback을 언어 memory로 축적; Harness²는 harness 파일/구성을 직접 탐색·합성 |
| [OpenAI agent evals](https://developers.openai.com/api/docs/guides/agent-evals) | trace·grader·dataset 기반 품질 측정 | 명시적 evaluator/grader | eval/관측 계층이며, Harness²처럼 harness 변경을 자동 탐색·채택하는 framework는 아님 |

## Selection guide

- **Harness²**: executor behavior를 바꾸는 여러 runtime surface를 함께 실험하고, task 간 경험을 재사용하려 할 때
- **DSPy**: metric이 있고 LM pipeline의 prompt/demo/module을 선언적으로 최적화할 때
- **Reflexion**: 실패 feedback을 agent memory로 간단히 축적하는 연구 패턴이 필요할 때
- **OpenAI agent evals**: dataset, grader, trace로 품질을 측정·회귀 방지할 때. Harness²의 adoption gate로 함께 둘 수 있다.
- **Meta-Harness**: source-level harness 후보를 offline search하는 접근을 비교 연구할 때

## Complementary operating model

Harness²가 후보 patch를 만들더라도 evaluator는 분리한다. sealed eval set, `--bases` 비교, CI, security review, human approval을 promotion gate로 두면 “개선했다”는 자기 판단과 실제 배포 판단을 분리할 수 있다.
