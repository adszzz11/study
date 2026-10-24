---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# The Pragmatic Engineer — Projects

[[tech/devtools/the-pragramitic-engineer/README|학습 진입점]] · 다음: [[tech/devtools/the-pragramitic-engineer/cheatsheet|Cheatsheet]]

## 1. AI Developer Tooling Radar

Cursor, Claude Code, Codex를 월간 scorecard로 비교한다. 제품 사실은 vendor 문서에서 확인하고, 비교 기준과 팀 영향은 사례 분석으로 보완한다.

| 항목 | 질문 | 기록 예시 |
|---|---|---|
| Privacy | 어떤 code·telemetry가 외부로 가는가? | 정책 URL, opt-out, data retention |
| Context | context window와 repo indexing은 어떤가? | 한계, freshness, 권한 모델 |
| Autonomy | agent가 할 수 있는 변경 범위는? | approval, shell·CI 접근 |
| Integration | CI/CD와 review에 연결되는가? | checks, PR flow, audit log |
| Cost | 실제 team 비용은? | seat, usage, 운영 시간 |

## 2. AI-assisted PR Governance

AI 생성 PR에 대한 team policy를 작성한다. test/eval, human ownership, security scan, small-batch rollout, rollback 기준을 최소 항목으로 둔다. 정책은 도구 이름이 아니라 risk tier와 change scope로 적용해 교체 가능한 구조로 유지한다.

## 3. Engineering Intelligence Brief

매주 The Pulse와 1차 vendor release를 읽고 “우리에게 영향 있는 변화 3개”를 한 페이지로 쓴다.

```text
변화 / 원문 링크 / 우리에게의 영향 / 확신도 / 다음 행동 / 담당자
```

확신도가 낮은 항목은 결정이 아니라 조사 backlog로 분류한다.

## 4. Reliability Case Study

Cursor의 growth·migration 사례를 템플릿으로 삼아 자사 서비스의 bottleneck, data migration, outage response plan을 문서화한다. 특히 migration 전후의 data integrity check, feature flag, rollback owner를 명시한다.

## 5. Career/Skills Map

AI engineering 전환에 필요한 LLM eval, RAG/context engineering, observability, secure coding 역량을 현재 competency matrix에 매핑한다. 개인의 도구 숙련도와 팀의 안전한 release 능력을 별도 축으로 평가한다.

## Sources

- [Building Cursor](https://newsletter.pragmaticengineer.com/p/cursor)
- [2025 Survey](https://newsletter.pragmaticengineer.com/p/the-pragmatic-engineer-2025-survey)
- [2026 Sitemap](https://newsletter.pragmaticengineer.com/sitemap/2026)
