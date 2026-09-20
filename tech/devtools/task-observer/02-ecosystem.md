---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Task Observer — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 포지션

Task Observer는 다음 범주 사이에 위치한다.

- Agent Skill packaging 위에 놓이는 **skill lifecycle layer**
- session memory와 구별되는 **high-signal methodology event store**
- telemetry가 아닌 **LLM-driven observation protocol**
- live auto-update가 아닌 **review/staging/human approval workflow**

## 접근 방식 비교

| 접근 | 주로 저장하는 것 | 자동성 | 검토 경계 | Task Observer와의 차이 |
|---|---|---|---|---|
| Task Observer | correction, reusable workflow, skill defect, principle | 관찰·기록은 agent 주도 가능 | staged change를 사람이 승인 | skill 개선 lifecycle 자체가 목적 |
| General memory | 사실, 선호, 대화 맥락 | 제품마다 다름 | 보통 항목별 검토가 약함 | skill diff보다 recall이 목적 |
| Transcript/logging | 대화와 tool event 원문 | 높음 | 사후 분석 중심 | 고신호 선별 대신 전체 기록 |
| Runtime telemetry/APM | latency, error, CPU, trace | 높음 | dashboard/alert 중심 | prompt·방법론 개선을 직접 모델링하지 않음 |
| `AGENTS.md`/`CLAUDE.md` 규칙 | 현재 지켜야 할 instruction | 정적 | 파일 변경 시 검토 | observation backlog와 review lifecycle이 없음 |
| 수동 retrospective | 사람이 기억한 문제와 교훈 | 낮음 | 사람 중심 | 실행 중 즉시 capture하기 어렵고 반복성이 낮음 |
| 자동 self-modifying agent | live rules/code 변경 | 매우 높음 | 약하거나 사후적일 수 있음 | Task Observer는 staging과 approval로 분리 |

## Agent Skills 표준과의 관계

Agent Skills specification은 다음을 제공한다.

1. skill directory와 `SKILL.md` format
2. metadata 기반 discovery
3. instruction과 resource의 progressive disclosure
4. `scripts/`, `references/`, `assets/` convention

하지만 activation enforcement와 경험 기반 update lifecycle은 표준 범위 밖이다. Activation RFC는 이를 `discovery ≠ activation` 문제로 설명한다. Task Observer의 dual-layer activation은 이 공백을 client별 instruction/hook으로 보완하는 실용적 해법이지, portability가 완전히 해결됐다는 뜻은 아니다.

## 어떤 방식을 선택할까

### Task Observer가 맞는 경우

- 여러 skill을 실제 업무에 반복 사용한다.
- correction의 출처와 해결 상태를 추적해야 한다.
- 변경 전에 diff, validation, human approval이 필요하다.
- 병렬 session과 장기 backlog를 파일 기반으로 운영할 수 있다.

### 단순 규칙 파일이 더 나은 경우

- 규칙 수가 작고 거의 변하지 않는다.
- 관찰·review backlog를 운영할 사람이 없다.
- 한 repository에서 몇 개의 instruction만 강제하면 충분하다.

### memory가 더 나은 경우

- 사용자의 장기 preference나 factual context를 recall하는 것이 주목적이다.
- 관찰을 skill artifact로 승격할 필요가 없다.

### telemetry가 더 나은 경우

- 숫자로 측정되는 runtime behavior, error rate, latency가 필요하다.
- agent의 판단보다 deterministic instrumentation이 중요하다.

## 함께 쓰는 조합

```text
Agent Skills specification
        ↓ packaging/loading
Task Observer
        ↓ observation/review/staging
Git diff + validation
        ↓ approval/install
AGENTS.md / CLAUDE.md / harness hook
        ↓ activation reinforcement
다음 실제 session
```

General memory는 “누구와 무엇을 했는가”를 보완하고, telemetry는 “시스템이 어떻게 동작했는가”를 보완한다. Task Observer는 “agent의 절차적 지식을 어떻게 개선할 것인가”에 집중한다.

## 평가 기준

| 기준 | 확인 질문 |
|---|---|
| Activation | 새 session 첫 tool call 전에 실제로 load되고 protocol이 실행되는가? |
| Signal quality | 단발성 메모보다 reusable methodology 사건을 선별하는가? |
| Concurrency | parallel session이 서로의 기록을 덮어쓰지 않는가? |
| Reviewability | observation에서 staged diff까지 provenance를 따라갈 수 있는가? |
| Safety | confidential context가 공개 skill에 섞이지 않는가? |
| Context cost | backlog 증가에도 header scan과 on-demand loading이 유지되는가? |
| Closure | 적용된 observation이 계속 open으로 남지 않는가? |

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [RFC: Skill Activation Mechanisms](https://github.com/agentskills/agentskills/issues/57)
- [Task Observer user guide](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/USER-GUIDE.md)
- [Task Observer environment reference](https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/references/environments.md)

