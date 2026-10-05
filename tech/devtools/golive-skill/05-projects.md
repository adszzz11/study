---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — Projects

[[tech/devtools/golive-skill/README|학습 진입점]]

## 1. AI-generated MVP 출시

Next.js + Supabase 앱을 Vercel에 출시한다. environment wiring, Supabase Auth policy, custom domain, handoff를 범위로 둔다.

- disposable Vercel/Supabase project와 subdomain에서 detect·plan을 먼저 수행한다.
- plan에서 redirect URL, RLS, environment variable 주입 위치, DNS record를 승인한다.
- verify 뒤에는 신규 signup과 권한 경계를 browser E2E로 별도 확인한다.
- `GOLIVE_HANDOVER.md`에 organization owner, domain renewal, DB backup 책임을 기록한다.

## 2. 결제 가능한 micro-SaaS

Vercel + Supabase 또는 Neon + Resend + Stripe **test mode**를 연결한다.

- test customer와 product/price를 사용하며 live-mode flag를 사용하지 않는다.
- webhook endpoint, signature verification, idempotency, retry와 실패 email을 테스트한다.
- payment success가 entitlement·DB row·email에 일관되게 반영되는지 확인한다.
- test 환경에서만 teardown rehearsal을 하고, plan과 삭제 대상 증거를 보관한다.

## 3. 고객 인계형 prototype

agency 또는 indie hacker가 만든 앱을 고객 account로 넘긴다.

| 인계 항목 | 완료 증거 |
|---|---|
| Resource ownership | 고객 organization의 dashboard에서 owner/access 확인 |
| Billing / renewal | 결제 수단, domain renewal 담당자와 날짜 기록 |
| 비밀값 | secret의 실제 값이 아닌 보관 위치·rotation 책임 기록 |
| 반복 작업 | deploy, migration, webhook 재등록 절차 |
| 제거 절차 | GoLive 대상과 수동 삭제가 필요한 항목의 구분 |

## 4. Ephemeral launch rehearsal

production zone 대신 disposable subdomain에서 DNS, HTTPS, email, payment 설정을 검증한다. rehearsal의 state/report와 실패 기록을 바탕으로 production plan을 새로 만들고, 기존 rehearsal plan의 승인이나 confirmation을 재사용하지 않는다.

## Sources

- [GoLive README](https://github.com/mikehasa/golive-skill)
- [Provider scope](https://github.com/mikehasa/golive-skill/blob/main/docs/PROVIDERS.md)
- [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
