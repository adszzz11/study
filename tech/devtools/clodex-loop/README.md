---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — tool-study

> **한 줄 정의**: Clodex loop는 Claude Code가 계획하고 Codex CLI가 격리된 worktree에서 구현한 뒤, 두 agent가 같은 최종 diff hash를 독립 audit하여 만장일치 승인될 때까지 제한적으로 수정·재감사하는 local-first dual-agent workflow다.

## Overview

여기서 다루는 Clodex는 **[9thLevelSoftware/Clodex](https://github.com/9thLevelSoftware/Clodex)** 다. 동명 프로젝트와 혼동하지 않는다. 핵심은 agent 수를 늘리는 일이 아니라 `plan → isolated build → dual audit → bounded fix loop → manual apply`라는 상태 전이를 artifact와 정책으로 남기는 데 있다.

- Claude Code: brainstorm, product/design, structured implementation plan
- Codex CLI: accepted plan 구현, test·변경·미해결 사항 기록
- 두 agent: **같은 최종 diff hash**를 audit하고 explicit approval이 모두 있어야 완료
- 운영자: 승인된 patch도 `clodex apply <run-id>` 전 사람이 확인

## Learning Path

- [ ] [[01-overview|What / Why / 핵심 특징]] — dual-agent loop의 문제 정의와 state machine을 이해한다.
- [ ] [[02-ecosystem|Ecosystem]] — 동명 도구와 단일-agent·CI baseline을 비교한다.
- [ ] [[03-references|References]] — 공식 contract, 설치 요구사항, CLI 문서를 확인한다.
- [ ] [[04-learning/01-getting-started|Getting started]] — non-production repository에서 dry-run을 실행한다.
- [ ] [[04-learning/02-deep-dive|Deep dive]] — artifacts, MCP handoff, audit policy, failure 경계를 살핀다.
- [ ] [[05-projects|Projects]] — backend, refactor, CI, PR remediation에 적용한다.
- [ ] [[cheatsheet|Cheatsheet]] — 명령과 apply 전 확인표를 빠르게 참조한다.

## When To Use

- 계획·구현·review를 의도적으로 분리하고 audit trail을 남겨야 하는 중간~고위험 변경
- source checkout 오염 없이 agent patch를 검토해야 하는 repository
- handoff 품질, test evidence, 종료 조건을 재현 가능하게 운영하려는 팀
- CI artifact와 사람의 PR/apply 승인을 별도 gate로 유지하려는 workflow

## When Not To Use

- 즉시 수정할 수 있는 작은 변경에 plan·dual audit 비용이 더 클 때
- Claude Code와 Codex CLI, Git worktree, Python 요구사항을 안전하게 운영할 수 없을 때
- test/lint/SAST 같은 결정론적 품질 gate 없이 agent 합의만으로 배포하려 할 때
- automatic apply 또는 무제한 self-fix가 필요한 것으로 오해할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/codex/README|Codex]]

## Sources

- https://github.com/9thLevelSoftware/Clodex
- https://github.com/9thLevelSoftware/Clodex/blob/main/README.md
- https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md
- https://developers.openai.com/docs/config-file/config-reference
- https://docs.anthropic.com/en/docs/claude-code/cli-usage
