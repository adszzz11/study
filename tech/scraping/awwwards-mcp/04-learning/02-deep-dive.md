---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: evidence-to-verification loop

## 검색과 cache

검색은 자연어, tag, color, technology, award 기준과 BM25/FTS5 ranking을 활용한다. 큰 탐색에서만 local index를 만들며, 약 200개 tag page를 ≤1 req/s로 수집하고 7일 freshness를 전제로 한다. 결과는 최신 사실이 아니라 candidate discovery로 취급한다.

## Capture와 structure

Playwright/Chromium을 설치한 경우 다음 순서로 관찰한다.

```text
reference URL ─capture_live_site→ screenshot
reference URL ─analyze_page_structure→ band map / section rhythm
local build    ─capture_component→ computed-style component pack
                    ↓
                 compare_sites → design decision 조정
```

동일한 viewport, font loading 상태, reduced-motion 조건을 기록해야 비교가 의미 있다. screenshot 차이는 pixel-perfect 복제가 아니라 information hierarchy와 section rhythm의 차이를 찾는 데 사용한다.

## Motion DNA

`record_site_motion`은 filmstrip을 만들고, `get_motion_dna`는 animation library, easing, scroll model, canvas pose 같은 관찰치를 추출한다. `capture_pose_3d`, `build_pose_stub`은 3D pose를 재현 가능한 stub으로 옮기는 데 쓴다.

- 무단 asset 추출보다 interaction principle을 기록한다.
- `prefers-reduced-motion`을 지원하고 motion이 없는 fallback을 제공한다.
- ffmpeg-static은 WebM filmstrip 같은 분석에만 필요한 optional dependency다.

## stdio reliability

MCP는 local child process의 stdio JSON-RPC transport다. stdout에 일반 로그가 출력되면 framing이 깨질 수 있으므로 diagnostic output은 stderr로 보낸다. host와 server의 version, command, environment를 기록하면 재현이 쉬워진다.

## Sources

- https://github.com/INSANE0777/Awwwards-mcp/tree/main/src
- https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio
