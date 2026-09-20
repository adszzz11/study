---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Observer References

## Primary References

| 자료 | 용도 | 확인할 내용 |
|---|---|---|
| [Claude Observer repository](https://github.com/svenliebig/claude-observer) | 구현과 성숙도 확인 | source tree, commits, license, install/update 방식 |
| [Claude Observer README](https://github.com/svenliebig/claude-observer#readme) | 사용자 기능과 설정 파악 | UI mode, terminal 지원, Web Dashboard, cleanup |
| [Claude Code hooks reference](https://code.claude.com/docs/en/hooks) | protocol 검증 | event input/output, exit behavior, decision schema |
| [PermissionRequest decision control](https://code.claude.com/docs/en/hooks#permissionrequest-decision-control) | 승인 broker 검증 | `allow`, `deny`, `updatedPermissions` |
| [Claude Code permissions](https://code.claude.com/docs/en/permissions) | 안전한 rule 설계 | allow/ask/deny 우선순위, matcher 범위 |

## Comparison Projects

- Claude Dashboard: https://github.com/sonpham-org/claude-dashboard
- Claude Code Monitor: https://github.com/bruceyxli/claude-code-monitor

## 조사 메모

- 조사 기준일: 2026-09-20
- “Claude Observer”는 `svenliebig/claude-observer`를 뜻한다.
- Anthropic 공식 제품이 아니라 독립 오픈소스 프로젝트다.
- stars, commits, release, license 표시는 변할 수 있으므로 도입 시점에 다시 확인한다.
- README 설명만으로 Web Dashboard의 authentication, TLS, bind address, CSRF/origin 검증을 단정하지 않는다. 관련 server source가 최종 근거다.

## Source Review Checklist

- [ ] 설치 script가 수정하는 파일과 backup/rollback 동작 확인
- [ ] `~/.claude/settings.json` hook merge 방식 확인
- [ ] session JSON에 command, path, code가 얼마나 저장되는지 확인
- [ ] permission response와 timeout의 fail-safe 동작 확인
- [ ] Web server의 bind address와 authentication 확인
- [ ] WebSocket origin validation과 HTTP CSRF 방어 확인
- [ ] dependency와 build artifact provenance 확인
- [ ] `LICENSE`와 third-party license 확인
- [ ] 최신 Claude Code hook schema와 compatibility 확인

## Sources

- https://github.com/svenliebig/claude-observer
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/permissions
- https://github.com/sonpham-org/claude-dashboard
- https://github.com/bruceyxli/claude-code-monitor

