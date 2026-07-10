---
date: 2026-07-09
tags: [tech, ai, claude, fable, agentic-ai, alignment, tool-use]
status: published
type: tech-tool-study
---

# 01. Overview — What / Why / 핵심 특징

## 1. What

| 항목 | 내용 |
|------|------|
| 이름 | Claude Fable 5 |
| 제공사 | Anthropic |
| 모델 포지션 | 5세대 frontier model, hardest knowledge work and coding problems용 |
| 핵심 기조 | **long-horizon autonomous work** |
| 주요 실행 환경 | Claude, Claude Code, Claude Managed Agents, Claude API, AWS, Google Cloud, Microsoft Foundry |
| 사용 모델명 | `claude-fable-5` |

Claude Fable 5는 단발성 Q&A보다 **장시간 agentic coding**, migration, research, enterprise workflow처럼 여러 단계를 거치는 작업에 맞춰진 모델이다. Anthropic의 소개에 따르면 Fable 5는 Claude Code 같은 agent harness 안에서 며칠 단위 작업을 계획하고, sub-agent에 위임하고, 자체 검증까지 수행하는 방향으로 설계되어 있다.

## 2. Why

기존 LLM 사용은 대체로 “질문 → 답변” 구조였다. 하지만 실제 소프트웨어 작업은 다음 문제가 있다.

| 문제 | 왜 어려운가 | Fable식 접근 |
|------|-------------|--------------|
| 큰 코드베이스 | 필요한 파일과 규칙을 찾는 데 시간이 듦 | 먼저 탐색하고 context를 선별 |
| 장기 migration | 한 번에 끝나지 않고 중간 검증이 필요 | plan stage와 checkpoint |
| 복잡한 설계 | tradeoff와 hidden constraint가 많음 | architecture reasoning + review |
| 구현 품질 | 코드 생성만으로는 regression을 막기 어려움 | test 작성, 실행, 실패 시 반복 |
| enterprise workflow | 문서, 표, PDF, 내부 tool이 섞임 | vision, MCP, tool use |

즉 Fable 5의 핵심 가치는 “더 똑똑한 답변”보다 **긴 작업을 끝까지 끌고 가는 agentic reliability**다.

## 3. 핵심 특징

### Constitutional AI / RLAIF

Anthropic의 alignment 철학은 사람이 모든 harmful example을 직접 라벨링하는 방식만으로는 확장성이 낮다고 보고, 원칙 목록(constitution)을 바탕으로 self-critique, revision, preference model, RL from AI Feedback을 수행하는 구조다.

```text
draft answer
→ critique against principles
→ revise answer
→ AI preference data
→ preference model
→ reinforcement learning
```

이 구조는 Fable 5의 안전장치와도 연결된다. 능력이 커질수록 cyber/bio/chem misuse risk가 커지므로, 단순 거절이 아니라 위험 요청 분류, fallback, monitoring까지 붙는다.

### Agentic loop

Claude Code의 실전 루프는 다음처럼 정리할 수 있다.

```text
explore
→ plan
→ edit / tool use
→ run verification
→ iterate
→ summarize
```

Claude에게 “바로 구현해”라고 시키는 것보다, **검증 가능한 목표와 test command**를 함께 주고 “먼저 탐색한 뒤 계획하고 구현하라”고 지시하는 편이 품질이 높다.

### Tool use + MCP

MCP(Model Context Protocol)는 AI app과 외부 tool/data/workflow를 연결하는 open standard다. Claude Code에서는 file edit, shell, browser/search, GitHub, Slack, DB 같은 action surface를 tool로 붙여 agent가 실제 업무를 수행하게 만든다.

```text
LLM alone: prompt + answer
LLM with MCP: prompt + repo + ticket + DB + shell + editor + verification
```

### Long context + context management

Long context는 강점이지만 공짜 자원이 아니다. context window가 가득 차면 모델이 중요한 제약을 놓치거나 이전 결정을 흐릴 수 있다.

효율적인 운용 원칙:

- 전체 repo를 무작정 읽히지 않고 필요한 파일부터 탐색한다.
- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` 같은 memory files에 불변 규칙을 저장한다.
- 큰 작업은 checkpoint, summary, compaction을 사용한다.
- 완료 조건은 “설명”이 아니라 “검증 command PASS”로 둔다.

### Self-verification

Fable 5는 자체 검증을 강조한다.

| 검증 방식 | 예 |
|-----------|----|
| Unit/integration test | `npm test`, `pytest`, `go test ./...` |
| Static check | `typecheck`, `lint`, `cargo clippy` |
| UI/vision check | screenshot, design goal 비교 |
| Diff review | 의도와 무관한 변경, regression, security issue 탐지 |

### Safety classifier + fallback

Fable 5는 cyber/bio/chem 위험 도메인에서 더 강한 safeguard가 적용된다. Anthropic은 cyber classifier를 prohibited, high-risk dual use, low-risk dual use, benign 같은 범주로 나누어 block, monitor, allow를 결정한다고 설명한다. 위험 요청은 Opus 4.8로 자동 routing될 수 있고, API 사용자는 Fallback API 설정을 확인해야 한다.

## 4. 한 줄 요약

Claude Fable 5의 본질은 “더 긴 시간 동안, 더 많은 tool을 쓰고, 더 엄격히 검증하면서, 복잡한 coding/knowledge work를 완료하는 모델”이다.

## 관련 노트

- [[claude/03-claude-code]] · [[model-context-protocol-mcp/01-overview]] · [[lazy-codex/04-learning/02-verified-completion]] · [[agent-orchestration/cli-agents]]
