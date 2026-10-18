---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# awwwards-mcp: What / Why

## What

TypeScript/Node 기반 local `stdio` MCP server다. Codex, Claude Code, Cursor 같은 MCP host의 child process로 실행되어, Awwwards 공개 페이지를 reference 검색과 design analysis에 사용한다.

```text
MCP host → stdio JSON-RPC → awwwards-mcp (Node ≥ 22.13)
  ├─ public Awwwards pages / CDN (polite fetch, ≤1 req/s)
  ├─ SQLite cache + FTS5/BM25 index (7-day freshness)
  └─ optional Playwright/Chromium + ffmpeg-static
```

## Why

디자인 요구가 “premium”, “Awwwards급”처럼 모호할 때, agent는 추측 대신 후보 사이트의 관찰 증거를 수집할 수 있다. palette·typography·section 구조·interaction을 brief로 정리하고, build 결과를 reference와 다시 비교하는 loop가 핵심이다.

## 주요 도구군

| 목적 | 도구 |
|---|---|
| 후보 탐색·brief | `search_sites`, `get_site_details`, `compare_sites`, `create_design_brief` |
| component cue | `search_elements`, `get_site_elements` |
| 화면·구조 검증 | `capture_live_site`, `analyze_page_structure`, `capture_component` |
| motion 관찰 | `record_site_motion`, `get_motion_dna`, `capture_pose_3d`, `build_pose_stub` |
| 변화 추적 | `new_winners`, `watch_site` |

## 운영상 특징과 주의점

- 약 200개 tag page를 1 req/s로 index하고, SQLite에 저장한 뒤 7일 후 background refresh한다. 상세는 on-demand cache다.
- Playwright/Chromium과 `ffmpeg-static`은 필요한 분석에서만 설치한다.
- `stdio` transport는 stdout이 JSON-RPC 채널이므로 debug log가 stdout으로 섞이면 protocol failure가 난다. log는 stderr로 보낸다.
- 공개 페이지라고 해서 자유 이용 콘텐츠는 아니다. copyright, robots.txt, ToS, rate limit과 `prefers-reduced-motion`을 존중한다.

## 기술스택 요약

TypeScript/Node 기반 local `stdio` MCP server가 host와 JSON-RPC로 통신한다. rate-limited scraping과 SQLite·FTS5/BM25가 reference retrieval을 담당하고, Playwright/Chromium 및 `ffmpeg-static`이 screenshot, structure, motion 분석을 보조한다. 가치는 스타일 생성이 아니라 관찰 증거를 brief와 검증 loop로 연결하는 데 있다.

## Sources

- https://github.com/INSANE0777/Awwwards-mcp
- https://github.com/INSANE0777/Awwwards-mcp/blob/main/package.json
- https://github.com/INSANE0777/Awwwards-mcp/tree/main/src
- https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio
