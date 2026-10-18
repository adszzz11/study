---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# awwwards-mcp Cheatsheet

## Install / register

```sh
node --version                 # Node >= 22.13 확인
codex mcp add awwwards -- npx -y awwwards-mcp
```

## Tool map

| 작업 | 우선 도구 | 산출물 |
|---|---|---|
| 후보 찾기 | `search_sites` | 3개 안팎의 reference 후보 |
| 상세 확인 | `get_site_details` | palette, technology, award 정보 |
| element 찾기 | `search_elements`, `get_site_elements` | hero / CTA / footer cue |
| 방향 합성 | `compare_sites`, `create_design_brief` | 구현 원칙과 제외 범위 |
| 화면 검증 | `capture_live_site`, `analyze_page_structure`, `capture_component` | screenshot, band map, style pack |
| motion 관찰 | `record_site_motion`, `get_motion_dna` | filmstrip, easing/scroll 모델 |
| 변화 감시 | `new_winners`, `watch_site` | delta, watchlist |

## Guardrails

```text
검색 결과 → 사람이 screenshot 검토 → cue 추출 → brief 작성
→ local build capture → structure 비교 → 설계 조정
```

- ≤1 req/s와 robots.txt, ToS, copyright를 준수한다.
- 원본 logo, imagery, copy, 고유 composition을 복제하지 않는다.
- `prefers-reduced-motion`과 motion fallback을 제공한다.
- MCP stdout은 JSON-RPC channel: log는 stderr로 보낸다.
- large index와 Playwright/ffmpeg는 필요한 경우에만 사용한다.

## Sources

- https://github.com/INSANE0777/Awwwards-mcp
- https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio
