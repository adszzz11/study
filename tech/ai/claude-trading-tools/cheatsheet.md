---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

[[tech/ai/claude-trading-tools/README|README]] · [[tech/ai/claude-trading-tools/04-learning/01-getting-started|시작하기]]

## 계층별 역할

| 계층 | 하는 일 | 확인할 것 |
|---|---|---|
| MCP client | tool discovery·호출 | 승인 UI와 stdio 설정 |
| MCP server | tool schema를 CDP 작업으로 변환 | release, dependency, tool 권한 |
| CDP | Desktop chart session 접근 | localhost bind, 외부 노출 차단 |
| TradingView Desktop | chart·study·Pine context 제공 | 열린 profile과 data timestamp |
| Claude Skills | review·sizing·journal workflow | 입력 data·provider dependency |

## Read-only 순서

```text
tools/list → health check → chart_get_state
→ data_get_study_values → screenshot → human review → journal
```

## 매 세션 점검

- [ ] 실제 symbol/timeframe/study 값인가, AI 추정인가?
- [ ] data source와 timestamp를 기록했는가?
- [ ] CDP가 localhost에만 열렸는가?
- [ ] fork의 commit/release를 확인했는가?
- [ ] tool output을 주문 지시가 아닌 검토 자료로 다루는가?
- [ ] human decision과 risk limit을 journal에 남겼는가?

## 기억할 제한

MCP는 TradingView의 공식 integration이 아니다. Skills catalog의 수량도 고정값이 아니며, 설치 전 `skills-index.yaml`과 release를 확인한다. backtest·AI analysis는 수익을 보장하지 않는다.

## Sources

- https://github.com/tradesdontlie/tradingview-mcp/wiki
- https://github.com/tradermonty/claude-trading-skills
