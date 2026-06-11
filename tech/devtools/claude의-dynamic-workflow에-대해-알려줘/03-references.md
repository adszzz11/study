---
date: 2026-06-09
tags:
  - tech
  - devtools
  - claude
  - dynamic-workflows
  - references
status: learning
type: tech-tool-study
parent: "[[README]]"
---

# Claude Dynamic Workflows - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. 공식 문서

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Anthropic announcement | https://claude.com/blog/introducing-dynamic-workflows-in-claude-code | research preview 공개 배경, 권한/비용 주의 |
| Anthropic deep dive | https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code | task-specific harness, orchestration pattern |
| Claude Code docs - Dynamic Workflows | https://code.claude.com/docs/en/workflows | trigger, `/workflows`, 제한, 저장/재실행 |
| Claude Code docs - Subagents | https://code.claude.com/docs/en/sub-agents | subagent 개념, 역할 분리 |
| Claude Agent SDK subagents | https://code.claude.com/docs/en/agent-sdk/subagents | SDK 기반 subagent embedding |
| Claude Code Skills | https://code.claude.com/docs/en/skills | Skills와 workflow의 책임 차이 |
| Claude Code FAQ/admin controls | https://support.claude.com/en/articles/12386420-claude-code-faq | admin disable, managed settings, token/cost 관련 |

---

## 2. 비교 자료

| 자료 | URL | 비교 관점 |
|------|-----|-----------|
| OpenAI Codex announcement | https://openai.com/index/introducing-codex/ | cloud coding agent, sandbox, PR flow |
| GitHub Copilot coding agent | https://github.com/newsroom/press-releases/coding-agent-for-github-copilot | GitHub-native issue/PR automation |
| LangGraph multi-agent docs | https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/ | developer-defined graph/state workflow |

---

## 3. 핵심 claim 정리

| Claim | 근거 | 노트 |
|-------|------|------|
| Claude가 task-specific JavaScript workflow를 생성한다 | Claude Code Dynamic Workflows docs, Anthropic deep dive | [[01-overview]] |
| 중간 결과는 Claude context 대신 script variables에 저장될 수 있다 | Claude Code Dynamic Workflows docs | context overload 완화 |
| 한 run은 최대 16 concurrent agents, 총 1,000 agents 제한 | Claude Code Dynamic Workflows docs | budget 설계 필요 |
| `ultracode`, `use a workflow`, `/effort ultracode`로 trigger 가능 | Claude Code Dynamic Workflows docs | [[04-learning/01-getting-started]] |
| `/deep-research` built-in workflow가 제공된다 | Claude Code Dynamic Workflows docs | research workflow 실습 |
| workflow는 token을 크게 사용할 수 있다 | Anthropic announcement, FAQ | [[cheatsheet]] |

---

## 4. 읽는 순서

1. Announcement로 제품 의도와 preview 상태를 파악한다.
2. Dynamic Workflows docs에서 실제 trigger, UI, limit를 확인한다.
3. Deep dive에서 pattern vocabulary를 정리한다.
4. Subagents/Skills 문서로 Claude 내부 구성요소의 책임을 분리한다.
5. Codex, Copilot, LangGraph와 비교해 도입 기준을 만든다.

```text
announcement -> docs/workflows -> deep dive -> subagents/skills -> ecosystem compare
```

---

## 5. 관련 노트

- [[study/tech/ai/claude/README]] - Claude 전체 학습 시리즈
- [[study/tech/ai/claude/08-subagents]] - subagents 상세
- [[study/tech/ai/codex/02-ecosystem]] - Codex ecosystem 비교
- [[study/tech/ai/langchain-crewai/02-ecosystem]] - agent framework 비교
