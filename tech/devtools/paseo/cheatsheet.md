---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — Cheatsheet

> [[05-projects|이전: Projects]] | [[README|목차로 돌아가기]]

## Session Commands

```bash
# 새 agent 실행
paseo run "fix the failing tests"

# 목록과 연결
paseo ls
paseo attach <agent-id>

# follow-up과 관찰
paseo send <agent-id> "also add regression tests"
paseo logs <agent-id>
paseo wait <agent-id>
```

| 명령 | 용도 |
|---|---|
| `paseo run "<task>"` | 새 agent session 실행 |
| `paseo ls` | agent 목록과 상태 확인 |
| `paseo attach <agent-id>` | interactive session에 연결 |
| `paseo send <agent-id> "<text>"` | follow-up 전달 |
| `paseo logs <agent-id>` | session log 확인 |
| `paseo wait <agent-id>` | 완료까지 대기 |

## 자주 쓰는 옵션

| 옵션 | 의미 | 주의 |
|---|---|---|
| `--background` | background 실행 | log와 completion을 별도로 확인 |
| `--workspace` | 기존 workspace 선택 | concurrent writer 충돌 주의 |
| `--new-workspace worktree` | 새 worktree에서 실행 | security sandbox는 아님 |
| `--output-schema` | structured JSON output 요구 | schema validation 필요 |

```bash
paseo run --background "investigate the failure without editing files"
paseo run --new-workspace worktree "implement the fix and run tests"
```

## Orchestration 기능 지도

- provider/model discovery
- subagent 생성과 follow-up
- same workspace 또는 new worktree 선택
- terminal, script, service 실행
- agent completion wait
- heartbeat와 cron schedule
- structured JSON output

## Workspace Rule of Thumb

| 상황 | 선택 |
|---|---|
| Read-only 조사 여러 개 | same workspace 가능 |
| 하나의 변경에 순차 follow-up | same workspace |
| 병렬 구현 | separate worktree |
| 서로 다른 provider 결과 비교 | separate session, write가 있으면 separate worktree |
| shared DB/service 사용 | worktree 외에 namespace/port도 분리 |

## Security Checklist

- [ ] Paseo/worktree를 sandbox로 간주하지 않는다.
- [ ] agent는 현재 사용자 권한으로 실행된다고 가정한다.
- [ ] local credential과 Docker mount를 최소화한다.
- [ ] pairing QR/URL을 secret처럼 관리한다.
- [ ] direct password는 encryption이 아님을 기억한다.
- [ ] `0.0.0.0` bind 시 password와 HTTPS/VPN을 적용한다.
- [ ] relay의 IP, timing, size, session metadata 노출을 평가한다.
- [ ] branch 통합 전 diff와 test 결과를 사람이 검토한다.

## 장애 확인 순서

| 증상 | 먼저 확인할 것 |
|---|---|
| Agent가 시작되지 않음 | provider CLI 설치·인증·직접 실행 여부 |
| Model/mode가 보이지 않음 | adapter capability discovery와 provider version |
| Worktree setup 실패 | setup script idempotency, dependency, path |
| Dev server 충돌 | dynamic port와 external shared resource |
| Remote 연결 실패 | pairing 정보, daemon reachability, relay/VPN |
| 예상 밖 permission | provider CLI permission model과 daemon OS account |

## Version 메모

- 기준일: `2026-08-08`
- stable: `v0.2.5`
- pre-release: `v0.3.0-beta.4`
- 설치·upgrade 전 [Releases](https://github.com/getpaseo/paseo/releases) 재확인

## Sources

- [CLI reference](https://paseo.sh/docs/cli)
- [Orchestration](https://paseo.sh/docs/orchestration)
- [Git worktrees](https://paseo.sh/docs/worktrees)
- [Security](https://paseo.sh/docs/security)
- [GitHub Releases](https://github.com/getpaseo/paseo/releases)
