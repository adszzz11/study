---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# References

## Foundational papers

1. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — Lewis et al.](https://arxiv.org/abs/2005.11401)
2. [Don’t Do RAG: When Cache-Augmented Generation Is All You Need — Chan et al.](https://arxiv.org/abs/2412.15605)
3. [KAG: Boosting LLMs in Professional Domains via Knowledge Augmented Generation](https://arxiv.org/abs/2409.13731)
4. [From Local to Global: A Graph RAG Approach — Microsoft Research](https://arxiv.org/abs/2404.16130)

## Implementations and documentation

1. [OpenSPG/KAG GitHub repository](https://github.com/OpenSPG/KAG)
2. [KAG official documentation](https://openspg.github.io/v2/)
3. [Microsoft GraphRAG documentation](https://microsoft.github.io/graphrag/get_started/)
4. [OpenAI Prompt Caching guide](https://developers.openai.com/api/docs/guides/prompt-caching)
5. [vLLM Automatic Prefix Caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/)
6. [LangChain RAG Agent learning resources](https://docs.langchain.com/oss/python/learn)

## 읽는 순서

RAG 원 논문으로 retrieval-augmented memory의 출발점을 확인한 뒤 CAG 논문으로 적용 전제를 읽는다. 다음으로 KAG와 GraphRAG 문서에서 graph 기반 설계의 비용과 query 유형을 비교한다. 구현 전에는 prompt cache 문서로 provider semantics와 cache 조건을 확인한다.

## Sources

- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2412.15605
- https://arxiv.org/abs/2409.13731
- https://microsoft.github.io/graphrag/get_started/
