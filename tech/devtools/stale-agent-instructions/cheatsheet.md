---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## Session 전

- [ ] active path의 `AGENTS.md`·`AGENTS.override.md`·`CLAUDE.md`를 찾았다.
- [ ] instruction의 command와 path가 현재 repository에 존재한다.
- [ ] code와 문서의 conflict를 code-precedence rule로 처리할 준비가 됐다.

## Conflict 발생 시

1. code, test, lint, CI config를 확인한다.
2. code convention이 현재 의도인지 migration context와 owner signal로 검증한다.
3. 기존 code를 문서에 맞추어 재작성하지 않는다. 명시적 migration authority가 있을 때만 예외다.
4. 불일치와 선택 근거를 final report에 기록한다.

## Rule Placement

| 필요 | 위치 |
|---|---|
| 설명·맥락 | instruction file |
| 재현 가능한 correctness | test/type check/linter |
| format | formatter/pre-commit |
| 권한·배포 | policy/CI gate |

자세한 절차: [[tech/devtools/stale-agent-instructions/04-learning/01-getting-started|시작하기]] · [[tech/devtools/stale-agent-instructions/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://arxiv.org/abs/2610.30571
- https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts
