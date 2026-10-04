---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Middleware, Policy, Validation

## `next(e)`는 control-flow 결정이다

middleware는 먼저 load된 Mod부터 nested된다. 앞선 handler는 event를 먼저 보고, `next(e)`가 반환한 최종 result도 마지막에 받는다. `next`를 호출하지 않으면 아래 chain과 Claude Code 기본 동작을 대체한다.

```ts
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  await $.store.set({ plugin: "audit", key: "last" }, { command: e.command });
  if (!allowed(e.command)) return { deny: "Allowlist policy" };
  return next(e);
});
```

따라서 handler마다 다음을 명확히 한다.

- 관찰만 할 것인가? 반드시 `next(e)`를 호출하고 결과를 보존한다.
- 어떤 field를 rewrite할 것인가? schema와 downstream 영향을 확인한다.
- 직접 답할 것인가? 사용자가 이해할 수 있는 deny/error를 반환한다.
- retry할 것인가? idempotency, timeout, duplicate side effect를 먼저 설계한다.

## Event ordering과 policy

여러 Mod의 semantics는 load order에 영향을 받는다. 개인 Mod가 조직 guardrail보다 앞선다는 가정을 두지 않는다. managed 환경에서 `sec-default`는 개인 설치 plugin이 조직 policy를 변경하지 못하도록 outermost에 배치될 수 있다. 이 특성은 local test와 managed production 모두에서 확인해야 한다.

## Observe-only에서 enforcement로

1. tool/permission event를 기록하되 결과는 그대로 `next(e)`에 전달한다.
2. allowlist와 exception 데이터의 false positive를 측정한다.
3. 명확한 destructive action만 deny한다.
4. approval UI, audit event, rollback path를 마련한다.
5. threat model과 owner 승인 후 범위를 확대한다.

처음부터 broad block을 켜면 legitimate workflow를 멈추고 사용자가 우회로를 만들 가능성이 높다. 반대로 secret을 model context에 전달한 뒤 redaction하는 것은 너무 늦다. 보호 위치와 event timing을 event contract에서 검증한다.

## Test와 review checklist

```bash
claude plugin validate ./my-mod
claude plugin test ./my-mod
```

- manifest, module 경로, event/API/state contract가 validate되는가?
- 정상 전달, rewrite, deny, exception 각각을 test하는가?
- `next` 누락이 의도된 replace인지 test로 드러나는가?
- state schema와 hot reload 동작을 검증하는가?
- secret, PII, tool output이 log·UI·network request로 새지 않는가?
- network access, dependency lock/update, telemetry retention을 review했는가?
- event ordering과 managed policy 아래의 실제 동작을 확인했는가?

## Sources

- https://github.com/anthropics/claude-code/blob/main/mods/README.md
- https://github.com/anthropics/claude-code/issues/91870
- https://claude.dev/blog/getting-started-with-claude-code-mods/
