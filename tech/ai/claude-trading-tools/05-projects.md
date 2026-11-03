---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

[[tech/ai/claude-trading-tools/README|README]] · [[tech/ai/claude-trading-tools/cheatsheet|Cheatsheet]]

## 1. Daily market review assistant

chart state와 market breadth를 읽어 risk-on/risk-off의 **근거와 human checklist**만 만든다. 주문을 제안하거나 실행하지 않으며, 각 항목의 source와 timestamp를 남긴다.

## 2. Pine Script development loop

요구사항 → Pine inject/compile → compiler error와 visual output 확인 → test record 순서로 운영한다. screenshot은 change review의 증거로 보관한다.

## 3. Trade journal / postmortem

진입 전 thesis, risk limit, chart snapshot을 YAML/CSV로 기록하고, 종료 후 outcome과 반복 실수를 분석한다. `signal-postmortem`은 결론을 대신 내리는 도구가 아니라 review template이다.

## 4. Research-only dashboard

MCP의 chart context와 외부 CSV/API 데이터를 분리 저장한다. dashboard는 report와 alert 후보만 생산하며, execution capability와 broker credential을 포함하지 않는다.

## 공통 acceptance criteria

- 모든 output에 source, timestamp, assumption, human decision이 있다.
- chart read와 external data의 provenance를 구분한다.
- 자동 주문·계좌 접근·투자 조언을 scope에서 제외한다.

## Sources

- https://github.com/tradermonty/claude-trading-skills
- https://github.com/tradesdontlie/tradingview-mcp/wiki
