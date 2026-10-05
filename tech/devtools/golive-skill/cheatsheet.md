---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — Cheatsheet

[[tech/devtools/golive-skill/README|학습 진입점]]

## Mental model

```text
detect → plan (read-only) → approve → apply → verify → handoff / status
```

## 시작 명령과 prompt

```bash
npx skills add https://github.com/mikehasa/golive-skill --skill golive --global --agent codex --yes
```

```text
$golive Help me take this app live.
```

설치는 provider account 연결이나 deploy를 수행하지 않는다. 설치 전 공식 repository URL, Node.js 20+ 요구사항, team의 global Skill 정책을 확인한다.

## Gate 요약

| 목적 | 필요한 확인 |
|---|---|
| 변경 제안 보기 | `plan`은 read-only; account/team, resource, 비용, secret, DNS를 검토 |
| 일반 적용 | plan ID + `--yes` |
| DNS 변경 | `--confirm-dns`와 zone/record/traffic 영향 검토 |
| 삭제 | `--confirm-destroy`와 backup·복구 불가 범위 검토 |
| 첫 production / live-mode | `--confirm-live`와 billing·rollback owner 검토 |

## 산출물

| 산출물 | 용도 |
|---|---|
| `.golive/state.json` | 기록된 baseline/state |
| `.golive/report.json` | 실행·검증 결과의 기계 판독 기록 |
| `GOLIVE_REPORT.md` | 사람이 검토할 출시 보고 |
| `GOLIVE_HANDOVER.md` | account 접근, 소유권, 반복 작업, 제거 절차 인계 |

## 출시 전·후 점검

- [ ] disposable project와 test-mode Stripe로 시작했다.
- [ ] plan의 organization, 비용, DNS, secret 주입 위치를 사람 검토했다.
- [ ] `verify` 결과와 provider dashboard를 비교했다.
- [ ] signup, RLS, webhook signature, payment, email delivery를 별도 테스트했다.
- [ ] `golive status`로 baseline 대비 drift를 확인했다.
- [ ] handoff 문서에 billing/renewal 및 manual step의 owner를 적었다.

## 기억할 한계

- credential은 `0600` local plaintext file이며 OS keychain이 아니다.
- confirmation gate는 provider에 로그인한 agent의 직접 변경을 막지 못한다.
- teardown은 생성 증명이 되는 resource만 대상으로 하며 automatic rollback은 없다.
- alpha 도구이므로 지원 provider와 검증된 조합은 production 전 최신 Validation 문서로 재확인한다.

## Sources

- [GoLive README](https://github.com/mikehasa/golive-skill)
- [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
- [Validation](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md)
