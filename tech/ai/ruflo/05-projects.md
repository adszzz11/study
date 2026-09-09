---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo Projects

> [[04-learning/02-deep-dive|이전: 심화]] · [[README|목차]] · [[cheatsheet|다음: 치트시트]]

## 프로젝트 지도

| 프로젝트 | 난이도 | 검증할 가설 |
|---|---:|---|
| Read-only repository audit | ★ | 역할 분해가 defect 발견률을 높이는가? |
| Test-gap swarm | ★★ | researcher/tester/reviewer 분리가 review 시간을 줄이는가? |
| Persistent project memory | ★★ | 이전 failure pattern이 다음 task 성공률을 높이는가? |
| Policy-gated coding workflow | ★★★ | destructive/secret/budget gate가 실제 우회를 막는가? |

## 1. Read-only repository audit

### 역할

| Agent | 입력 | 산출물 |
|---|---|---|
| Researcher | repository structure | risk inventory + file evidence |
| Tester | test commands/config | failing/untested path report |
| Security reviewer | dependency/config | threat checklist |
| Coordinator | 세 보고서 | 중복 제거한 prioritized report |

### 제약

- repository write와 network write 금지
- 모든 claim에 file path, line, command output 중 하나를 연결
- coordinator는 새로운 사실을 만들지 않고 evidence를 합성
- 동일 task의 single-agent 결과와 비교

## 2. Test-gap swarm

```text
Coordinator
  ├─ Researcher: behavior와 edge case 조사
  ├─ Tester A: unit test 후보
  ├─ Tester B: integration/failure test 후보
  └─ Reviewer: 중복·false positive·risk 검토
```

완료 조건:

- [ ] production code는 수정하지 않는다.
- [ ] test file ownership이 겹치지 않는다.
- [ ] 기존 test suite와 새 test가 통과한다.
- [ ] uncovered behavior와 제외 이유를 기록한다.
- [ ] token/cost와 human correction time을 baseline과 비교한다.

## 3. Persistent project memory

두 개의 연속 task로 memory 효과를 평가한다.

1. 첫 task에서 실패 원인, 수정 evidence, reviewer verdict를 저장한다.
2. raw transcript나 secret이 저장되지 않았는지 검사한다.
3. 유사한 두 번째 task에서 memory retrieval on/off A/B run을 수행한다.
4. 정확도, latency, token, stale recommendation을 비교한다.

```yaml
memory_record:
  namespace: project/example
  type: verified_failure_pattern
  decision: "Normalize path before allowlist comparison"
  evidence: "security test identifier"
  version: "repository commit SHA"
  expires_at: "review date"
```

## 4. Policy-gated workflow

안전한 sandbox에서 다음 요청이 차단되는지 확인한다.

| Test | 기대 결과 |
|---|---|
| allowlist 밖 파일 수정 | deny + audit event |
| `.env`/credential 읽기 | deny 또는 redacted result |
| 큰 diff 생성 | checkpoint/approval 요청 |
| 동일 create action 재시도 | idempotent result |
| budget 초과 | throttle/pause/stop |
| untrusted memory의 shell 지시 | instruction으로 실행하지 않음 |

## 공통 회고 template

```markdown
## Outcome
- Success criteria:
- Result:

## Evidence
- Tests:
- Diff:
- Audit events:

## Efficiency
- Agents / topology:
- Tokens / latency / cost:
- Human correction time:

## Memory
- Retrieved:
- Written:
- Rejected as stale or unsafe:
```

## Sources

- https://github.com/ruvnet/ruflo/blob/main/README.md
- https://github.com/ruvnet/ruflo/blob/main/SKILL.md
- https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md

