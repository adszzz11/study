---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## 핵심 공식

```text
목표: output equality가 아니라 process predictability

좋은 Skill
= routing precision/recall
+ explicit workflow
+ checkable completion criteria
+ progressive disclosure
+ eval-driven pruning
```

## Minimal Structure

```text
skill-name/
├── SKILL.md             # metadata + common workflow + gates
├── references/          # branch-specific knowledge
├── scripts/             # deterministic operations
├── assets/              # output에 재사용할 files
└── agents/openai.yaml   # optional client metadata
```

## Description Checklist

- [ ] capability와 use trigger를 모두 썼는가?
- [ ] leading word 또는 명확한 leading verb가 앞에 있는가?
- [ ] 실제 user/domain vocabulary인가?
- [ ] 서로 다른 branch마다 trigger가 하나씩 있는가?
- [ ] 같은 branch의 동의어를 반복하지 않았는가?
- [ ] implementation detail은 body에 있는가?
- [ ] third-person인가?
- [ ] 1,024자 이내인가?

```yaml
description: Audits release notes for breaking changes when users ask to upgrade, migrate, or verify version compatibility.
```

## Step Template

```markdown
1. <Action>
   - Produce: <observable artifact>
   - Verify: <comparison, test, or evidence>
   - Continue only when: <binary/exhaustive exit condition>
```

| 약함 | 강함 |
|---|---|
| “변경 목록 작성” | “diff의 모든 modified model과 대조” |
| “tests 확인” | “지정 command를 실행하고 exit status 기록” |
| “영향 검토” | “각 breaking change를 affected/not affected로 근거와 함께 분류” |

## Inline Or Disclose?

```text
모든 branch에 즉시 필요?       → inline
특정 branch에서만 필요?        → reference + load condition
정확히 반복되는 operation?     → script
항상 적용되는 repo policy?      → AGENTS.md / higher instruction
한 번만 쓰는 간단한 지시?      → prompt
```

## Leading Words

| Term | Anchor |
|---|---|
| `red` | bug를 재현하는 failing test |
| `tight loop` | 짧고 반복 가능한 feedback |
| `tracer bullet` | narrow end-to-end vertical slice |
| `fog of war` | 현재 step에만 집중 |

효과가 trajectory에서 측정되지 않으면 제거한다.

## Failure → Fix

| Failure | Fix |
|---|---|
| Premature completion | checkable + exhaustive criterion |
| Duplication | Single Source of Truth |
| Sediment | version/relevance review 후 삭제 |
| Sprawl | branch resource로 disclose |
| No-op | behavioral delta가 없으면 삭제 |
| Negation | positive target과 검증 행동으로 rewrite |
| Negative Space | 중요한 omission만 branch/default로 명시 |
| Version mismatch | scope 명시 + client별 validation |

## Eval Matrix

| Case | 목적 |
|---|---|
| Clear positive | 기본 trigger |
| Paraphrased positive | vocabulary robustness |
| Near neighbor | false positive 방지 |
| Clear negative | non-trigger 확인 |
| Missing input | boundary behavior |
| Version mismatch | contextual compatibility |

```text
trigger precision = correct triggers / all triggers
trigger recall    = correct triggers / expected triggers
step coverage     = completed required steps / required steps
evidence coverage = evidenced findings / total findings
```

## Portability Check

- [ ] core frontmatter만으로 동작하는 variant가 있는가?
- [ ] `disable-model-invocation` 등 extension을 core field로 가정하지 않았는가?
- [ ] target client마다 parse/discovery/invocation을 검사했는가?
- [ ] tool syntax와 relative path가 target harness에서 작동하는가?
- [ ] Skill과 dependency/API version 범위가 맞는가?

## Final Review

- [ ] `SKILL.md`가 5,000 tokens / 500 lines 권장 범위인가?
- [ ] reference chain이 가능한 한 한 단계인가?
- [ ] pointer에 “언제 읽는지”가 있는가?
- [ ] 모든 step에 artifact와 exit criterion이 있는가?
- [ ] positive/negative/regression eval 근거가 있는가?
- [ ] 실패 증거 없이 instruction을 늘리지 않았는가?

## Sources

- [원본 SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- [GLOSSARY.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

