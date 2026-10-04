---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: Read-only Token Weather

첫 실습은 동작을 block하지 않는 context usage panel이다. 최신 Claude Code에서 built-in `/diff`를 먼저 열어 본 뒤, session 시작과 turn 완료 후 usage를 읽고 `AbovePrompt`에 표시한다.

## 1. 버전과 폴더 확인

공식 튜토리얼 기준 Mods는 Claude Code 2.1.287 이상에서 기본 활성화된다. 설치 버전의 API는 변할 수 있으므로 load 후 생성된 type declaration을 확인한다.

```bash
claude --version
mkdir -p token-weather/{.claude-plugin,hooks,types,tests}
```

`.claude-plugin/plugin.json`:

```json
{
  "name": "token-weather",
  "version": "0.1.0",
  "description": "Context-window usage above the prompt.",
  "author": { "name": "You" },
  "types": "./types/index.d.ts"
}
```

`hooks/hooks.json`은 module 하나를 지정한다.

```json
{ "modules": ["./register.mjs"] }
```

## 2. Event를 관찰해 state 저장

`next(e)` 뒤에 기록하면 Claude Code의 기본 행동을 바꾸지 않는다. module-level 변수는 hot reload 때 초기화되므로 `$.state`를 사용한다.

```js
const readings = { plugin: "token-weather", key: "readings" };

async function takeReading($) {
  const { context } = await $.session.usage();
  if (!context?.window) return;
  const { value: history = [] } = await $.state.get(readings);
  await $.state.set(readings, [...history, {
    tokens: context.tokens ?? 0,
    window: context.window,
    percent: context.percent ?? 0,
  }].slice(-12));
}

export function register(on) {
  on("session.start", async ($, e, next) => {
    const result = await next(e);
    await takeReading($);
    return result;
  });
  on("turn.complete", async ($, e, next) => {
    const result = await next(e);
    if (!e.agentId) await takeReading($);
    return result;
  });
}
```

## 3. `AbovePrompt`에 그리기

`ui.render`에는 event surface에 맞는 constructors를 `$.ui.resolve(e)`로 얻는다. render 중 `$.state.get`을 하면 이후 `$.state.set`에 redraw가 연결된다.

```js
on("ui.render", { component: "AbovePrompt" }, async ($, e) => {
  const { value: history = [] } = await $.state.get(readings);
  const last = history.at(-1);
  const { Box, Text } = $.ui.resolve(e);
  return Box({ paddingX: 1, children: [
    Text({ color: "cyan", children: last
      ? `Context: ${last.percent}% (${last.tokens}/${last.window})`
      : "Context: waiting for first reading" }),
  ] });
});
```

## 4. State contract, 실행, 검증

`types/index.d.ts`에서 state schema를 선언한다.

```ts
export type Reading = { tokens: number; window: number; percent: number };
declare module "claude-code" {
  interface PluginState { "token-weather": { readings: Reading[] } }
}
```

```bash
claude --plugin-dir ./token-weather
claude plugin validate ./token-weather
claude plugin test ./token-weather
```

## 완료 기준

- session start와 main turn complete 뒤 panel이 갱신된다.
- subagent turn은 main context reading에 섞이지 않는다.
- hot reload 뒤 history가 유지된다.
- validation/test가 통과한다.

## Sources

- https://claude.dev/blog/getting-started-with-claude-code-mods/
- https://github.com/anthropics/claude-code/blob/main/mods/README.md
