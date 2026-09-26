---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian — Ecosystem

> [[README|목차로 돌아가기]] · [[01-overview|이전: Overview]] · [[03-references|다음: References]]

## 비교표

| 도구 | 포지션 | Provider 범위 | 차별점 / 적합한 경우 |
|---|---|---|---|
| **Claudian** | Obsidian용 local agent workspace | Claude Code, Codex, Grok, OpenCode, Pi | vault를 직접 workspace로 쓰고 CLI-native MCP/Skills를 활용할 때 |
| **Oh My Claudian** | Claudian fork | Claude Code, Codex, Cursor Agent, Grok, OMP, OpenCode, Pi | Cursor까지 포함하고 CLI discovery·health·update UX를 중시할 때 |
| **Claudian Plus** | 독립 multi-agent plugin | Codex, Claude Code, Antigravity, Kimi, OpenCode, Pi | Node 24 기반 RPC sidecar와 provider 확장을 선호할 때 |
| **Claude Code terminal** | CLI-first coding agent | Claude 중심 | Obsidian UI 없이 repository/vault를 terminal에서 직접 다룰 때 |
| **일반 Obsidian AI chat plugin** | note Q&A·작성 보조 | 보통 API-key 모델 | file-system agent와 Bash가 과도하고 단일 노트 생성·요약이면 충분할 때 |

## 선택 기준

```text
Obsidian에서 vault 파일을 agent가 다뤄야 하나?
├─ 아니오 → 일반 AI chat plugin 또는 terminal CLI
└─ 예
   ├─ 기존 CLI의 MCP/Skills/approval을 그대로 쓸 것인가? → Claudian
   ├─ Cursor Agent와 provider health UX가 중요한가? → Oh My Claudian 검토
   └─ 독립 sidecar/provider 확장이 우선인가? → Claudian Plus 검토
```

### Claudian이 특히 맞는 경우

- Claude Code 또는 Codex를 이미 설치·로그인했고, 그 CLI의 MCP·Skills·approval을 Obsidian에서도 재사용하려는 경우
- 노트 간 검색과 파일 수정 제안을 sidebar와 inline diff에서 검토하고 싶은 경우
- provider 중립 UI는 원하지만 provider의 native behavior를 유지하고 싶은 경우

### terminal이 더 단순한 경우

Obsidian context picker와 diff UI가 필요 없고 terminal에서 repository와 vault를 모두 제어할 수 있다면, Claude Code 같은 CLI를 직접 쓰는 편이 계층이 적다. Claudian은 CLI를 대체하는 model runtime이 아니라 Obsidian-native adapter다.

### 일반 chat plugin이 더 안전한 경우

현재 노트의 요약, 번역, 초안 생성처럼 file-system traversal·Bash·외부 tool이 필요 없는 작업은 권한이 작은 chat plugin 또는 API 호출이 적합할 수 있다. 필요 capability와 신뢰 경계를 먼저 비교한다.

## 호환성 확인 항목

- 원하는 provider가 목록에 있어도 현재 version에서 adapter가 지원하는 capability인지 확인한다.
- GUI app의 `PATH`와 CLI executable path가 실제로 발견되는지 확인한다.
- OpenCode v1은 2026-10-30 종료 예정이므로 v2 migration 계획을 확인한다.
- fork의 provider 목록은 main Claudian과 동일하다고 가정하지 말고 각 manifest/release를 확인한다.

## Sources

- [Claudian README — Requirements](https://github.com/YishenTu/claudian#requirements)
- [Oh My Claudian Community listing](https://community.obsidian.md/plugins/oh-my-claudian)
- [Claudian Plus Community listing](https://community.obsidian.md/plugins/claudian-plus)
- [Claude Code documentation](https://code.claude.com/docs/en/overview)
- [OpenCode v2 migration guide](https://opencode.ai/v2/docs/migrate-v1)
