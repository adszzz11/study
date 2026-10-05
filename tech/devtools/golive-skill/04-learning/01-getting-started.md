---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — Getting started

[[tech/devtools/golive-skill/README|학습 진입점]] · 다음: [[tech/devtools/golive-skill/04-learning/02-deep-dive|Deep dive]]

## 목표와 준비

**실제 변경 없이 disposable app의 출시 요구를 탐지하고 plan을 읽는 법을 익힌다.** 이 노트의 명령은 account 연결이나 deploy를 실행하지 않는 설치·계획 단계에 한정한다. production domain·실서비스 DB·live-mode Stripe 계정으로 시작하지 않는다.

- Node.js 20+, npm/npx, Git, Skill을 로드할 수 있는 agent를 준비한다.
- 별도 disposable project와 disposable provider project를 준비한다.
- Stripe는 test mode만 사용한다.
- 설치 시점의 최신 사용법과 package version은 [공식 README](https://github.com/mikehasa/golive-skill)에서 다시 확인한다.

## 1. Skill 설치

Codex 예시는 다음과 같다.

```bash
npx skills add https://github.com/mikehasa/golive-skill --skill golive --global --agent codex --yes
```

이 명령은 Skill을 설치할 뿐 provider account를 연결하거나 resource를 생성·배포하지 않는다. global 설치 정책이 팀 환경과 맞는지, source URL이 공식 repository인지 확인한다.

## 2. Detect 결과 검토

대상 app repository에서 agent에게 다음처럼 요청한다.

```text
$golive Help me take this app live.
```

detect 결과에서 framework, 필요한 environment variable, database/Auth/email/payment 흔적, deploy 후보 provider를 확인한다. agent의 추정은 사실이 아닐 수 있으므로 app의 `.env.example`, deployment configuration, webhook route, Auth policy를 함께 읽는다.

## 3. Plan을 승인 전 문서로 읽기

plan은 read-only여야 한다. 아래를 표처럼 대조하고, 하나라도 모호하면 apply로 진행하지 않는다.

| 확인 항목 | 질문 |
|---|---|
| 대상 account/team | 개인 sandbox인가, 올바른 organization인가? |
| resource 이름 | 기존 production resource와 충돌하지 않는가? |
| 비용/위험 flag | 유료 tier, egress, email, payment, 공개 endpoint가 포함되는가? |
| environment variable | secret의 이름·주입 위치·노출 경로가 맞는가? |
| DNS | zone·record·값·TTL·영향 받는 hostname이 맞는가? |
| Auth / data | RLS, redirect URL, migration, seed data가 의도와 맞는가? |

DNS와 production 관련 변경은 특히 별도 사람 검토를 둔다. plan ID는 apply에 연결되는 승인 대상이므로 다른 plan의 ID와 섞지 않는다.

## 4. Apply 전 종료 기준

이 시작 실습은 apply하지 않아도 성공이다. 실제 disposable apply를 하기로 결정했다면 plan ID와 `--yes` 외에도 상황에 따라 DNS는 `--confirm-dns`, 첫 production deploy·live-mode는 `--confirm-live`가 필요함을 확인한다. 그 뒤 `verify`, `status`, `handoff --write`까지 완료한 결과만 출시 증거로 취급한다.

## Sources

- [GoLive README](https://github.com/mikehasa/golive-skill)
- [GoLive skill source directory](https://github.com/mikehasa/golive-skill/tree/main/skills/golive)
- [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
