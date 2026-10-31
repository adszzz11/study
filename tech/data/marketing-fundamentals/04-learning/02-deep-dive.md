---
date: 2026-06-11
tags:
  - tech
  - data
  - marketing
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# 심화: 4-6개월차

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

## 4-5개월차: 디지털 마케팅 실행

### 학습 개념

- SEO, content marketing, paid search, paid social
- email marketing, CRM, influencer, community
- campaign brief, media plan, creative testing
- landing page optimization

### Campaign Brief 템플릿

```markdown
## Campaign Brief

- Objective:
- Target segment:
- Insight:
- Value proposition:
- Main message:
- Offer:
- Channels:
- Budget:
- KPI:
- Creative hypotheses:
- Landing page sections:
- Measurement plan:
```

### Creative Test 설계

| 가설 | Creative angle | 측정 지표 |
|---|---|---|
| 고객은 가격보다 시간 절약에 반응한다 | "하루 30분 절약" | CTR, CVR |
| 고객은 social proof에 반응한다 | "10만 명이 선택" | CTR, add-to-cart |
| 고객은 risk reversal에 반응한다 | "7일 무료 환불" | CVR, refund rate |

---

## 6개월차: 데이터와 실험

### 핵심 지표

| Metric | 의미 | 주의점 |
|---|---|---|
| CTR | impression 대비 click 비율 | 클릭만 높고 전환이 낮을 수 있음 |
| CVR | visit/click 대비 conversion 비율 | traffic quality와 offer 영향을 함께 받음 |
| CAC | 고객 1명 획득 비용 | 채널별 attribution 기준 확인 필요 |
| LTV | 고객 생애 가치 | retention과 margin 가정에 민감 |
| ROAS | 광고비 대비 매출 | profit이 아니라 revenue 기준인 경우가 많음 |
| Retention | 고객 유지율 | cohort 단위로 봐야 의미가 커짐 |

### KPI Tree

```text
Business goal: 월 매출 1억원
  -> New customers
     -> Traffic
        -> Impressions
        -> CTR
     -> Conversion
        -> Landing page CVR
        -> Checkout CVR
  -> Existing customers
     -> Repeat purchase rate
     -> Email conversion
  -> Economics
     -> CAC
     -> LTV
     -> Gross margin
```

### Funnel Dashboard 예시

| 단계 | 지표 | 예시 값 | 개선 질문 |
|---|---|---:|---|
| Ad impression | impressions | 100,000 | targeting이 충분히 관련 있는가? |
| Click | CTR | 1.8% | creative hook이 약한가? |
| Landing visit | bounce rate | 62% | 메시지 일관성이 있는가? |
| Signup/Purchase | CVR | 2.4% | offer, trust, checkout friction 문제인가? |
| Repeat | 30-day retention | 18% | onboarding과 CRM이 작동하는가? |

---

## A/B Test 기본 설계

```text
Hypothesis:
  Social proof headline will increase landing page conversion rate.

Control:
  "업무 시간을 줄이는 마케팅 자동화"

Variant:
  "3,000개 팀이 쓰는 마케팅 자동화"

Primary metric:
  signup conversion rate

Guardrail metric:
  bounce rate, refund rate, support ticket rate
```

### 체크리스트

- [ ] 하나의 실험은 하나의 primary metric을 둔다.
- [ ] 실험 전 sample size와 최소 실행 기간을 정한다.
- [ ] creative, audience, landing page를 동시에 바꾸면 원인 해석이 어렵다.
- [ ] 단기 ROAS만 보지 말고 retention과 LTV도 확인한다.
- [ ] 유의미한 결과가 나오지 않아도 고객 학습을 기록한다.

---

## AI와 LLM 활용

| 작업 | LLM 활용 | 검증 방법 |
|---|---|---|
| 리뷰 분석 | sentiment, topic, pain point clustering | 사람이 샘플 라벨 검수 |
| 광고 문구 | angle별 copy variation 생성 | creative test 결과로 판단 |
| 경쟁사 분석 | 웹페이지, 리뷰, 가격표 요약 | 원문 링크와 수치 확인 |
| 고객 세그먼트 | CRM note와 행동 로그 요약 | 실제 cohort 지표와 대조 |
| 리서치 자동화 | agent workflow로 반복 수집 | source quality checklist |

관련 구현은 [[study/tech/ai/litellm/README|LiteLLM]], [[study/tech/ai/autoresearch-study/README|AutoResearch Study]], [[study/tech/ai/codex/README|Codex]] 노트를 참고한다.

## 관련 노트

- [[study/tech/ai/litellm/README]]
- [[study/tech/ai/autoresearch-study/README]]
- [[study/tech/data/dolt/README]]
