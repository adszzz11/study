---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 02. Headroom Ecosystem

## 어디에 위치하는가

Headroom은 model, vector database, agent framework 자체가 아니다. application 또는 agent runtime과 model provider 사이에서 **전송할 context를 최적화하는 middleware**다.

```text
Data source → Agent / RAG framework → Headroom → Provider API → LLM
                  │                    │
                  └─ retrieval        └─ compression + CCR
```

## 접근법 비교

| 접근법 | 핵심 동작 | 장점 | 한계 | 적합한 상황 |
|---|---|---|---|---|
| Headroom | content-aware local compression + CCR | 구조별 처리, 원문 retrieval, proxy/wrapper/API 통합 | retrieval 조건과 자체 품질 평가 필요 | 큰 tool output이 반복되는 agent |
| Truncation | 앞/뒤 또는 token limit로 절단 | 단순하고 deterministic | error, JSON 구조, ordering 손실 가능 | 오래된 context를 버려도 되는 단순 flow |
| Generic summarization | LLM이 text를 요약 | 자연어 압축에 유연 | 별도 inference 비용·latency, 사실 손실 | narrative history 요약 |
| Retrieval / RAG | query와 관련된 chunk만 선택 | corpus 전체를 prompt에 넣지 않음 | retrieval miss, indexing 운영 | 큰 외부 knowledge corpus |
| Prompt caching | 반복 prefix의 계산 비용 재사용 | 동일 prefix의 경제성 개선 | context 자체 크기와 window는 그대로 | 안정적인 multi-turn prefix |
| Framework trimming | message history/window 정책 | framework에 밀착, 제어 단순 | payload 내부 구조까지 이해하지 못할 수 있음 | 기본 history 관리 |

이 접근법들은 서로 배타적이지 않다. 예를 들어 RAG가 고른 documents나 MCP가 반환한 rows를 Headroom으로 다시 줄이고, proxy `cache` mode로 provider prompt caching을 보존할 수 있다.

## Integration surface 비교

| Surface | 시작점 | 장점 | 주의점 |
|---|---|---|---|
| Transparent proxy | `headroom proxy --port 8787` | application 변경 최소화 | base URL, provider compatibility, telemetry 점검 |
| Agent wrapper | `headroom wrap codex` 등 | CLI agent에 빠르게 적용 | 실제 child process와 환경변수 전달 확인 |
| Python API | `compress(messages, model=...)` | application-level control | message schema와 failure fallback 설계 |
| TypeScript SDK | `await compress(...)` | JS/TS application에서 사용 | local proxy가 별도로 필요하며 CLI는 없음 |
| MCP server | compress/retrieve/stats tools | agent가 명시적으로 압축·복구 | tool permission과 호출 신뢰성 필요 |
| Framework adapter | LangChain, LangGraph 등 | 기존 pipeline에 결합 | adapter와 framework version compatibility 확인 |

## Headroom과 LiteLLM

[[litellm/README|LiteLLM]]은 여러 provider를 공통 API로 연결하고 routing, retry, budget 같은 gateway 기능을 제공한다. Headroom은 provider routing보다 **context payload 최적화**가 중심이다. 둘은 경쟁재라기보다 계층이 다르며 Headroom은 LiteLLM adapter를 제공한다.

| 질문 | Headroom | LiteLLM |
|---|---|---|
| 어떤 provider로 보낼까? | 주 관심사 아님 | 핵심 |
| 보내기 전에 context를 줄일까? | 핵심 | 주 기능 아님 |
| 원문을 local cache에서 재조회할까? | CCR | 별도 설계 필요 |
| multi-provider routing/retry | 제한적 | 핵심 |

## 선택 기준

1. **Token profile**: 총 prompt가 아니라 tool-generated payload 비중을 측정한다.
2. **Correctness**: representative tasks로 answer equivalence와 anomaly retention을 평가한다.
3. **Cache economics**: multi-turn이면 `cache`와 `token` mode의 실비용을 비교한다.
4. **Recovery path**: CCR tool이 실제 provider/agent 경로에서 호출되는지 failure injection으로 확인한다.
5. **Privacy**: local compression과 별개인 telemetry/Beacon 설정을 검토한다.
6. **Fallback**: proxy 또는 store 장애 시 passthrough할지 fail closed할지 정한다.

## Sources

- https://docs.headroomlabs.ai/docs
- https://docs.headroomlabs.ai/docs/architecture
- https://docs.headroomlabs.ai/docs/configuration
- https://docs.headroomlabs.ai/docs/ccr
- https://pypi.org/project/headroom-ai/
- https://www.npmjs.com/package/headroom-ai
