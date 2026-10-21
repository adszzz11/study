---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started: baseline RAG

## 1. 작고 검토 가능한 corpus를 고른다

Markdown/PDF 문서 10~50개처럼 원문을 사람이 확인할 수 있는 corpus로 시작한다. 각 chunk에 `document_id`, `version`, `section`, `source_url`, `acl`, `updated_at` metadata를 붙인다. parsing 오류나 오래된 문서를 retrieval 오류로 오인하지 않기 위해서다.

## 2. 최소 pipeline을 만든다

```text
documents → parse → chunk → embed/index
question → ACL filter → hybrid retrieve → rerank → prompt → answer with citations
```

처음부터 agent나 graph를 더하지 않는다. vector retrieval만 시작한 다음 BM25/vector hybrid, query rewrite, reranker를 한 항목씩 추가해 효과를 비교한다.

## 3. evaluation set을 먼저 만든다

질문 30~100개에 다음을 기록한다.

| 필드 | 의미 |
|---|---|
| question | 실제 사용자가 할 질문 |
| expected answer | 검토 가능한 정답 또는 채점 기준 |
| required evidence | 반드시 검색되어야 할 문단/문서 |
| query type | fact, comparison, temporal, multi-hop 등 |
| ACL context | 검색 권한 조건 |

측정값은 answer correctness뿐 아니라 **context recall**, citation correctness, p50/p95 latency, token cost다. citation이 존재하는지와 citation이 주장을 실제로 지지하는지는 별도 항목으로 채점한다.

## 4. 실험 matrix

| 변수 | 시작값 | 바꿔 볼 값 |
|---|---|---|
| chunking | heading/문단 경계 | size, overlap, parent-child |
| retrieval | vector top-k | BM25 hybrid, metadata filter |
| ranking | top-k 직접 사용 | reranker, top-n 축소 |
| generation | 원문 인용 지시 | abstain, citation format |

한 번에 하나만 바꾸고 같은 set으로 재실행한다. retrieval trace와 최종 context를 저장하면 답변 실패를 검색 실패·생성 실패·citation 실패로 나눌 수 있다.

## Sources

- https://arxiv.org/abs/2005.11401
- https://docs.langchain.com/oss/python/learn
