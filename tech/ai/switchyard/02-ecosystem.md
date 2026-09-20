---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## Positioning

Switchyard의 핵심은 **protocol translation + model routing algorithm + agent-stage awareness**다. model server 자체도, agent framework도, tool integration protocol도 아니다.

```text
Agent / Application
        ↓ OpenAI or Anthropic semantics
Switchyard ── routing policy / translation / telemetry
        ↓ provider-specific wire format
Gateway or Model Server
        ↓
Hosted model / Local model
```

## Comparison

| 대안 | 주 역할 | Switchyard가 더 맞는 경우 | 대안이 더 맞는 경우 |
|---|---|---|---|
| Direct provider SDK | 특정 provider API 호출 | client protocol과 backend를 분리하고 model routing 필요 | provider 하나만 쓰며 최신 native feature가 중요 |
| LiteLLM Proxy | 광범위한 provider abstraction, gateway, spend/budget 관리 | agent stage 기반 routing, Rust embedding, provider-neutral trace가 핵심 | provider 수, virtual key, budget·quota·enterprise gateway 기능이 핵심 |
| Envoy AI Gateway 계열 | infrastructure-grade traffic policy와 proxy integration | LLM-aware classifier/stage policy를 빠르게 실험 | Kubernetes/Envoy 운영, 조직 표준 ingress와 정책 집행이 핵심 |
| OpenRouter | hosted multi-model aggregation | self-hosted/local endpoint와 자체 routing logic을 통제 | 운영할 proxy 없이 한 API로 다양한 hosted model 사용 |
| vLLM / Ollama / NVIDIA NIM | model inference serving | 여러 server 앞에서 protocol과 route를 통합 | 단일 model을 직접 serving하는 것이 목적 |
| Custom FastAPI proxy | 맞춤형 request forwarding | streaming/tool-call translation과 router를 재사용 | 요구가 매우 작고 모든 동작을 직접 통제해야 함 |
| Agent framework | planning, tool execution, memory, workflow | framework 아래의 model traffic layer가 필요 | agent 행동과 workflow orchestration 자체가 목적 |
| MCP | agent-to-tool/data protocol | model request의 backend 선택·변환이 필요 | external tool/resource/prompt 연결이 필요 |

> [!note]
> LiteLLM과 Switchyard는 완전한 양자택일이 아니다. Switchyard의 upstream으로 provider gateway를 두거나, routing algorithm만 `libsy`로 기존 gateway에 내장할 수 있다. 다만 retry, fallback, telemetry를 양쪽에서 동시에 켜면 중복 호출과 attribution 혼란이 생길 수 있다.

## Selection Guide

| 요구사항 | 권장 선택 |
|---|---|
| Anthropic client를 OpenAI-compatible local endpoint에 연결 | Switchyard `passthrough`로 protocol bridge 검증 |
| 여러 provider의 key, team budget, quota를 중앙 관리 | mature gateway 우선 검토 |
| weak/strong model cascade 실험 | `llm_classifier` capability 또는 escalation |
| 긴 coding session에서 탐색·오류·edit 단계별 model 변경 | `stage_router` |
| traffic percentage 기반 단순 실험 | `random` weighted split |
| 기존 Rust runtime 안에서 selection state machine만 사용 | `switchyard-libsy` |
| 단일 model endpoint와 단일 SDK | direct provider SDK |

## Integration Patterns

### Edge proxy

```text
Claude Code / Codex CLI → switchyard-server → OpenRouter / vLLM / NIM
```

가장 단순한 도입 방식이다. launcher가 local proxy lifecycle과 agent endpoint environment를 관리한다.

### Gateway composition

```text
Application → Switchyard → enterprise gateway → providers
```

Switchyard는 intelligent routing을, downstream gateway는 auth, quota, provider connectivity를 담당한다. retry budget과 model identity를 어느 계층이 책임질지 먼저 정해야 한다.

### Embedded routing

```text
Rust agent runtime → libsy Step::CallModel → host transport → model
```

HTTP proxy hop을 추가하지 않고 algorithm만 재사용한다. host가 model call, secret, timeout, span을 통제한다.

## Trade-offs

| 장점 | 비용/위험 |
|---|---|
| client와 provider API decoupling | translation fidelity를 지속적으로 검증해야 함 |
| complexity/stage-aware routing | judge 호출 비용과 오분류 가능성 |
| fallback과 session affinity | state와 실제 serving model 추적 복잡도 |
| Rust server와 embeddable library | Python gateway 생태계 대비 초기 integration 비용 |
| detailed telemetry | cardinality, privacy, log retention 설계 필요 |

## Sources

- [Switchyard Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md)
- [LLM Classifier Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/llm_classifier_routing.md)
- [Stage-Router Routing](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/routing_algorithms/stage_router_routing.md)
- [`libsy` README](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/crates/libsy/README.md)

