---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver: 심화

[[tech/ai/cua-driver/README|Cua Driver 목차]] · [[tech/ai/cua-driver/05-projects|Projects]] · [[tech/ai/cua-driver/cheatsheet|Cheatsheet]]

## Browser binding과 CDP

Chrome/Edge 또는 지원되는 Electron 대상을 native `(pid, window_id)`로 정확히 bind한 뒤 `browser_*` tool을 사용한다. 이 route는 tab snapshot, navigate, click, type, upload/download 같은 typed browser action에 적합하다. extension 없이 동작하지만 inactive·occluded tab 지원 여부는 OS와 browser 조합을 확인해야 한다.

## 안전한 agent loop

```text
observe fresh state
  → plan one reversible action
  → authorize against allowlist/policy
  → act
  → observe fresh state
  → validate expected result or cancel/escalate
```

- **allowlist**: app, domain, window, 파일 경로, 허용 action을 좁힌다.
- **limits**: step, time, cost, retry 상한과 cancellation을 둔다.
- **approval**: upload, download, form submit, external side effect는 사용자 confirmation 경계로 둔다.
- **validation**: success message가 아니라 실제 저장 결과·export file·record 변화를 확인한다.
- **isolation**: 민감 workflow는 isolated VM/Space와 최소 권한 profile을 고려한다.

## 실패 모드

| 상황 | 대응 |
|---|---|
| tree가 canvas/virtualized UI라 비어 있음 | screenshot을 보조 신호로 쓰고, 좁은 범위의 좌표 fallback 후 즉시 검증 |
| focus가 필요한 입력 | background guarantee를 가정하지 말고 제약을 보고하거나 foreground 승인 요청 |
| 동일한 label의 요소가 여러 개 | window와 element context를 다시 읽고 하나의 명확한 token만 실행 |
| logged-in tab에서 민감 동작 | domain allowlist, human approval, 결과 audit을 적용 |

## Sources

- https://cua.ai/docs/cua-driver/guides/browsers
- https://cua.ai/docs/cua-driver/guides/permissions
- https://developers.openai.com/api/docs/guides/tools-computer-use
