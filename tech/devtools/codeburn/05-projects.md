---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]] · [[cheatsheet|다음: Cheatsheet]]

## 프로젝트 1: 개인 AI Coding Cost Baseline

### 목표

7일 동안 provider, model, project, task별 사용 패턴을 기록하고 “비용을 줄이되 delivery를 해치지 않는” baseline을 만든다.

```bash
codeburn status --format json
codeburn export -f json
codeburn models --format markdown
```

### 절차

- [ ] Day 0에 version, Node.js, 감지 provider 기록
- [ ] 매일 같은 timezone에서 status snapshot 저장
- [ ] 가장 비싼 session 3개를 실제 작업과 대조
- [ ] unknown/estimated model 표시를 별도 분류
- [ ] 7일 후 task mix, cache hit, cost per edit 비교

### 산출물

| 항목 | 예시 |
|---|---|
| Baseline | provider/model별 7-day cost |
| Outlier notes | 고비용 session의 task와 원인 |
| Caveats | subscription, Auto model, 누락 provider |
| Action | context 축소나 model routing 가설 1개 |

## 프로젝트 2: Retry Tax 실험

### 질문

비싼 model이 더 높은 one-shot rate로 총 retry cost를 줄이는가, 아니면 저렴한 model이 충분한가?

```bash
codeburn compare -p week
codeburn models --by-task
```

### 설계

1. 비슷한 난이도의 task category 하나를 고른다.
2. model별 cost per edit, one-shot rate, retry rate를 기록한다.
3. task 난이도와 project 차이를 메모한다.
4. 최소 1주 더 관찰한 뒤 routing rule을 제안한다.

> [!caution] 사람 평가 금지
> 이 실험은 model routing과 prompt/context 개선용이다. 개인 생산성 평가나 코드 품질 점수로 사용하지 않는다.

## 프로젝트 3: Context/MCP Hygiene Audit

```bash
codeburn optimize -p 30days
```

검토 대상:

- duplicate 또는 junk reads
- oversized `CLAUDE.md`
- 낮은 MCP tool coverage와 unused MCP server
- ghost agents, skills, commands
- cache/context bloat
- project 평균 대비 expensive session outlier

각 finding에 대해 `관찰 → 원본 설정 확인 → 작은 변경 → 7일 재측정` 순서로 진행한다. `mv`, config edit 등 제안 command는 그대로 실행하기 전에 target을 검토한다.

## 프로젝트 4: Yield Calibration

Git repository 안에서 실행한다.

```bash
codeburn yield
codeburn yield -p 30days
```

### Sample audit

| CodeBurn 분류 | 사람이 확인할 것 |
|---|---|
| Productive | main에 실제 반영됐는가, 후속 fix는 없었는가? |
| Reverted | revert가 agent 오류 때문인가, 요구 변경 때문인가? |
| Abandoned | 다른 branch/repo, squash, delayed commit은 아닌가? |

20개 정도의 session sample로 false positive/negative를 기록한 뒤 팀 맥락에서 metric을 사용할지 결정한다.

## 프로젝트 5: MCP Self-Observability

### 목표

AI coding agent가 작업 도중 자신의 usage와 savings 후보를 조회하게 하되 privacy boundary를 검증한다.

```bash
claude mcp add codeburn -- npx -y codeburn mcp
```

- [ ] 기본 응답에서 project name이 pseudonym인지 확인
- [ ] `get_usage` 결과가 CLI total과 일치하는지 sample 비교
- [ ] `get_savings` latency와 결과 민감도 확인
- [ ] MCP client가 tool result를 외부에 보존하는지 확인
- [ ] 실제 이름 노출은 필요한 session에서만 opt-in

## 완료 기준

- baseline과 변경 후 수치를 같은 version·timezone·period로 비교했다.
- provider invoice와 CodeBurn estimate를 구분해 표기했다.
- metric의 교란 요인과 sample validation을 함께 남겼다.
- 설정 변경을 되돌릴 방법을 준비했다.
- transcript/export를 public vault에 첨부하지 않았다.

## Sources

- https://codeburn.app/docs/status-export
- https://codeburn.app/docs/models
- https://codeburn.app/docs/compare
- https://codeburn.app/docs/optimize
- https://codeburn.app/docs/yield
- https://github.com/getagentseal/codeburn

