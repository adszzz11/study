---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## 목표

Skill을 문서가 아니라 **routing + execution + context + evaluation system**으로 분석하고, 실패 증거를 바탕으로 최소 수정한다.

## 1. Routing Eval

Description은 precision과 recall의 trade-off를 가진 classifier interface다.

| Dataset | 예시 | 기대 |
|---|---|---|
| Clear positive | “PR의 migration risk를 audit해줘” | trigger |
| Paraphrased positive | “upgrade 전에 깨질 API를 찾아줘” | trigger |
| Near neighbor | “release notes를 요약해줘” | scope에 따라 non-trigger |
| Clear negative | “변수명을 변경해줘” | non-trigger |
| Adversarial overlap | “audit이라는 단어를 문서에서 찾아줘” | non-trigger |

```text
precision = true_positive / all_triggered
recall    = true_positive / all_should_trigger
```

False negative가 많으면 실제 사용자 vocabulary를 trigger로 보강한다. False positive가 많으면 capability boundary를 좁힌다. 동의어를 무작정 늘리면 metadata context만 커지고 branch 구분은 좋아지지 않을 수 있다.

## 2. Completion Criterion의 두 축

| 축 | 질문 | 실패 시 수정 |
|---|---|---|
| Clarity | agent가 완료 여부를 binary하게 판정할 수 있는가? | artifact, count, comparison 명시 |
| Demand | 필요한 legwork 전체를 요구하는가? | exhaustive scope와 evidence gate 추가 |

```markdown
Weak: Review all affected files.

Clear: Compare the changed API list against repository search results.

Clear + demanding: Continue only after every changed API is marked
affected or not affected, with at least one code or configuration location
supporting the classification.
```

Agent가 rush할 때 바로 subagent나 더 긴 설명을 추가하지 않는다. 먼저 exit condition이 실제로 checkable하고 exhaustive한지 본다.

## 3. Progressive Disclosure Audit

각 문장을 branch frequency와 action dependency로 분류한다.

| 질문 | Yes | No |
|---|---|---|
| 모든 branch가 즉시 필요로 하는가? | inline | 다음 질문 |
| 특정 branch에서 반드시 읽어야 하는가? | linked reference + load condition | 삭제 후보 |
| 반복 가능한 deterministic operation인가? | script | prose 유지 여부 검토 |
| 다른 reference를 다시 따라가야 하는가? | chain flatten | 유지 |

```text
SKILL.md
  ├─ common workflow
  ├─ completion gates
  ├─ pointer → references/framework-a.md
  └─ pointer → scripts/validate.sh
```

Reference target만 적지 말고, pointer 문장에 branch condition과 읽는 시점을 넣는다. Reference chain은 가능한 한 한 단계로 유지한다.

## 4. Leading Word Experiment

Leading word의 효과는 A/B run으로 확인한다.

```yaml
variants:
  A: "Review the implementation carefully."
  B: "Use a tight loop: reproduce, patch, rerun the smallest test."
runs_per_case: 10
observe:
  - reproduction_before_edit_rate
  - smallest_test_rerun_rate
  - premature_completion_rate
```

`tight loop`가 실제 trajectory를 바꾸지 않으면 멋진 표현이어도 제거한다. Behavioral delta가 있는 단어만 남긴다.

## 5. Pruning Pass

문장마다 다음 decision tree를 적용한다.

```text
이 문장이 behavior를 바꾸는가?
├─ No  → delete
└─ Yes
   ├─ 다른 곳과 중복? → Single Source of Truth만 유지
   ├─ 일부 branch만 필요? → disclose
   ├─ stale/version-bound? → update or remove
   └─ 금지문? → positive target으로 rewrite
```

| 원문 | 문제 | Rewrite |
|---|---|---|
| “Do not skip tests.” | Negation이 `skip`을 활성화 | “Run the named verification command and record its exit status.” |
| “Be thorough.” | No-op 가능성 | “Map every diff entry to one verification result.” |
| description과 body에 같은 trigger 반복 | Duplication | description만 routing source로 유지 |
| 과거 client field를 계속 보존 | Sediment | target matrix에서 미지원이면 adapter로 이동 |

## 6. Negative Space Review

Negative space는 명시하지 않아 model prior가 선택하는 영역이다. 모든 세부사항을 지시하라는 뜻은 아니다. 결과를 크게 바꾸는 omission만 찾는다.

- source priority를 안 쓰면 blog와 official docs 중 무엇을 고르는가?
- missing input에서 추측할지 질문할지 정했는가?
- destructive action 전 approval boundary가 있는가?
- 여러 valid branch 중 선택 criterion이 있는가?
- completion report에 uncertainty를 남기는가?

중요하지 않은 choice는 agent에게 남겨 flexibility를 유지한다.

## 7. Version And Client Matrix

```yaml
targets:
  core-agent-skills:
    frontmatter: [name, description]
    validate: true
  client_a:
    extensions: [disable-model-invocation]
    validate: true
  client_b:
    extensions: []
    portable_variant: true
```

Skill 변경 때마다 client별 parse, discovery, activation, tool execution을 따로 확인한다. Version mismatch가 성능을 낮출 수 있으므로 dependency/API 범위를 description이나 reference에 명확히 둔다.

## 8. Evaluation Loop

```text
collect failures
  → classify: routing / execution / context / compatibility
  → smallest instruction change
  → positive + negative + regression runs
  → compare trajectory metrics
  → keep or revert
```

| Metric | 의미 |
|---|---|
| Trigger precision/recall | 올바른 Skill selection |
| Required-step coverage | process adherence |
| Criterion violation rate | premature completion |
| Resource-load accuracy | 필요한 reference만 읽는가 |
| Token/context cost | disclosure 효과 |
| Task pass rate | 최종 outcome |
| Cross-client validation | portability |

## Sources

- [원본 SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- [GLOSSARY.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md)
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)
- [호환성 issue #360](https://github.com/mattpocock/skills/issues/360)
- [v1.1 releases](https://github.com/mattpocock/skills/releases)

