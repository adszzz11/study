---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Mod: What, Why, How

## What

Claude Mod는 Claude Code plugin의 hooks module이다. module은 `register(on, options)`를 export하고, 각 handler는 `($, e, next)`로 engine API, event data, 다음 middleware를 받는다.

```ts
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  if (e.command.includes("rm -rf")) return { deny: "Destructive command blocked" };
  return next(e);
});
```

이 모델은 event를 세 방식으로 다룬다.

| 방식 | 구현 | 예 |
| --- | --- | --- |
| Observe | `await next(e)` 뒤 결과를 기록 | turn 완료 뒤 usage 저장 |
| Rewrite | 수정한 event로 `next()` 호출 | 안전한 command로 교체 |
| Answer/Replace | `next()` 없이 결과 반환 | 위험한 tool call 거부 |

## Why

Skills, slash commands, MCP, classic Hooks는 각각 knowledge/workflow, 명령 진입점, 외부 capability, lifecycle 자동화에 강하다. 하지만 Claude Code의 event 자체를 rewrite하거나 persistent UI를 render하는 데는 한계가 있다. Mods는 그 간극을 메운 runtime extension layer다.

예를 들어 prompt 전처리, tool output secret redaction, allow/deny permission 판단, retry logic, terminal/Desktop side panel을 하나의 event model에서 구현할 수 있다.

## 특징과 구조

일반적인 Mod plugin은 아래처럼 배치한다.

```text
my-mod/
├── .claude-plugin/
│   ├── plugin.json
│   └── types/                 # Claude Code가 load 때 생성하는 선언
├── hooks/
│   ├── hooks.json
│   └── register.ts
├── types/
│   └── index.d.ts             # plugin state/추가 contract
└── tests/
    └── register.test.ts
```

- `hooks/hooks.json`은 정확히 하나의 module을 `modules`로 가리킨다.
- `$.state`는 hot reload 뒤에도 session state를 유지한다.
- `ui.render`는 `AbovePrompt` 등 component에 UI tree를 반환한다.
- runtime이 제공하는 `claude-code` type declaration이 해당 설치 버전의 API 기준이다.

## Security Model

Mod module에는 DOM/Node globals가 없고 외부 동작은 `$` API를 거친다. 그러나 이것을 third-party code의 보안 sandbox로 보면 안 된다. Mod는 Claude Code session 안에서 실행되고 host가 허용한 capability에 영향을 미칠 수 있다. 설치 전 source·transitive dependency·network 사용·event handling을 검토하고, 처음에는 observe-only로 배포한다.

Managed 환경에서는 built-in `sec-default`가 개인 설치 plugin이 조직의 classic hooks, managed settings, tool policy, deny rule에 닿지 못하게 보호한다. 이는 조직 policy의 우회 방지를 돕지만 모든 Mod를 신뢰해도 된다는 뜻은 아니다.

## Built-in Mods

공개 source에는 `diff`, `telemetry`, `sec-default`, `agents-md`가 포함된다. `/diff` pane과 `AGENTS.md` 처리도 Mod 구현을 읽을 수 있는 좋은 출발점이다.

## Sources

- https://claude.com/blog/claude-code-mods
- https://github.com/anthropics/claude-code/blob/main/mods/README.md
- https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts
