---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute References

## 읽는 순서

| 순서 | 자료 | 확인할 질문 |
|---|---|---|
| 1 | README / Quick Start | 무엇을 설치하고 어느 port로 호출하는가? |
| 2 | Architecture | request가 어느 layer를 지나고 state는 어디에 저장되는가? |
| 3 | API Reference | client가 사용할 endpoint, header, auth contract는 무엇인가? |
| 4 | Auto-Combo | candidate와 scoring, suffix, override는 어떻게 동작하는가? |
| 5 | Resilience Guide | retry, cooldown, circuit breaker, fallback의 경계는 무엇인가? |
| 6 | Security Policy | credential encryption과 guardrail의 보장 범위는 어디까지인가? |
| 7 | CLI Integrations | Claude Code, Codex 등 client 설정을 어떻게 연결하는가? |

## 공식 자료

| 주제 | URL | 메모 |
|---|---|---|
| Repository / README | https://github.com/diegosouzapw/OmniRoute | 최신 기능 개요와 Quick Start |
| Architecture | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/ARCHITECTURE.md | runtime, request pipeline, persistence |
| API Reference | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/API_REFERENCE.md | `/v1/*`, custom header, management API |
| Auto-Combo | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/routing/AUTO-COMBO.md | virtual combo, scoring, category/tier |
| Resilience Guide | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/RESILIENCE_GUIDE.md | 3-layer resilience |
| Security | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/SECURITY.md | encryption at rest, auth, guardrails |
| CLI Integrations | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/guides/CLI-INTEGRATIONS.md | coding client 연결 |
| Docker Guide | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/guides/DOCKER_GUIDE.md | container와 volume |
| Provider Reference | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/PROVIDER_REFERENCE.md | provider별 connection 방식 |
| Environment Reference | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/ENVIRONMENT.md | production 환경 변수 |
| Changelog | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/CHANGELOG.md | version 차이와 migration 확인 |
| License | https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/LICENSE | MIT license |

## Version을 읽는 법

OmniRoute는 release cadence가 빠르므로 “최신 README”와 “고정 version 문서”를 섞어 읽을 때 주의한다.

```text
학습/비교:
  최신 README로 현재 방향 확인
  + release/v3.8.50 문서로 재현 가능한 기준 고정

운영:
  실제 설치 version 확인
  → 같은 tag/branch의 README, docs, CHANGELOG 확인
  → staging smoke test
  → data backup
  → upgrade
```

### 숫자 검증 규칙

- “290+ providers”, “90+ free-tier providers”, “500+ models”, “19 strategies”는 프로젝트 측 catalog/README 집계로 표기한다.
- provider와 model 수는 documentation version과 live catalog가 다를 수 있다.
- free tier의 quota와 약관은 upstream provider 공식 페이지에서 다시 확인한다.
- cost telemetry는 routing 참고값으로 사용하고 실제 invoice와 정기적으로 대조한다.

## 소스 검토 체크리스트

- [ ] URL이 `diegosouzapw/OmniRoute`를 가리키는가?
- [ ] 문서 branch/tag가 설치 version과 일치하는가?
- [ ] endpoint와 header가 API Reference에 존재하는가?
- [ ] provider authentication 방식이 공식적으로 지원되는가, wrapper인가?
- [ ] OAuth 또는 cookie 사용이 upstream terms와 조직 policy에 맞는가?
- [ ] deprecated option과 migration note를 CHANGELOG에서 확인했는가?
- [ ] 보안 주장을 “기능 존재”와 “formal compliance 인증”으로 구분했는가?

## 이 vault의 학습 노트

- [[README|학습 진입점]]
- [[01-overview|What, Why, architecture]]
- [[02-ecosystem|대안 비교]]
- [[04-learning/01-getting-started|설치와 첫 호출]]
- [[04-learning/02-deep-dive|routing과 운영 심화]]
- [[05-projects|프로젝트]]
- [[cheatsheet|빠른 참조]]

## Sources

- https://github.com/diegosouzapw/OmniRoute
- https://github.com/diegosouzapw/OmniRoute/tree/release/v3.8.50/docs
- https://github.com/diegosouzapw/OmniRoute/releases
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/CHANGELOG.md
