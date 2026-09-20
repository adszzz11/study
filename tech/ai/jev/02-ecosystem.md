---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev Ecosystem

> [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 비교

| 선택지 | 강점 | Jev보다 적합한 경우 | 한계 |
|---|---|---|---|
| Jev / System One | typed probability, parallel question evaluation, low-latency 목표 | 정해진 action space의 routing·triage·scoring·guardrail | prose/code 생성, 긴 reasoning에는 부적합 |
| Generative LLM + Structured Output | 자유로운 생성·설명·넓은 task coverage | option 발견, 사용자 문장·code 생성 | parsing/validation, latency·비용, output control 필요 |
| Rule engine | 결정론적, explainable, 저렴 | 조건이 명확하고 안정된 policy | 언어 의미·모호한 새 표현에 취약 |
| classifier / embedding model | domain batch classification·retrieval | labeled data와 안정된 taxonomy | retraining·label 운영, context 판단 한계 |
| LLM-backed System One adapter | Jev contract를 유지한 fallback/eval | Jev 도입 전 interface·threshold 실험 | Jev의 speed/cost 특성을 보장하지 않음 |

## 선택 가이드

- **Rule first**: 명확한 authorization, compliance constraint, deterministic routing은 rule engine으로 고정한다.
- **Jev next**: language context가 필요하지만 출력 action space가 닫혀 있으면 Jev를 둔다.
- **LLM last**: open-ended 생성이나 reasoning이 필요할 때 선택한다.
- **Human override**: low confidence, high impact, ambiguous input은 review queue로 보낸다.

## Adapter의 의미

공식 LLM-backed System One adapter는 Jev와 같은 interface를 local/evaluation 환경에서 유지하는 선택지다. 이 경우에도 model latency, cost, output calibration은 underlying LLM에 좌우된다. adapter 결과를 Jev 성능의 proxy로 일반화하지 않는다.

## Sources

- https://github.com/typesafe-ai/system-one-adapter-python
- https://docs.typesafe.ai/introduction
- https://typesafe.ai/blog/introducing-system-one-models-and-jev
