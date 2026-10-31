---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Agentic Design Patterns cheatsheet

| Pattern | 사용할 때 | 반드시 정할 것 |
|---|---|---|
| Prompt Chaining | 순차 변환·검증 | 단계별 schema와 실패 경로 |
| Routing | 입력 유형별 다른 처리 | route confidence와 fallback |
| Tool Use | 외부 data/action 필요 | typed input, allowlist, timeout |
| RAG | 근거 기반 답변 | citation, 권한 필터, retrieval 평가 |
| Reflection | 품질 개선이 필요 | rubric, max iterations, threshold |
| Planning | 여러 의존 단계 | plan schema, replanning/stop 조건 |
| Memory | 장기 context 필요 | 저장 근거, retention, 삭제 |
| HITL | 고위험 결정·write | preview, approval, rollback |
| Multi-Agent | 역할/권한/context 분리가 실제로 필요 | handoff schema, ownership, timeout |
| Evaluation | 모든 production system | golden set, trace, 비용·latency 지표 |

## Production checklist

- [ ] 고정 workflow로 해결 가능한지 먼저 확인했다.
- [ ] tool은 least privilege이며 input schema가 있다.
- [ ] timeout, retry, exception recovery, 종료 조건이 있다.
- [ ] citation/grounding과 offline evaluation set이 있다.
- [ ] 고위험 write action 앞에 human approval이 있다.
- [ ] trace, cost, latency, tool error를 관측한다.
- [ ] multi-agent 구조가 single-agent baseline보다 나은지 비교했다.

## Protocol mnemonic

```text
MCP = model/agent ↔ tools and data
A2A = agent ↔ agent collaboration
```

## Sources

- https://link.springer.com/book/10.1007/978-3-032-01402-3
- https://modelcontextprotocol.io/docs/getting-started/intro
- https://a2a-protocol.org/latest/
