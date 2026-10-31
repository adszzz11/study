---
date: 2026-06-09
tags:
  - tech
  - ai
  - stock
  - investing
  - trading-ai
type: tech-tool-study
status: learning
---

# 주식에 대해 공부하고싶어. 어떤거부터 시작하면될지 알려줘. 난 하나도 모르는 초보자니까 초보자에게 알려준다는 기준으로 친절히 알려줘. 그리고 주식 자동화 ai를 만들때 필요한 요소들도 알려줘

> **한 줄 정의**: 주식 투자는 기업의 일부 지분인 `stock`을 사서 장기 성장, 배당, 가격 변동 수익을 기대하는 활동이고, 주식 자동화 AI는 `market data -> strategy/model -> backtest -> risk control -> paper/live execution -> monitoring`을 연결한 의사결정 시스템이다.

## 개요

이 노트는 주식을 처음 배우는 사람을 기준으로 `주식이 무엇인지`, `어떤 순서로 공부해야 하는지`, `자동화 AI를 만들려면 어떤 구성요소가 필요한지`를 정리한다.

중요한 출발점은 "싸게 사서 비싸게 판다"가 아니라 `risk management`다. 초보자는 개별 주식으로 수익을 맞히는 법보다 먼저 손실 가능성, 분산 투자, 투자 기간, 주문 방식, 수수료와 미끄러짐을 이해해야 한다.

관련 AI 자동화 맥락은 [[study/tech/ai/langchain-crewai/README|LangChain-CrewAI]], [[study/tech/ai/codex/README|Codex]], [[study/tech/ai/litellm/README|LiteLLM]] 노트와 함께 보면 좋다.

---

## Quick Start

```text
1. 투자 기초
   stock, ETF, index, dividend, market cap, volatility

2. 계좌와 주문
   market order, limit order, bid/ask spread, slippage

3. 위험 관리
   diversification, position sizing, max loss, cash ratio

4. 데이터 읽기
   OHLCV, adjusted close, split/dividend adjustment, financial statements

5. 전략 실험
   moving average, rebalancing, ETF dollar-cost averaging, momentum

6. 검증
   backtest, out-of-sample, transaction cost, survivorship bias

7. 자동화
   paper trading -> monitoring -> small live execution
```

---

## 학습 경로

### 1단계: 주식 기초 이해

- [ ] [[01-overview|개요]] 읽기 - 주식, ETF, risk, diversification 이해
- [ ] `주식은 회사의 소유권 일부`라는 개념부터 시작
- [ ] `ETF`가 왜 초보자에게 상대적으로 친화적인지 이해

### 2단계: 생태계와 선택지 비교

- [ ] [[02-ecosystem|생태계]] 읽기 - 상품, 데이터, 백테스트, broker API 비교
- [ ] 개별 주식과 ETF 차이 정리
- [ ] VectorBT, Backtrader, QuantConnect LEAN의 역할 구분

### 3단계: 공식 자료 확인

- [ ] [[03-references|참고자료]] 확인 - SEC, FINRA, Alpaca, QuantConnect, OpenAI 문서
- [ ] 규제와 broker 정책은 최신 문서를 확인해야 한다는 점 기록

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - ETF와 개별 주식 비교, 단순 전략 만들기
- [ ] [[04-learning/02-deep-dive|심화]] - bias, risk overlay, execution, monitoring

### 5단계: 프로젝트

- [ ] [[05-projects|실전 프로젝트]] - Portfolio Tracker, DCA Simulator, Backtest Lab
- [ ] [[cheatsheet|치트시트]] - 용어, 체크리스트, 자동화 구조 빠른 참조

---

## 파일 구조

```text
주식에-대해-공부하고싶어-어떤거부터-시작하면될지-알려줘-난-하나도-모르는/
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
| 개요 | [[01-overview]] | What/Why, 초보자 핵심 개념, 자동화 AI 아키텍처 |
| 생태계 | [[02-ecosystem]] | 투자 상품, 데이터/API, 백테스트, AI 도구 비교 |
| 참고자료 | [[03-references]] | 공식 문서, 논문, 학습 소스 |
| 시작하기 | [[04-learning/01-getting-started]] | 초보자 실습 순서 |
| 심화 | [[04-learning/02-deep-dive]] | backtest bias, risk, execution, monitoring |
| 프로젝트 | [[05-projects]] | 실전 프로젝트 아이디어 |
| 치트시트 | [[cheatsheet]] | 용어와 체크리스트 |

---

## 관련 노트

- [[study/tech/ai/langchain-crewai/README]]
- [[study/tech/ai/codex/README]]
- [[study/tech/ai/litellm/README]]
- [[study/tech/ai/llm-wiki-study/README]]

---

**생성일**: 2026-06-09
**상태**: 학습 중
