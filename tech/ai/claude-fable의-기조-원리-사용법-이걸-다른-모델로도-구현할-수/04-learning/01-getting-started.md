---
date: 2026-07-09
tags: [tech, ai, claude, claude-code, getting-started, workflow]
status: published
type: tech-tool-study
---

# 04-1. Getting Started — Claude를 효율적으로 쓰는 기본 세팅

## 1. 프로젝트 루트에 `CLAUDE.md` 만들기

Claude Code에서 가장 먼저 할 일은 프로젝트 규칙을 memory file로 고정하는 것이다.

```md
# Project Instructions

## Build / Test
- Install: `pnpm install`
- Typecheck: `pnpm typecheck`
- Test: `pnpm test`
- Lint: `pnpm lint`

## Workflow
- 수정 전 relevant files를 먼저 탐색한다.
- 구현 전 짧은 plan을 작성한다.
- 파일 수정 후 반드시 test/typecheck를 실행한다.
- 실패하면 원인을 분석하고 다시 수정한다.
- 테스트를 실행하지 못했다면 완료라고 말하지 않는다.

## Architecture
- 기존 패턴을 우선한다.
- 불필요한 abstraction을 만들지 않는다.
- public API 변경은 migration note를 남긴다.
```

## 2. Claude에게 줄 기본 프롬프트

```text
이 repo에서 먼저 관련 파일과 기존 패턴을 탐색해.
그다음 간단한 plan을 세우고 구현해.
구현 후 test/typecheck/lint를 실행하고 실패하면 반복해.
완료 답변에는 변경 파일, 검증 결과, 남은 risk만 요약해.
```

## 3. 작업 크기별 모델 선택

| 작업 크기 | 추천 |
|-----------|------|
| 단순 bug fix | Claude Sonnet 또는 Codex |
| 복잡한 root cause 분석 | Claude Fable |
| 장기 migration plan | Claude Fable |
| 좁은 구현 task 병렬 처리 | Codex |
| 긴 문서/공식 문서 조사 | Gemini |
| 최종 review | Claude와 Gemini/Codex 교차 |

## 4. Codex와 병렬로 쓰기

Claude가 전체 plan을 만들면 Codex에는 작은 단위로 쪼개서 맡긴다.

```text
Claude Fable에게:
"이 migration의 risk map, 단계별 plan, test strategy를 작성해."

Codex에게:
"plan의 Step 2만 구현해. 관련 파일만 수정하고 test를 실행해."
```

Codex는 implementation과 verification에 강하다. 대신 너무 넓은 목표를 한 번에 주면 의도와 다르게 scope가 커질 수 있으므로 module, file, test 기준으로 잘라준다.

## 5. Gemini와 같이 쓰기

Gemini는 긴 context와 검색 grounding이 필요할 때 쓴다.

```text
Gemini에게:
"공식 문서 기준으로 이 API의 최신 migration requirement를 조사하고,
Claude의 plan에서 틀렸거나 오래된 부분만 지적해."
```

## 6. 완료 조건 정의

좋은 완료 조건:

- “`pnpm test` PASS”
- “migration guide의 required API 5개 모두 반영”
- “UI screenshot이 reference와 비교해 주요 layout mismatch 없음”
- “adversarial review에서 blocker 없음”

나쁜 완료 조건:

- “대충 정리”
- “가능하면 개선”
- “알아서 잘”
- “문제 없어 보이면 끝”

## 7. Claude 사용 체크리스트

| 단계 | 체크 |
|------|------|
| 시작 | `CLAUDE.md`가 있는가 |
| 탐색 | 관련 파일, test, docs를 먼저 읽었는가 |
| 계획 | 완료 조건과 rollback/risk를 적었는가 |
| 구현 | 기존 패턴을 따랐는가 |
| 검증 | 실제 command를 실행했는가 |
| 리뷰 | 다른 모델 또는 사람 review를 거쳤는가 |

## 관련 노트

- [[claude/03-claude-code]] · [[codex/04-learning/01-getting-started]] · [[model-context-protocol-mcp/04-learning/01-getting-started]] · [[lazy-codex/cheatsheet]]
