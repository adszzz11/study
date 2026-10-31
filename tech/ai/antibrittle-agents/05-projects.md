---
date: 2026-06-24
tags:
  - tech
  - ai
  - agents
  - projects
  - reliability
type: tech-tool-study
parent: "[[README]]"
---

# Antibrittle Agents - 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 1. Deep Research Agent

긴 research pipeline에 source crawling, evidence receipts, domain diversity run box, citation audit를 넣는다.

| 항목 | 설계 |
|------|------|
| Runtime | OpenAI Agents SDK 또는 LangGraph |
| Trenches | query generation, source selection, evidence extraction, synthesis, citation audit |
| Run box | source diversity, link-follow depth, repeated failed fetch |
| Receipts | source URL, quote/excerpt pointer, retrieval timestamp, claim mapping |

```text
query_set.json
selected_sources.json
evidence_table.md
claim_receipts.json
final_report.md
```

---

## 2. Financial Reconciliation Agent

CSV/DB/API를 읽고 discrepancy를 추적하되, 모든 판단에 receipt와 reproducible script를 남긴다.

| 항목 | 설계 |
|------|------|
| Input | bank CSV, ledger DB, payment API |
| Tool minimalism | read file, query DB, run script, write report |
| Receipts | row id, query hash, script path, output checksum |
| Human interruption | write-back, adjustment, irreversible close |

```python
receipt = {
    "claim": "invoice INV-1042 is duplicated",
    "source_rows": ["bank.csv:182", "ledger:invoice:INV-1042"],
    "script": "scripts/reconcile.py",
    "output_hash": "sha256:..."
}
```

---

## 3. Code Maintenance Agent

repo 분석, patch, test, rollback point, trace를 LangGraph/OpenAI Agents SDK로 구성한다.

| Trench | Artifact |
|--------|----------|
| Repo scan | relevant files, symbols, failing tests |
| Patch plan | target files, invariants, rollback point |
| Edit | diff, changed files |
| Verify | test output, lint output, manual checks |
| Report | summary, residual risk |

Run box metric:

- repeated failed command count
- changed file count
- test coverage touched
- unresolved TODO count
- final claim receipt coverage

---

## 4. Data Mining / Indexing Agent

heterogeneous document를 chunking/RAG에 바로 넣지 않고, agent가 schema discovery, normalization, provenance graph를 구축한다.

| 단계 | Antibrittle 포인트 |
|------|--------------------|
| Schema discovery | exploration region으로 여러 sample 조사 |
| Normalization | deterministic script와 receipt 남김 |
| Provenance graph | document -> chunk -> field -> claim 연결 |
| Indexing | 실패 row와 skipped field 기록 |

```text
raw_docs/
schemas/
normalized/
provenance_graph.json
index_manifest.json
```

---

## 5. Agent Reliability Harness

동일 작업을 N회 반복 실행하고 outcome consistency, trajectory variance, cost variance, harmful action rate를 리포트한다.

| Metric | 설명 |
|--------|------|
| Outcome consistency | 반복 실행 결과가 얼마나 같은가 |
| Trajectory variance | tool path와 loop 수가 얼마나 흔들리는가 |
| Cost variance | latency/token/cost 편차 |
| Robustness | perturbation에도 성공하는가 |
| Harmful action rate | 위험 action 시도 빈도 |
| Receipt coverage | 핵심 claim 중 receipt 연결 비율 |

```yaml
suite:
  task: code-maintenance-small
  repeats: 10
  perturbations:
    - paraphrase
    - tool_timeout
    - missing_field
  metrics:
    - outcome_consistency
    - trajectory_variance
    - cost_variance
    - receipt_coverage
```

---

## 프로젝트 선택 기준

| 원하는 학습 | 추천 프로젝트 |
|-------------|---------------|
| receipts와 citation audit | Deep Research Agent |
| reproducibility와 audit | Financial Reconciliation Agent |
| real-world agent loop | Code Maintenance Agent |
| provenance graph | Data Mining / Indexing Agent |
| reliability measurement | Agent Reliability Harness |

---

## 관련 노트

- [[study/tech/ai/autoresearch-study]] - research automation 프로젝트와 연결
- [[study/tech/ai/lazy-codex]] - code maintenance 검증 harness
- [[study/tech/ai/llm-wiki-study]] - indexing/provenance 지식 관리
- [[study/tech/ai/model-context-protocol-mcp]] - tool/data access layer
