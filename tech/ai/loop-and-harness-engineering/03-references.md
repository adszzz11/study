---
date: 2026-06-23
tags: [tech, ai, references, agent-harness, loop-engineering]
status: learning
type: tech-tool-study
---

# 03. References — 논문·공식문서·소스

## 핵심 논문

| 우선순위 | 자료 | 읽을 포인트 |
|----------|------|-------------|
| 1 | [AI Harness Engineering: A Runtime Substrate for Foundation-Model Software Agents, 2026](https://arxiv.org/abs/2605.13357) | harness를 `runtime substrate`로 보는 관점, 11개 구성요소 |
| 2 | [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses, 2026](https://arxiv.org/abs/2604.25850) | traces와 observability로 harness를 자동 개선하는 방향 |
| 3 | [Claude Code 분석 논문, 2026](https://arxiv.org/abs/2604.14228) | `model call -> tool execution -> repeat` while-loop와 주변 시스템 복잡성 |

## 공식 문서

| 영역 | 자료 | 읽을 포인트 |
|------|------|-------------|
| OpenAI | [OpenAI Cookbook: Build an Agent Improvement Loop with Traces, Evals, and Codex](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop) | `traces -> feedback -> evals -> ranked harness changes -> Codex implementation` |
| OpenAI | [OpenAI Codex Docs](https://developers.openai.com/codex) | coding agent workflow, repo 작업, 검증 중심 사용 |
| OpenAI | [OpenAI Agents SDK Docs](https://developers.openai.com/api/docs/guides/agents) | orchestration, tools, approvals, state 설계 |
| Anthropic | [Claude Code Docs: Run prompts on a schedule `/loop`](https://code.claude.com/docs/en/scheduled-tasks) | 반복 prompt 실행과 scheduled task |
| Anthropic | [Claude Code Docs: Routines](https://code.claude.com/docs/en/routines) | schedule/API/GitHub event 기반 자동 실행 |
| Anthropic | [Claude Code Docs: Settings](https://code.claude.com/docs/en/settings) | project/local/managed scope, permissions, plugin settings |
| Anthropic | [Claude Code Docs: Memory](https://code.claude.com/docs/en/memory) | `CLAUDE.md` 기반 project memory |
| Anthropic | [Claude Code Docs: Skills](https://code.claude.com/docs/en/skills) | 반복 업무 절차를 skill로 캡슐화 |
| Anthropic | [Claude Code Docs: Plugins](https://code.claude.com/docs/en/plugins) | skills, agents, hooks, MCP server를 재사용 패키지로 배포 |
| Anthropic | [Claude Code Docs: Subagents](https://code.claude.com/docs/en/sub-agents) | specialist agent를 나누는 방식 |
| Anthropic | [Claude Code Docs: Hooks reference](https://code.claude.com/docs/en/hooks) | lifecycle hook으로 harness에 정책 삽입 |

## 생태계 문서

| 자료 | 정체성 | harness 관점 |
|------|--------|--------------|
| [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) | durable agent runtime | persistence, human-in-the-loop, long-running workflow |
| [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) | external tool/context protocol | tool registry와 context 연결 표준 |
| [AGENTS.md open format](https://agents.md/) | repo-level agent instruction | build/test/style/security 지침의 공통 파일 |
| [SWE-bench](https://www.swebench.com/) | software engineering benchmark | real GitHub issue 해결률 |
| [Terminal-Bench](https://www.tbench.ai/) | terminal task benchmark | CLI tool-use와 long-horizon task 평가 |

## 읽는 순서

```text
1. AI Harness Engineering 논문으로 개념 지도 잡기
2. OpenAI Cookbook으로 improvement loop 구조 보기
3. Claude Code docs로 제품화된 loop/harness 기능 확인
4. MCP / AGENTS.md로 repo와 tool 연결 표준 확인
5. SWE-bench / Terminal-Bench로 평가 관점 이해
```

## 핵심 문장으로 기억하기

- 모델 성능은 **model alone**이 아니라 **model-harness-environment system**에서 나온다.
- 좋은 harness는 agent에게 자유를 주는 것이 아니라, **관찰 가능한 자유**를 준다.
- trace가 없으면 실패를 학습할 수 없고, eval gate가 없으면 개선을 검증할 수 없다.

## 관련 노트

- [[study/tech/ai/codex]]
- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/lazy-codex]]
