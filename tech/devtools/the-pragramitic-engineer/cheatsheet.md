---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# The Pragmatic Engineer — Cheatsheet

[[tech/devtools/the-pragramitic-engineer/README|학습 진입점]]

## 매체 구조

| 항목 | 요약 |
|---|---|
| Author | Gergely Orosz — 전 Uber, Skype/Microsoft 및 startup engineer/manager 경력 |
| Format | Research-led Deepdive, The Pulse, Podcast |
| Access | 무료 일부 Deepdive·podcast / 유료 전체 Deepdive·The Pulse·리소스 |
| 읽는 목적 | engineering·AI industry signal을 내부 검증 가능한 가설로 바꾸기 |

## 읽기 프레임

```text
claim → evidence → 내 조직 적용 조건 → 측정 지표
```

- **Claim:** 무엇이 변하고 있다는가?
- **Evidence:** 사례, 수치, 인용 원문은 무엇인가?
- **적용 조건:** 규모, 규제, architecture, team topology가 비슷한가?
- **측정 지표:** 어떤 baseline과 비교해 효과·위험을 판단할까?

## AI coding 도입 지표

| 지표 | 의미 | 주의점 |
|---|---|---|
| Review throughput | reviewer 시간당 완료 PR | code 양과 혼동하지 않기 |
| Test pass rate | CI 통과 PR 비율 | test 품질도 함께 확인 |
| Incident rate | 배포당 incident | change size·배포 빈도 영향 분리 |
| Rollback time | 감지부터 안전 복구까지 시간 | rollback path를 사전에 연습 |

## 빠른 판단

- product spec·가격·privacy: vendor 공식 문서
- 사례·조직 trade-off: The Pragmatic Engineer
- 즉시 code 문제: 공식 문서·issue tracker·Q&A
- 도입 결정: 내부 baseline + small-batch rollout + rollback plan

## Sources

- [About](https://newsletter.pragmaticengineer.com/about)
- [Archive](https://newsletter.pragmaticengineer.com/archive?sort=new)
- [Building Cursor](https://newsletter.pragmaticengineer.com/p/cursor)
- [2026 Sitemap](https://newsletter.pragmaticengineer.com/sitemap/2026)
