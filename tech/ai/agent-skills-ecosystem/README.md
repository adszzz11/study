---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills: AI coding agent를 위한 재사용 가능한 작업 역량 패키지

> **한 줄 정의**: Agent Skills는 `SKILL.md`를 중심으로 instructions·scripts·references·assets를 폴더 단위로 묶어, AI agent가 필요한 시점에 선택·로딩하는 재사용 가능한 전문 작업 역량이다.

## Overview

Agent Skills는 모델에 긴 prompt를 매번 주입하는 대신, 반복되는 전문 workflow를 발견 가능한 패키지로 분리한다. 2026년 9월 GitHub star 증가량으로 주목받은 Claude Skills 저장소들(Ponytail, Superpowers, Graphify, Impeccable 등)은 이 생태계가 단일 제품 기능이 아니라 재사용 가능한 업무 방식의 유통 계층으로 성장하고 있음을 보여 준다.

기본 원리는 **progressive disclosure**다. agent는 먼저 `name`과 `description`만 보고 적합한 Skill을 고른 뒤, 선택했을 때만 `SKILL.md`와 필요한 resources를 읽는다. 따라서 context bloat를 줄이면서 code review, incident response, release, architecture, security audit 같은 작업을 검증 가능한 단위로 재사용할 수 있다.

## Learning Path

- [ ] [[tech/ai/agent-skills-ecosystem/01-overview|Overview]] — What, Why, 핵심 특징
- [ ] [[tech/ai/agent-skills-ecosystem/02-ecosystem|Ecosystem]] — 대안과 플랫폼 비교
- [ ] [[tech/ai/agent-skills-ecosystem/04-learning/01-getting-started|시작하기]] — 첫 Skill 만들기
- [ ] [[tech/ai/agent-skills-ecosystem/04-learning/02-deep-dive|Deep Dive]] — 설계·평가·보안 심화
- [ ] [[tech/ai/agent-skills-ecosystem/05-projects|Projects]] — 실전 적용 과제
- [ ] [[tech/ai/agent-skills-ecosystem/cheatsheet|Cheatsheet]] — 빠른 참조
- [ ] [[tech/ai/agent-skills-ecosystem/03-references|References]] — 공식 문서와 출처

## When To Use

- 조건부로 호출되는 반복 전문 workflow가 있고, 입력·출력·품질 기준을 명확히 정의할 수 있을 때
- instructions뿐 아니라 validation script, template, reference 문서를 version control 해야 할 때
- 여러 repository 또는 팀에 같은 작업 방식을 이식하고 평가하려 할 때

## When Not To Use

- 모든 task에 늘 적용해야 하는 짧은 repo 규칙이라면 `AGENTS.md` 또는 custom instructions가 더 알맞다.
- 한 번뿐인 단순 요청은 prompt template이 더 빠를 수 있다.
- Slack, database, GitHub 같은 live data/tool 연결 자체가 목표라면 MCP를 먼저 검토한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://www.instagram.com/reel/Dd_wlJNqYVv/
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://developers.openai.com/api/docs/guides/tools-skills
- https://docs.github.com/en/copilot/concepts/customizations/agent-skills
