---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Perplexity Decider for Mac overview

## What

**Perplexity Decider for Mac**은 menu bar에서 동작하는 local inference app이다. `pplx-decider-flash-v1.2` 4B 모델을 실행하고 `http://127.0.0.1:8080/v1/decisions`에 Decisions API를 제공한다. API key와 usage bill 없이 `state`와 named question을 전송하면 생성 문장이 아니라 확률형 답을 받는다.

## Why

“이 티켓은 어느 팀이 담당해야 하는가?”를 chat LLM에 물으면 설명 텍스트를 다시 parse해야 한다. 그 과정은 output format, 일관성, 비용, 민감 데이터 전송 문제를 만든다. Decider는 후보와 rubric을 request에서 고정하고 code가 직접 비교할 수 있는 숫자를 반환한다.

특히 고객 export, meeting note, source diff, 내부 screenshot처럼 hosted API로 보내기 곤란한 자료를 local에서 반복 평가할 수 있다. 이후 scale 또는 높은 품질이 필요하면 hosted endpoint로 옮길 수 있지만, model/serving 차이가 있으므로 threshold를 다시 검증해야 한다.

## 핵심 특징

| 영역 | 내용 |
|---|---|
| local network | loopback `127.0.0.1`만 기본 사용하므로 외부 network에 직접 노출되지 않는다. |
| model | Qwen3.5-4B 기반 4B `pplx-decider-flash-v1.2`; 27B Decider의 probability distribution을 distillation했다. |
| input | text, JSON, image를 `state`로 보낸다. 첫 실행 때 약 5.8 GB Q8_0 GGUF weights와 F16 vision projector를 내려받는다. |
| output | `noul`, `choice`, `score`의 typed probability로 thresholding과 queue routing에 쓴다. |
| requirements | M1+, macOS 13+, 16 GB RAM, 약 6 GB 여유 디스크가 필요하다. Intel Mac/Windows/Linux은 앱 대상이 아니다. |

## Decision type

| Type | 질문 형태 | 핵심 반환값 | 예 |
|---|---|---|---|
| `noul` | yes/no | `P(true)` 0~1 | secret이 포함됐는가? |
| `choice` | 정의한 option 중 하나 | option별 probability, 최고 choice, confidence | billing / shipping / technical |
| `score` | 순서가 있는 rubric | level별 probability, expected score | low / medium / high severity |

## 아키텍처와 경계

```text
private text / JSON / screenshot
              │ state + one named question
              ▼
Decider for Mac ── localhost Decisions API ──► typed probability
              │                                      │
              └─ Flash 4B local inference       threshold / review queue
```

Flash는 질문 하나당 request 하나가 기본이다. 여러 question을 넣어도 Flash는 각각 독립 처리하며 `state` 처리도 question별로 발생한다. 반면 hosted 27B는 관련 question을 joint inference로 다룰 수 있다.

## Runtime 주의

공개 GGUF가 있다고 해서 일반 `llama.cpp` server가 자동으로 호환된다고 가정하지 않는다. 이 checkpoint는 protocol v3, non-causal/full-attention, marker별 readout을 요구한다. local app을 공식 runtime으로 사용하는 편이 안전하다.

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
- https://huggingface.co/perplexity-ai/pplx-decider-flash-gguf-v1.2
- https://huggingface.co/perplexity-ai/pplx-decider-v1.2
