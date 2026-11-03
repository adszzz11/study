---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem 비교

[[tech/ai/claude-trading-tools/README|README]] · [[tech/ai/claude-trading-tools/01-overview|Overview]]

| 선택지 | 역할 | 강점 | 주의점 |
|---|---|---|---|
| `tradesdontlie/tradingview-mcp` | TradingView Desktop MCP bridge | 실제 열린 chart/Pine output을 읽음 | 비공식, CDP 권한과 Desktop 실행 필요 |
| `LewisWJackson/tradingview-mcp-jackson` | 원 프로젝트 계열 fork | 다른 수정·기능을 제공할 수 있음 | fork별 code review·update 추적 필요 |
| `tradermonty/claude-trading-skills` | Claude Skills workflow toolkit | risk review·journal·postmortem process화 | FMP, Alpaca, FINVIZ, CSV가 필요할 수 있음 |
| 직접 Market-data API | 정형 시세·fundamental 데이터 | 재현성, server-side automation | Pine drawing·현재 chart UI context가 약함 |
| 수동 TradingView + spreadsheet | human-led 분석 | 최소 권한, 단순한 audit trail | 반복 작업과 기록 누락 |

## 선택 기준

- 화면에 열려 있는 분석 맥락이 필요하면 MCP bridge를 우선 검토한다.
- 대량 데이터 처리나 nightly report에는 provider API/CSV를 source of truth로 둔다.
- trade execution과 research workflow를 결합하지 않는다. MCP와 Skills의 output은 검토 자료이며 주문 명령이 아니다.
- fork를 채택할 때는 upstream 대비 commit, release, dependency, CDP 접근 범위를 별도 비교한다.

## Sources

- https://github.com/tradesdontlie/tradingview-mcp
- https://github.com/LewisWJackson/tradingview-mcp-jackson
- https://github.com/tradermonty/claude-trading-skills
