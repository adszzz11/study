---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차]] | [[cheatsheet|다음: Cheatsheet]]

## Project 1: Two-Session Recall Lab

### Goal

비민감 sample repository에서 memory의 최소 end-to-end value를 측정한다.

### Tasks

- Session A에서 작은 bug를 재현하고 두 가지 가설을 조사한다.
- 실패한 가설과 실제 root cause를 분명히 남긴다.
- Session을 종료하고 Session B를 시작한다.
- 자동 injection만으로 root cause, 관련 file, next step을 복원한다.
- `search → timeline → get_observations`로 원래 observation을 확인한다.

### Acceptance Criteria

- 관련 없는 observation을 대량 주입하지 않는다.
- 실패한 가설과 확정된 원인을 구분한다.
- 수정 file과 next step이 정확하다.
- 필요한 상세를 3단계 retrieval로 찾을 수 있다.

## Project 2: Privacy Boundary Drill

### Goal

실제 secret 없이 capture exclusion과 network boundary를 검증한다.

### Tasks

- `<private>TEST_MARKER</private>`를 포함한 입력을 만든다.
- viewer, MCP search, local DB-derived output에서 marker를 검색한다.
- worker listening address가 `127.0.0.1`인지 확인한다.
- provider와 optional Cloud Sync로 전송되는 field를 문서화한다.
- DB/log/backup retention table을 만든다.

### Acceptance Criteria

- Test marker가 persistent storage와 retrieval 결과에 없다.
- Worker가 external interface에 bind되지 않는다.
- “local”, “provider 전송”, “cloud sync” 데이터가 구분돼 있다.

## Project 3: Failure And Recovery Lab

### Goal

Memory subsystem 장애가 host 작업을 막지 않으면서도 관측 가능하도록 만든다.

### Scenarios

| Scenario | 확인할 결과 |
|---|---|
| Worker unavailable | coding host는 계속 동작하고 memory failure signal은 남음 |
| Chroma unavailable | FTS5 keyword search는 유지됨 |
| Provider quota/timeout | queue/error가 관측되고 fabricated summary가 생기지 않음 |
| Rapid log growth | disk alert 또는 rotation 기준이 작동함 |
| Upgrade regression | backup으로 known-good state에 복귀 가능 |

### Acceptance Criteria

- 각 장애마다 detection signal과 operator action이 있다.
- “조용한 observation 누락”을 찾는 audit 방법이 있다.
- Restore 후 이전 observation을 검색할 수 있다.

## Project 4: Staged Team Pilot

### Phases

1. **Disposable repo**: 기능 확인, 민감 데이터 없음
2. **Single developer**: 1주간 recall quality와 noise 측정
3. **Small team**: provider policy, retention, upgrade runbook 검토
4. **Broader rollout**: version pinning과 rollback window를 유지하며 확대

### Metrics

- 과거 조사 재수행에 절약한 시간
- 관련/비관련 injected observation 비율
- search 성공률과 detail fetch 횟수
- observation 누락 또는 잘못된 summary 사례
- DB/log disk growth
- provider cost와 token usage

## Promotion Rule

Claude-Mem에서 반복적으로 유용한 memory를 발견하면 다음과 같이 승격한다.

```text
Transient observation
  → 반복 검증
  → 중요한 team knowledge 판별
  → ADR / issue / repository docs에 기록
  → review와 version control 적용
```

자동 memory는 발견과 회상을 돕고, tracked documentation은 팀의 authoritative knowledge를 보존한다.

## Sources

- https://github.com/thedotmack/claude-mem/blob/main/docs/public/usage/search-tools.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
- https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md
- https://github.com/thedotmack/claude-mem/issues

