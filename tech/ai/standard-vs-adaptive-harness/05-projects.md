---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 공통 Core 위에서 Profile 검증하기

[학습 진입점](README.md) · 선수 학습: [Getting started](04-learning/01-getting-started.md), [Deep dive](04-learning/02-deep-dive.md)

아래는 수행을 제안하는 학습 프로젝트다. 완료한 프로젝트나 측정된 결과가 아니며, 이 노트에는 계획과 acceptance criteria만 기록한다.

## 프로젝트 1: 페이지 읽기 Profile 비교

**문제**: 모델이 첫 페이지에 없는 정보를 누락한 채 완료한다.

- 입력: 정답이 첫 페이지·중간·마지막에 흩어진 문서, 한 페이지짜리 문서, 빈 문서
- 공통 core: 같은 `read_page` tool, 호출 예산, 정답 verifier
- profile 변경: pagination 안내와 남은 페이지 표시
- 산출물: baseline/adapted traces, 과제별 성공 표, tool 호출·비용·시간 비교

절차:

1. [입문 simulation](04-learning/01-getting-started.md)을 실행해 실패 위치를 확인한다.
2. 실제 모델을 연결하고 개발 과제와 holdout 과제를 분리한다.
3. profile 변경 하나만 적용해 반복 평가한다.
4. 개선과 함께 과도한 추가 읽기나 비용 증가가 생겼는지 확인한다.

**완료 기준**: 누락 여부를 자동 판정할 수 있고, 동일 모델에서 profile 전후 결과를 재현할 설정 기록이 있다. 작은 표본의 성공을 전체 파일 작업의 성공 보장으로 설명하지 않는다.

착안 사례: [NVIDIA Harness Profile](https://developer.nvidia.com/blog/?p=119638).

## 프로젝트 2: Checkpoint 기반 작업 재개

**문제**: context가 초기화되거나 provider가 바뀌면 완료한 작업을 다시 수행한다.

- 입력: 여러 단계로 수행하는 작은 자료 정리 과제와 의도적인 중단 지점
- 공통 core: task 상태·남은 예산·tool 결과·artifact 참조 저장
- 적응 계층: 같은 API의 정상 continuation과 provider 변경 후 새 context 생성 경로
- 산출물: checkpoint 예시, 중단 전후 traces, 최종 verifier 결과

절차:

1. 한 단계 완료 후 checkpoint를 만들고 실행을 중단한다.
2. 같은 provider/API에서 native state 보존 경로로 재개한다.
3. 별도 실험에서 portable state만으로 다른 provider에 작업을 넘긴다.
4. 예산 누적과 이미 실행한 tool의 중복 여부를 비교한다.

**완료 기준**: 두 재개 경로가 동일 acceptance criteria를 통과하고, native reasoning 상태를 다른 provider에 잘못 전달하지 않으며, 완료된 쓰기 작업을 중복 실행하지 않는다. adapter만 시험한 경우 실제 provider 전환 검증과 구분해 보고한다.

착안 사례: [Anthropic 장기 실행 구조](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

## 프로젝트 3: Profile Regression Matrix

**문제**: M1에서 만든 profile을 M2에 그대로 적용했을 때 개선이 유지되는지 알 수 없다.

- 입력: 버전이 고정된 과제 집합과 두 model/API 조합
- 비교: M1 baseline/adapted, M2 baseline/adapted의 네 조건
- 산출물: 성공 건수, 비용, 지연, 실패 유형, profile 유지·제거 결정

절차:

1. [심화 실험표](04-learning/02-deep-dive.md)의 네 조건을 구성한다.
2. 동일 tool 권한·평가 기준·예산 상한으로 반복 실행한다.
3. middleware 또는 prompt 보정을 하나씩 제거하는 ablation을 수행한다.
4. holdout 결과와 사전 채택 기준을 비교하고 이전 profile로 돌아갈 경로를 남긴다.

**완료 기준**: 모델 교체 효과와 profile 효과를 구분한 결과표를 만들고, 실패한 조건도 포함한다. “토큰 감소”와 “총비용 감소”를 별도 지표로 계산한다.

착안 자료: [Deep Agents v0.7](https://www.langchain.com/blog/deep-agents-v0-7), [HarnessDev — preprint](https://arxiv.org/abs/2609.01437).

## 결과 기록 양식

```text
Task suite / verifier version:
Provider / API / model version:
Harness / SDK / profile version:
Baseline and changed setting:
Runs / passed runs:
Tool calls / latency / tokens / actual cost:
Failure examples:
Holdout result:
Decision and rollback profile:
```

## Sources

- [NVIDIA Harness Profile](https://developer.nvidia.com/blog/?p=119638)
- [Anthropic: Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [LangChain: Harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- [Deep Agents v0.7](https://www.langchain.com/blog/deep-agents-v0-7)
- [HarnessDev — preprint](https://arxiv.org/abs/2609.01437)
