---
date: 2026-07-09
tags: [tech, ai, agent-algorithms, react, self-refine, multi-agent, safety]
status: published
type: tech-tool-study
---

# 04-2. Deep Dive — 다른 모델로 구현 가능한 알고리즘

## 1. Fable식 agent behavior를 분해하기

Fable 5의 강점은 모델 능력만이 아니라 agent harness가 강제하는 작업 형태에 있다.

```text
goal
→ context acquisition
→ plan
→ tool execution
→ verification
→ critique
→ retry
→ final summary
```

이 패턴은 Claude가 아니어도 Codex, Gemini, OpenAI API, local model 조합으로 구현할 수 있다.

## 2. Planner-Executor-Reviewer

가장 실용적인 multi-agent pattern이다.

| 역할 | 책임 | 추천 모델 |
|------|------|-----------|
| Planner | 목표 분해, risk map, acceptance criteria | Claude Fable / Gemini |
| Executor | 파일 수정, command 실행, test fix | Codex / Claude Sonnet |
| Reviewer | diff 검토, hidden regression, security issue 탐지 | Gemini / Claude / Codex |

```text
Planner: "작업을 5개 step과 test strategy로 나눠라."
Executor: "Step 2만 구현하고 tests를 실행해라."
Reviewer: "diff에서 blocker만 찾아라. 칭찬 금지."
```

## 3. ReAct loop

ReAct는 reason about task, choose tool, observe result, update plan을 반복하는 구조다.

```pseudo
state = initial_task
while not done:
  thought = model.reason(state)
  action = model.choose_tool(thought)
  observation = tool.run(action)
  state = update(state, observation)
  if verification_passed(state):
    done = true
```

실전에서는 thought를 길게 노출시키기보다, plan과 observation summary를 짧게 남기는 편이 좋다.

## 4. Self-Refine

Self-Refine은 초안 생성, critique, revision을 반복한다.

```text
draft
→ critique against requirements
→ revised answer/code
→ test
→ repeat until pass
```

코딩에서는 다음처럼 쓴다.

```text
1. 구현 초안 생성
2. 요구사항 checklist와 diff를 비교
3. test failure를 critique로 사용
4. 수정
5. PASS까지 반복
```

## 5. Tree / Graph of Thoughts

복잡한 설계에서는 plan branch를 여러 개 만든 뒤 evaluator가 고른다.

| 단계 | 예 |
|------|----|
| Branch generation | “migration 전략 3개를 제안” |
| Evaluation | 비용, risk, rollback, testability 비교 |
| Selection | 가장 낮은 blast radius 선택 |
| Execution | 선택한 branch만 구현 |

```text
Plan A: big bang migration
Plan B: strangler fig migration
Plan C: compatibility adapter first
Evaluator: B 또는 C 선택, 이유와 rejected risk 기록
```

## 6. Test-time compute / parallel sampling

같은 task를 여러 agent attempt로 병렬 실행하고 결과를 test와 diff 품질로 선택한다.

```text
attempt-1: Codex
attempt-2: Claude Sonnet
attempt-3: Gemini-assisted implementation
→ run same test suite
→ compare diff size, readability, regression risk
→ choose or merge best parts
```

주의: parallel sampling은 비용이 늘고 conflict가 생긴다. package, file, branch, worktree를 분리해야 한다.

## 7. RAG + MCP

Fable식 long-horizon work는 context 품질이 핵심이다.

| context source | 공급 방식 |
|----------------|-----------|
| repo docs | retrieval index |
| tickets | GitHub/Jira MCP |
| runbooks | filesystem or docs MCP |
| DB schema | database MCP |
| Slack/Discord thread | connector/MCP |

```text
Question
→ retrieve relevant docs/code/tickets
→ provide compact context
→ agent uses tools
→ verification writes back result
```

## 8. Safety gate

Fable 5의 safeguard 방향은 다른 모델에도 구현할 수 있다.

```pseudo
classification = safety_classifier(request)
if classification == "prohibited":
  block()
elif classification == "high-risk dual use":
  route_to_safer_model_or_human_review()
elif classification == "low-risk dual use":
  allow_with_monitoring()
else:
  allow()
```

defensive secure coding, patch review, log analysis는 허용하되, offensive exploit 자동화나 weaponization으로 흐르지 않게 task boundary를 명시한다.

## 9. Memory files

모델별 memory file을 맞춰두면 agent 품질이 올라간다.

| 모델/도구 | 파일 | 내용 |
|-----------|------|------|
| Claude Code | `CLAUDE.md` | build/test, style, architecture, workflow |
| Codex | `AGENTS.md` | repo instructions, verification rules |
| Gemini CLI | `GEMINI.md` | docs/search/review conventions |

핵심은 “이번 채팅에서 다시 설명하지 않아도 되는 불변 규칙”을 파일로 저장하는 것이다.

## 관련 노트

- [[agent-orchestration/README]] · [[model-context-protocol-mcp/04-learning/02-deep-dive]] · [[lazy-codex/04-learning/02-verified-completion]] · [[autoresearch-study/04-learning/02-experiment-loop]]
