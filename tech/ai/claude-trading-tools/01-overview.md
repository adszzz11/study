---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: TradingView MCP와 Claude Trading Skills

[[tech/ai/claude-trading-tools/README|README]]로 돌아가기.

## What

- `tradingview-mcp`는 TradingView Desktop에 Chrome DevTools Protocol(CDP)로 연결하고, MCP `tools/list`/`tools/call`로 chart state, quote, study value, Pine Script output, screenshot, replay 등을 노출한다.
- `tradingview-mcp-jackson`은 upstream과 별개로 검토해야 하는 fork다. 이름이 비슷해도 tool surface와 security change는 같다고 가정할 수 없다.
- `claude-trading-skills`는 실시간 chart 연결이 아니라 market regime, position sizing, journal, postmortem 같은 **의사결정 process**를 재사용하게 한다.

## Why

LLM은 현재 보고 있는 symbol, indicator 값, Pine output을 스스로 알 수 없다. MCP bridge가 실제 열린 chart의 상태를 읽어 이 간극을 줄이며, Skills가 분석 결과를 일관된 review와 기록으로 바꾼다.

## 특징과 권한 경계

| 구분 | MCP bridge | Trading Skills |
|---|---|---|
| 주 역할 | 현재 chart context 획득 | 분석·risk·기록 workflow 재사용 |
| 핵심 입력 | Desktop chart와 CDP | chart 결과, CSV, 선택적 data provider |
| 산출물 | state, indicator 값, screenshot | checklist, sizing 계산, journal, postmortem |
| 안전 경계 | localhost CDP, tool 승인 | human decision, provenance 기록 |

공개 wiki는 15개 범주·84개 tool을 표방하지만, 실제 설치 전 release와 `tools/list` 결과로 확인한다. 이는 TradingView 공식 제품이 아니며 투자 조언 또는 자동 주문 도구가 아니다.

## 안전한 기본 흐름

```text
read → analyze → human review → journal
```

CDP remote-debugging endpoint는 Desktop automation 권한을 줄 수 있다. `localhost`에만 bind하고, 민감하거나 상태를 바꾸는 MCP 호출에는 명시적 confirmation을 둔다.

## Sources

- https://github.com/tradesdontlie/tradingview-mcp/wiki
- https://chromedevtools.github.io/devtools-protocol/
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
