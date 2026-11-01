---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills References

## Primary source

1. [Instagram Reel — Kumail Pirzada](https://www.instagram.com/reel/Dd_wlJNqYVv/) — 2026년 9월 star 증가량을 기준으로 주목받은 Claude Skills 저장소들을 소개한 원본 Reel.

## Official documentation

2. [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — discovery와 progressive disclosure의 기본 개념.
3. [Anthropic: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — 설계와 실제 적용 배경.
4. [Anthropic Skills repository](https://github.com/anthropics/skills) — 공개 Skill 예시와 package 구조.
5. [Anthropic: Introducing Agent Skills](https://claude.com/resources/articles/skills) — 제품 관점 소개.
6. [OpenAI: Skills API guide](https://developers.openai.com/api/docs/guides/tools-skills) — Skills의 API/runtime 사용법.
7. [OpenAI: Skills로 OSS maintenance 가속](https://developers.openai.com/blog/skills-agents-sdk) — Agents SDK 사용 사례.
8. [GitHub: Agent Skills concepts](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) — Copilot의 Skill 개념.
9. [GitHub: Copilot에 Agent Skills 추가](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) — 설정과 배포 절차.
10. [Anthropic: Enterprise security guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) — third-party Skill 보안 검토 지침.

## 읽는 순서

1. Overview로 포맷과 lifecycle을 파악한다.
2. OpenAI/GitHub 문서로 실행 환경 차이를 비교한다.
3. 공개 repository를 읽되, 설치 전에 모든 script와 network 호출을 audit한다.

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/02-ecosystem|Ecosystem]]
- [[tech/ai/agent-skills-ecosystem/cheatsheet|Cheatsheet]]

## Sources

- https://www.instagram.com/reel/Dd_wlJNqYVv/
- https://github.com/anthropics/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise
