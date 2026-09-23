---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — tool-study

> **한 줄 정의**: ECC(affaan-m/ECC)는 Claude Code·Codex 같은 AI coding agent에 재사용 가능한 skills, rules, hooks, memory, security scan을 제공하는 오픈소스 cross-harness operating layer다.

## Overview

ECC는 LLM 자체가 아니라, agent가 반복 가능한 engineering workflow로 일하도록 만드는 **harness**다. `plan → test → implement → review → verify → remember → improve` 흐름을 rules·skills·agents·hooks로 조립해 세션마다 절차를 다시 설명하거나 harness마다 설정을 중복 관리하는 비용을 줄인다.

- 핵심: 필요한 rule pack과 skill만 선택하는 portable workflow layer
- 대상: Claude Code가 가장 성숙하며, Codex를 포함한 여러 harness는 adapter별 지원 범위가 다르다.
- 주의: 현재 공개 안정 release는 dossier 기준 `v2.2.1`(2026-09-08)이다. main의 `2.2.2` 변경은 배포됐다고 가정하지 말고 GitHub Releases와 npm registry를 함께 확인한다.

## Learning Path

- [ ] [[01-overview|What / Why / 핵심 특징]] — harness가 해결하는 문제와 구성요소를 이해한다.
- [ ] [[02-ecosystem|Ecosystem]] — native rules, Cursor, OpenCode, 직접 구성과 비교한다.
- [ ] [[03-references|References]] — 공식 문서와 release 상태를 확인한다.
- [ ] [[04-learning/01-getting-started|Getting started]] — Codex에 최소 profile을 dry-run으로 계획한다.
- [ ] [[04-learning/02-deep-dive|Deep dive]] — adapters, hooks, memory, AgentShield 경계를 파고든다.
- [ ] [[05-projects|Projects]] — 팀 도입·modernization·security gate를 설계한다.
- [ ] [[cheatsheet|Cheatsheet]] — 설치 전 확인과 핵심 명령을 빠르게 찾는다.

## When To Use

- Claude Code와 Codex 등 둘 이상의 harness에서 공통 TDD·review·security workflow가 필요할 때
- rule/skill/hook의 설치 상태와 upgrade·uninstall 경로를 일관되게 관리해야 할 때
- agent 설정의 permission, hook, MCP, secret을 AgentShield로 점검하고 CI gate를 만들 때
- 작은 PoC에서 handoff·memory가 실제 재작업을 줄이는지 측정하려 할 때

## When Not To Use

- 단일 harness의 소수 프로젝트 규칙만 필요하고 native plugin/rules로 충분할 때
- hooks나 persistent memory가 조직의 보안·privacy 정책과 맞지 않을 때
- scanner 결과만으로 안전을 보증하거나 사람이 권한 변경을 검토하지 않을 운영일 때
- 설치 경로(plugin, guided installer, manual copy)를 중첩해야 하는 상황일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://github.com/affaan-m/ECC
- https://github.com/affaan-m/ECC/releases
- https://www.npmjs.com/package/ecc-universal
- https://ecc.tools/
