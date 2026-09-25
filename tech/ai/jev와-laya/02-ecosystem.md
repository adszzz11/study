---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev와 laya Ecosystem

> [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 선택지 비교

| 선택지 | 강점 | 트레이드오프 | 적합한 경우 |
|---|---|---|---|
| Jev | managed API, typed primitive, 빠른 integration | vendor·network 의존, weights 비공개 | 운영 부담 없이 decision layer를 도입할 때 |
| laya | self-host, Apache-2.0, offline/egress 통제, MCP·FastAPI 지원 | calibration·infra·fine-tuning 책임 | 데이터 경계가 엄격하거나 on-prem이 필요할 때 |
| LLM Structured Outputs / JSON mode | 범용 reasoning·생성·복잡한 문맥 해석 | 느리거나 비쌀 수 있고, schema가 판단 품질·calibration을 보장하지 않음 | 자유 서술, 장문 reasoning, 새 class가 필요할 때 |
| fine-tuned classifier / BERT | 좁고 고정된 task의 latency·cost 최적화 | 데이터·학습 pipeline 필요, 범용 question interface 부족 | label schema가 안정적이고 traffic이 클 때 |
| rules / policy engine | 결정성·감사성 | 의미 해석과 예외에 약함 | 명확한 compliance rule 또는 최종 승인 gate |

## Jev 또는 laya

| 질문 | Jev 쪽 | laya 쪽 |
|---|---|---|
| 운영을 최소화해야 하는가? | 적합 | 모델/serve 운영 필요 |
| network egress가 허용되는가? | API 호출 필요 | local 배치 가능 |
| weights·license 검토가 필요한가? | proprietary | Apache-2.0 |
| 언어 다양성이 큰가? | 공개 동등 multilingual benchmark 정보는 제한적 | 100+ 언어 지향 Router 제공 |
| 자체 calibration과 fine-tuning을 할 수 있는가? | domain validation은 여전히 필요 | 특히 중요 |

## 성능 주장 읽는 법

laya repository의 T4 측정은 질문당 약 33–39.5ms, batch에서는 질문당 약 7ms 수준으로 소개된다. 이는 vendor/repository 측정치이며 input 길이, batch, hardware, checkpoint에 따라 달라진다. hosted Jev API latency와 직접 동등 비교하지 않는다.

> [!WARNING]
> laya의 base checkpoint zero-shot 성능을 production gate의 근거로 삼지 않는다. held-out data에서 temperature calibration, accuracy, coverage, false-positive cost를 확인한 뒤 rollout한다.

## 결정 예시

```text
명확하고 결정적인 규칙인가? ─ yes → rules/policy engine
                 │ no
자유 설명·깊은 추론이 필요한가? ─ yes → generative LLM
                 │ no
egress/weight 통제가 중요한가? ─ yes → laya + evaluation
                 │ no
운영을 최소화해야 하는가? ─ yes → Jev + evaluation
                 │ no
고정 label·대량 traffic인가? ─ yes → fine-tuned classifier도 비교
```

## Sources

- https://docs.typesafe.ai/introduction
- https://github.com/NandhaKishorM/laya
- https://github.com/NandhaKishorM/laya/blob/main/BENCHMARKS.md
