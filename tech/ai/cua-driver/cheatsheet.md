---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver: Cheatsheet

[[tech/ai/cua-driver/README|Cua Driver 목차]] · [[tech/ai/cua-driver/04-learning/01-getting-started|시작하기]]

## 빠른 흐름

```bash
# host와 권한 상태 점검
cua-driver doctor
cua-driver call list_apps

# Codex MCP 설정 명령 생성
cua-driver mcp-config --client codex
```

```text
list_windows
  → get_window_state
  → element_token 기반 action
  → get_window_state (fresh verification)
```

## 우선순위

| 먼저 선택 | 다음 선택 | 마지막 fallback |
|---|---|---|
| API / MCP | Accessibility의 named element action | screenshot 기반 좌표 click |
| 구조화된 browser action | 명확한 window binding | 무검증 multi-step 입력 |

## Production checklist

- [ ] OS Accessibility / Screen Recording 권한과 platform 제약을 확인했다.
- [ ] app·domain·file path·action allowlist를 정의했다.
- [ ] step/time/cost limit, cancellation, retry 정책이 있다.
- [ ] upload/download/submit에 human approval을 둔다.
- [ ] 매 action 뒤 fresh state와 실제 결과를 검증한다.
- [ ] 민감 workflow에는 isolated environment와 audit trail을 적용한다.

## Sources

- https://cua.ai/docs/cua-driver/quickstart
- https://cua.ai/docs/cua-driver/guides/permissions
- https://cua.ai/docs/cua-driver/guides/connect-your-agent
