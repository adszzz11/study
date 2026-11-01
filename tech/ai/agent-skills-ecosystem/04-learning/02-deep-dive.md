---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills Deep Dive: 설계·평가·보안

## Information architecture

`SKILL.md`에는 짧고 행동 가능한 절차만 둔다. 길고 자주 필요하지 않은 도메인 지식은 `references/`, 반복 계산과 검증은 `scripts/`, 재사용 산출물은 `assets/`로 옮긴다.

```text
metadata → routing
SKILL.md → execution plan
references/ → conditional knowledge
scripts/ → deterministic checks
assets/ → reusable output material
```

## Composition과 baseline

한 task에서 `architecture-review`, `implementation`, `testing`, `security-audit` 같은 Skill을 조합할 수 있다. 그러나 credential policy, build command, formatting 같은 항상 적용되는 repo 규칙은 Skill이 아니라 `AGENTS.md`에 유지한다.

## Evaluation loop

| 측정 대상 | 확인 질문 |
|---|---|
| Trigger precision | 필요한 때 호출되고 불필요한 때는 호출되지 않는가? |
| Outcome quality | 산출물이 acceptance criteria를 충족하는가? |
| Cost/context | 불필요한 reference를 읽지 않는가? |
| Recovery | 입력이 부족하거나 script가 실패할 때 안전하게 멈추는가? |

실제 task set을 만들고 Skill 사용/미사용을 비교한다. 실패한 사례는 description, 순서, quality gate 중 어디가 원인인지 분류해 수정한다.

## Supply-chain security

외부 Skill은 문서가 아니라 agent가 읽고 실행할 수 있는 software package다. 설치 전 다음을 검사한다.

- `SKILL.md`뿐 아니라 모든 script, nested reference, asset을 읽는다.
- network 호출, encoded payload, download-and-execute, credential 접근 지시를 찾는다.
- 최소 권한 sandbox에서 실행하고, secret을 주입하지 않은 상태로 동작을 관찰한다.
- pinning, source provenance, 변경 검토 절차를 적용한다.

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/02-ecosystem|Ecosystem]]
- [[tech/ai/agent-skills-ecosystem/04-learning/01-getting-started|시작하기]]
- [[tech/ai/agent-skills-ecosystem/cheatsheet|Cheatsheet]]

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://docs.github.com/en/copilot/concepts/customizations/agent-skills
