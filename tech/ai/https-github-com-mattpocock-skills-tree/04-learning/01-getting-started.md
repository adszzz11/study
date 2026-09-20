---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## 목표

작은 반복 workflow 하나를 골라 routing 가능한 `description`, 명시적인 steps, 검증 가능한 completion criteria를 가진 최소 Skill로 만든다.

## 1. Skill 후보 판정

다음 질문 중 여러 개에 `yes`라면 Skill 후보가 된다.

- [ ] 여러 session 또는 project에서 반복되는가?
- [ ] 한 줄 prompt보다 branch와 순서가 중요한가?
- [ ] domain vocabulary나 reference가 필요한가?
- [ ] agent가 자주 누락하거나 조기에 끝내는가?
- [ ] script만으로는 처리하기 어려운 판단이 있는가?

반대로 항상 적용되는 policy는 상위 instruction에, 완전히 deterministic한 작업은 script에 둔다.

## 2. Behavioral Contract 작성

먼저 문서가 아니라 관찰할 process를 쓴다.

```yaml
task: release-note-audit
trigger:
  - user asks to upgrade a dependency
  - user asks whether a version is compatible
process:
  - identify current and target versions
  - read primary release notes
  - classify breaking changes
  - map changes to repository usage
  - verify every risk has evidence
done_when:
  - all relevant version intervals are covered
  - every reported risk has a source and code location
```

이 contract가 eval의 expected trajectory가 된다.

## 3. 최소 Frontmatter

Portable variant는 core field부터 시작한다.

```yaml
---
name: release-note-audit
description: Audits release notes for breaking changes when users ask to upgrade, migrate, or verify version compatibility.
---
```

Description 검토:

- `Audits`라는 leading verb가 capability를 앞에서 고정한다.
- `when` 뒤에 실제 trigger vocabulary가 있다.
- 내부 file 구조나 구현 방식은 넣지 않았다.
- 서로 다른 intent인 upgrade, migrate, compatibility를 branch trigger로 제시한다.

## 4. Step과 Exit Criterion

```markdown
## Workflow

1. Resolve versions
   - Record the installed and target versions from repository evidence.
   - Continue only when both are known or the missing value is reported as a blocker.

2. Read release notes
   - Cover every release between the installed and target versions.
   - Use primary release notes; record URLs beside extracted changes.

3. Map impact
   - Search the repository for each changed API or behavior.
   - Continue only when every breaking change is marked affected or not affected with evidence.

4. Report
   - Include version range, findings, code locations, sources, and residual uncertainty.
```

“조사한다”보다 무엇을 대조하고 어떤 상태에서 다음 단계로 가는지를 쓴다.

## 5. Resource 분리

첫 버전은 작게 시작한다.

```text
release-note-audit/
├── SKILL.md
├── references/
│   └── provider-source-map.md
└── scripts/
    └── detect-installed-version.sh
```

| 내용 | 위치 |
|---|---|
| 모든 실행이 따라야 하는 steps | `SKILL.md` inline |
| provider별 release URL | 조건부 reference |
| 설치 version 검출 | deterministic script |
| 드문 legacy exception | 해당 branch용 reference |

Pointer는 load condition을 포함한다.

```markdown
When the dependency is maintained by a provider listed in
`references/provider-source-map.md`, read that file before web search.
```

## 6. 첫 Evaluation Set

최소 세 종류를 반복 실행한다.

| Case | Prompt | 기대 |
|---|---|---|
| Positive | “v2로 올릴 때 breaking change를 확인해줘” | Skill trigger, 전 step 실행 |
| Paraphrase | “이 dependency migration 위험은?” | 같은 Skill과 process |
| Negative | “이 함수 이름만 바꿔줘” | Skill이 trigger되지 않음 |
| Boundary | 현재 version이 없음 | 추측하지 않고 blocker/탐색 branch |

```yaml
metrics:
  trigger_precision: correct_triggers / all_triggers
  trigger_recall: correct_triggers / expected_triggers
  step_coverage: completed_required_steps / required_steps
  evidence_coverage: evidenced_findings / total_findings
```

한 번의 성공보다 prompt paraphrase와 반복 run에서 process가 유지되는지 본다.

## 7. 완료 체크

- [ ] capability와 trigger가 description에 모두 있는가?
- [ ] 각 step에 관찰 가능한 artifact가 있는가?
- [ ] 각 step에 exit criterion이 있는가?
- [ ] deterministic 부분을 script로 옮겼는가?
- [ ] conditional resource에 load condition이 있는가?
- [ ] positive, negative, boundary eval을 실행했는가?
- [ ] target client validator를 통과했는가?

## Sources

- [원본 SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

