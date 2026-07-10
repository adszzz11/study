---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# GPT-5.6 / Codex 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[cheatsheet|다음: 치트시트]]

---

## 1. Legacy repo migration

### 목표

Codex cloud에서 branch별 병렬 refactor를 실행하고, `AGENTS.md`로 test/lint 규칙을 고정한다.

### 구성

| 요소 | 선택 |
|------|------|
| Model | `gpt-5.6-sol` |
| Effort | `high` 또는 `max` |
| Surface | Codex cloud |
| Guardrail | PR 단위 review, CI required |

```text
Task:
Migrate one module from legacy API usage to the new client.
Keep public behavior unchanged, update tests, and summarize compatibility risks.
```

## 2. PR review bot

### 목표

GPT-5.6 Sol + Codex review workflow로 backward compatibility, security, test gap 중심 review를 만든다.

### Review rubric

- public API 변경 여부
- auth/permission/security regression
- test coverage gap
- migration/backward compatibility
- operational risk

```text
Review prompt:
Review this PR as a senior engineer.
Prioritize behavioral regressions, security issues, missing tests, and migration risks.
Return findings with file/line references first.
```

## 3. Tool-heavy research agent

### 목표

Responses API + Programmatic Tool Calling으로 web/search/db tool 결과를 code로 필터링 후 요약한다.

### 흐름

```text
Query
  -> search tools
  -> programmatic filtering
  -> source ranking
  -> summary
  -> citations/reference table
```

### 적합한 주제

- 신기술 release 분석
- API migration guide 비교
- vendor pricing/policy change 추적
- internal docs + public docs 교차 검증

## 4. Large codebase exploration

### 목표

Multi-agent beta 또는 Codex `ultra`로 frontend/backend/infra/test 영역을 병렬 조사한다.

| Agent | 역할 |
|-------|------|
| Frontend | UI route, state, component 영향 조사 |
| Backend | API, schema, service boundary 조사 |
| Infra | deployment, env, CI 영향 조사 |
| Test | existing coverage, missing regression test 조사 |
| Coordinator | 결과 병합, implementation plan 작성 |

## 5. Security hardening

### 목표

trusted defensive workflow 안에서 vulnerability triage, patch generation, regression test 작성을 수행한다.

### Boundary

- exploit weaponization이 아니라 defensive patch에 집중한다.
- secrets와 production credential 접근은 제한한다.
- patch는 CI와 human review를 통과해야 한다.
- high-risk 결과는 log와 rationale을 남긴다.

## 6. 도입 평가 프로젝트

### 목표

`Sol/Terra/Luna`와 `medium/high/max` 조합을 실제 repo task로 비교한다.

| Task | Terra medium | Terra low | Sol medium | Sol high | Sol max |
|------|--------------|-----------|------------|----------|---------|
| small bugfix | | | | | |
| flaky test fix | | | | | |
| API migration | | | | | |
| PR review | | | | | |
| docs rewrite | | | | | |

### 기록할 지표

- elapsed time
- tool/test command 수
- diff size
- review findings 수
- CI pass/fail
- human correction 필요 여부
- token/cost

## 관련 노트

- [[study/tech/ai/lazy-codex]] - false completion 차단과 검증 루프
- [[study/tech/ai/agent-orchestration/cli-agents]] - 여러 coding agent 운영
- [[study/tech/ai/model-context-protocol-mcp]] - tool-heavy agent integration
