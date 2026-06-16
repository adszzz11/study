---
date: 2026-06-11
tags:
  - tech
  - data
  - marketing
  - consumer-behavior
type: tech-tool-study
status: learning
---

# 마케팅 기초부터 정석적으로 공부하기

> **한 줄 정의**: Marketing은 고객, 파트너, 사회에 가치 있는 `offering`을 만들고, 전달하고, 교환하기 위해 시장을 이해하고 전략을 설계하며 실행과 측정을 반복하는 체계다.

## 개요

이 노트는 "광고 운영"부터 시작하지 않고 `시장 -> 고객 -> 가치제안 -> 실행 -> 측정` 순서로 마케팅을 공부하기 위한 로드맵이다.

초기에는 `STP`, `4P`, `3C`, `SWOT`, `Customer Journey`, `Brand Positioning`으로 전략의 뼈대를 잡고, 이후 `Consumer Behavior`, `Behavioral Economics`, `Marketing Analytics`, `Experimentation`을 얹는다.

AI와 데이터 활용 맥락은 [[study/tech/ai/litellm/README|LiteLLM]], [[study/tech/ai/llm-wiki-study/README|LLM Wiki Study]], [[study/tech/data/dolt/README|Dolt]]와 함께 보면 좋다.

---

## 학습 경로

| 기간 | 주제 | 핵심 개념 | 산출물 |
|---|---|---|---|
| 0-1개월차 | 마케팅 원론 | AMA definition, `3C`, `STP`, `4P`, `SWOT` | 브랜드 3개 분석 |
| 2-3개월차 | 소비자 행동 | motivation, perception, attitude, social proof | 리뷰 100개 pain point 분류 |
| 4-5개월차 | 디지털 실행 | SEO, paid search, paid social, content, email | campaign brief, ad copy, landing page |
| 6개월차 | 데이터와 실험 | GA4, UTM, funnel, cohort, A/B test, CAC, LTV, ROAS | funnel dashboard, 개선 가설 5개 |

## 파일 구조

```text
마케팅에-대해서-기초부터-정석적으로-공부하고-싶어-stp-4p와-같은-기/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|---|---|---|
| 개요 | [[01-overview]] | What/Why, 핵심 프레임워크, 2025-2026 변화 |
| 생태계 | [[02-ecosystem]] | 전략, 소비자 이해, 디지털 실행, 분석, 자격증 비교 |
| 참고자료 | [[03-references]] | 공식 문서, 자격증, 연구 자료 |
| 시작하기 | [[04-learning/01-getting-started]] | 0-3개월차 기초 학습과 실습 |
| 심화 | [[04-learning/02-deep-dive]] | 디지털 실행, 데이터 분석, 실험 설계 |
| 프로젝트 | [[05-projects]] | 브랜드 분석, 소비자 조사, 캠페인 시뮬레이션 |
| 치트시트 | [[cheatsheet]] | 프레임워크, KPI, 자격증 순서 |

---

## 자격증 추천 순서

| 순서 | 자격증 | 추천 이유 |
|---|---|---|
| 1 | HubSpot Digital Marketing / Content Marketing | 무료, 입문자 친화적, content/email/CRM 기본기 |
| 2 | Google Ads Search + Google Analytics via Skillshop | 검색광고와 측정의 실무 기본 |
| 3 | AMA PCM Marketing Management | STP, research, pricing, customer behavior, positioning 정석 검증 |
| 4 | DMI CDMP | digital strategy, AI, PPC, email, GA4를 묶은 실무 패키지 |
| 5 | CIM Foundation/Certificate/Diploma | 영국 및 글로벌 커리어용 체계적 qualification |

## 관련 노트

- [[study/tech/ai/litellm/README]]
- [[study/tech/ai/llm-wiki-study/README]]
- [[study/tech/data/dolt/README]]
- [[study/tech/ai/autoresearch-study/README]]

## Q&A
**Q:** 매주 가설 검증 실험을 한다면 어떤 단계로 시작하는게 좋을까?
**A:** 처음에는 광고 채널이나 copy부터 바꾸기보다, 이 노트의 기본 흐름인 `시장 -> 고객 -> 가치제안 -> 실행 -> 측정`을 1주 단위로 작게 반복하는 게 좋다. 추천 시작 순서는 다음과 같다.

1. `Business goal`을 하나 정한다. 예: signup 20건, 첫 구매 10건, 상담 신청 5건처럼 이번 주에 판단 가능한 목표로 둔다.
2. `Target segment`와 `Customer insight`를 좁힌다. 모든 고객이 아니라 "누가 어떤 pain point/barrier 때문에 망설이는가"를 한 문장으로 쓴다.
3. 하나의 `Hypothesis`만 세운다. 예: "가격 부담을 느끼는 신규 방문자에게 risk reversal 메시지를 보여주면 landing page CVR이 오른다."
4. `4P` 중 무엇을 건드리는 실험인지 정한다. 보통 초반 주간 실험은 `Promotion`의 headline, offer, creative angle, landing page section부터 시작하되, 결과가 계속 약하면 `Product`, `Price`, `Place` 문제인지 되돌아본다.
5. `Primary metric` 하나와 `guardrail metric`을 정한다. 예: primary는 signup CVR, guardrail은 bounce rate, refund rate, unsubscribe rate.
6. 작게 실행하고 기록한다. Control/Variant, audience, channel, 기간, sample size, 결과, 배운 점을 남긴다. 유의미한 결과가 없어도 고객의 pain point, benefit, barrier에 대한 학습을 기록하면 다음 실험의 질이 좋아진다.

초보자라면 첫 4주는 `Customer insight` 검증에 집중하는 편이 좋다. 1주차는 리뷰/인터뷰로 pain point를 모으고, 2주차는 메시지 angle을 테스트하고, 3주차는 offer나 trust 요소를 테스트하고, 4주차는 landing page funnel에서 이탈 구간을 확인한다. 이렇게 해야 매주 실험이 단순한 A/B test가 아니라 `STP`, `4P`, `funnel`, `KPI Tree`를 연결하는 학습 루프가 된다.
