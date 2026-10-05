---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# fast-jev-compaction: Overview

## What

`fast-jev-compaction`은 agent transcript에서 과거 tool call과 결과를 call 단위로 정리하는 context-engineering 도구다. LLM이 대화를 새 prose summary로 바꾸는 대신, TypeSafe Jev가 각 `tool_use`와 `tool_result` pair의 필요성을 평가한다.

```text
Transcript → pair by tool_use_id → exclude pinned region → Jev decisions
                                                        ├─ keep
                                                        ├─ truncate
                                                        └─ drop
```

## Why

긴 session에는 전체 파일, `rg` 결과, build/test log가 누적된다. summary는 이력을 짧게 만들지만 file path·error text·command·제약을 생략하거나 바꿀 수 있다. 이 접근은 아직 필요한 tool evidence를 원문으로 남기는 데 초점을 둔다.

## 핵심 특징

| 특징 | 의미 |
|---|---|
| Pair integrity | `tool_use`와 `tool_result`를 함께 처리해 dangling result를 만들지 않는다. |
| Dual decision | call 자체의 필요성과 result 원문의 필요성을 별도로 묻는다. |
| Pinned context | 첫 메시지와 최근 `preserveRecentMessages`(기본 6개)는 보존한다. |
| State fitting | 입력이 `maxStateTokens`(기본 25,000)를 넘으면 input 축소 → text head/tail abridgement → 오래된 message collapse를 시도한다. |
| Batching | 기본 30,000 estimated tokens 상한으로 질문을 나누고 병렬 결과를 병합한다. |
| Fallback | key 누락·Jev 오류·malformed response·state 초과·감소 부족이면 Claude Code built-in summary로 되돌린다. |

## 한계

- 남긴 record만 verbatim일 뿐, 삭제 결정까지 정확하다는 보장은 없다.
- history rewrite와 외부 API latency/cost가 생긴다.
- 공개 저장소 기준 실험적 community project로 보며 production standard로 단정하지 않는다.

## 다음

- [[02-ecosystem|Ecosystem 비교]]
- [[04-learning/02-deep-dive|판정과 재구성 흐름]]
