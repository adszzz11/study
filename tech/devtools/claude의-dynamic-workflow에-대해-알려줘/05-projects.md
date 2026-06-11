---
date: 2026-06-09
tags:
  - tech
  - devtools
  - claude
  - dynamic-workflows
  - projects
status: learning
type: tech-tool-study
parent: "[[README]]"
---

# Claude Dynamic Workflows - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 딥다이브]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 1. Repo-wide Security Sweep

### 목표

route별 auth, input validation, unsafe SQL, secret leakage를 병렬 탐지하고 verifier agents가 false positive를 제거한다.

### Workflow prompt

```text
ultracode: Run a repo-wide security sweep.

Scope:
- Inspect server routes, auth middleware, database query builders, and config files.
- Do not modify files.

Split:
- Discovery agents by route group or package.
- Specialized agents for auth, input validation, SQL safety, and secret leakage.

Verification:
- For every finding, run a verifier agent that tries to disprove it.
- Only include verifier-confirmed findings in the final report.

Output:
- file path, line/evidence, risk, exploit scenario, suggested fix, verifier status.

Stop:
- Stop after all scoped route groups/packages are checked once and every finding is verified.
```

### 산출물

| 산출물 | 설명 |
|--------|------|
| confirmed findings | verifier-confirmed 보안 이슈 |
| rejected findings | false positive로 제거된 후보 |
| risk matrix | severity/likelihood 기준 정렬 |
| fix plan | 우선순위별 수정 계획 |

---

## 2. Large Migration

### 목표

deprecated API callsite를 찾고, 파일 단위 변환과 test/review를 분리해 안전하게 migration한다.

```text
use a workflow: Migrate deprecated FooClient.getUser() calls to UserService.fetchUser().

Phase 1:
- Discover all callsites.
- Group by package and owner area.

Phase 2:
- Generate minimal patches per file group.
- Preserve public behavior.

Phase 3:
- Run relevant tests per group.
- Reviewer agents inspect risky diffs.

Stop:
- No deprecated callsites remain.
- Tests pass or every failing test has a triage note.
- Reviewer agents approve each changed group.
```

### 체크리스트

- [ ] 먼저 report-only discovery 실행
- [ ] callsite 목록과 migration rule을 검증
- [ ] 작은 package부터 patch 적용
- [ ] test failure를 migration failure와 기존 failure로 분리
- [ ] reviewer agent가 semantic regression을 검토

---

## 3. Deep Research Dossier

### 목표

source search fan-out, claim extraction, adversarial source verification, cited report 생성을 workflow로 구성한다.

```text
/deep-research Build a dossier on Claude Dynamic Workflows.

Focus:
- official announcement
- docs and limits
- comparison with Codex, Copilot coding agent, LangGraph, AutoGen
- operational risks: token usage, permissions, admin controls

Verification:
- Every major claim needs a source URL.
- Flag contradictions instead of silently resolving them.
```

이 프로젝트는 [[study/tech/ai/llm-wiki-study]]와 잘 맞는다. raw source를 먼저 모으고, wiki page에는 claim 단위 출처와 contradiction flag를 남긴다.

---

## 4. Incident Root Cause Mining

### 목표

로그, metric, alert, recent commit, deploy event를 병렬 조사해 root cause 후보를 좁힌다.

| Phase | Agent 역할 | 결과 |
|-------|------------|------|
| Timeline | incident 전후 event 정리 | 시간순 사건 목록 |
| Logs | error pattern 탐색 | error cluster |
| Metrics | saturation/latency/traffic 변화 분석 | anomaly 후보 |
| Commits | 최근 변경점과 위험 diff 탐색 | suspect changes |
| Verifier | 각 root cause 후보 반박 | confirmed/rejected status |

```text
ultracode: Investigate the root cause of the 2026-06-09 API latency incident.

Do not make changes. Split by evidence source: logs, metrics, deploys, commits,
and external dependencies. Use verifier agents to challenge each root cause
hypothesis. Produce a timeline, likely cause, rejected causes, and follow-up checks.
```

---

## 5. Best Practices

| 원칙 | 이유 |
|------|------|
| 작은 scope로 시작 | token 폭주와 agent 중복을 줄임 |
| report-only 먼저 실행 | 대규모 변경 전 discovery 품질 확인 |
| verifier를 별도 phase로 둠 | self-preferential bias 감소 |
| stop condition을 명시 | premature completion과 runaway loop 방지 |
| 저장 전 workflow 검토 | 재사용 command의 path/권한/budget 위험 감소 |

---

## 관련 노트

- [[study/tech/ai/codex/05-projects]]
- [[study/tech/ai/autoresearch-study/05-projects]]
- [[study/tech/ai/llm-wiki-study/05-projects]]
- [[study/tech/ai/multi-agent-platforms]]
