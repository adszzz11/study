---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — References

## 1차 출처: project contract

| 자료 | 확인할 내용 |
|---|---|
| [9thLevelSoftware/Clodex repository](https://github.com/9thLevelSoftware/Clodex) | 프로젝트 정체, native collaboration 범위, source tree |
| [README](https://github.com/9thLevelSoftware/Clodex/blob/main/README.md) | install, commands, requirements, artifacts, safety defaults |
| [CLODEX.md](https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md) | default workflow policy, reviewer personas, `max_fix_loops` |
| [installer](https://github.com/9thLevelSoftware/Clodex/blob/main/install.sh) | Python/Git/Claude/Codex 사전 요구사항과 설치 경로 |

## 기반 CLI와 protocol

- [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage) — Plan mode와 CLI usage를 확인한다.
- [Anthropic MCP documentation](https://docs.anthropic.com/en/docs/mcp) — MCP 연결과 tool handoff의 개념적 기반을 읽는다.
- [OpenAI: consistent workflows with Codex CLI and Agents SDK](https://developers.openai.com/cookbook/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk) — Codex workflow/MCP 설계 사례를 비교한다.
- [OpenAI Codex config reference](https://developers.openai.com/docs/config-file/config-reference) — sandbox mode와 config의 의미를 확인한다.
- [OpenAI: Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) — 지속 목표 기반 Codex workflow와 비교한다.

## 읽는 순서와 검증 메모

1. README로 artifact, command, source checkout 격리의 범위를 읽는다.
2. `CLODEX.md`에서 현재 repository가 선언한 model·sandbox·worktree·reviewer policy를 확인한다.
3. 목표 repository에서 `doctor`, `init --dry-run`, `build --dry-run`으로 설치 전 side effect를 확인한다.
4. CLI 제품 문서에서 현재 사용 중인 model, sandbox, MCP 지원을 별도로 확인한다.

> Project contract의 model string은 해당 Clodex repository의 설정값이다. 현재 Claude Code/Codex CLI에서의 가용성과 entitlement는 설치 시점의 공식 제품 문서와 `doctor` 결과로 다시 확인한다.
