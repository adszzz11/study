---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# 카카오 P-14519 Agentic Search Platform tool study

> **한 줄 정의**: 이 포지션은 LLM Agent, 검색 랭킹, 검색 데이터 품질을 결합해 실제 서비스에서 답을 찾고 검증하는 `Agentic Search Platform`을 연구·서비스화하는 AI Research Engineer 역할이다.

## Overview

카카오의 상품·장소·웹 문서·대화 데이터는 형식과 의도가 다르다. 이 노트는 단순 `keyword match`를 넘어 `Planning → Search/Browse → Tool Calling → Answer`로 이어지는 검색 시스템의 용어와 설계 판단을 정리한다.

- `Agentic Search LLM`: 도구 사용과 답변 합성을 결정한다.
- `Search Ranking Model`: 많은 후보 중 관련 결과를 위로 올린다.
- `Search Data Modeling`: spam·중복·잘못된 속성을 줄여 입력 품질을 높인다.
- 목표는 benchmark 최고점만이 아니라 latency, 비용, 안전성, 사용자 만족을 포함한 production 품질이다.

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 문제와 end-to-end 구조를 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)에서 작은 hybrid retrieval을 만든다.
- [ ] [02-ecosystem](./02-ecosystem.md)에서 retrieval·ranking·agent 실행 방식의 trade-off를 비교한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)에서 RL, 평가, data quality를 연결한다.
- [ ] [05-projects](./05-projects.md)의 실습으로 로그 기반 평가와 guardrail을 추가한다.
- [ ] [cheatsheet](./cheatsheet.md)로 면접·설계 리뷰 전 핵심 용어를 복습한다.

## When To Use

- 하나의 답을 위해 검색, browse, API 같은 여러 도구를 순서 있게 호출해야 할 때
- 키워드 정확도와 의미 유사도를 함께 확보하는 상품·장소·문서 검색이 필요할 때
- 대규모 검색 로그와 data quality 개선을 retrieval/ranking 품질로 연결할 때

## When Not To Use

- 단일 DB lookup처럼 도구 선택이나 검색 후보 생성이 필요 없는 결정적 질의일 때
- 최신성·근거 검증이 중요한데 출처 없는 자유 생성만 허용하는 경우
- offline benchmark만 있고 실제 트래픽, latency budget, human evaluation을 검증할 수 없는 상태에서 production 성능을 주장할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-garden|Agent Garden]]

## Sources

- https://careers.kakao.com/jobs/P-14519
- https://openreview.net/forum?id=Oljnxmf4pc
- https://arxiv.org/abs/2505.23006
- https://arxiv.org/abs/1706.03762
- https://arxiv.org/abs/1707.06347
