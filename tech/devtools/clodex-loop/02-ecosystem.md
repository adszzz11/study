---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — Ecosystem / 비교

## 이름이 같은 프로젝트를 먼저 구분하기

`clodex`라는 이름은 여러 프로젝트가 쓴다. 이 study의 기준은 **9thLevelSoftware/Clodex**이며, plan부터 isolated build, dual audit, manual apply까지를 하나의 contract로 다룬다.

| 도구/접근 | 주된 목적 | loop의 검증 주체 | 상태·격리 | 적합한 경우 |
|---|---|---|---|---|
| **9thLevelSoftware/Clodex** | Claude Code ↔ Codex CLI 협업 build | Claude + Codex dual audit, unanimous agreement | SQLite, artifacts, Git worktree, manual apply | 계획·구현·감사를 강하게 분리할 repo |
| [lukaskucinski/clodex](https://github.com/lukaskucinski/clodex) | Claude Code plugin의 Codex adversarial review 반복 | Codex review 중심, severity threshold | `.clodex/state.json`, resume/continue | Claude 중심 PR flow에 review loop를 붙일 때 |
| [bman654/clodex](https://github.com/bman654/clodex) | Claude Code에서 Codex/OpenAI/OpenCode model 사용 | provider/model routing 중심 | local OpenAI-compatible endpoint | Claude Code의 model choice를 확장할 때 |
| Claude Code 단독 | plan·구현·review 단일 CLI | 동일 agent self-review | Claude session/config | 빠른 소규모 변경 |
| Codex 단독 + worktree/Goal | 지속 목표 기반 구현 | Codex review + 사용자 검토 | Codex workspace·Goal | 한 agent에게 명확한 목표를 장기 위임할 때 |
| CI test/lint/SAST | 결정론적 품질 gate | test runner/보안 도구 | CI artifact | 어떤 agent flow에도 필요한 baseline |

## 선택 기준

1. **분리 수준**: plan·implementation·audit의 책임과 artifact를 분리해야 하면 9thLevelSoftware/Clodex를 검토한다.
2. **기존 workflow**: 이미 Claude Code PR workflow가 있고 Codex review 재시도만 필요하면 lukaskucinski/clodex의 범위가 더 작다.
3. **model routing**: workflow contract보다 provider/model 선택이 목적이면 bman654/clodex가 다른 문제를 푼다.
4. **품질 gate**: 어떤 선택도 CI의 test/lint/SAST를 대신하지 않는다.

## review loop의 종료 조건

lukaskucinski/clodex는 `review → blocking finding 수정 → re-review`를 명시적 loop로 모델링하며 stall, 재현 가능한 hang, 최대 반복 수를 종료 조건으로 둔다. 9thLevelSoftware/Clodex도 `max_fix_loops`와 agreement로 bounded autonomy를 둔다. 둘 다 “더 이상 agent가 답하지 않을 때까지” 반복하는 방식보다 사람이 개입할 지점을 명확히 한다.

## Sources

- https://github.com/9thLevelSoftware/Clodex
- https://github.com/lukaskucinski/clodex
- https://github.com/bman654/clodex
- https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex
