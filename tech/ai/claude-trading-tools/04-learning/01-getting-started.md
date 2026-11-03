---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Read-only chart 검증

[[tech/ai/claude-trading-tools/README|README]] · 다음: [[tech/ai/claude-trading-tools/04-learning/02-deep-dive|심화]]

## 목표

TradingView Desktop의 별도 profile에서 MCP 연결을 만들고, 상태 변경 없이 실제 chart context를 읽는다.

## 순서

1. MCP의 `tools/list`, tool input schema, `tools/call`, `stdio` transport를 먼저 확인한다.
2. TradingView Desktop을 별도 profile로 실행하고 CDP endpoint를 `localhost`에만 연다. 외부 IP bind와 port forwarding은 금지한다.
3. MCP client에서 health check를 호출한다.
4. `chart_get_state`로 symbol, timeframe, pane 등 현재 chart 상태를 확인한다.
5. `data_get_study_values`로 RSI, MACD, EMA 등 실제 study 값을 읽는다.
6. screenshot을 남기고, response의 timestamp·source·assumption을 journal에 기록한다.

```text
health check
  → chart_get_state
  → data_get_study_values
  → screenshot
  → human review + journal
```

## 최소 Skills 묶음

처음부터 전체 catalog를 설치하지 않는다. `market-breadth-analyzer`, `uptrend-analyzer`, `position-sizer`, `trader-memory-core`, `signal-postmortem` 중 필요한 workflow만 선택한다. 선택한 skill이 요구하는 CSV, API key, provider 약관도 별도로 확인한다.

## 완료 조건

- AI의 추정이 아닌 열린 chart의 symbol과 study value를 확인했다.
- endpoint가 localhost 외부에서 접근되지 않는다.
- 결과에 data timestamp, source, human decision을 남겼다.

## Sources

- https://github.com/tradesdontlie/tradingview-mcp
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
