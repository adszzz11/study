---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — Projects / 적용

## 1. 고위험 backend 변경

**상황**: migration, API compatibility, authorization 경계를 함께 바꾼다.

```text
Claude: migration + rollback + compatibility plan
  → Codex: isolated worktree 구현 및 test evidence
  → dual audit: security / portability / plan-adherence
  → operator: diff와 migration 실행 계획을 별도 승인
```

성공 기준은 “agent가 승인했다”가 아니라 backward compatibility test, migration rollback 검증, 승인된 patch, 운영 change approval이 모두 남는 것이다.

## 2. 대형 refactor

architecture plan을 artifact로 고정하고 Codex가 구현한다. audit에는 plan-adherence와 test-gap을 required 혹은 high-priority persona로 둔다.

| 측정 | 예시 |
|---|---|
| 계획 충실도 | planned module 경계와 non-goal이 지켜졌는가? |
| 회귀 | characterization/integration test가 통과하는가? |
| 불확실성 | unresolved finding이 agreement 전에 명시됐는가? |
| 재개성 | 새 session이 trace와 artifact만으로 run을 이해하는가? |

## 3. CI-ready patch factory

headless 환경에서는 run directory와 `trace.jsonl`을 CI artifact로 보관한다. API key/token은 fallback일 수 있으므로 secret scope·rotation·log redaction을 별도 검토한다. agreement가 true여도 `manual apply`와 PR approval을 분리해 source branch와 deployment 권한을 보호한다.

## 4. PR review remediation

review-only loop이 목표라면 lukaskucinski/clodex처럼 Codex adversarial review의 blocking severity만 fix 대상으로 삼을 수 있다. max iteration 또는 stall에 도달하면 자동 배포가 아니라 reviewer에게 escalate한다. 이 경우에도 test/lint/SAST 결과는 review finding과 병렬로 확인한다.

## 도입 순서

```text
non-production small task
  → dry-run에서 artifact/state 확인
  → max_fix_loops: 1 + manual apply
  → test evidence와 audit quality 측정
  → reviewer persona / CI artifact를 점진 확장
```

## Sources

- https://github.com/9thLevelSoftware/Clodex
- https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md
- https://github.com/lukaskucinski/clodex
