---
date: 2026-06-11
tags:
  - tech
  - data
  - marketing
  - framework
type: tech-tool-study
parent: "[[README]]"
---

# 마케팅 개요

> Marketing은 `creating, communicating, delivering, and exchanging offerings`를 통해 고객과 시장에 가치를 만드는 활동이다.

## What

마케팅은 광고 집행만 뜻하지 않는다. 정석적인 마케팅은 아래 흐름으로 움직인다.

```text
Market understanding
  -> Customer insight
  -> Value proposition
  -> STP strategy
  -> 4P execution
  -> Measurement and learning
```

| 층위 | 질문 | 대표 도구 |
|---|---|---|
| 시장 이해 | 어떤 시장과 카테고리인가? | `3C`, `PESTEL`, category analysis |
| 고객 이해 | 누가 왜 구매하는가? | persona, interview, survey, review mining |
| 전략 | 누구에게 어떤 위치로 기억될 것인가? | `STP`, positioning map, value proposition |
| 실행 | 제품, 가격, 유통, 프로모션을 어떻게 설계할 것인가? | `4P`, campaign brief, media plan |
| 측정 | 무엇이 성과이고 무엇을 배웠는가? | funnel, CAC, LTV, ROAS, A/B test |

---

## Why

마케팅을 처음 배울 때 바로 `Google Ads`, `Instagram`, `SEO`부터 들어가면 채널 운영 기술은 익힐 수 있지만 전략 판단력이 약해지기 쉽다.

- `STP` 없이 광고를 하면 누구에게 말하는지 흐려진다.
- `4P` 없이 promotion만 최적화하면 제품, 가격, 유통 문제가 가려진다.
- `Consumer Behavior` 없이 메시지를 쓰면 고객의 동기, 불안, 구매 장벽을 놓친다.
- `Measurement` 없이 캠페인을 돌리면 예산 배분과 학습이 감에 의존한다.

정석 학습의 목표는 "광고 세팅을 할 줄 아는 사람"이 아니라 `시장과 고객을 해석하고, 실행을 설계하고, 데이터로 검증하는 사람`이 되는 것이다.

---

## 핵심 특징

### 1. Foundation

- `Marketing definition`: 가치 있는 offering을 만들고 전달하고 교환하는 체계
- `Market`: 고객, 경쟁자, 대체재, 유통 구조가 만나는 장
- `Customer value`: 고객이 얻는 benefit과 지불하는 cost의 균형
- `Brand`: 고객 기억 속의 의미, 차별점, 신뢰

### 2. Strategy

- `3C`: Customer, Company, Competitor
- `STP`: Segmentation, Targeting, Positioning
- `4P`: Product, Price, Place, Promotion
- `Positioning statement`: 누구에게, 어떤 문제를, 어떤 차별점으로 해결하는지 한 문장으로 정리

```text
For [target segment],
[brand/product] is the [category]
that provides [primary benefit]
because [reason to believe].
```

### 3. Consumer Behavior

- 구매 의사결정: need recognition -> information search -> evaluation -> purchase -> post-purchase
- 심리 요소: motivation, perception, attitude, memory
- 행동경제학: heuristics, social proof, loss aversion, anchoring
- 접점 설계: customer journey, touchpoint, moment of truth

### 4. Execution

- Content, SEO, paid search, paid social
- Email, CRM, influencer, community
- Campaign brief, media plan, creative testing
- Landing page optimization, lifecycle marketing

### 5. Measurement

- `KPI tree`: business goal -> marketing KPI -> channel metric
- Funnel metrics: impression, CTR, CVR, retention
- Unit economics: CAC, LTV, ROAS, payback period
- Experimentation: A/B test, cohort analysis, attribution, incrementality

---

## 2025-2026 변화

| 변화 | 의미 | 학습 포인트 |
|---|---|---|
| AI in Search/Shopping/Creative/Bidding | 마케터가 수동 운영자에서 전략, 데이터, 브랜드 의사결정자로 이동 | AI-assisted creative, smart bidding, agentic workflow |
| Privacy와 third-party cookie 약화 | first-party data와 consent 기반 측정 중요 | CRM, consent, server-side tagging, measurement design |
| LLM 기반 소비자 분석 | 리뷰, 검색어, CRM, VOC, 행동 로그 분석 확장 | sentiment analysis, topic clustering, insight validation |

## 관련 노트

- [[study/tech/ai/litellm/README]] - LLM 기반 소비자 리뷰 분석을 구현할 때 참고
- [[study/tech/ai/autoresearch-study/README]] - 조사와 실험 루프 설계 참고
- [[study/tech/data/dolt/README]] - 마케팅 데이터셋 버전 관리 참고
