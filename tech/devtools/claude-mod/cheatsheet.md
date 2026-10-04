---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Mod Cheatsheet

## 최소 구조

```text
my-mod/
├── .claude-plugin/plugin.json
├── hooks/hooks.json
├── hooks/register.mjs
├── types/index.d.ts
└── tests/register.test.ts
```

```json
// hooks/hooks.json
{ "modules": ["./register.mjs"] }
```

## Handler 패턴

```ts
// Observe
on("turn.complete", async ($, e, next) => {
  const result = await next(e);
  await record($, e);
  return result;
});

// Rewrite
on("tool.call", async ($, e, next) => next({ ...e, command: safer(e.command) }));

// Answer/replace
on("tool.call", async ($, e) => ({ deny: "Policy denied" }));
```

| 항목 | 기억할 점 |
| --- | --- |
| `on(event, matcher?, hook)` | event handler 등록 |
| `$` | UI, session, state, store, fs, process, clock, http 등 engine API |
| `e` | plain event data |
| `next(e)` | 다음 Mod와 Claude Code 기본 동작으로 전달 |
| `$.state` | session 동안 유지되고 hot reload 후에도 살아 있는 state |
| `ui.render` | UI component에 element tree를 반환 |
| `$.ui.resolve(e)` | 해당 surface의 UI constructors 획득 |

## 검증 명령

```bash
claude --version
claude --plugin-dir ./my-mod
claude plugin validate ./my-mod
claude plugin test ./my-mod
```

## 안전 점검

- Mod는 untrusted code 실행을 위한 sandbox가 아니다.
- default는 observe-only, enforcement는 측정 뒤 최소 범위로 전환한다.
- `next`를 생략하면 replace가 된다. 의도와 test를 일치시킨다.
- model context에 들어가기 전에 secret을 처리한다.
- source, dependency, network, load order, managed policy를 review한다.

## Sources

- https://claude.dev/blog/getting-started-with-claude-code-mods/
- https://github.com/anthropics/claude-code/blob/main/mods/README.md
