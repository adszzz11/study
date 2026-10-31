---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - projects
  - repairable-agents
type: tech-tool-study
parent: "[[README]]"
---

# Hankweave - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 1. Research dossier generator

긴 research workflow를 gather → verify → synthesize → citation sentinel → final report로 분리한다.

| Codon | 역할 | Output |
|-------|------|--------|
| `gather` | 공식 문서, source, issue, blog 수집 | `work/sources.md` |
| `verify` | 주장과 source 매칭, 오래된 정보 표시 | `work/verified-facts.json` |
| `synthesize` | dossier 초안 작성 | `work/draft.md` |
| `finalize` | 최종 report 생성 | `results/report.md` |

Sentinel:

- missing citation sentinel
- source freshness sentinel
- contradiction sentinel

```text
Use case: 기술 조사, vendor evaluation, 공개 repo 분석
핵심 가치: citation 누락과 context drift를 별도 observer가 잡는다.
```

## 2. Data codebook builder

CSV/schema observation → Zod schema generation → annotation → diagram/report output으로 구성한다.

| Codon | 역할 | Output |
|-------|------|--------|
| `observe-schema` | CSV column, null, sample, distribution 관찰 | `work/schema-observation.md` |
| `generate-zod` | Zod schema 초안 생성 | `work/schema.ts` |
| `annotate` | column description, caveat, data quality note 작성 | `work/codebook.md` |
| `report` | 최종 codebook과 diagram 생성 | `results/codebook.md` |

운영 포인트:

- 원본 dataset은 read-only mount
- generated schema는 checkpoint
- sentinel은 PII, missing description, suspicious type inference 감시

## 3. Legacy migration assistant

source scan → migration plan → codon별 conversion → validation → rollback 패턴이다.

| Codon | 역할 | Output |
|-------|------|--------|
| `scan` | legacy structure와 dependency 조사 | `work/inventory.md` |
| `plan` | migration sequence 작성 | `work/migration-plan.md` |
| `convert-module-a` | 모듈 단위 변환 | source changes |
| `validate` | test/build/lint 실행 결과 정리 | `work/validation.md` |

Hankweave가 유용한 이유:

- 모듈 단위 checkpoint로 rollback 가능
- codon별 budget과 failure policy 설정 가능
- convention sentinel이 style drift를 감시

## 4. Long-running data mining pipeline

read-only dataset mount → batch research loop → event journal audit → archived outputs 구조다.

```text
/data        read-only input
/executions  resumable run state
/results     exported artifacts
```

| 관심사 | 설계 |
|--------|------|
| 재실행 | batch마다 codon/checkpoint 분리 |
| 감사 | JSONL event journal 보존 |
| 비용 | batch/codon budget, run `--max-cost` |
| 품질 | drift, duplicate, citation sentinel |

## 5. AI workflow CI job

Docker로 hanks를 실행하고 `/executions` volume으로 resume state를 유지하며 `/results`로 final artifact를 export한다.

```yaml
steps:
  - run: bunx hankweave@latest --validate
  - run: bunx hankweave@latest --headless --autostart --max-cost 10
  - uses: actions/upload-artifact
    with:
      name: hankweave-results
      path: results/
```

적합한 작업:

- nightly research report
- release note synthesis
- data quality audit
- docs migration draft
- competitor monitoring

## 6. 프로젝트 선택 기준

| 프로젝트 | 처음 해보기 좋음 | Hankweave 가치 |
|----------|------------------|----------------|
| Research dossier | 높음 | citation sentinel, codon handoff 실습 |
| Data codebook | 중간 | read-only data, schema validation |
| Legacy migration | 높음 | checkpoint/rollback 가치가 큼 |
| Data mining pipeline | 낮음 | long-run observability 실습 |
| CI job | 중간 | headless, volume, artifact export |

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - data/API tool을 agent에게 노출하는 방법
- [[study/tech/ai/lazy-codex]] - coding workflow 검증 루프
- [[study/tech/data/dolt]] - data versioning과 checkpoint 관점 비교
- [[study/tech/infra/prefect]] - pipeline orchestration 비교
