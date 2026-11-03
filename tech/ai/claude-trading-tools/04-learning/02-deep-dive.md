---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: Pine, Skills, Journal, 보안

[[tech/ai/claude-trading-tools/README|README]] · 이전: [[tech/ai/claude-trading-tools/04-learning/01-getting-started|시작하기]]

## Pine Script development loop

Pine Script sample 하나를 열고, AI가 설명으로 만든 값과 chart의 실제 compiler/visual output을 구분한다.

```text
요구사항 작성 → Pine inject/compile → compiler error 확인
→ visual output·screenshot 검토 → 테스트 결과 기록
```

AI가 생성한 script, tool response, screenshot, human review 결과를 한 record로 연결하면 재현성과 복기 품질이 높아진다.

## Journal schema

YAML 또는 CSV에 다음 필드를 고정한다.

```yaml
timestamp: 2026-11-03T09:30:00+09:00
source: TradingView Desktop / external CSV
symbol: EXAMPLE
assumptions: [data-delay-unknown]
thesis: human-written thesis
risk_limit: predefined limit
human_decision: review-required
outcome: pending
```

`position-sizer`의 계산 결과도 추천 주문이 아니라, 사람이 검토할 risk limit 검산 자료로 취급한다. backtest와 AI analysis는 미래 수익을 보장하지 않는다.

## 보안 checklist

- CDP remote-debugging을 `localhost`에만 bind한다.
- MCP server와 Skills dependency의 release, commit, 권한을 설치 전에 검토한다.
- 읽기와 상태 변경 tool을 분리하고, 후자에는 explicit confirmation을 둔다.
- broker credential, account number, private journal은 prompt와 screenshot에서 최소화·redact한다.
- tool output이 외부 data provider에서 왔으면 provider와 timestamp를 기록한다.

## Sources

- https://chromedevtools.github.io/devtools-protocol/
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://tradermonty.github.io/claude-trading-skills/
