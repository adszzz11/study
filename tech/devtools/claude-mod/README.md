---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Mod

> **한 줄 정의**: Claude Mod는 Claude Code plugin 안의 TypeScript/JavaScript function hooks로 event pipeline과 UI를 middleware처럼 관찰·변경·대체하는 runtime extension이다.

## Overview

Claude Mod는 Claude Code에 “무엇을 할지” 지시하는 기능을 넘어, prompt·tool call·permission·UI가 흐르는 순간의 동작을 programmatically 다룬다. Hook은 `($, e, next)` 형태로 event를 받고, 관찰한 뒤 다음 단계로 넘기거나(`next(e)`), event를 바꾸거나, 응답을 직접 반환해 처리를 끝낼 수 있다.

- Plugin 내부의 hooks module로 배포한다.
- TypeScript/JavaScript, Plugin manifest, function-hooks API로 구성한다.
- tool call 보호, secret redaction, context usage panel, 맞춤 `/diff` 같은 용도에 적합하다.
- Mod code는 신뢰 경계가 아니다. Claude Code 권한으로 민감한 동작에 관여할 수 있으므로 source와 dependency를 code review한다.

| 노트 | 초점 |
| --- | --- |
| [[01-overview]] | 개념, 동작 모델, 보안 경계 |
| [[02-ecosystem]] | Hooks·Skills·MCP·Plugin·`CLAUDE.md` 비교 |
| [[03-references]] | 공식 문서와 source code |
| [[04-learning/01-getting-started]] | read-only Token Weather 실습 |
| [[04-learning/02-deep-dive]] | middleware, 상태, ordering, 검증 |
| [[05-projects]] | 적용 아이디어와 설계 기준 |
| [[cheatsheet]] | 구조와 명령 빠른 참조 |

## Learning Path

- [ ] [[01-overview|문제와 핵심 모델]]을 읽고 Mod가 필요한 경계를 정한다.
- [ ] Claude Code의 built-in `/diff`를 관찰하고 plugin 구조를 훑는다.
- [ ] [[04-learning/01-getting-started|read-only context panel]]을 만들어 event와 UI를 연결한다.
- [ ] [[02-ecosystem|기능 선택 기준]]으로 Mod 대신 Hook·Skill·MCP가 맞는지 검토한다.
- [ ] [[04-learning/02-deep-dive|middleware와 state]]를 익히고 observe-only audit를 운영한다.
- [ ] `claude plugin validate`와 `claude plugin test`를 CI에 넣고 ordering·secret leakage를 review한다.

## When To Use

- event 입력 또는 결과를 deterministic하게 관찰·rewrite·block해야 할 때
- tool call 직전에 policy gate 또는 approval UI가 필요할 때
- model context에 들어가기 전 secret/PII를 redaction해야 할 때
- terminal/Desktop에 session 상태를 표시하는 custom UI가 필요할 때
- session 동안 state를 유지하며 Claude Code 동작을 확장해야 할 때

## When Not To Use

- 단순한 지식, 반복 workflow, prompt guidance만 필요할 때: Skill 또는 `CLAUDE.md`
- 외부 system의 tool/data 연결이 목적일 때: MCP
- shell/HTTP 기반 lifecycle 자동화만으로 충분할 때: Classic Hook
- 반드시 안전하게 격리돼야 하는 untrusted code를 실행하려 할 때: Mod는 sandbox 대체재가 아니다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://claude.com/blog/claude-code-mods
- https://github.com/anthropics/claude-code/blob/main/mods/README.md
- https://claude.dev/blog/getting-started-with-claude-code-mods/
- https://code.claude.com/docs/en/features-overview
