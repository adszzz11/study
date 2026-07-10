---
date: 2026-06-11
tags:
  - tech
  - data
  - marketing
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# 실전 프로젝트

## 1. Brand Teardown

Nike, Apple, Toss, 무신사 중 1개 브랜드를 골라 `STP + 4P + Positioning Map`으로 분석한다.

### 산출물

- 1-page brand summary
- `3C` 분석표
- `STP` 분석
- `4P` 분석
- 경쟁 브랜드 2개와 positioning map
- 개선 가설 3개

```text
Positioning Map 예시

Premium
  ^
  |       Apple
  |
  |  Samsung
  |
  +-----------------> Simplicity
```

---

## 2. Consumer Research Sprint

인터뷰 5명, 설문 30명, 리뷰 100개로 `persona`, `buying trigger`, `purchase barrier`를 도출한다.

| 방법 | 목표 | 산출물 |
|---|---|---|
| Interview 5명 | 맥락과 언어 수집 | quote bank |
| Survey 30명 | 패턴 확인 | segment table |
| Review 100개 | 실제 pain/benefit 수집 | topic clusters |
| Journey map | 구매 흐름 정리 | touchpoint map |

### 인터뷰 질문 예시

```text
1. 이 제품/카테고리를 처음 찾게 된 계기는 무엇인가요?
2. 구매 전에 비교한 대안은 무엇인가요?
3. 구매를 망설이게 만든 요인은 무엇인가요?
4. 최종적으로 구매하게 만든 결정적 이유는 무엇인가요?
5. 사용 후 기대와 달랐던 점은 무엇인가요?
```

---

## 3. Campaign Simulation

예산 100만원을 가정하고 `Google Search + Instagram + Email` campaign을 설계한다.

| 항목 | 설계 |
|---|---|
| Objective | 첫 구매 100건 |
| Budget | 1,000,000 KRW |
| Channels | Google Search, Instagram, Email |
| Primary KPI | CAC, CVR |
| Guardrail | refund rate, unsubscribe rate |

### Budget Plan 예시

| Channel | Budget | 역할 |
|---|---:|---|
| Google Search | 500,000 | high-intent demand capture |
| Instagram | 350,000 | awareness와 creative test |
| Email | 150,000 | lead nurturing과 재방문 |

---

## 4. Landing Page Experiment

같은 제품에 대해 landing page headline과 offer를 바꾸는 A/B test를 설계한다.

| Version | Headline | Offer | 가설 |
|---|---|---|---|
| Control | "업무 시간을 줄이는 마케팅 도구" | 무료 체험 | 기능 benefit 중심 |
| Variant A | "마케터의 반복 업무를 하루 30분 줄이세요" | 무료 체험 | 구체적 시간 절약 |
| Variant B | "3,000개 팀이 선택한 마케팅 자동화" | 무료 체험 | social proof |

### 측정 계획

- Primary metric: signup CVR
- Secondary metric: click depth, scroll depth
- Guardrail metric: refund, support ticket, unsubscribe
- Segment: new visitor vs returning visitor

---

## 5. Marketing Analytics Mini Dashboard

샘플 데이터를 만들어 funnel dashboard와 cohort table을 구성한다.

```csv
date,channel,impressions,clicks,visits,signups,purchases,cost,revenue
2026-06-01,google_search,10000,430,390,45,12,120000,360000
2026-06-01,instagram,20000,260,240,30,5,90000,150000
```

| Dashboard | 포함 지표 |
|---|---|
| Acquisition | impressions, clicks, CTR, CPC |
| Activation | visits, signups, signup CVR |
| Revenue | purchases, CAC, ROAS |
| Retention | repeat purchase, cohort retention |

## 관련 노트

- [[study/tech/data/dolt/README]] - 프로젝트 데이터셋 버전 관리
- [[study/tech/ai/litellm/README]] - 리뷰/문구 분석 자동화
- [[study/tech/ai/autoresearch-study/README]] - 리서치 프로젝트 루프
