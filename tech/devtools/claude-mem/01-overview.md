---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem Overview

> [[README|목차]] | [[02-ecosystem|다음: Ecosystem]]

## What

Claude-Mem은 coding agent의 lifecycle과 tool event를 hook으로 관찰하고, raw transcript를 압축된 observation과 summary로 바꿔 local database에 저장하는 persistent memory layer다. 이후 session은 최근 또는 관련 memory를 자동으로 받고, 필요하면 MCP/API/Web Viewer로 더 오래된 기록을 찾는다.

저장 model은 내용을 한 덩어리 문서로 취급하지 않고 다음 entity로 분리한다.

```text
sdk_sessions
 ├─ user_prompts
 ├─ observations
 └─ session_summaries
```

Observation에는 `bugfix`, `feature`, `refactor`, `decision`, `discovery` 같은 작업 유형, narrative/facts, 읽거나 변경한 파일이 들어갈 수 있다. Summary에는 request, investigated, learned, completed, next steps가 구조화된다.

## Why

Session boundary는 coding workflow의 지식을 잘라낸다. 그 결과 사용자는 다음 session에서 다음 내용을 다시 설명하게 된다.

- 이미 확인한 root cause와 재현 조건
- 실패했거나 보류한 접근
- architecture decision과 trade-off
- 수정하거나 읽은 파일
- 아직 끝나지 않은 next steps

Claude-Mem은 “무엇을 기억하라”는 별도 수동 작업보다 실제 tool usage를 관찰하는 방식을 택한다. 이 접근은 기록 누락을 줄이지만, 불필요하거나 민감한 활동까지 capture할 수 있으므로 privacy boundary가 기능만큼 중요하다.

## Core Architecture

```text
Claude Code / IDE hooks
        │ HTTP
        ▼
Local Worker (Bun, 127.0.0.1, 37700 + uid % 100)
        ├─ Session Manager
        ├─ Observation Queue
        ├─ AI compression provider
        ├─ Search / Context API
        ├─ MCP adapter
        └─ Web Viewer / SSE
                │
                ▼
SQLite + FTS5 ─── optional Chroma
```

### Hook lifecycle

| Event | 역할 |
|---|---|
| `Setup` | install version marker 확인 |
| `SessionStart` | worker 시작, 과거 context injection |
| `UserPromptSubmit` | session과 prompt 등록 |
| `PreToolUse(Read)` | file context 처리 |
| `PostToolUse(*)` | tool observation capture |
| `Stop` | session summary 생성 |

Hook은 local worker로 request를 넘기고 AI compression은 비동기로 처리한다. Worker 문제가 coding session을 중단시키지 않도록 fail-open 성격을 갖는다. 이는 availability에는 유리하지만, memory 누락을 조용히 지나칠 수 있으므로 health와 log 확인이 필요하다.

## Key Features

### AI compression

Raw tool input/output 전체를 다시 prompt에 싣지 않고 structured observation으로 축약한다. Claude provider의 문서화된 기본 compression model은 `claude-haiku-4-5-20251001`이며, Gemini, OpenRouter, Anthropic plan, CMEM Pro, host observer 같은 provider 선택지가 있다.

### Local-first storage

- SQLite 3/`bun:sqlite`: session, prompt, observation, summary의 source of truth
- FTS5: keyword/full-text retrieval
- Chroma: optional semantic vector retrieval
- WAL mode: worker write와 viewer read의 concurrency 지원
- 기본 DB: `~/.claude-mem/claude-mem.db`

Chroma가 실패해도 SQLite FTS5-only 검색으로 degrade할 수 있다.

### Progressive Disclosure

```text
search → timeline → get_observations
```

1. `search`: compact index에서 ID, 제목, 날짜, 유형 탐색
2. `timeline`: 선택한 observation 전후의 시간적 맥락 확인
3. `get_observations`: 필요한 ID의 상세 내용만 batch fetch

문서의 “약 10x token savings”는 project 자체의 architecture estimate다. 독립 benchmark 결과로 해석하지 않는다.

## Privacy And Security Boundary

| 경계 | 확인할 점 |
|---|---|
| Local state | 기본적으로 `~/.claude-mem/`에 DB, config, logs 저장 |
| Redaction | `<private>...</private>` 내용은 hook layer에서 storage 제외 가능 |
| AI provider | prompt, transcript, tool output이 선택한 provider로 전송될 수 있음 |
| Cloud Sync | observation narrative와 full prompt가 sync hub에 upload될 수 있음 |
| Worker network | 기본 request authentication이 없으므로 `127.0.0.1` 유지가 핵심 방어선 |
| Updates | latest version만 security update 대상으로 명시 |

자체 telemetry가 없다는 주장과 provider 또는 Cloud Sync로 데이터가 전송된다는 사실은 서로 다른 문제다. 실제 data flow는 provider 설정, sync opt-in, redaction 규칙을 함께 봐야 한다.

## Strengths And Limits

### 강점

- 거의 모든 coding activity를 자동 timeline으로 남긴다.
- structured history와 FTS5/semantic search를 결합한다.
- MCP, API, Web Viewer로 같은 memory를 여러 방식으로 탐색한다.
- 여러 coding host로 확장 가능한 worker 중심 구조다.

### 한계

- AI compression이 원문의 nuance를 누락하거나 잘못 요약할 수 있다.
- capture 범위가 넓을수록 privacy와 storage noise가 커진다.
- 빠른 release cadence와 배포 채널 시차가 운영 재현성을 낮춘다.
- 2026-09-20 기준 open issue에는 worker log 폭증, sync conflict, stale quota state, hook output parsing 문제가 보인다.

## Sources

- https://github.com/thedotmack/claude-mem
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/hooks.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/worker-service.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/database.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/search-architecture.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/usage/search-tools.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
- https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md

