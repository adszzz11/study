---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — Deep dive

[[tech/devtools/golive-skill/README|학습 진입점]] · 이전: [[tech/devtools/golive-skill/04-learning/01-getting-started|Getting started]]

## 1. Approval은 provider 권한이 아니다

GoLive의 trust model은 변경을 plan과 confirmation으로 분리하지만, provider에 로그인한 agent가 dashboard·API·다른 CLI로 직접 변경하는 일을 막지는 못한다. 따라서 account에는 최소 권한, 별도 sandbox organization, review 가능한 API token 정책을 둔다. credential file은 local plaintext이며 `0600` 권한이라는 점도 운영 기준에 반영한다.

## 2. Gate를 위험도에 맞춰 읽기

| 작업 | 기대하는 gate | 사람이 확인할 내용 |
|---|---|---|
| 일반 apply | plan ID + `--yes` | account, resource, 비용, secret 주입 위치 |
| DNS 변경 | `--confirm-dns` | zone, hostname, record type/value, TTL, 기존 traffic 영향 |
| 삭제 | `--confirm-destroy` | 정확한 resource, backup/retention, 복구 불가 범위 |
| 첫 production / live-mode | `--confirm-live` | 실제 사용자 영향, billing, rollback/incident owner |

flag는 자동화 허가의 증거일 뿐, 변경이 안전하다는 보증은 아니다. 특히 DNS 전환과 live payment는 independent reviewer와 준비된 rollback 절차를 둔다.

## 3. Provenance와 drift

GoLive는 `.golive/state.json`, `.golive/report.json`, `GOLIVE_REPORT.md`에 생성 resource와 검증 결과를 남긴다. `golive status`는 이 baseline을 provider의 현재 상태와 read-only로 비교해 drift를 보여 준다.

```text
plan 승인 → apply → verify → report/state 보관
                              ↓
                    이후 status로 drift 확인
```

drift가 발견되어도 바로 “되돌리기”보다 원인을 분류한다. dashboard 수동 변경, provider의 관리형 변경, configuration 누락, baseline 부정확성을 구분하고, 새 plan으로 의도한 변경을 재승인한다.

## 4. Verify는 application test와 다르다

`verify`가 deployment/resource wiring을 통과해도 실제 고객 여정은 별도다.

- 신규 signup과 email confirmation
- Auth redirect URL과 RLS가 다른 사용자 데이터를 막는지
- Stripe test webhook signature와 idempotency
- transaction 이후 권한/entitlement 변화
- Resend delivery와 bounce/실패 경로
- custom domain의 HTTPS, DNS propagation, health endpoint

## 5. Handoff와 teardown rehearsal

`handoff --write`로 만든 `GOLIVE_HANDOVER.md`에는 account 진입 경로, ownership 증거, renewal/billing 책임, 수동 작업, 제거 절차가 담겨야 한다. recipient가 provider dashboard에 실제 접근 가능한지도 별도로 확인한다.

teardown은 disposable resource로만 연습한다. GoLive가 생성 증명을 할 수 있는 resource만 대상이며 automatic rollback은 없다. plan을 검토한 뒤에만 `--confirm-destroy`를 사용하고, DB export·domain·external webhook 등 도구 밖의 잔여물을 점검한다.

## Sources

- [Architecture](https://github.com/mikehasa/golive-skill/blob/main/docs/ARCHITECTURE.md)
- [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
- [Validation](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md)
