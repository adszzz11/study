---
date: 2026-06-11
tags:
  - tech
  - data
  - marketing
  - ecosystem
type: tech-tool-study
parent: "[[README]]"
---

# 마케팅 생태계와 비교

## 학습 영역 비교

| 영역 | 먼저 배울 것 | 대안/확장 | 언제 중요한가 |
|---|---|---|---|
| 전략 프레임워크 | `STP`, `4P`, `3C` | Jobs-to-be-Done, Blue Ocean, Brand Equity | 시장, 고객, 포지셔닝을 잡을 때 |
| 소비자 이해 | Consumer Journey, Motivation, Perception | Behavioral Economics, UX Research, Ethnography | 메시지와 제품 경험을 설계할 때 |
| 디지털 실행 | SEO, Content, Google Ads, Email | Meta, TikTok, YouTube, Influencer, Community | 트래픽과 수요 창출이 필요할 때 |
| 데이터/분석 | GA4, Funnel, Cohort, A/B Test | MMM, Incrementality, CDP, Clean Room | 예산 배분과 성과 검증이 필요할 때 |
| 자격증 | AMA PCM, Google Ads/Analytics, HubSpot | DMI CDMP, CIM, Meta Blueprint | 취업, 전직, 실무 신뢰도 확보 시 |

---

## 프레임워크별 역할

| Framework | 핵심 질문 | 결과물 |
|---|---|---|
| `3C` | 고객, 회사, 경쟁자는 어떤 상태인가? | 시장 상황 진단 |
| `SWOT` | 내부 강약점과 외부 기회위협은 무엇인가? | 전략 이슈 목록 |
| `STP` | 어떤 세그먼트를 고르고 어떤 위치를 차지할 것인가? | target segment, positioning |
| `4P` | 제품, 가격, 유통, 프로모션을 어떻게 맞출 것인가? | go-to-market mix |
| Customer Journey | 고객은 어떤 접점을 거쳐 구매하는가? | touchpoint map |
| KPI Tree | 어떤 지표가 최종 목표와 연결되는가? | measurement plan |

```text
3C/SWOT -> STP -> 4P -> Journey -> Campaign -> KPI Tree
```

---

## 채널 생태계

| Channel | 강점 | 약점 | 우선 학습 상황 |
|---|---|---|---|
| SEO | 장기 organic demand 확보 | 시간이 오래 걸림 | 정보 탐색형 카테고리 |
| Paid Search | 구매 의도가 강한 수요 포착 | 경쟁이 높으면 CPC 상승 | 명확한 검색 수요가 있을 때 |
| Paid Social | 타겟 확장과 creative test | 의도 낮은 traffic이 많음 | D2C, app, lifestyle brand |
| Email/CRM | retention과 재구매에 강함 | first-party data 필요 | 기존 고객 기반이 있을 때 |
| Content | 교육, 신뢰, thought leadership | 성과 측정이 느릴 수 있음 | B2B, 고관여 제품 |
| Community | loyalty와 advocacy 형성 | 운영 난이도 높음 | 팬덤, 전문가, 개발자 시장 |

---

## 도구와 데이터 스택

| 목적 | 기본 도구 | 확장 도구 |
|---|---|---|
| Web/App analytics | GA4 | Amplitude, Mixpanel |
| Ads execution | Google Ads, Meta Ads | TikTok Ads, YouTube Ads |
| CRM | HubSpot | Salesforce, Braze |
| SEO | Google Search Console | Ahrefs, Semrush |
| Experiment | GA4 experiments, Optimizely | Statsig, GrowthBook |
| Data analysis | Sheets, Looker Studio | BigQuery, dbt, Python |
| AI analysis | LLM prompt, sentiment analysis | RAG, agent workflow, text clustering |

마케팅 데이터가 커지면 raw event, campaign cost, CRM, sales data를 연결해야 한다. 이때 데이터 버전과 분석 재현성은 [[study/tech/data/dolt/README|Dolt]] 같은 데이터 버전 관리 개념과도 연결된다.

---

## 자격증 비교

| Certification | 난이도 | 비용 감각 | 적합한 사람 |
|---|---|---|---|
| HubSpot Academy | 입문 | 무료 중심 | content, inbound, CRM 기초를 빠르게 익히려는 사람 |
| Google Ads / Analytics Skillshop | 입문-실무 | 무료 중심 | 검색광고, 측정, GA4 기본을 증명하려는 사람 |
| AMA PCM Marketing Management | 중급 | 유료 | 마케팅 원론과 전략 프레임워크를 정석 검증하려는 사람 |
| DMI CDMP | 중급 | 유료 | digital marketing 전반을 포트폴리오와 함께 묶으려는 사람 |
| CIM Qualifications | 중급-고급 | 유료 | 글로벌 커리어와 장기 qualification이 필요한 사람 |
| Meta Blueprint | 실무 | 일부 유료 | Meta/Instagram 광고 운영 신뢰도를 보강하려는 사람 |

## 관련 노트

- [[study/tech/ai/llm-wiki-study/README]] - 마케팅 지식 베이스와 리서치 워크플로우 설계 참고
- [[study/tech/ai/litellm/README]] - 여러 LLM으로 소비자 리뷰 분석을 돌릴 때 참고
- [[study/tech/data/cloudflare-r2/README]] - 크리에이티브와 리서치 파일 저장소 설계 참고
