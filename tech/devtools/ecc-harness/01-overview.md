---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — What / Why / 핵심 특징

## What: agent operating layer

ECC는 agent model 위에 얹는 cross-harness workflow layer다. LLM이 답변을 생성하는 능력과 별개로, 실제 engineering에는 계획, 테스트, 구현, 독립 review, 검증, 다음 세션을 위한 기록, 보안 경계가 필요하다. ECC는 이를 재사용 가능한 catalog와 installer로 제공한다.

```text
Agent harness (Claude Code / Codex / …)
        │ adapter
        ▼
ECC rules + skills + specialized agents
        │ lifecycle hooks / MCP conventions
        ▼
plan → test → implement → review → verify → remember → improve
```

## Why: 세션과 도구를 넘는 반복성

매 세션 프롬프트에 team rules와 검증 절차를 재입력하면 누락·편차가 생긴다. 각 harness에 별도 설정을 복제하면 update와 uninstall도 어려워진다. ECC의 목표는 다음을 하나의 설치·운영 모델로 줄이는 것이다.

- language/framework rule pack과 TDD·security·research·ops skill을 조합한다.
- lifecycle hook으로 session summary, context control, verification, continuous learning을 연결한다.
- Unified Memory를 CLI/MCP 기반 handoff와 search에 사용한다.
- AgentShield로 instructions, permissions, hooks, MCP config, secrets를 검사한다.

## 핵심 특징

| 영역 | 내용 | 운영상 의미 |
|---|---|---|
| Catalog | 공개 README 기준 68 specialized agents, 약 286~292 skills, 94 legacy command shims | 수치는 branch/release에 따라 변하므로 고정 계약으로 보지 않는다. |
| Selective install | 필요한 profile/component만 선택 | 모든 asset을 무조건 로드해 context와 충돌을 늘리지 않는다. |
| Hooks / Memory | 세션 요약, 검증, 학습, handoff/search | 자동 기록도 민감 정보와 retention 정책을 검토한다. |
| Cross-harness adapters | Claude Code, Codex 및 Cursor·OpenCode·Gemini·Zed·Copilot adapter | harness별 parity를 가정하지 않고 지원표를 확인한다. |
| AgentShield | configuration scan 및 CI-friendly output | finding은 보조 신호이며 권한 검토를 대체하지 않는다. |
| Control plane | 2.x의 session adapter, MCP inventory, worktree lifecycle, Control Pane | 여러 session/worktree 관찰·운영 방향의 기능이다. |

## 설치·버전의 판단 기준

`ecc-universal`은 Node.js 18+ 기반 installer다. 최신 여부는 main branch changelog만으로 판단하지 않는다. GitHub release tag, release note, npm dist-tag/version을 함께 보고 설치 channel과 변경 파일을 dry-run으로 확인한다.

```bash
# Codex 설치 전에 예정된 변경과 channel을 확인한다.
npx ecc-universal install --guided --harness codex --dry-run
```

## 한계와 보안 경계

- scanner가 clean이어도 hook, permission, MCP server가 안전하다는 보장은 없다.
- 한 harness에 plugin·guided installer·manual copy를 중첩하면 hook/command/config가 충돌할 수 있다.
- memory와 hook은 편의 기능이지만 data flow와 side effect를 늘린다. minimal 또는 no-hooks profile부터 검증한다.

## Sources

- https://github.com/affaan-m/ECC
- https://github.com/affaan-m/ECC/blob/main/docs/architecture/cross-harness.md
- https://github.com/affaan-m/ECC/blob/main/CHANGELOG.md
- https://github.com/affaan-m/agentshield
