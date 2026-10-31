---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Agentic Design Patterns tool study

> **한 줄 정의**: 《Agentic Design Patterns》는 LLM 기반 AI agent를 서비스에 적용하기 위한 21개 architecture/design pattern과 runnable code를 담은 실습형 가이드다.

## Overview

Instagram 릴에서 소개한 책은 Antonio Gullí의 **《Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems》**다. Springer가 2025년에 출간한 424쪽 책으로, 단일 prompt 호출을 넘어 tool 호출, 계획, 상태, 복구, 안전 검토를 갖춘 agent system을 설계하는 언어를 제공한다.

- 릴의 “AI 에이전트 교과서 / 424쪽” 설명과 부합한다.
- Springer 공식판은 유료 eBook/softcover다. 저자가 공유한 공개 초안·자료와 정식 출간본을 혼동하지 않는다.
- 핵심은 agent를 먼저 고르는 것이 아니라 예측 가능성, cost, latency, human approval을 기준으로 가장 작은 pattern을 택하는 것이다.

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 workflow와 agent의 문제 범위를 구분한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)에서 Prompt Chaining과 typed Tool Use를 구현한다.
- [ ] RAG에 source citation과 평가셋을 추가한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)에서 state, memory, HITL, guardrail을 연결한다.
- [ ] [02-ecosystem](./02-ecosystem.md)으로 framework와 protocol의 역할을 비교한다.
- [ ] [05-projects](./05-projects.md)의 single-agent 프로젝트를 평가한 뒤에만 multi-agent로 확장한다.

## When To Use

- API, DB, 검색 같은 외부 tool과 다단계 의사결정이 필요한 업무 자동화를 설계할 때
- RAG, retry, human approval, trace/evaluation을 포함한 production agent의 설계 리뷰를 할 때
- LangGraph, CrewAI, Google ADK 중 무엇을 쓸지보다 재사용 가능한 pattern부터 학습할 때

## When Not To Use

- 정해진 입력-출력 변환 하나면 충분한 경우: 일반 code 또는 고정 workflow가 더 단순하다.
- 오류 비용이 큰 write action인데 approval, audit, least-privilege tool 권한을 설계할 수 없는 경우
- 아직 single-agent의 prompt, tool schema, evaluation을 검증하지 않은 상태에서 multi-agent를 도입하려는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/mark-it-down/README|MarkItDown]]

## Sources

- https://link.springer.com/book/10.1007/978-3-032-01402-3
- https://www.instagram.com/reel/De-WKUCy-9d/
- https://www.anthropic.com/research/building-effective-agents
- https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
