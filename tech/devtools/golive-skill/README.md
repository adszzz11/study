---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive

> **한 줄 정의**: GoLive는 AI coding agent가 만든 앱을 사용자의 provider account에 실제 출시하도록 돕는 오픈소스 **Agent Skill + zero-dependency Node CLI**다.

## Overview

GoLive는 단순한 deploy 명령이 아니라, 앱 출시의 마지막 단계를 `detect → plan → approve → apply → verify`로 다룬다. hosting, database, environment variable, DNS, email, payment, Auth, ownership handoff처럼 provider를 가로지르는 작업을 탐지하고, 변경 전 plan을 보여 주며, 명시적 승인 뒤에 실행·검증·기록한다.

- **역할 분리:** Agent는 대화·선택·승인을, bundled CLI는 provider API/CLI 호출과 state/evidence 기록을 맡는다.
- **승인 우선:** `plan`은 read-only이고 `apply`에는 plan ID와 `--yes`가 필요하다. DNS·삭제·첫 production deploy·live-mode 변경에는 추가 confirmation gate가 있다.
- **출시 기록:** `.golive/state.json`, `.golive/report.json`, `GOLIVE_REPORT.md`와 handover 문서로 resource와 검증 증거를 남긴다.
- **도입 판단:** 2026-10 기준 초기 alpha로 본다. disposable 환경에서 provider 조합과 business flow를 검증한 뒤 production으로 옮긴다.

## Learning Path

- [ ] [[tech/devtools/golive-skill/01-overview|1. Overview]] — 문제, workflow, 안전 경계 이해하기
- [ ] [[tech/devtools/golive-skill/02-ecosystem|2. Ecosystem]] — provider CLI·IaC·ClickOps와 비교하기
- [ ] [[tech/devtools/golive-skill/03-references|3. References]] — 공식 문서의 검증 범위와 provider scope 확인하기
- [ ] [[tech/devtools/golive-skill/04-learning/01-getting-started|4. Getting started]] — disposable app에서 detect와 plan 검토하기
- [ ] [[tech/devtools/golive-skill/04-learning/02-deep-dive|5. Deep dive]] — approval, provenance, drift, teardown 익히기
- [ ] [[tech/devtools/golive-skill/05-projects|6. Projects]] — MVP·micro-SaaS·고객 인계 시나리오 적용하기
- [ ] [[tech/devtools/golive-skill/cheatsheet|7. Cheatsheet]] — gate와 점검표 빠르게 복습하기

## When To Use

- AI agent가 만든 web app의 첫 출시를 provider 선택·계정 연결·검증까지 구조화하고 싶다.
- Vercel/Netlify, Supabase/Neon, Resend, Stripe test mode, 일부 DNS 작업을 하나의 approval workflow로 묶고 싶다.
- 어떤 resource를 만들었는지, 누가 소유하는지, 인계 후 무엇을 수동 운영하는지 문서로 남겨야 한다.
- disposable project 또는 subdomain에서 launch rehearsal을 안전하게 반복하고 싶다.

## When Not To Use

- 복잡한 multi-cloud network, IAM, 장기 desired-state 관리는 Pulumi, Terraform, OpenTofu 같은 IaC가 더 적합하다.
- 반복 배포만 필요하고 provider별 CI/CD pipeline이 이미 안정적이라면 기존 pipeline이 더 단순할 수 있다.
- live-mode payment 또는 지원 여부가 불확실한 provider 조합을 무검증으로 production에 적용하려 한다.
- provider account에 이미 로그인한 agent의 직접 조작까지 기술적으로 차단해야 한다. GoLive의 approval gate는 provider 권한을 강제하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/scraping/playwright/README|Playwright]] — 출시 뒤 signup·결제·email 같은 사용자 흐름을 browser E2E로 확인할 때 연결된다.

## Sources

- [GoLive GitHub repository / README](https://github.com/mikehasa/golive-skill)
- [Architecture](https://github.com/mikehasa/golive-skill/blob/main/docs/ARCHITECTURE.md)
- [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
- [Provider scope](https://github.com/mikehasa/golive-skill/blob/main/docs/PROVIDERS.md)
- [Validation scope and live-test evidence](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md)
