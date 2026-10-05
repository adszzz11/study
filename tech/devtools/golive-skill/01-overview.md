---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — Overview

[[tech/devtools/golive-skill/README|학습 진입점]] · 다음: [[tech/devtools/golive-skill/02-ecosystem|Ecosystem]]

## What

GoLive는 agent-built SaaS/web app을 실제 사용자의 provider account에 출시하기 위한 오픈소스 Agent Skill과 zero-dependency Node CLI다. 자체 hosted backend나 telemetry 대신, 로컬 CLI가 provider API/CLI를 호출하고 작업 상태와 검증 증거를 프로젝트에 남긴다.

## Why

코드가 준비되어도 공개에는 hosting, DB, secret, DNS, email, payment, Auth, 소유권 인계가 남는다. 이 과정은 dashboard를 오가며 누락하기 쉽고, 누가 무엇을 만들었는지 추적하기 어렵다. GoLive는 이 마지막 단계를 다음 상태 전이로 분리한다.

```text
detect → plan → human approval → apply → verify → handoff / status
```

`plan`은 변경하지 않고 대상 account/team, resource 이름, 비용·위험 flag, DNS record를 드러낸다. 이후에만 `apply`가 실행되므로, “agent에게 배포해 달라”고 말하는 것과 “어느 계정에 무엇을 만들지 승인한다”를 구분할 수 있다.

## 특징

| 특징 | 의미 | 학습 시 확인할 점 |
|---|---|---|
| Agent + CLI 분리 | Agent는 의사결정, CLI는 provider 작업·secret·증거 처리를 담당한다. | 어떤 명령이 실제 변경인지 구분한다. |
| Approval-first | `apply`는 plan ID와 `--yes`가 필요하다. | plan의 계정·비용·DNS를 먼저 읽는다. |
| 추가 gate | DNS는 `--confirm-dns`, 삭제는 `--confirm-destroy`, 첫 production/live-mode 변경은 `--confirm-live`를 요구한다. | flag가 무엇을 허용하는지 문서와 plan으로 확인한다. |
| Provenance | state/report와 `GOLIVE_REPORT.md`에 결과를 기록한다. | provider dashboard와 report가 일치하는지 비교한다. |
| Handoff | `handoff --write`가 `GOLIVE_HANDOVER.md`를 만든다. | dashboard 접근, renewal 책임, 수동 작업을 검토한다. |
| Drift check | `golive status`가 baseline과 현재 provider 상태를 read-only로 비교한다. | drift는 자동 수정되지 않는다는 점을 기억한다. |

## 안전 경계와 한계

- credential은 권한 `0600`의 local plaintext file을 사용한다. OS keychain 기반 보관은 아니다.
- provider에 이미 로그인한 agent는 GoLive 바깥에서 직접 변경할 수 있다. 따라서 confirmation은 provider 권한을 대체하지 않는다.
- `teardown`은 GoLive가 생성했다고 증명할 수 있는 resource만 대상으로 하며 자동 rollback을 제공하지 않는다.
- Vercel+Supabase, Netlify+Neon, 일부 DNS, Resend, Stripe test-mode 조합의 disposable E2E 근거가 있어도 모든 provider 조합·live-mode payment·drift subject가 동일하게 검증된 것은 아니다.

출시 성공 화면만으로 business flow가 정상이라는 뜻은 아니다. signup, RLS, webhook signature, payment, email delivery를 별도로 테스트한다.

## Sources

- [GoLive README](https://github.com/mikehasa/golive-skill)
- [Architecture](https://github.com/mikehasa/golive-skill/blob/main/docs/ARCHITECTURE.md)
- [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
- [Validation](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md)
