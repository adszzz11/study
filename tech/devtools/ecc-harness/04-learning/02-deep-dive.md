---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — Deep dive

## 1. Portable workflow와 adapter의 경계

ECC의 공통 자산은 Markdown형 rules/skills/agents, JavaScript hook runtime, MCP conventions, install-state 관리다. 하지만 이를 실제 harness에 연결하는 adapter는 제각각이다.

```text
common catalog
  ├─ rules / skills / agents
  ├─ hooks + memory conventions
  └─ installer state
          │
          ├─ Claude Code adapter (성숙한 target)
          ├─ Codex adapter (native marketplace/plugin path와 sync)
          └─ Cursor / OpenCode / Gemini / Zed / Copilot adapters
```

따라서 “ECC가 지원한다”는 말은 기능 완전성의 보증이 아니다. 목표 adapter별로 installation, lifecycle hooks, command compatibility, memory handoff, upgrade/uninstall의 동작을 테스트한다.

## 2. Hooks: 자동화와 side effect

hook은 session summary, context control, verification, continuous learning을 연결할 수 있다. 반면 다음 위험도 함께 생긴다.

- 예상하지 못한 command 실행 또는 permission 확장
- session content가 memory로 남는 retention/privacy 문제
- 중복 설치로 인한 hook의 이중 실행
- 실패한 hook이 workflow를 막거나, 반대로 실패를 숨기는 문제

도입 시에는 hook마다 **trigger, command, 입력·출력, 실패 시 행동, 기록 위치, 제거 방법**을 문서화한다. minimal/no-hooks profile에서 시작해 한 번에 하나씩 활성화한다.

## 3. Unified Memory와 handoff 실험

Unified Memory는 CLI/MCP를 통해 harness 사이에서 handoff/search를 지향한다. 유효성은 “저장했는가”가 아니라 새 context가 실제로 재작업을 줄였는가로 판단한다.

| 측정 대상 | 질문 |
|---|---|
| Retrieval quality | 새 session이 결정·제약·검증 결과를 찾는가? |
| Fresh-context review | 이전 구현의 가정을 독립적으로 재검토하는가? |
| Privacy | secret·개인정보·불필요한 source가 기록되지 않는가? |
| Cost | 저장·검색이 token/time 절감을 상쇄하는가? |

## 4. AgentShield의 역할

AgentShield는 instructions, permissions, hooks, MCP config, secret 등을 검사한다. security scanner는 **정책 집행의 입력**이지 security guarantee가 아니다.

```text
scan finding → triage → config / permission diff 검토
             → 승인 또는 수정 → CI baseline 갱신
```

특히 baseline은 known finding을 숨기는 용도가 아니라, 새 위험과 기존 위험의 변화를 분리하는 기준이어야 한다. 자동 수정 전에는 사람이 command·permission 변경을 확인한다.

## 5. Control-plane 방향성

2.x는 session adapter, MCP inventory, worktree lifecycle, Control Pane을 더해 여러 agent session/worktree를 관찰·운영하는 control-plane 방향으로 확장 중이다. 생산 환경 적용 전에는 지원 harness와 version에서 이 기능이 실제 release됐는지, worktree와 repository state에 어떤 권한을 요구하는지 검증한다.

## Sources

- https://github.com/affaan-m/ECC/blob/main/docs/architecture/cross-harness.md
- https://github.com/affaan-m/ECC/blob/main/CHANGELOG.md
- https://github.com/affaan-m/agentshield
