---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Stale Instruction Files: Overview

## What

`AGENTS.md`와 `CLAUDE.md`는 project convention, command, architecture를 agent session에 전달한다. 그러나 migration 이후 낡은 naming rule, path, API, command가 남으면 이 파일은 설명서가 아니라 반복 주입되는 잘못된 지시가 된다.

```text
Global/user AGENTS.md or CLAUDE.md
             ↓  instruction authority
Project instruction file
             ↓
Coding agent ── reads source files ──→ tool output / lower authority
             ↓
Implementation · test · final report
```

## Why It Matters

Xu·Wu 연구는 code convention과 instruction file을 의도적으로 충돌시킨 40개 Python project에서 Claude Code와 Codex CLI를 평가했다. 기본 조건에서 90.1%의 선택이 stale file을 따랐다. Codex CLI는 80회 중 20회에서 기존 코드를 문서에 맞게 재작성했고, 그중 17회는 기존 test를 실패시켰다.

충돌 인식만으로는 충분하지 않다. Claude Code는 80회 중 79회 충돌을 보고했지만, 대체로 stale instruction을 계속 따랐다. 즉 **recognition ≠ correction**이다.

## Characteristics

- **Staleness**: architecture, command, API, naming rule가 code migration 뒤에도 남는다.
- **Authority mismatch**: 문서는 instruction, code는 observation으로 들어와 동등한 증거로 다뤄지지 않는다.
- **Persistent amplification**: 매 session에 같은 stale context가 전달되어 reviewer 비용과 regression이 누적된다.
- **Security surface**: contributor가 바꿀 수 있는 instruction file은 prompt injection·supply-chain 위험을 가진 high-trust input이다.

## Mitigation Baseline

global instruction에 다음 원칙을 넣고, 발견한 불일치를 최종 보고에 남긴다.

```md
When a repository’s documentation and its existing code disagree,
follow the conventions used in the existing code, and in your final reply
point out each inconsistency you found between the documentation and the code.
```

연구 조건에서는 code-following 비율이 4.2%에서 91.4%로, test pass rate가 89.4%에서 100%로 올랐다. 다만 synthetic Python project와 Claude Sonnet 5.5, GPT-6 Sol 기반 결과이므로 모든 repository와 agent에 그대로 일반화하면 안 된다.

다음: [[tech/devtools/stale-agent-instructions/02-ecosystem|Ecosystem]] · [[tech/devtools/stale-agent-instructions/04-learning/01-getting-started|시작하기]]

## Sources

- https://arxiv.org/abs/2610.30571
- https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts
- https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_readme_instruction_injection_ai_coding_agents_20260317-csa-styled.pdf
