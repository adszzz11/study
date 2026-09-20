---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Failure와 AI System Design

## Distributed systems 연습

chat 또는 notification system을 대상으로 아래 failure scenario를 설계에 추가한다.

| 주제 | 확인할 질문 | 구현 힌트 |
| --- | --- | --- |
| fan-out | 한 이벤트를 누가, 어디까지 받는가? | fan-out on write/read를 비교 |
| ordering | 사용자별 순서가 필요한가? | partition key와 sequence 사용 |
| retry | 재시도는 언제 멈추는가? | exponential backoff와 retry budget |
| idempotency | 중복 전달을 어떻게 무해하게 하는가? | idempotency key 또는 dedup store |
| DLQ | 계속 실패한 메시지는? | 원인 보존, replay 절차, alert |
| observability | 무엇을 측정하는가? | queue lag, error rate, delivery latency |

`at-least-once delivery`는 중복 가능성을 뜻한다. consumer가 idempotent하지 않다면 retry가 성공률 대신 이중 발송을 만들 수 있다.

## AI Track: RAG 설계

```text
documents → ingestion → chunking → embedding → vector database
user query → retrieval → reranking → LLM → cited response
                         ↘ evaluation / tracing / cost metrics
```

### 설계 체크포인트

1. ingestion에서 source, version, access policy를 보존한다.
2. chunking과 embedding model 선택을 offline evaluation set으로 비교한다.
3. retrieval 뒤 reranking을 적용할지 latency와 quality로 판단한다.
4. 답변에는 citation을 남기고 hallucination/unsupported answer를 측정한다.
5. tracing으로 prompt, retrieved context, model latency, token cost를 연결한다.
6. untrusted document와 user input 모두에 대해 prompt-injection을 가정하고, instruction/data 분리와 red teaming을 수행한다.

## 45분 Mock Interview

| 시간 | 활동 | 산출물 |
| --- | --- | --- |
| 0–5분 | requirements 확인 | functional/non-functional 요구사항 |
| 5–15분 | high-level design | component diagram, 핵심 API |
| 15–35분 | deep dive | bottleneck, data model, failure handling |
| 35–45분 | wrap-up | trade-off, metrics, scale/migration 계획 |

발표 뒤 [[../cheatsheet]]의 질문으로 빈칸을 찾는다.

## Sources

- https://blog.bytebytego.com/p/our-new-book-generative-ai-system
- https://live.bytebytego.com/courses/ai-evals
- https://live.bytebytego.com/
