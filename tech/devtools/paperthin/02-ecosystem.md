---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## 포지션

Paperthin은 model runtime, orchestration engine, IDE가 아니라 기존 agent 위에 설치하는 procedure layer다. 따라서 “어떤 agent가 일할 것인가”보다 “일하는 동안 어떤 reflex를 언제 적용할 것인가”를 다룬다.

## 접근 방식 비교

| 접근 | 주된 역할 | 강점 | 한계 | Paperthin과의 관계 |
|---|---|---|---|---|
| Agent framework | tool calling, state, workflow orchestration | 복잡한 application 구성 | runtime lock-in과 운영 surface 증가 | 대체재보다 하위 discipline layer |
| Repository rule file | project convention을 항상 제공 | 단순하고 예측 가능 | context를 계속 차지하고 상황별 절차가 약함 | 상시 규칙은 rule file, 조건부 procedure는 skill |
| Prompt/snippet library | 사람이 복사해 사용 | 도입 비용이 낮음 | discovery, activation, resource 구조가 비표준 | Paperthin은 `SKILL.md`로 packaging |
| Hook/guardrail | 특정 event에서 자동 검사 | 강제력이 높음 | 잘못된 trigger와 environment coupling 위험 | catalog adapter와 조합 가능 |
| 개별 specialist agent | 독립 관점과 context | evaluator separation 가능 | latency/cost와 coordination 필요 | `prism`/`mandela`가 필요성을 판단 |
| Paperthin | 실패 지점별 작은 reflex | vendor-neutral, progressive disclosure, 조합 가능 | 효과가 agent 준수와 skill 품질에 의존 | 기존 stack 위에 추가 |

## 유사 개념과 구분

### Linter/Test와 비교

- linter와 unit test는 machine-checkable invariant에 강하다.
- `re0`, `hate`, `mandela`는 stale narrative, load-bearing assumption, shared framing처럼 정형화하기 어려운 문제를 다룬다.
- 둘은 대체 관계가 아니다. Paperthin의 procedure가 test 실행을 요구할 수 있지만 test 자체가 되는 것은 아니다.

### Multi-agent debate와 비교

- debate는 여러 agent가 같은 정보를 보고 논쟁해 apparent consensus를 만들 수 있다.
- `prism`의 관심사는 합의가 아니라 독립 lens 사이의 divergence다.
- `mandela`는 evaluator 수보다 external ground truth가 실제로 독립적인지를 묻는다.

### Memory/plan 문서와 비교

- 일반 memory는 많은 상태를 보존하기 쉽다.
- `re0-memo`와 `re0-work`는 다음 iteration에 필요한 learning과 next action으로 압축하는 방향이다.
- 보존량이 아니라 재시작 품질이 기준이다.

## 선택 가이드

| 상황 | 먼저 고려할 것 |
|---|---|
| deterministic style/type 오류 | linter, compiler, test |
| 문서가 과거 delta로 비대해짐 | `re0` |
| 사실이 여러 manifest에 반복됨 | `ssotize` |
| plan의 치명적 가정이 의심됨 | 사람이 명시적으로 `hate` 호출 |
| 결과 평가가 자기확증처럼 보임 | `mandela` + 독립 source |
| 장기 작업이 매번 context부터 복원함 | `re0-loop`, `re0-memo`, `re0-work` |
| catalog 일부만 설치되어 drift | confirmation을 거치는 `re0-upgrade` |

## Trade-offs

- 절차가 늘수록 latency와 context cost가 증가한다.
- destructive skepticism을 상시 켜면 유효한 plan까지 반복적으로 흔들 수 있다.
- Markdown instruction은 hard sandbox가 아니므로 실제 권한 통제와 review가 별도로 필요하다.
- vendor-neutral format이어도 host별 discovery, hook, filesystem semantics는 검증해야 한다.

## Sources

- https://agentskills.io/specification
- https://github.com/LilMGenius/paperthin/blob/main/docs/invocation.md
- https://github.com/LilMGenius/paperthin/blob/main/skills/mesh/prism/SKILL.md

