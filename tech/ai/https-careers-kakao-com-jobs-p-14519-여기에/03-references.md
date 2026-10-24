---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## 공고와 카카오 연구

1. [카카오 채용 공고 P-14519](https://careers.kakao.com/jobs/P-14519) — 역할, 요구 기술, 적용 제품을 확인하는 원문.
2. [OrchestrationBench: LLM-Driven Agentic Planning and Tool Use in Multi-Domain Scenarios](https://openreview.net/forum?id=Oljnxmf4pc) — agent planning과 tool use 평가 맥락.
3. [Workflow Graphs 기반 Production Conversational Agent — ACL 2025 Industry Track](https://arxiv.org/abs/2505.23006) — production agent orchestration 사례.

## 검색·학습 기초

4. [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Transformer의 원 논문.
5. [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) — PPO의 clipping 기반 policy update.
6. [Sentence Transformers: Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) — bi-encoder와 cross-encoder의 2단계 검색 설명.
7. [MTEB](https://github.com/embeddings-benchmark/mteb) — embedding 평가 task와 실행 체계.
8. [BrowseComp](https://browsecomp.github.io/) — 전략적 browsing이 필요한 web research benchmark.

## 읽는 순서

공고로 문제 범위를 고정한 뒤 retrieve-rerank 문서로 pipeline을 이해한다. 다음으로 PPO와 agent benchmark를 읽어 policy·평가의 한계를 익히고, 마지막으로 공개 benchmark 결과를 product log와 online metric으로 검증하는 실험을 설계한다.
