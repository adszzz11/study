---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Primary Sources

| 자료 | 역할 | 읽을 포인트 |
|---|---|---|
| [원본 SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md) | 실제 meta-skill | determinism, leading word, criteria, pruning |
| [GLOSSARY.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md) | disclosed reference | context pointer, negative space 등 용어 |
| [공식 설명 페이지](https://www.aihero.dev/skills-writing-great-skills) | 저자 해설 | output equality와 process predictability 구분 |
| [GitHub releases](https://github.com/mattpocock/skills/releases) | version history | v1.1의 Negation, Negative Space 변경 |

## Specifications And Guides

| 자료 | 확인할 규칙 |
|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | required frontmatter, naming, 5,000-token/500-line 권장, reference 구조 |
| [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Skill packaging과 progressive disclosure |
| [Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | concise description, trigger keywords, evaluation |

## Evidence And Compatibility

| 자료 | 시사점 |
|---|---|
| [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) | Skill의 평균 효과는 작고 specialization과 compatibility가 중요 |
| [mattpocock/skills issue #360](https://github.com/mattpocock/skills/issues/360) | `disable-model-invocation` 같은 extension의 cross-client validation 필요 |

## Source Reading Order

1. `SKILL.md`에서 workflow와 diagnostic vocabulary를 표시한다.
2. `GLOSSARY.md`에서 inline/reference/disclosed hierarchy를 정리한다.
3. core specification에서 portable minimum을 확인한다.
4. Anthropic guide에서 discovery와 description 규칙을 비교한다.
5. release와 issue를 읽어 version/client 차이를 기록한다.
6. benchmark를 읽고 “Skill이 있으면 좋아진다”는 가정을 검증한다.

## Evidence Note Template

```markdown
## Claim
- 주장:
- 적용 범위:

## Evidence
- source URL:
- version/date:
- observed behavior:

## Decision
- keep / revise / remove:
- evaluation case:
- compatibility risk:
```

## 출처 평가 체크리스트

- [ ] 원본 repository 또는 공식 specification인가?
- [ ] 문서 날짜와 Skill version을 기록했는가?
- [ ] core rule과 client extension을 구분했는가?
- [ ] 저자의 원칙과 benchmark의 empirical result를 구분했는가?
- [ ] 사례 한 번을 일반 법칙으로 확대하지 않았는가?

## Sources

- https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md
- https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md
- https://www.aihero.dev/skills-writing-great-skills
- https://agentskills.io/specification
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- https://arxiv.org/abs/2603.15401
- https://github.com/mattpocock/skills/issues/360
- https://github.com/mattpocock/skills/releases

