---
date: 2026-11-07
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Instruction Drift 첫 감사

## 목표

한 repository에서 agent가 실제로 받을 instruction file을 찾고, 각 rule을 code 또는 실행 가능한 검증에 연결한다.

## 절차

1. root와 하위 directory의 `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`를 inventory한다.
2. 각 문장을 path, command, test, tool 중 무엇으로 검증하는지 표기한다.
3. 검증 불가한 과거 이력, 중복 lint rule, 폐기된 command를 삭제하거나 최신 근거로 바꾼다.
4. global instruction에 code-precedence와 inconsistency reporting rule을 추가한다.
5. agent run마다 발견한 불일치, 선택한 근거, test 결과를 final report에 남긴다.

## 최소 Audit 표

| Rule | 검증 근거 | 조치 |
|---|---|---|
| `npm run check` 실행 | `package.json`, CI workflow | 없으면 제거 또는 명령 갱신 |
| `src/api` 사용 | directory와 import | rename 뒤 path 갱신 |
| camelCase naming | existing modules, lint config | code convention이 다르면 문서 정정 |

## Disposable 실험

작은 disposable repository에 code와 반대되는 stale rule 하나를 둔다. agent에게 feature를 맡긴 뒤 다음을 기록한다.

- 어느 convention을 택했는가?
- 충돌을 final report에 명시했는가?
- 기존 및 새 test가 통과했는가?

다음: [[tech/devtools/stale-agent-instructions/04-learning/02-deep-dive|Deep Dive]] · 빠른 점검: [[tech/devtools/stale-agent-instructions/cheatsheet|Cheatsheet]]

## Sources

- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://arxiv.org/abs/2610.30571
