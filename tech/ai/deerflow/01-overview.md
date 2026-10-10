---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — Overview

> [[README|목차로 돌아가기]]

## What

DeerFlow는 long-horizon task를 위한 **SuperAgent harness**다. Lead Agent가 요청을 계획하고 tool을 route하며 `task` tool로 isolated subagent를 호출한다. LangGraph 기반 runtime 위에 model, tools, skills, memory, sandbox, middleware와 persistence를 결합한다.

Harness와 App은 구분해서 이해한다.

| 층 | 책임 |
|---|---|
| Harness | agent runtime/SDK, orchestration, tool·skill·sandbox·memory interface |
| App | FastAPI Gateway와 agent runtime, Next.js frontend, nginx reverse proxy를 묶은 reference application |

문서 기준 `pip install deerflow` Harness package는 아직 public release 전이다. 따라서 현재 학습·평가의 출발점은 repository 기반 설치다.

## Why

여러 단계의 agent 작업은 답변 품질 외에도 실행 방식이 결과를 좌우한다.

| 문제 | DeerFlow의 접근 |
|---|---|
| main context가 조사 로그로 오염 | 독립 context의 subagent에 탐색을 위임 |
| tool 권한이 과도하거나 불명확 | config와 allowlist로 tool·skill 범위를 명시 |
| 파일·코드 실행의 위험 | LocalSandbox, AIO, E2B 등 sandbox provider 선택 |
| 긴 실행 중 state 손실 | LangGraph checkpoint와 application data 관리 |
| 행동을 한 class에 고정 | middleware chain으로 turn 전후 behavior를 조합 |

## 핵심 특징

### Lead Agent와 Subagent

Lead Agent는 최종 작업의 책임을 갖고 `task` tool로 subagent를 호출한다. 기본 `general-purpose` subagent는 조사·분석을, `bash` subagent는 sandbox command 수행을 주로 담당한다. 각 subagent의 context는 main thread와 분리되므로 병렬 탐색과 결과 요약에 유리하다.

### Middleware-first

agent subclass를 계속 늘리는 방식 대신 LLM turn 전후를 감싸는 middleware chain을 조합한다. `config.yaml`에서 model, tool, summarization, memory, guardrail, subagent 제한을 바꾸는 것이 핵심 운영 interface다.

### Skills와 Tools

`SKILL.md` 기반 skill package를 on-demand loading하고, built-in/community/MCP/skill tool을 연결할 수 있다. 예를 들어 web search, fetch, filesystem, bash, ACP agent 연결을 task별 최소 집합으로 제공한다.

### State와 Memory

checkpoint 및 application data는 database에서 관리한다. memory는 중요한 정보를 추출·주입하는 middleware가 기본이며, tool mode는 실험적 옵션이다. memory는 source of truth가 아니므로 원문·근거 링크와 별도로 검증해야 한다.

## Sandbox 경계

LocalSandbox는 기본적으로 host bash를 차단하지만 host filesystem isolation을 제공하지 않는다. 신뢰된 단일 사용자 개발에 한정하고, production 또는 multi-user 환경은 container 기반 AIO나 E2B 같은 격리 provider를 평가한다. 어떤 provider든 write, network, secret 접근은 최소 권한과 별도 approval을 둔다.

## Sources

- https://deerflow.tech/en/docs/introduction/core-concepts
- https://deerflow.tech/en/docs/harness/design-principles
- https://deerflow.tech/en/docs/harness/subagents
- https://deerflow.tech/en/docs/harness/sandbox
