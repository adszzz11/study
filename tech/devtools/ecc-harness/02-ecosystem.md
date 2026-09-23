---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — Ecosystem / 비교

## 선택지 비교

| 선택지 | 강점 | 한계 / 적합성 |
|---|---|---|
| **ECC** | 다중 harness 공통 workflow, install manifest, memory/hooks, AgentShield | 구성 폭이 크고 adapter별 feature parity가 다르다. |
| **Claude Code native plugin/rules** | Claude Code와 자연스러운 통합, 단순한 운영 | 다른 harness로 workflow를 이식하기 어렵다. |
| **Cursor Rules/Agents** | IDE 중심의 빠른 UX, 프로젝트 규칙 적용 | runtime hook·portable memory 운영 범위는 상대적으로 제한적이다. |
| **OpenCode config/plugin** | open tooling, 로컬 구성 자유도 | 설치·운영의 일관성을 팀이 직접 설계해야 한다. |
| **직접 AGENTS.md + scripts** | 최소 의존성, 완전한 통제 | skill catalog, lifecycle, security audit, upgrade/uninstall을 직접 유지한다. |
| **AgentShield 단독** | agent configuration 보안 감사와 CI gate | workflow, memory, agent orchestration을 제공하는 harness 자체는 아니다. |

## 선택 기준

1. **harness 수**: 한 도구만 쓰면 native configuration 또는 `AGENTS.md`가 더 작은 선택일 수 있다. 여러 도구를 함께 쓰면 ECC의 portable layer 가치가 커진다.
2. **운영 능력**: hooks·memory·MCP를 검토하고 rollback할 담당자가 있는지 확인한다. catalog의 크기는 운영 비용도 의미한다.
3. **보안 경계**: AgentShield는 CI signal로 유용하지만 security decision은 findings, diff, permission을 사람이 검토해야 한다.
4. **adapter 검증**: 목표 harness의 install path, hook support, memory integration을 release 문서에서 개별 확인한다.

## 권장 도입 순서

```text
단일 repo / 최소 rules + TDD skill
        ↓ 측정: 품질·token cost·security findings
minimal 또는 no-hooks profile
        ↓ adapter별 검증
팀 공통 rule + CI AgentShield gate
        ↓
선택적 memory / cross-harness handoff
```

## Sources

- https://github.com/affaan-m/ECC
- https://github.com/affaan-m/ECC/blob/main/docs/architecture/cross-harness.md
- https://github.com/affaan-m/agentshield
