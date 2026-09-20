---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## 접근법 비교

| 접근법 | Trigger / 적재 | 가장 적합한 용도 | `writing-great-skills`와의 관계 |
|---|---|---|---|
| Agent Skill | description 기반 자동 선택 또는 slash 호출, on-demand load | 재사용 가능한 multi-step procedure, references, scripts | 직접 대상. predictability와 context economy를 설계 |
| Custom instructions / `AGENTS.md` | session 또는 repository 범위에서 상시 적재 | 모든 작업에 적용할 coding convention, policy, workflow invariant | Skill로 빼면 안 되는 always-on rule의 위치 |
| System / developer prompt | application이 매 request 또는 session에 주입 | identity, authority, safety, 전역 behavior | Skill보다 우선하는 runtime policy layer |
| Tool / MCP server | model이 schema를 보고 호출, 결과를 context에 반환 | 외부 system 접근과 deterministic operation | Skill이 “언제·어떻게 tool을 쓸지” 절차화 |
| Script / CLI | 사람이 직접 또는 agent가 명시 실행 | deterministic transform, validation, repetitive mechanics | 불확실한 지시를 executable check로 이동 |
| Workflow engine | graph/event/schedule 기반 실행 | stateful production orchestration, retry, approval | Skill보다 강한 runtime control과 observability 제공 |
| One-off prompt | 현재 turn에만 적재 | 단순하거나 다시 쓰지 않을 작업 | packaging overhead가 불필요한 대안 |

## Invocation 방식 비교

| 유형 | Discovery | 비용 | 적합한 경우 | 주요 위험 |
|---|---|---|---|---|
| Model-invoked | agent가 `description`을 보고 자동 선택 | metadata가 매 turn context에 노출 | 사용자가 기억하지 않아도 적용돼야 하는 specialized capability | false positive/negative routing |
| User-invoked | 사용자가 `/skill-name`으로 호출 | 사람의 cognitive load | 중요 workflow 시작을 인간이 통제 | discoverability와 이름 기억 부담 |
| Router skill | 사용자가 router 하나만 호출 | 낮은 context load와 탐색 보조 | user-invoked Skill이 많을 때 | router 자체의 분류 오류와 추가 hop |

`writing-great-skills`는 user-invoked다. Skill을 작성하거나 진단할 때만 명시적으로 context에 넣어, 평상시 token 비용과 accidental trigger를 줄인다.

## Skill, Instruction, Tool의 경계

```text
Always true?                 → system/developer prompt or AGENTS.md
Reusable judgment workflow? → Agent Skill
Deterministic operation?     → script/tool
Long-lived state machine?    → workflow engine
One-time small request?      → prompt
```

하나만 선택할 필요는 없다. 좋은 Skill은 판단과 branch를 설명하고, 정확해야 하는 작업은 script에 위임하며, repository-wide invariant는 `AGENTS.md`에 남긴다.

```text
Skill: "변경된 schema를 찾아 migration 필요성을 판정한다"
Script: "schema diff를 계산하고 exit code를 반환한다"
AGENTS.md: "모든 schema 변경은 migration test를 통과해야 한다"
```

## Portability Matrix

| 요소 | Core specification | Client-specific 가능성 | 운영 원칙 |
|---|---|---|---|
| `name` | 필수 | naming restriction 차이 가능 | 각 validator에서 검사 |
| `description` | 필수, 최대 1,024자 | routing model 차이 | capability와 trigger를 함께 eval |
| `SKILL.md` body | 표준 핵심 | tool syntax 차이 | portable instruction과 adapter 분리 |
| `disable-model-invocation` | core field 아님 | 일부 Claude/Copilot 계열에서 지원 | portable variant에 무조건 복사하지 않기 |
| `agents/openai.yaml` | core 필수 아님 | client UI/metadata용 | 없어도 core Skill이 이해되게 작성 |

2026년 6월 공개 issue에서는 Codex validator가 `disable-model-invocation`을 거부한다는 호환성 문제가 제기됐다. 결론은 어느 client가 “옳다”가 아니라 다음 배포 형태를 구분하는 것이다.

```text
portable/
└── SKILL.md              # core frontmatter only

adapters/
├── claude-or-copilot/    # supported extensions
└── openai/agents/...     # client display metadata
```

## 선택 가이드

| 상황 | 우선 선택 |
|---|---|
| 모든 repo task에 적용되는 rule | `AGENTS.md` 또는 상위 instruction |
| 반복되지만 특정 요청에만 필요한 review 절차 | Agent Skill |
| 정확히 같은 변환이 필요 | script + tests |
| 배포 승인, retry, state persistence 필요 | workflow engine |
| tool 연결 자체가 필요 | MCP/tool server |
| 여러 client에 Skill 배포 | core-only portable variant + adapter validation |

## Trade-offs

- Skill은 context를 절약하지만 discovery 실패라는 새 failure surface를 만든다.
- User invocation은 통제력이 높지만 cognitive load가 생긴다.
- Router는 목록 기억을 줄이지만 routing layer가 하나 더 생긴다.
- Script는 deterministic하지만 ambiguous domain judgment를 스스로 해결하지 못한다.
- Workflow engine은 강한 통제를 주지만 authoring과 운영 비용이 크다.

## Sources

- [Anthropic, Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic, Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [호환성 issue #360](https://github.com/mattpocock/skills/issues/360)
- [Model Context Protocol introduction](https://modelcontextprotocol.io/docs/getting-started/intro)

