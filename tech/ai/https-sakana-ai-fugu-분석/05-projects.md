---
date: 2026-06-23
tags:
  - tech
  - ai
  - fugu
  - sakana-ai
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# Sakana Fugu - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 1. Code Review Gate

### 목표

PR diff를 Fugu Ultra에 넣고 기존 static analyzer, SAST, test 결과와 교차검증한다.

| 항목 | 설계 |
|------|------|
| 입력 | PR diff, changed files, failing tests, dependency diff |
| 모델 | `fugu-ultra-20260615` for hard review, `fugu` for normal review |
| 출력 | blocking issues, severity, evidence, suggested fix |
| 평가 | 실제 bug 발견률, false positive, review latency |

```text
PR opened
  -> static analyzer/SAST
  -> Fugu review
  -> merge gate report
  -> human reviewer approval
```

### 산출물

- Markdown review report
- severity별 finding table
- evidence line reference
- "must fix before merge" checklist

---

## 2. Research Reproduction Agent

### 목표

논문 PDF, repo, dataset instruction을 주고 implementation/training/evaluation gap report를 생성한다.

| 입력 | 출력 |
|------|------|
| paper PDF | claimed method summary |
| official repo | missing implementation detail |
| dataset README | preprocessing/evaluation ambiguity |
| training log | reproduction risk |

```text
Paper + Repo + Dataset
  -> Fugu / Fugu Ultra
  -> Gap report
  -> Reproduction checklist
  -> Experiment plan
```

### 평가 기준

- 빠뜨린 hyperparameter를 찾아내는가
- figure/table claim과 code가 일치하는지 확인하는가
- 재현 불가능한 부분을 명확히 분리하는가
- 실행 가능한 next experiment를 제안하는가

---

## 3. Patent/Literature Landscape

### 목표

20개 이상 paper/patent를 넣고 claim map, novelty, overlap matrix를 만든다.

| 산출물 | 설명 |
|--------|------|
| Claim map | 문헌별 핵심 claim과 evidence |
| Novelty table | 새로움, 기존 기술 대비 차이 |
| Overlap matrix | claim 간 중복/충돌 |
| Risk notes | obviousness, prior art, terminology ambiguity |

```text
Documents
  -> chunk/index
  -> Fugu landscape analysis
  -> claim map
  -> human legal/technical review
```

> [!warning]
> 법률 판단을 자동화하지 않는다. Fugu 결과는 patent attorney나 domain expert가 검토할 technical briefing으로 둔다.

---

## 4. Security Assessment Assistant

### 목표

명확한 scope 안에서 recon, XSS/SQLi checklist, evidence, retest steps 보고서를 자동화한다.

| 항목 | 설계 |
|------|------|
| Scope | authorized asset, test account, allowed technique |
| 입력 | app docs, endpoint list, logs, scanner output |
| 출력 | finding, evidence, reproduction, retest steps |
| 제한 | exploit automation 금지, out-of-scope 금지 |

```text
Scanner output + app docs
  -> Fugu triage
  -> evidence-focused report
  -> retest checklist
```

### 평가 기준

- scope 밖 권고를 하지 않는가
- evidence와 추론을 분리하는가
- 재현 단계가 방어적 검증에 충분한가
- false positive를 줄이는가

---

## 5. Model Procurement Benchmark

### 목표

Fugu, 단일 frontier model, custom LangGraph/AutoGen agent를 동일 task suite로 비교해 enterprise model policy를 수립한다.

| 비교 대상 | 역할 |
|-----------|------|
| Fugu | managed multi-agent API |
| Fugu Ultra | high-quality hard task escalator |
| Single frontier model | latency/simple debugging baseline |
| Custom LangGraph/AutoGen | 직접 소유하는 orchestration baseline |
| LiteLLM/OpenRouter route | provider routing baseline |

```text
Private task suite
  -> all candidate systems
  -> deterministic + human evaluation
  -> cost/latency/quality dashboard
  -> procurement decision
```

### dashboard 지표

| 지표 | 설명 |
|------|------|
| success rate | task solved |
| critical recall | 중요한 issue 발견률 |
| hallucination rate | 없는 사실/코드/인용 생성 |
| cost per success | 성공 기준 비용 |
| p95 latency | interactive usability |
| compliance score | provider/model policy 만족 |

---

## 관련 노트

- [[study/tech/ai/autoresearch-study]] - research reproduction project 설계 참고
- [[study/tech/ai/litellm]] - procurement benchmark에서 provider gateway baseline
- [[study/tech/ai/multi-agent-platforms/autogen]] - custom multi-agent baseline
