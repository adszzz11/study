---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Browser — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 선택지 비교

| 선택지 | 주요 interface | 장점 | 한계·적합한 용도 |
|---|---|---|---|
| **Playwright / Selenium** | selector·script | 빠르고 재현 가능하며 test에 강함 | workflow를 미리 알아야 함. 안정된 반복 업무의 기본 선택 |
| **Playwright MCP** | accessibility snapshot + MCP tools | vision 없이 구조화된 element 조작, coding agent 연동 용이 | planner는 MCP client가 담당. rich UI·Canvas는 추가 수단 필요 |
| **Stagehand** | Playwright-style API + `act`·`extract`·`observe` | deterministic code와 AI primitive를 한 workflow에서 조합 | model/provider·runtime 비용과 prompt 품질을 관리해야 함 |
| **Browser Use** | Python agent + browser actions, optional vision | agent loop를 빠르게 구성하고 custom tool/model 연결 가능 | production 권한·격리·검증은 application이 설계해야 함 |
| **OpenAI Computer Use / ChatGPT agent** | screenshot UI control + virtual browser/tool | 범용 visual UI와 사용자 제품 경험 | 좌표 오류·latency, 지원 환경과 approval 정책에 의존 |
| **Anthropic Computer Use** | screenshot + mouse/keyboard tool | desktop/browser를 포괄하는 low-level control | prompt injection과 long-horizon reliability 방어 필요 |
| **Remote browser infrastructure** | browser session API/CDP | session 격리, 병렬화, proxy, recording | agent planner가 아니며 운영 비용·data governance 필요 |
| **WebMCP** | declarative HTML + imperative JavaScript tools | website가 semantic typed action을 직접 제공 | 2026 early preview; adoption 필요, manifest/output도 공격 경로 |

## 계층으로 보기

서로 경쟁하는 제품처럼 보여도 실제로는 다른 계층을 담당할 수 있다.

```text
Agent / Planner
  ├─ Browser Use, custom LLM loop
  └─ ChatGPT agent 같은 integrated product
          ↓
Action interface
  ├─ Playwright MCP
  ├─ Stagehand primitives
  ├─ raw Playwright / Selenium
  └─ WebMCP tools
          ↓
Browser runtime
  ├─ local Chrome
  ├─ isolated container
  └─ remote/cloud browser
```

## 목적별 선택

| 요구사항 | 먼저 검토할 선택 | 이유 |
|---|---|---|
| 안정된 E2E test | Playwright | deterministic assertion, trace, CI 재현성 |
| coding agent가 page 구조를 탐색 | Playwright MCP | accessibility snapshot과 structured action |
| 기존 Playwright code에 AI 탐색 일부 추가 | Stagehand | deterministic/agentic step을 혼합하기 쉬움 |
| Python으로 browser agent prototype | Browser Use | agent loop와 browser integration을 빠르게 시작 |
| Canvas·image-only UI·remote desktop | visual Computer Use | DOM 없이 pixel로 관찰·조작 가능 |
| 대규모 병렬 session·recording | remote browser infrastructure | runtime 운영 기능을 분리 |
| website 자체를 agent-ready로 설계 | WebMCP | semantic action을 site가 명시적으로 노출 |
| API가 존재하는 반복 workflow | API + script | browser를 거치지 않는 편이 더 빠르고 안정적 |

## Playwright MCP: MCP와 CLI의 역할

Playwright MCP는 accessibility snapshot을 model에 제공하고 browser action을 MCP tool로 노출한다. 공식 README는 최신 coding agent의 고처리량 workflow에서는 간결한 CLI+Skills가 더 token-efficient할 수 있고, 지속 session·구조 탐색·iterative reasoning이 중요한 agentic loop에는 MCP가 유리하다고 구분한다.

| 기준 | CLI + Skills | Playwright MCP |
|---|---|---|
| Context 비용 | 목적별 command가 간결 | tool schema와 snapshot이 더 큼 |
| Session | command 중심 | persistent state와 introspection에 강함 |
| 적합성 | coding workflow, test 실행 | 탐색, self-healing, long-running loop |

## WebMCP가 바꾸는 interface

기존 browser agent는 pixel coordinate나 DOM selector에서 action을 추론했다. WebMCP는 site가 `search_flights`, `submit_ticket` 같은 의미론적 tool을 제공하도록 하며 두 API 방향을 제안한다.

- **Declarative API:** HTML form으로 표현할 수 있는 표준 action
- **Imperative API:** JavaScript 실행이 필요한 복잡하고 동적인 action

이는 raw DOM actuation의 ambiguity를 줄이지만 security boundary가 되지는 않는다. Tool name, description, parameter, output 모두 indirect prompt injection을 담을 수 있다.

## 조합 패턴

### Deterministic shell, agentic center

```text
fixed login/navigation
  → agent discovers changed form fields
  → deterministic validation
  → user approval
  → fixed submit + receipt verification
```

### Structure-first, vision-fallback

```text
accessibility tree → role/label action
                   ↘ missing/Canvas → screenshot + coordinate action
```

### Discovery-to-script

1. Agent가 unknown workflow를 탐색한다.
2. 성공 trace에서 stable selector와 precondition을 추출한다.
3. 반복 경로를 Playwright script로 승격한다.
4. UI drift가 생길 때만 agentic fallback을 호출한다.

## Sources

- [Playwright](https://playwright.dev/)
- [Selenium](https://www.selenium.dev/documentation/)
- [Microsoft — Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Browserbase — Stagehand](https://github.com/browserbase/stagehand)
- [Browser Use](https://github.com/browser-use/browser-use)
- [OpenAI — Computer-Using Agent](https://openai.com/index/computer-using-agent/)
- [Anthropic — Computer Use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool)
- [Chrome for Developers — WebMCP early preview](https://developer.chrome.com/blog/webmcp-epp)

