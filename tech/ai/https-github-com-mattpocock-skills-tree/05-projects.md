---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## 1. Existing Skill Audit

실제 `SKILL.md` 하나를 failure taxonomy로 audit한다.

| 단계 | 산출물 | 완료 조건 |
|---|---|---|
| Inventory | description, steps, references, scripts 목록 | 모든 file이 분류됨 |
| Failure scan | duplication/sediment/sprawl/no-op/negation 표 | 각 의심 문장에 근거가 있음 |
| Rewrite | 최소 diff | behavioral contract가 유지됨 |
| Regression | positive/negative/boundary cases | routing과 step coverage가 악화되지 않음 |

```markdown
| Location | Failure | Evidence | Action |
|---|---|---|---|
| description:1 | synonym duplication | same branch repeated 4x | collapse |
| step 3 | weak criterion | exits without diff check | sharpen |
```

## 2. Description Routing Lab

Skill 세 개의 description이 겹치는 작은 testbed를 만든다.

```yaml
skills:
  - dependency-upgrade
  - release-note-summary
  - compatibility-audit
cases:
  - prompt: "v3로 올려도 깨지지 않을까?"
    expected: compatibility-audit
  - prompt: "v3 변경 사항만 요약해줘"
    expected: release-note-summary
```

측정값은 trigger precision/recall, wrong-skill rate, non-trigger accuracy다. 실패 prompt의 실제 vocabulary로만 description을 수정한다.

## 3. Progressive Disclosure Refactor

비대한 Skill 하나를 common path와 branch resource로 분리한다.

| Before | After |
|---|---|
| 모든 framework 지침이 `SKILL.md`에 inline | common workflow만 inline |
| reference가 다시 다른 reference를 링크 | `SKILL.md`에서 직접 한 단계 link |
| “자세한 내용 참고” pointer | framework branch와 load timing 명시 |
| prose로 version 검출 | script가 version과 exit code 반환 |

성공 기준:

- `SKILL.md`가 5,000 tokens와 500 lines 이내다.
- common case에서 불필요한 reference를 load하지 않는다.
- rare branch의 pass rate가 떨어지지 않는다.
- total context cost와 step coverage를 전후 비교한다.

## 4. Skill Linter

정적 검사 가능한 규칙을 CLI로 구현한다.

```text
skill-lint path/to/skill
├─ frontmatter schema
├─ name and description limits
├─ line/token budget warning
├─ broken relative links
├─ reference depth
├─ duplicate paragraph candidates
└─ client-extension warning
```

`no-op`, negative space, completion criterion quality는 완전 자동 판정하기 어렵다. linter는 후보를 표시하고 사람이 behavioral evidence로 결정하게 한다.

## 5. Skill Evaluation Harness

동일 task를 반복해 output보다 process를 평가한다.

```yaml
suite: migration-audit
runs_per_case: 10
perturbations:
  - paraphrase
  - missing_version
  - stale_reference
  - version_mismatch
metrics:
  - trigger_precision
  - trigger_recall
  - required_step_coverage
  - premature_completion_rate
  - context_tokens
  - task_pass_rate
```

각 run에서 selected Skill, loaded resources, completed steps, criterion evidence, final outcome을 trace한다.

## 6. Cross-Agent Compatibility Pack

portable core와 client adapter를 분리하고 CI validation matrix를 만든다.

```text
skill-pack/
├── portable/SKILL.md
├── adapters/client-a/SKILL.md
├── agents/openai.yaml
└── tests/
    ├── routing.yaml
    └── validation-matrix.yaml
```

| Gate | 확인 |
|---|---|
| Parse | 각 client가 frontmatter를 수용 |
| Discover | expected prompt에서 후보로 노출 |
| Invoke | user/model invocation policy가 의도와 일치 |
| Execute | tools와 relative reference가 작동 |
| Regress | portable variant의 process coverage 유지 |

## 추천 순서

1. Existing Skill Audit로 failure vocabulary를 익힌다.
2. Description Routing Lab으로 discovery를 수치화한다.
3. Progressive Disclosure Refactor로 context 구조를 바꾼다.
4. Skill Linter로 정적 규칙을 자동화한다.
5. Evaluation Harness와 Compatibility Pack으로 운영 수준까지 확장한다.

## Sources

- [원본 SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)
- [호환성 issue #360](https://github.com/mattpocock/skills/issues/360)

