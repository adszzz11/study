---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — Ecosystem

[[tech/devtools/golive-skill/README|학습 진입점]] · 이전: [[tech/devtools/golive-skill/01-overview|Overview]]

## 비교

| 도구/방식 | 주 대상 | 운영 모델 | GoLive 대비 |
|---|---|---|---|
| **GoLive** | agent-built SaaS/web app 출시 | Agent-led, plan/approval/evidence | 여러 SaaS provider를 하나의 출시 workflow로 엮고 human gate를 둔다. alpha이며 provider 범위가 제한적이다. |
| Vercel / Netlify CLI | 해당 플랫폼 배포 | provider-native CLI, Git flow | hosting 배포에는 직접적이고 성숙했지만 DB·email·payment·handoff를 통합하지 않는다. |
| Pulumi / Terraform / OpenTofu | 재현 가능한 cloud infrastructure | IaC desired-state, Git/CI | 복잡한 multi-cloud/IAM/network에 적합하다. GoLive는 앱 출시 대화와 provider onboarding에 초점이 있어 IaC 대체재가 아니다. |
| 직접 dashboard 작업 | 소규모 단발 출시 | 수동 ClickOps | 빠르게 시작할 수 있지만 변경 이력·재현성·ownership handoff가 약하다. GoLive는 plan/report로 이를 보완한다. |
| CI/CD + provider별 CLI | 반복 배포 팀 | pipeline automation | 안정적 반복 배포에 강하지만 최초 account 연결·DNS·결제·human-only 절차를 하나의 agent UX로 묶지는 않는다. |

## Provider scope

| 영역 | built-in 또는 명시적 범위 | guided flow 중심 예 |
|---|---|---|
| Hosting | Vercel, Netlify | Railway, Render, Fly.io, Cloudflare |
| Database | Supabase, Neon | Turso, PlanetScale |
| DNS | Porkbun, GoDaddy 일부 | provider·zone별 지원 범위를 plan에서 재확인 |
| Email / payment / Auth | Resend, Stripe test payments, Supabase Auth | live-mode 및 조합별 검증은 Validation 문서 확인 |

provider 이름이 목록에 있다고 해서 모든 기능과 조합이 production-ready인 것은 아니다. 먼저 `detect`와 `plan`으로 실제 제안 범위를 보고, [Provider scope](https://github.com/mikehasa/golive-skill/blob/main/docs/PROVIDERS.md) 및 [Validation](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md)의 최신 근거와 비교한다.

## 선택 가이드

- **처음 출시와 인계:** GoLive + disposable rehearsal을 우선 검토한다.
- **hosting만 배포:** Vercel/Netlify CLI나 Git integration이 더 짧은 경로일 수 있다.
- **반복 가능한 기반시설:** IaC를 system of record로 두고, GoLive는 초기 onboarding/handoff 보조 역할로 제한한다.
- **팀의 표준 release:** CI/CD를 중심으로 두고, DNS·결제·ownership 같이 승인자가 필요한 작업만 분리한다.

## Sources

- [Provider scope](https://github.com/mikehasa/golive-skill/blob/main/docs/PROVIDERS.md)
- [Vercel deployment documentation](https://vercel.com/docs/deployments/overview)
- [Pulumi IaC concepts](https://www.pulumi.com/docs/iac/concepts/)
