---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Stale Instruction Files와 Coding Agent의 Code-Precedence 문제

> **한 줄 정의**: `CLAUDE.md`·`AGENTS.md`처럼 지속적으로 주입되는 instruction file이 실제 code와 충돌할 때, coding agent가 낡은 문서를 우선해 잘못 구현하거나 기존 코드를 훼손하는 현상이다.

## Overview

Instruction file은 agent에게는 높은 authority의 지시지만 source code는 tool output으로 읽히는 관찰값이다. 이 비대칭 때문에 문서가 오래되면 agent는 충돌을 알아차려도 문서를 따를 수 있다. Xu·Wu의 40개 synthetic Python project 실험에서는 기본 조건의 선택 중 90.1%가 stale file을 따랐고, Codex CLI는 80회 중 20회 기존 코드를 문서에 맞춰 재작성했다.

핵심은 “문서를 더 많이 쓰기”가 아니라 code-precedence, 불일치 보고, 실행 가능한 검증을 함께 두는 것이다.

기술스택 요약:

- Core: `AGENTS.md` / `CLAUDE.md`, Codex CLI, Claude Code, GitHub Copilot.
- Validation: test, type check, linter, formatter, pre-commit hook, CI.
- Automation: GitHub Actions 기반 instruction drift audit 및 migration checklist.
- Security: protected branch, CODEOWNERS review, permission policy로 high-trust prompt surface를 보호.

## Learning Path

- [ ] [[tech/devtools/stale-agent-instructions/01-overview|Overview]] — 현상의 구조와 위험을 이해한다.
- [ ] [[tech/devtools/stale-agent-instructions/02-ecosystem|Ecosystem]] — Codex, Claude Code, Copilot의 instruction 범위를 비교한다.
- [ ] [[tech/devtools/stale-agent-instructions/04-learning/01-getting-started|시작하기]] — repository inventory와 첫 감사 규칙을 적용한다.
- [ ] [[tech/devtools/stale-agent-instructions/04-learning/02-deep-dive|Deep Dive]] — CI·security·평가 harness까지 확장한다.
- [ ] [[tech/devtools/stale-agent-instructions/05-projects|Projects]] — 팀에 적용할 자동화 아이디어를 고른다.
- [ ] [[tech/devtools/stale-agent-instructions/cheatsheet|Cheatsheet]] — session 전후 체크 항목을 빠르게 확인한다.
- [ ] [[tech/devtools/stale-agent-instructions/03-references|References]] — 원문과 공식 문서를 검증한다.

## When To Use

- framework migration, directory rename, API 교체 뒤 instruction file을 점검할 때
- Codex·Claude Code·Copilot을 repository에서 병행할 때
- agent가 “문서대로” 변경했지만 regression이 발생한 incident를 분석할 때
- 반복되는 convention을 test, lint, CI gate로 옮길 우선순위를 정할 때

## When Not To Use

- source code가 의도적으로 legacy 상태이고 migration spec이 최신 진실인 경우: code를 기계적으로 우선하지 말고 owner의 결정을 확인한다.
- 보안·권한·배포 절차처럼 code만으로 검증할 수 없는 정책: authority를 낮추기보다 승인 경로와 policy enforcement를 명시한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/codex/README|Codex]]

## Sources

- https://x.com/ai_database/status/2114184481951330365
- https://arxiv.org/abs/2610.30571
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts
