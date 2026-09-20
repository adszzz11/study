---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: Cheatsheet]]

## Project 1: 두 Provider의 Read-only 비교

### 목표

같은 bug report를 서로 다른 provider에 맡겨 분석 품질, latency, evidence를 비교한다. 첫 프로젝트에서는 code를 수정하지 않는다.

### Workflow

1. 범위가 작은 test failure를 선택한다.
2. 각 agent를 별도 session에서 실행한다.
3. 같은 output contract를 요청한다.
4. log와 structured result를 비교한다.

```text
Do not modify files. Return:
1. likely root cause,
2. evidence with file paths,
3. smallest proposed fix,
4. tests that should be run.
```

| 평가 항목 | 기록 |
|---|---|
| 정확한 root cause | 근거 file/line과 함께 비교 |
| 불필요한 탐색 | log에서 확인 |
| Permission 요구 | provider별 차이 기록 |
| 후속 질문 반영 | `paseo send`로 같은 질문 전달 |

## Project 2: Parallel Worktree Implementation

### 목표

서로 독립적인 두 issue를 별도 worktree에서 구현해 edit와 dev server port 충돌을 줄인다.

```bash
paseo run --new-workspace worktree "implement issue A and run its tests"
paseo run --new-workspace worktree "implement issue B and run its tests"
paseo ls
```

### Checklist

- [ ] 두 task의 수정 범위가 독립적인지 확인
- [ ] worktree setup이 반복 실행 가능하고 idempotent한지 확인
- [ ] service마다 dynamic port 할당
- [ ] database/cache namespace 분리
- [ ] 각 branch에서 test/lint 실행
- [ ] 사람 review 후 하나씩 통합하고 통합 test 실행

## Project 3: Cross-provider Delegation

### 목표

한 agent는 계획과 review, 다른 provider의 agent는 implementation을 담당하게 한다.

```text
Coordinator
  ├─ repository 조사와 task 분해
  ├─ Worker A: isolated implementation
  ├─ Worker B: regression test review
  └─ 결과 수집, conflict 확인, 최종 검토
```

### Guardrails

- task마다 input, allowed scope, expected output을 명시한다.
- 같은 workspace에 concurrent writer를 두지 않는다.
- worker 완료가 곧 merge 승인이라는 의미는 아니다.
- structured JSON output은 schema validation 후 소비한다.
- heartbeat/cron은 명확한 종료 조건과 함께 사용한다.

## Project 4: Mobile Supervision Drill

### 목표

장시간 read-only task를 mobile에서 확인하고 follow-up을 보내는 연결·복구 절차를 검증한다.

### 절차

1. daemon의 pairing QR/link를 안전한 환경에서 client에 전달한다.
2. pairing URL을 password manager의 secret과 같은 수준으로 취급한다.
3. E2EE relay 연결에서 session log를 확인한다.
4. network 전환 후 reconnect 동작을 시험한다.
5. mobile에서 follow-up을 보내고 daemon에서 수신을 확인한다.
6. device 분실을 가정해 pairing revoke/rotation 절차를 문서화한다.

### Security review

| 질문 | 합격 기준 |
|---|---|
| Pairing secret이 log/chat에 남는가? | 남지 않음 |
| Direct exposure가 필요한가? | 가능하면 relay/VPN 사용 |
| `0.0.0.0` bind가 있는가? | password + HTTPS/VPN 적용 |
| Agent가 읽을 수 있는 credential은? | task에 필요한 최소 범위 |

## Project 5: Repository Automation 설계

### 목표

`paseo.json`에 반복되는 setup, test, lint, dev server를 선언해 새 worktree가 예측 가능하게 시작되도록 한다.

### 설계 항목

- setup/teardown의 idempotency
- dependency cache 공유 범위
- named script의 timeout과 exit code
- workspace별 environment variable과 dynamic port
- reverse proxy route naming
- crash 후 orphan process 정리

### 완료 조건

- [ ] 두 worktree를 동시에 생성해도 setup 성공
- [ ] 같은 app service가 port collision 없이 실행
- [ ] test/lint 결과가 agent와 사람 모두에게 보임
- [ ] teardown 후 process와 temporary resource가 남지 않음
- [ ] 실패 시 수동 recovery 절차가 문서화됨

## Sources

- [Orchestration](https://paseo.sh/docs/orchestration)
- [Orchestration workflows](https://paseo.sh/docs/orchestration-workflows)
- [Git worktrees](https://paseo.sh/docs/worktrees)
- [CLI reference](https://paseo.sh/docs/cli)
- [Security](https://paseo.sh/docs/security)
