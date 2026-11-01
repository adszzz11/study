---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — Claude Code Skills와 Multi-Agent

## What

`SKILL.md`는 특정 일을 언제, 어떤 입력으로, 어떤 순서와 완료 기준으로 수행할지를 담는 on-demand procedure다. Claude Code의 subagent와 MCP를 함께 쓰면 procedure가 외부 도구·repository·CI까지 연결된 실행 흐름이 된다.

```text
task + success criteria
→ coordinator (scope / budget)
→ research · implementation · design workers
→ critic / judge
→ evidence, deterministic tests, human approval
```

## Why

단일 agent는 탐색 편향과 누락, 과도한 확신을 만들기 쉽다. 반대로 무분별한 병렬화는 context, token, merge 충돌을 키운다. 따라서 worker의 산출물을 “그럴듯한 답”이 아니라 citation, test 결과, scope 준수 여부로 평가해야 한다.

## 핵심 특징

| 요소 | 역할 | 실무 원칙 |
|---|---|---|
| Skills | 반복 절차 재사용 | 단일 목적·명확한 입력/출력으로 좁힌다 |
| Parallel specialists | 독립 탐색 가속 | 공유 상태가 없을 때만 병렬화한다 |
| Critic / judge | draft를 공격하고 통합 | 생성자와 검토자를 분리한다 |
| MCP | GitHub·DB·browser 등 연결 | least privilege와 credential 격리가 우선이다 |
| Git/CI | 검증 가능한 종료 조건 | 설명보다 test와 diff를 신뢰한다 |

`draft → critique → refine`은 self-critique의 기본 패턴이다. 다만 judge도 hallucination할 수 있으므로, 최종 gate는 근거 URL, 재현 가능한 test, regression 확인, 사람의 승인으로 둔다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://docs.anthropic.com/en/docs/claude-code/getting-started
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
