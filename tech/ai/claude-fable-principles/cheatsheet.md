---
date: 2026-07-09
tags: [tech, ai, claude, fable, cheatsheet, codex, gemini]
status: published
type: tech-tool-study
---

# cheatsheet — Claude Fable 5 빠른 참조

## 모델 선택

| 상황 | 선택 |
|------|------|
| 가장 어려운 설계·migration | Claude Fable 5 |
| 일반 coding / test 작성 | Claude Sonnet 5 또는 Codex |
| 좁은 구현 task 병렬 처리 | Codex |
| 긴 문서·검색·멀티모달 조사 | Gemini |
| 최종 검토 | 작업하지 않은 다른 모델 |

## Claude Code 기본 프롬프트

```text
먼저 관련 파일과 기존 패턴을 탐색해.
그다음 plan을 작성하고 구현해.
구현 후 test/typecheck/lint를 실행해.
실패하면 원인을 분석하고 반복해.
완료 답변에는 변경 파일, 검증 결과, 남은 risk만 요약해.
```

## `CLAUDE.md` 필수 항목

```md
## Build / Test
- Test: `...`
- Typecheck: `...`
- Lint: `...`

## Workflow
- explore before edit
- plan before implementation
- verify before final
- do not claim completion without running checks

## Architecture
- follow existing patterns
- keep scope narrow
- document public API changes
```

## Agent loop

```text
explore → plan → edit/tool use → verify → iterate → summarize
```

## 다른 모델로 구현하는 핵심 패턴

| 패턴 | 용도 |
|------|------|
| Planner-Executor-Reviewer | Claude/Codex/Gemini 역할 분리 |
| ReAct loop | tool 사용과 observation 기반 반복 |
| Self-Refine | 초안 → critique → revision → test |
| Tree/Graph of Thoughts | 여러 설계안 비교 후 선택 |
| Parallel sampling | 여러 attempt 중 tests/diff 품질로 선택 |
| RAG + MCP | repo/docs/tickets/DB를 context로 공급 |
| Safety gate | 요청 분류, fallback, output scanner |
| Memory files | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` |

## Claude + Codex + Gemini 분업

```text
Claude Fable: 어려운 plan, architecture, root cause
Codex: scoped implementation, refactor, test fix
Gemini: latest docs, long-context review, grounded comparison
```

## Review 프롬프트

```text
이 diff에서 숨은 regression, security issue, test gap만 찾아라.
스타일 취향이나 칭찬은 제외하고 blocker부터 severity 순서로 보고해.
```

## Safety 주의

- cyber/bio/chem 위험 도메인은 Fable safeguard와 fallback routing이 걸릴 수 있다.
- defensive secure coding, patch review, log analysis 중심으로 task boundary를 좁힌다.
- API 사용자는 Fallback API 설정과 data retention 조건을 확인한다.

## 링크

[[claude-fable의-기조-원리-사용법-이걸-다른-모델로도-구현할-수/README|시리즈 처음]] · [[claude]] · [[codex]] · [[model-context-protocol-mcp]] · [[agent-orchestration/README]] · [[lazy-codex/README]]
