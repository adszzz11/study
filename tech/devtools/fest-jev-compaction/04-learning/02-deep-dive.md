---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive

## 판정·재구성 흐름

```text
Agent transcript
  └─ tool_use ↔ tool_result (tool_use_id로 pairing)
       └─ pinned 영역 제외
            └─ Jev에 대화 state + call별 두 질문
                 ├─ call을 알아야 하는가?
                 └─ result 원문이 필요한가?
                      └─ threshold로 재구성
                           ├─ keep: call + result verbatim
                           ├─ truncate: call + result 앞부분 + 안내문
                           └─ drop: call + result 함께 제거
```

## State fitting

Jev 요청의 state가 기본 `maxStateTokens=25,000`을 넘으면 다음 순서로 축소한다.

1. tool input을 축소한다.
2. text의 head/tail abridgement를 적용한다.
3. 오래된 message를 collapse한다.
4. 그래도 맞지 않으면 실패하고 fallback한다.

이 순서는 판정기의 context 자체가 필요 evidence를 잃을 수 있음을 뜻한다. 따라서 “compaction 결과가 좋아 보인다”와 “판정이 충분한 state를 봤다”를 분리해 기록한다.

## Batching과 failure path

- 기본 request 상한은 30,000 estimated tokens다. 질문을 batch로 나누고 병렬 요청한 결과를 병합한다.
- API key 누락, Jev error, malformed response, state 초과, reduction 부족은 Claude Code built-in summary fallback 조건이다.
- 운영 환경에서는 fallback 발생률, 원인, 원본 transcript 보존 여부를 audit한다.

## 측정

| 지표 | 질문 |
|---|---|
| Token reduction | context는 얼마나 줄었는가? |
| Tool reruns | 삭제한 evidence 때문에 command를 다시 실행했는가? |
| Task success rate | 실제 debugging/수정 성공률은 유지됐는가? |
| Evidence rediscovery time | drop된 path/error를 찾는 데 얼마나 걸렸는가? |
| Latency / API cost | compaction 판정이 얻는 이득보다 비싼가? |
| Prompt-cache impact | rewrite가 cache 효율을 악화시키는가? |

## 권장 실험군

- 정확한 failing stack trace와 source read가 중요한 debugging task
- 최신 output만 대체로 중요한 exploratory task

두 군을 같은 trajectory와 native compaction baseline으로 비교한다.
