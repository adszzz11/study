---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# CLI-Anything ecosystem

| 선택지 | 주된 대상 | 접근 방식 | CLI-Anything 대비 적합한 경우 |
|---|---|---|---|
| CLI-Anything | desktop app, codebase, API | 대상 backend를 감싼 새 CLI harness 생성 | source/API가 있고 재현 가능한 domain workflow가 필요할 때 |
| Native API + 자체 CLI | 공식 API 서비스 | SDK/OpenAPI를 직접 사용 | API contract가 이미 충분히 좋을 때 |
| MCP server | tool-enabled agent | JSON Schema 기반 tool discovery/call protocol | 여러 agent client에 표준 tool interface가 필요할 때 |
| Playwright CLI | Web browser | DOM/browser automation CLI·skill | 웹 앱만 대상이고 UI/DOM automation이 필요할 때 |
| Microsoft UFO² | Windows desktop | GUI automation과 native API를 결합한 agent system | source 없이 여러 Windows 앱을 즉시 넘나들 때 |

## MCP와의 관계

MCP는 tool schema와 structured result를 표준화하지만, 특정 desktop app에 맞는 domain command를 자동 설계하지는 않는다. CLI-Anything은 harness 생성에 집중한다. 따라서 둘은 대체재라기보다, **CLI-Anything harness를 MCP tool로 감싸는 방식**으로 결합할 수 있다.

```text
Agent client → MCP tool schema → CLI-Anything harness → native backend → artifact
```

이 조합에서도 CLI 자체의 input validation, authorization, output schema, artifact 검증은 유지해야 한다. MCP wrapper는 policy와 transport를 표준화할 뿐 backend safety를 대신하지 않는다.

## 선택 질문

- API가 이미 task 단위 command와 안정적인 response를 제공하는가? 그렇다면 native API CLI를 먼저 고려한다.
- agent client가 여러 개인가? 그렇다면 MCP wrapper를 추가한다.
- UI가 유일한 접근 수단인가? Web은 Playwright, Windows desktop은 UFO² 평가가 출발점이다.
- source/API와 반복할 domain workflow가 있는가? CLI-Anything이 가장 잘 맞는다.

## Sources

- https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- https://playwright.dev/docs/getting-started-cli
- https://github.com/microsoft/UFO
- https://github.com/HKUDS/CLI-Anything
