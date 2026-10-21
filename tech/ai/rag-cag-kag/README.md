---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# RAG · CAG · KAG tool study

> **한 줄 정의**: RAG는 질의 시 외부 지식을 검색해 LLM에 주입하고, CAG는 제한된 지식 전체의 KV cache를 미리 적재하며, KAG는 Knowledge Graph·논리 추론·검색을 결합해 전문 도메인 질의에 답하는 knowledge-augmented generation 계열이다.

## Overview

LLM의 parametric knowledge만으로는 최신 사내 문서, 근거 추적, 관계가 복잡한 전문 지식을 안정적으로 다루기 어렵다. 이 노트는 corpus의 크기·변경 빈도·질의 반복성·관계 추론 필요성에 맞춰 RAG, CAG, KAG/GraphRAG를 선택하는 기준을 정리한다.

- **RAG**: 큰 corpus와 잦은 갱신의 기본값이다. 검색 품질이 답변 품질의 상한이므로 평가가 먼저다.
- **CAG**: 작고 비교적 정적인 공유 corpus에 반복 질의가 많을 때 KV cache로 prefill을 재사용한다.
- **KAG/GraphRAG**: multi-hop 관계, 규칙, entity constraint가 실제 실패 원인일 때 확장한다.

## Learning Path

- [ ] [01-overview](./01-overview.md)에서 세 접근의 문제와 구조를 이해한다.
- [ ] [04-learning/01-getting-started](./04-learning/01-getting-started.md)으로 작은 corpus의 baseline RAG와 evaluation set을 만든다.
- [ ] [02-ecosystem](./02-ecosystem.md)에서 corpus 특성별 선택 기준을 비교한다.
- [ ] [04-learning/02-deep-dive](./04-learning/02-deep-dive.md)에서 CAG benchmark와 KAG/GraphRAG 확장 조건을 검증한다.
- [ ] [05-projects](./05-projects.md) 중 실제 업무에 가까운 프로젝트 하나를 구현한다.
- [ ] [cheatsheet](./cheatsheet.md)를 배포 전 설계·운영 점검표로 사용한다.

## When To Use

- 최신 문서와 출처가 필요한 enterprise search/Copilot에는 RAG부터 시작할 때
- corpus가 context window에 들어가고 공유 prefix가 반복되는 지원 봇에는 CAG를 비교할 때
- 계약·규정처럼 관계와 예외 조항을 여러 단계로 따라가야 하는 전문 질의에는 KAG/GraphRAG를 검토할 때

## When Not To Use

- 지식 갱신이나 근거 제시가 필요 없는 고정된 출력 형식·행동 최적화만이 목적일 때: fine-tuning을 먼저 검토한다.
- 소량의 원문을 한 번만 분석할 때: long-context prompting이 더 단순할 수 있다.
- graph가 필요하다는 증거 없이 entity extraction과 ontology 운영을 추가하려 할 때: baseline RAG failure를 먼저 측정한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/docling/README|Docling]]

## Sources

- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2412.15605
- https://arxiv.org/abs/2409.13731
- https://microsoft.github.io/graphrag/get_started/
- https://developers.openai.com/api/docs/guides/prompt-caching
