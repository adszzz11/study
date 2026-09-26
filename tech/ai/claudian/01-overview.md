---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What: vault 안에서 실행하는 local agent workspace

Claudian은 Obsidian Desktop용 Community Plugin이다. Claude Code CLI, Codex CLI, Grok Build, OpenCode v2, Pi를 provider adapter로 연결해 sidebar chat, multi-session tab, inline edit에서 실행한다. agent는 단순히 노트 본문을 답변 context로 받는 수준을 넘어 vault 파일을 읽고 쓰며, 검색·Bash·MCP를 포함한 multi-step task를 수행할 수 있다.

## Why: PKM의 반복 정리 작업을 agent에게 넘기기

Markdown vault에는 조사 기록과 연결 맥락이 풍부하지만, 다음 작업은 수작업이 되기 쉽다.

- 관련 노트를 찾아 중복 claim과 누락 link를 확인하기
- 회의록을 action item·결정·미해결 질문으로 분해하기
- frontmatter와 제목 형식을 일괄 점검하기
- repository와 docs vault 사이의 불일치를 찾기

일반 AI chat plugin이 보통 열린 노트의 Q&A에 맞춰진 반면, Claudian은 이미 설치한 coding-agent CLI가 vault를 작업 디렉터리로 다루게 한다. 따라서 결과물은 답변뿐 아니라 review 가능한 file diff와 변경 제안이 될 수 있다.

## 핵심 특징

| 영역 | 내용 | 실무 의미 |
|---|---|---|
| Multi-provider | Claude Code, Codex, Grok Build, OpenCode v2, Pi | vendor를 바꿔도 Obsidian 안의 작업 흐름을 유지한다. |
| Native UX | sidebar chat, multi-tab/session, `@mention`, `/` command, `$` Skill | 노트 context를 빠르게 지정하고 반복 작업을 표준화한다. |
| Inline edit | word-level diff 기반 변경 검토·적용 | agent 변경을 바로 저장하지 않고 검토할 수 있다. |
| CLI-native 확장 | CLI가 관리하는 MCP config와 user/vault scope Skills 재사용 | 별도 tool ecosystem을 중복 구성하지 않는다. |
| Temporary thread | `/side`, `/btw` side conversation | 본 작업 session을 흐리지 않고 짧은 질문을 처리한다. |

## 아키텍처

```text
Obsidian UI
  ├─ chat · inline edit · settings feature
  └─ core: provider-neutral execution · registry · session lifecycle · approval
       ├─ claude: SDK
       ├─ codex: app-server / JSON-RPC
       ├─ grok: ACP
       ├─ opencode: RPC
       └─ pi: native JSONL history
```

UI와 provider 실행 계층이 분리되어 있지만, capability와 safety rule은 균일하지 않다. 예를 들어 tool approval, history, executable 설정은 각 native CLI의 정책을 보존한다. plugin은 TypeScript/Obsidian API, Node.js, esbuild, CodeMirror, Claude Agent SDK, MCP SDK, WebSocket/JSON-RPC를 사용하며 `package.json`은 개발 Node 범위를 `>=24 <25`로 명시한다.

## 권한과 privacy 경계

Prompt, 첨부파일, tool output은 선택한 provider로 전송될 수 있다. 또한 agent는 vault 안의 파일 및 허용된 shell 작업을 수행할 수 있다. 안전한 기본값은 다음과 같다.

1. 개인 vault 대신 disposable test vault에서 먼저 검증한다.
2. project vault와 개인·비밀 노트를 분리한다.
3. MCP는 read-only tool부터 추가하고, Bash·외부 write는 CLI approval을 유지한다.
4. vault-level instruction에 금지 경로, 금지 작업, 검토 기준을 선언한다.
5. inline diff와 `git diff`로 적용 전후를 확인한다.

> [!warning]
> Community Plugin은 third-party code를 실행한다. Claudian의 안전성은 plugin 하나만이 아니라 선택한 provider, CLI 권한 정책, MCP server, vault 내용의 신뢰 경계 전체에 달려 있다.

## Collab은 별도 plugin

협업 기능은 main Claudian이 아니라 **Claudian Collab**이 맡는다. 작은 팀의 Project 폴더를 독립 Git repository로 관리하고 `Publish → Change Request → Manager Accept` 흐름으로 accepted `main`을 보호한다. 현재 구현은 LAN Host 중심이며 self-hosted/managed cloud는 계획 상태다.

## Sources

- [Claudian README — Features, requirements, architecture, privacy](https://github.com/YishenTu/claudian)
- [Claudian package.json](https://raw.githubusercontent.com/YishenTu/claudian/main/package.json)
- [Claudian Collab — How it works](https://claudian.md/docs/collab-mode/how-it-works/)
- [Obsidian — Community plugins security](https://help.obsidian.md/community-plugins)
