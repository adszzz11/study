---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem Getting Started

> [[../03-references|이전: References]] | [[../README|목차]] | [[02-deep-dive|다음: Deep Dive]]

## Goal

작은 비민감 repository에서 설치부터 capture, 저장, 다음 session injection, MCP retrieval까지 한 cycle을 검증한다. 처음부터 production repository에 적용하지 않는다.

## 0. Preflight

- [ ] source code와 tool output을 보낼 AI provider를 정했다.
- [ ] provider의 data retention과 조직 policy를 검토했다.
- [ ] secret/credential을 prompt와 tool output에서 제거할 방법이 있다.
- [ ] worker bind를 `127.0.0.1`로 유지한다.
- [ ] `~/.claude-mem/` backup/삭제/retention 방침을 정했다.
- [ ] 설치할 exact version과 release note를 기록했다.

## 1. Requirements

공식 installation 문서 기준 주요 requirement는 다음과 같다.

- Node.js 20+
- Bun 1.0+ (`npx` installer가 필요하면 설치)
- `uv` (Chroma embedding service용, installer가 필요하면 설치)
- Claude Code 또는 지원 host
- SQLite 3은 `bun:sqlite`로 bundled

## 2. Install

가장 일반적인 interactive installer:

```bash
npx claude-mem install
```

Claude Code 안에서 plugin marketplace를 사용할 수도 있다.

```text
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

> [!WARNING]
> `npm install -g claude-mem`만 실행하면 SDK/library만 설치되고 hook 등록과 worker setup은 되지 않는다. `npx claude-mem install` 또는 `/plugin` 명령을 사용한다.

Installer가 host와 provider를 묻는다. “가장 편한 provider”보다 허용된 data flow를 기준으로 선택한다. 설치는 외부 package 실행과 local config 변경을 포함하므로 실행 전 현재 공식 installation 문서를 다시 읽는다.

## 3. Inspect Local State

기본 data directory:

```text
~/.claude-mem/
├── claude-mem.db
├── .install-version
├── .worker.pid
├── .worker.port
├── settings.json
└── logs/
```

기본 worker endpoint는 다음 규칙을 사용한다.

```text
host = 127.0.0.1
port = 37700 + (uid % 100)
```

설정에서 host가 `0.0.0.0`으로 바뀌지 않았는지 확인한다. Local worker는 기본 request authentication이 없으므로 public bind를 피한다.

## 4. Run A Capture Test

비민감 test repository에서 작은 작업을 수행한다.

```text
1. 새 session 시작
2. 파일 하나 읽기
3. 작은 수정 또는 test 실행
4. 작업 결과와 next step을 남기고 session 종료
5. 새 session 시작
```

다음 항목을 관찰한다.

- `SessionStart`에서 과거 context가 주입되는가?
- `PostToolUse` 뒤 observation이 생성되는가?
- `Stop` 뒤 summary가 생성되는가?
- DB와 log가 `~/.claude-mem/` 아래에 생기는가?
- worker failure가 host session을 막지 않는가?

## 5. Test Retrieval

MCP search는 처음부터 상세 payload를 모두 읽지 않는다.

```text
search("방금 수행한 작업의 핵심어")
  → observation ID 선택
timeline(anchor=ID)
  → 전후 작업 확인
get_observations(ids=[...])
  → 필요한 상세만 조회
```

검증 질문 예시:

- “이 repository에서 최근 실패한 test와 원인은?”
- “해당 decision 전후에 어떤 파일을 읽었는가?”
- “지난 session에서 남긴 next steps를 상세 observation과 함께 보여줘.”

## 6. Privacy Test

실제 secret이 아닌 marker로 redaction을 확인한다.

```text
<private>TEST_SECRET_DO_NOT_STORE</private>
```

Session 종료 후 viewer, search, DB-derived result에 marker가 없는지 확인한다. `<private>` tag는 이미 저장되거나 다른 channel로 유출된 secret을 되돌려 주는 장치가 아니다.

## 7. Go/No-Go Checklist

- [ ] 2개 이상의 session에서 capture/injection cycle이 재현됐다.
- [ ] FTS5 search가 동작하고 Chroma 장애 시 fallback을 확인했다.
- [ ] provider와 Cloud Sync의 전송 범위를 기록했다.
- [ ] backup 후 restore smoke test를 했다.
- [ ] log growth와 disk usage를 관찰할 방법이 있다.
- [ ] version pinning과 upgrade rollback 기준이 있다.

## Sources

- https://github.com/thedotmack/claude-mem/blob/main/docs/public/installation.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
- https://github.com/thedotmack/claude-mem/blob/main/docs/public/usage/search-tools.mdx
- https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md

