---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Lazyweb MCP Projects

## 1. Signup / paywall 개선

**목표**: 유사 SaaS의 onboarding과 paywall을 근거로 제한된 A/B test 후보를 만든다.

1. `search_screens → search_flows → search_experiments → finalize` 순으로 조사한다.
2. value exposure, CTA, pricing framing을 observation과 hypothesis로 분리한다.
3. 자사 pricing policy, legal copy, accessibility, analytics event를 점검한다.
4. backlog에는 owner, risk, primary metric, guardrail, rollback을 넣는다.

**완료물**: cited research brief, 2~3개 testable variant, measurement plan.

## 2. Competitive UX brief

**목표**: onboarding, checkout, referral flow를 경쟁사별로 비교하는 공유용 Markdown을 만든다.

| 비교 축 | 기록할 내용 |
|---|---|
| Flow | 시작 조건, screen order, exit/branch |
| Evidence | source, capture date, result_ref |
| Pattern | CTA, copy, permission, pricing framing |
| Applicability | 우리 user/job과 맞는 조건 |
| Risk | coverage gap, stale capture, compliance 차이 |

**완료물**: 링크가 있는 brief와 “채택/보류/제외” 결정 로그.

## 3. Landing page growth audit

**목표**: 자사 URL/화면에 대해 Growth Score와 recommendation을 받아 실행 가능한 ticket 후보를 만든다.

- 결과를 priority signal로만 사용한다.
- 유사 사례와 자사 baseline metric을 함께 제시한다.
- claim, price, testimonial은 원 출처와 legal review로 재확인한다.
- production 변경 전 작은 experiment와 rollback path를 합의한다.

## 4. Design QA 보조

현재 화면 이미지를 `compare_image`로 비교해 같은 사용자 목적의 실제 패턴을 찾고, code review checklist로 바꾼다.

```text
reference pattern → 우리 token/brand 제약 → a11y acceptance criteria → component diff → metric check
```

이미지·URL의 접근 scope를 넘어서 저장하거나 공유하지 않는다.

## 5. Agent workflow 표준화

팀 skill에 다음 계약을 넣는다.

1. 조사 목적과 source를 명시한다.
2. 관찰·해석·가설을 섞지 않는다.
3. Figma/design system과 accessibility를 적용한다.
4. implementation은 review 가능한 diff로 만든다.
5. metric으로 검증하고 결과를 research evidence와 분리해 기록한다.

## Sources

- https://www.lazyweb.com/product
- https://www.lazyweb.com/agent-access
