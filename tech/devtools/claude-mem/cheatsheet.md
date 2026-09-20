---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem Cheatsheet

> [[05-projects|이전: Projects]] | [[README|목차]]

## Mental Model

```text
Hooks capture → Worker compresses → SQLite stores
→ Context injects → MCP searches → Details fetched on demand
```

## Install

```bash
npx claude-mem install
```

Claude Code plugin marketplace:

```text
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

`npm install -g claude-mem`만으로는 hook/worker가 구성되지 않는다.

## Defaults

| Item | Default |
|---|---|
| Data directory | `~/.claude-mem/` |
| Database | `~/.claude-mem/claude-mem.db` |
| Settings | `~/.claude-mem/settings.json` |
| Worker host | `127.0.0.1` |
| Worker port | `37700 + (uid % 100)` |
| Claude compression model | `claude-haiku-4-5-20251001` |
| Primary store | SQLite 3 / `bun:sqlite` |
| Keyword search | FTS5 |
| Semantic search | optional Chroma |

## Hook Events

| Event | Action |
|---|---|
| `Setup` | version marker check |
| `SessionStart` | worker start + context injection |
| `UserPromptSubmit` | session/prompt register |
| `PreToolUse(Read)` | file context handling |
| `PostToolUse(*)` | observation capture |
| `Stop` | session summary |

## Search Pattern

```text
1. search(query, filters?)
2. timeline(anchor_observation_id)
3. get_observations(ids=[...])
```

- `search`: compact 후보 찾기
- `timeline`: 전후 맥락 확인
- `get_observations`: 필요한 상세만 batch fetch

## Privacy

```text
<private>이 내용은 storage에서 제외</private>
```

- 실제 secret을 넣어 test하지 않는다.
- `<private>`는 사후 삭제 기능이 아니다.
- Provider가 받을 prompt/transcript/tool output 범위를 검토한다.
- Cloud Sync 사용 시 full prompt와 observation upload 범위를 확인한다.
- Worker는 `127.0.0.1`에 유지한다. `0.0.0.0` 공개 금지.

## Troubleshooting Order

```text
Host hook loaded?
  → worker healthy?
  → event reached queue?
  → provider compression succeeded?
  → SQLite row exists?
  → FTS5 result exists?
  → Chroma semantic index healthy?
  → injection filter excluded it?
```

## Production Checklist

- [ ] Exact version 기록 및 pinning
- [ ] SQLite-consistent backup과 restore test
- [ ] Provider/data-flow review
- [ ] Secret redaction test
- [ ] Loopback bind 확인
- [ ] Log/disk monitoring
- [ ] Upgrade smoke test
- [ ] Rollback window 유지
- [ ] 중요한 decision은 ADR/docs로 승격

## Status Snapshot

- 조사 기준일: 2026-09-20
- `main` manifest: v13.25.2
- Releases 화면 최근 노출: v13.24.23
- License: Apache-2.0
- Project type: community project, Anthropic 공식 기능 아님

## Sources

- https://github.com/thedotmack/claude-mem
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/installation.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/usage/search-tools.mdx
- https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md
