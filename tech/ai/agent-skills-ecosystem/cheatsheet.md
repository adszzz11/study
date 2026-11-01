---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills Cheatsheet

## 빠른 판단

| 상황 | 선택 |
|---|---|
| 늘 적용되는 repository 규칙 | `AGENTS.md` / custom instructions |
| 조건부·반복 전문 workflow | Agent Skill |
| 외부 system 연결 | MCP |
| 한 번만 직접 실행할 문안 | Prompt template |

## 좋은 `description`

```yaml
# 나쁨: 너무 일반적
description: Use for release notes.

# 좋음: 시점·입력·결과가 선명함
description: Use when classifying merged pull requests and drafting customer-facing release notes for a release.
```

## Package checklist

- [ ] frontmatter `name`, `description`이 구체적인가
- [ ] `SKILL.md`에 순서, 입력/출력, failure behavior, quality bar가 있는가
- [ ] 긴 지식은 `references/`로, 결정적 검증은 `scripts/`로 분리했는가
- [ ] 실제 task set으로 trigger와 결과를 평가했는가
- [ ] third-party package의 scripts·network·credential 접근을 audit했는가

## 기술스택 요약

Agent Skills의 기본 단위는 YAML frontmatter를 가진 Markdown `SKILL.md`와 선택적 scripts/references/assets다. Claude Code는 filesystem discovery를 사용하며, API는 versioned Skill bundle과 code-execution container를 지원한다. OpenAI Codex/Agents API와 GitHub Copilot도 `SKILL.md` 중심의 on-demand capability 구조를 제공한다. 운영 핵심은 좋은 `description`, 작은 workflow 단위, evaluation, third-party Skill의 supply-chain 보안 검토다.

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/03-references|References]]
- [[tech/ai/agent-skills-ecosystem/04-learning/02-deep-dive|Deep Dive]]
- [[tech/ai/agent-skills-ecosystem/05-projects|Projects]]

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://developers.openai.com/api/docs/guides/tools-skills
- https://docs.github.com/en/copilot/concepts/customizations/agent-skills
