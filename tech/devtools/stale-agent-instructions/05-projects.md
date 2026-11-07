---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## Instruction Drift Auditor

`AGENTS.md`·`CLAUDE.md`에서 file path, script, package, API reference를 추출해 repository, `package.json`, CI config와 대조한다. stale reference를 담은 PR 초안을 생성하되, 삭제는 human review 뒤 수행한다.

## Agent Context CI Gate

instruction file 변경 시 sibling file과의 conflict, non-existent command, 200-line 초과, duplicate lint rule을 검사한다. hard failure는 명백한 broken reference에 한정하고, semantic conflict는 review evidence로 남긴다.

## Code-vs-Docs Eval Harness

주요 convention 10개를 fixture로 만들고 agent별 code-following rate, report quality, test pass rate, harmful rewrite rate를 release마다 비교한다.

## Migration Checklist Bot

framework upgrade 또는 directory rename PR이 merge될 때 관련 instruction file, skill, runbook 갱신 여부를 checklist로 요구한다.

시작 전 [[tech/devtools/stale-agent-instructions/04-learning/01-getting-started|시작하기]]를 완료하고, 운영 기준은 [[tech/devtools/stale-agent-instructions/04-learning/02-deep-dive|Deep Dive]]를 따른다.

## Sources

- https://github.com/WenJing95/stale-docs-data
- https://arxiv.org/abs/2606.15828
