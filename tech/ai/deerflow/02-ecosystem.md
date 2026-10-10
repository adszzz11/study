---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — Ecosystem

> [[README|목차로 돌아가기]]

## 어디에 위치하는가

```text
User / API
    ↓
DeerFlow App (frontend · gateway · deployment)
    ↓
DeerFlow Harness (Lead Agent · middleware · skills · tools · sandbox)
    ↓
LangGraph runtime / model providers / database / sandbox providers
```

DeerFlow는 model provider도, 단순 graph library도 아니다. 장시간 agent 작업에 필요한 opinionated runtime과 운영 가능한 App을 함께 제공하는 layer다.

## 비교

| 도구 | 적합한 경우 | DeerFlow와의 차이 |
|---|---|---|
| **DeerFlow** | sandbox와 artifact가 필요한 research·coding·analysis | batteries-included harness와 usable App을 함께 제공 |
| **LangGraph** | state transition, retry, HITL, deterministic node를 세밀하게 설계 | DeerFlow의 기반 기술이며 더 low-level; runtime/UX를 직접 구성 |
| **OpenAI Agents SDK** | OpenAI tools, handoff, tracing, guardrail을 code-first로 가볍게 조립 | primitive 중심; DeerFlow는 sandbox·skills·App 운영층을 더 강하게 기본 제공 |
| **Google ADK** | Google Cloud/Vertex와 multi-language enterprise integration이 중요 | Python·TypeScript·Go·Java 및 Cloud Run/GKE 확장성이 강점; DeerFlow는 self-hosted long-horizon 경험에 집중 |
| **CrewAI** | role/task/crew라는 명시적 팀 모델로 flow를 빠르게 모델링 | Crews/Flows 중심; DeerFlow는 lead agent + isolated subagent + sandbox/skill runtime 중심 |

## 선택 기준

```text
긴 작업용 실행 환경과 App까지 필요한가?
├─ Yes → DeerFlow를 sandbox·권한·artifact 요구와 함께 평가
└─ No
   ├─ graph의 모든 state transition을 직접 설계해야 하는가? → LangGraph
   ├─ OpenAI 중심의 작은 code-first agent가 필요한가? → OpenAI Agents SDK
   ├─ Google Cloud/Vertex 표준화가 핵심인가? → Google ADK
   └─ role 기반 팀·업무 flow가 우선인가? → CrewAI
```

## 함께 쓰는 구성요소

| 영역 | 예시 | 역할 |
|---|---|---|
| Model | OpenAI-compatible 또는 지원 provider | reasoning과 tool call 생성 |
| Search/fetch | DuckDuckGo, Jina | 조사 source 수집 |
| Skill | `deep-research`, `data-analysis`, custom `SKILL.md` | domain procedure와 tool 묶음 제공 |
| Sandbox | LocalSandbox, AIO, E2B | command·file 작업 격리 |
| Database | checkpoint/application data backend | 지속성, 재개, 대화 state |
| MCP/ACP | external tool 또는 agent 연결 | ecosystem 확장 |

도입 전에는 단순 기능표보다 같은 task set에서 citation quality, artifact correctness, sandbox escape 가능성, 권한 거부 동작, 비용·latency, 실패 후 resume을 검증한다.

## Sources

- https://langchain-ai.github.io/langgraph/reference/
- https://openai.github.io/openai-agents-python/
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/adk
- https://github.com/crewAIInc/crewAI/blob/main/docs/v1.14.7/en/concepts/flows.mdx
- https://deerflow.tech/en/docs
