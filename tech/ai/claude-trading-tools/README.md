---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude 기반 TradingView MCP와 Trading Skills

> **한 줄 정의**: Claude 같은 AI agent에 TradingView Desktop의 chart context와 재사용 가능한 trading workflow를 연결해 분석·기록·복기를 지원하는 오픈소스 MCP/Skills 조합이다.

## Overview

`tradesdontlie/tradingview-mcp`는 실행 중인 TradingView Desktop chart를 MCP tool로 읽고 조작하는 community bridge다. `tradermonty/claude-trading-skills`는 market review, position sizing, journal, postmortem을 반복 가능한 Claude Skills workflow로 만든다.

두 도구를 함께 쓰면 AI가 추측한 chart가 아니라 사용자가 열어 둔 chart state를 근거로 분석 초안을 만들 수 있다. 권장 범위는 **research, review, 기록**이며, 매수·매도 판단과 broker execution은 사람이 맡는다.

```text
Claude / MCP client → MCP server → CDP localhost:9222 → TradingView Desktop
       Skills: review · sizing · journal · postmortem
```

## Learning Path

- [ ] [[tech/ai/claude-trading-tools/01-overview|Overview]] — What/Why, 구성 요소와 권한 경계
- [ ] [[tech/ai/claude-trading-tools/02-ecosystem|Ecosystem]] — MCP bridge, fork, Skills, API 대안 비교
- [ ] [[tech/ai/claude-trading-tools/04-learning/01-getting-started|시작하기]] — read-only 연결과 첫 chart 검증
- [ ] [[tech/ai/claude-trading-tools/04-learning/02-deep-dive|심화]] — Pine, Skills, journal, 보안 설계
- [ ] [[tech/ai/claude-trading-tools/05-projects|Projects]] — 안전한 적용 패턴 네 가지
- [ ] [[tech/ai/claude-trading-tools/03-references|References]] — 설치 전 확인할 원문과 사양
- [ ] [[tech/ai/claude-trading-tools/cheatsheet|Cheatsheet]] — 도구 흐름과 점검표 빠른 참조

## When To Use

- 열린 TradingView chart, indicator, Pine Script output을 분석의 근거로 남길 때
- market review와 trade journal의 형식을 팀 또는 개인에게 일관되게 적용할 때
- read-only chart 검증, backtest 복기, Pine Script 개발 보조가 필요할 때

## When Not To Use

- 자동 주문, 투자 조언 생성, 손실 한도 우회가 목적일 때
- CDP endpoint를 외부 network에 공개해야 하는 환경일 때
- 재현 가능한 server-side 시세 파이프라인만 필요하고 chart UI context가 불필요할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://github.com/tradesdontlie/tradingview-mcp
- https://github.com/tradermonty/claude-trading-skills
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
