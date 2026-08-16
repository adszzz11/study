---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS Ecosystem

> [[01-overview|이전: Overview]] | [[README|목차로 돌아가기]] | [[03-references|다음: References]]

## Positioning

holaOS를 비교할 때는 “어느 agent가 더 똑똑한가?”보다 **어느 계층을 책임지는가?**를 먼저 본다.

```text
Workspace environment  holaOS
        ↓
Agent harness          pi / Claude Code / Codex 계열
        ↓
Model provider         OpenAI / Anthropic / Gemini / Ollama / ...
        ↓
Capabilities           Browser / Runtime tools / MCP / Apps
```

holaOS는 주로 environment/workspace layer에 있고, agent harness와 model provider는 그 안에서 선택되는 실행 요소다.

## Alternatives and Complements

| 범주 | 주 책임 | holaOS와의 차이 | 선택 기준 |
|---|---|---|---|
| **holaOS** | 장기 workspace, policy, state, memory, Apps, automation | 여러 실행 요소를 지속 가능한 환경으로 묶음 | session을 넘어 상태와 도구를 공유해야 할 때 |
| **Claude Code / Codex** | coding-oriented agent harness/CLI | 개별 session과 coding execution에 더 가까움 | repository 작업 자체가 핵심이고 별도 workspace OS가 불필요할 때 |
| **MCP host/client** | 외부 tool과 data 연결 | protocol integration이 중심이며 전체 workspace state model은 아님 | 여러 tool server의 discovery/call만 필요할 때 |
| **Agent framework** | code로 graph, loop, state machine 구현 | developer-defined application runtime에 가까움 | custom orchestration을 library/code 수준에서 통제할 때 |
| **LLM gateway** | provider routing, cost, retry, policy | tool, memory, Desktop workspace를 소유하지 않음 | model traffic을 중앙화해야 할 때 |
| **Desktop AI assistant** | chat UI와 provider/tool integration | 장기 authored environment contract의 범위가 다를 수 있음 | chat 중심 개인 assistant가 충분할 때 |
| **Local model UI** | local inference와 model management | local-first workspace보다 inference locality가 중심 | data가 device 밖으로 나가면 안 되고 local model 운용이 우선일 때 |

> [!note] 비교의 한계
> 위 표는 제품별 최신 feature 수가 아니라 **주된 추상화 계층** 비교다. 각 제품은 빠르게 확장되므로 실제 도입 전 최신 문서로 겹치는 기능을 다시 확인한다.

## Build vs Adopt

| 질문 | holaOS 쪽으로 기울 때 | 다른 접근이 나을 때 |
|---|---|---|
| 작업 수명 | 며칠~수개월, 반복 resume | 한 번의 session |
| harness | 여러 harness/model 사이 portability 필요 | 하나의 agent CLI로 고정 |
| memory | continuity, knowledge, preference를 분리 | 작은 chat history로 충분 |
| integrations | Apps, MCP, brokered grant, health check 필요 | API 한두 개를 직접 호출 |
| automation | workspace context로 cron/event task 실행 | stateless batch script가 단순 |
| governance | authored policy와 execution truth 분리 | application code 하나로 관리 가능 |
| maturity | 초기 project 변화 감수 가능 | stable SLA와 장기 support 필수 |

## MCP와의 관계

MCP는 holaOS의 경쟁 기술이라기보다 capability transport다.

```text
workspace.yaml / mcp_registry
  → Runtime discovery + allowlist
  → capability projection
  → reduced execution package
  → Harness가 MCP tool 호출
```

holaOS가 추가하는 것은 다음 운영 경계다.

- 어느 workspace에서 server를 enable할지
- 어느 tool을 run에 노출할지
- App lifecycle과 health를 어떻게 관리할지
- integration credential을 어떤 grant/scope로 전달할지
- tool result와 진행 상태를 어느 memory/state 계층에 반영할지

MCP 자체의 protocol 개념은 [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]에서 별도로 학습한다.

## Provider and Locality

| 설정 | inference 위치 | 주의점 |
|---|---|---|
| OpenAI, Anthropic, Gemini, OpenRouter 등 | cloud provider | prompt, selected memory, tool result 등 관련 context가 provider로 전송될 수 있음 |
| Ollama | local machine | model 품질, hardware, context limit, 운영 부담을 직접 감당 |
| holaOS Proxy | proxy 경유 | proxy의 data handling, auth, logging 정책 확인 필요 |

따라서 **local-first workspace**와 **fully local inference**는 별개의 축이다.

## License Fit

repository의 Modified Apache 2.0은 내부 사용과 제3자 상용 제공을 다르게 취급한다.

| 사용 형태 | dossier 기준 해석 | 다음 행동 |
|---|---|---|
| 단일 조직 내부 사용 | commercial license 없이 허용 | 최신 LICENSE 원문 확인 |
| 개인 학습/실험 | 일반적으로 내부·직접 사용 범위 | 배포 방식이 바뀌면 재검토 |
| 제3자 대상 SaaS/managed service | 상당 부분을 제공하면 별도 commercial license 필요 가능 | 출시 전에 법률·상용 license 검토 |
| 상용 제품 embedded component | 제한 대상이 될 수 있음 | vendor에 사용 시나리오 확인 |

이 표는 법률 자문이 아니다. 특히 “상당 부분”과 제공 형태의 해석은 실제 license 원문과 배포 구조를 기준으로 검토한다.

## Decision Checklist

- [ ] 장기 continuity가 실제 문제인가, 아니면 prompt/session 정리로 충분한가?
- [ ] `pi` harness의 현재 기능이 필요한 workflow를 만족하는가?
- [ ] target platform의 설치 path를 직접 검증했는가?
- [ ] cloud provider로 전송되는 context 범위를 이해했는가?
- [ ] MCP allowlist의 empty/default semantics를 확인했는가?
- [ ] App integration scope와 approval 이후 실제 side effect를 test했는가?
- [ ] backup, export, migration과 runtime DB 복구 절차가 있는가?
- [ ] license가 내부 사용 또는 제품 배포 방식에 맞는가?

## Sources

- https://www.holaos.ai/docs/concepts/concepts
- https://www.holaos.ai/docs/concepts/workspace-model
- https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools
- https://www.holaos.ai/docs/concepts/memory-and-continuity
- https://www.holaos.ai/docs/getting-started/quick-start
- https://github.com/holaboss-ai/holaOS/blob/main/INSTALL.md
- https://github.com/holaboss-ai/holaOS

