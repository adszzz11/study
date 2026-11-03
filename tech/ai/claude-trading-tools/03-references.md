---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# References

[[tech/ai/claude-trading-tools/README|README]] · 설치 전에는 repository README, release, `skills-index.yaml`을 함께 확인한다.

| 자료 | 확인 목적 |
|---|---|
| [원본 Instagram 릴](https://www.instagram.com/reel/DfN2HOyB0nU/?obrf=a2k0NHdiMDRjcDhp) | 학습 주제의 출발점 확인 |
| [tradesdontlie/tradingview-mcp](https://github.com/tradesdontlie/tradingview-mcp) | upstream source, setup, release 확인 |
| [TradingView MCP Wiki](https://github.com/tradesdontlie/tradingview-mcp/wiki) | architecture와 tool overview 확인 |
| [tradingview-mcp-jackson](https://github.com/LewisWJackson/tradingview-mcp-jackson) | fork의 독립 변경점 검토 |
| [claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | Skills catalog와 dependency 확인 |
| [Claude Trading Skills 문서](https://tradermonty.github.io/claude-trading-skills/) | workflow 사용법 확인 |
| [MCP Tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | `tools/list`, schema, `tools/call` 의미 확인 |
| [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) | CDP security surface 이해 |
| [Anthropic Agent Skills guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Skill package와 보안 원칙 확인 |

## 검증 메모

릴에서 언급된 “74개 skill”은 고정 사양으로 다루지 않는다. 2026-11-03 기준 catalog는 계속 확장될 수 있으므로, 설치 시점의 `skills-index.yaml`과 release note를 실제 기준으로 삼는다.

## Sources

- https://github.com/tradermonty/claude-trading-skills
- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
