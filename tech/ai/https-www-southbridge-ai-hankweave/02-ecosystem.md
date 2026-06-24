---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - ecosystem
  - comparison
type: tech-tool-study
parent: "[[README]]"
---

# Hankweave - 생태계와 비교

> [[01-overview|이전: 개요]] | [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

---

## 1. 포지션

Hankweave는 LangGraph, AutoGen, CrewAI처럼 agent application을 구성하는 framework라기보다, 이미 존재하는 agent harness를 긴 workflow 안에서 **실행·격리·관찰·복구**하는 runtime에 가깝다.

```text
Application framework: agent behavior를 코드로 직접 설계
Runtime/orchestrator: agent harness 실행을 durable workflow로 관리
```

## 2. 주요 도구 비교

| 도구 | 포지션 | Hankweave와의 차이 | 적합한 경우 |
|---|---|---|---|
| **Hankweave** | headless-first long-horizon agent runtime | agent loop와 harness 자체를 primitive로 보고, codon boundary·checkpoint·sentinel로 repairability를 우선 | 데이터 파이프라인, research/codebook/report generation처럼 오래 돌고 재실행·수리가 중요한 agent workflow |
| **LangGraph** | low-level orchestration runtime for long-running stateful agents | graph/state 기반 앱 개발 프레임워크에 가깝고 persistence, HITL, memory, streaming을 제공 | Python/JS agent app을 직접 설계하고 LangSmith ecosystem을 쓰는 팀 |
| **AutoGen** | Microsoft의 single/multi-agent framework | conversational multi-agent, event-driven Core, Studio 중심. Hankweave보다 agent 구성 자체에 초점 | Python 기반 multi-agent 연구·프로토타이핑·분산 agent |
| **CrewAI** | crews/flows 기반 multi-agent orchestration | role/task/process, enterprise console, integrations 중심. Hankweave보다 business automation UX가 강함 | 업무 자동화, crew/task abstraction, SaaS-style 운영 |
| **Temporal** | durable workflow platform | AI agent 전용은 아니지만 crash-proof execution, replay, retry, workflow durability가 강함 | mission-critical workflow를 코드로 엄격히 관리하고 agent는 일부 activity로 넣는 구조 |
| **bash/scripts + cron/CI** | 가장 단순한 orchestration | checkpoint, event journal, sentinel, context boundary, harness abstraction을 직접 만들어야 함 | 짧고 deterministic한 작업 또는 실험용 glue |

## 3. 선택 기준

| 질문 | Hankweave가 맞는 신호 | 다른 선택이 나은 신호 |
|------|----------------------|----------------------|
| Workflow 길이 | 수십 분~수일 실행, 중간 실패 복구 필요 | 한 번 호출로 끝나는 짧은 task |
| Agent 제어 방식 | 기존 CLI harness를 그대로 쓰고 싶음 | agent loop를 Python/JS 코드로 직접 설계하고 싶음 |
| 디버깅 기준 | event journal, checkpoint, rollback이 중요 | 단순 request/response logging이면 충분 |
| Context 전략 | codon마다 controlled forgetting 필요 | 하나의 대화 state를 계속 유지하는 편이 자연스러움 |
| 운영 환경 | Docker/CI/headless run과 artifact export 필요 | 로컬 실험이나 notebook 수준 |

## 4. Hankweave vs agent framework

| 축 | Agent framework | Hankweave |
|----|-----------------|-----------|
| 주요 abstraction | node, edge, role, tool, message, state | hank, codon, harness, checkpoint, sentinel |
| 구현 초점 | agent logic 작성 | agent run 관리 |
| 실패 처리 | retry, state persistence, HITL | rollback, repair, event audit, sentinel |
| context 관리 | memory/state 설계 | codon boundary, file handoff, fresh context |
| 운영 방식 | app server, worker, graph runner | headless runtime, TUI, CI/Docker execution |

## 5. 함께 쓰는 조합

- **Hankweave + Codex/Claude Code**: coding/research harness를 codon 단위로 실행하고 결과를 checkpoint한다.
- **Hankweave + MCP**: MCP server가 external tool/resource를 제공하고, harness가 이를 사용한다.
- **Hankweave + Temporal**: Temporal workflow 안에서 Hankweave run을 하나의 activity로 호출하거나, Hankweave 결과물을 durable workflow로 후처리한다.
- **Hankweave + LangGraph**: LangGraph app이 특정 codon에서 실행되는 내부 agent application이 될 수 있다.

```text
CI job
  -> bunx hankweave@latest --headless --autostart
      -> Codex harness uses MCP tools
      -> checkpointed outputs
      -> sentinel report
      -> final artifact export
```

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - agent가 쓰는 tool/resource integration layer
- [[study/tech/ai/lazy-codex]] - coding harness와 검증 loop
- [[study/tech/ai/multi-agent-platforms]] - AutoGen, CrewAI 등 multi-agent framework 맥락
- [[study/tech/infra/prefect]] - workflow orchestration 관점에서 비교 가능한 도구

## References

- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/overview)
- [AutoGen docs](https://microsoft.github.io/autogen/stable/)
- [CrewAI docs](https://docs.crewai.com/)
- [Temporal docs](https://docs.temporal.io/)
- [Hankweave Documentation](https://hankweave.southbridge.ai/)
