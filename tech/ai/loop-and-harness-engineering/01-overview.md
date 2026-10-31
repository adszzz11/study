---
date: 2026-06-23
tags: [tech, ai, agent-loop, agent-harness, harness-engineering]
status: learning
type: tech-tool-study
---

# 01. Overview — What / Why / 핵심 특징

## 1. What: 두 용어의 차이

| 용어 | 한국어 감각 | 핵심 질문 | 산출물 |
|------|-------------|-----------|--------|
| `loop engineering` | agent가 일을 반복하는 방식 설계 | "실패했을 때 무엇을 보고 어떻게 다시 시도할까?" | plan-act-observe-verify loop, retry rule, stop condition |
| `harness engineering` | agent가 돌아가는 실행 기반 설계 | "agent가 어떤 문맥·도구·권한·검증 안에서 일할까?" | context manager, tool registry, permissions, evals, traces |

**Loop engineering**은 agent의 행동 흐름을 설계한다. 예를 들어 `테스트 실행 -> 실패 로그 읽기 -> 원인 추정 -> 코드 수정 -> 다시 테스트` 같은 반복을 명시한다.

**Harness engineering**은 그 반복이 안전하고 재현 가능하게 돌아가도록 주변 장치를 만든다. 예를 들어 어떤 명령은 허용하고, 어떤 파일은 읽게 하며, 어떤 테스트를 통과해야 완료로 인정할지 정한다.

## 2. Why: prompt engineering만으로 부족해진 이유

2025-2026년 agentic coding은 단순 답변 생성이 아니라 장기 작업 실행으로 이동했다.

```text
과거: prompt -> model answer
현재: goal -> read files -> run commands -> patch -> test -> retry -> report
```

이때 실패의 원인은 모델 지능 하나만이 아니다. 2026년 AI Harness Engineering 논문은 autonomous software engineering 능력을 **model-harness-environment system**으로 본다. 모델이 프로젝트를 어떻게 관찰하는지, 어떤 tool을 쓰는지, 어떤 feedback을 받는지, 완료를 어떻게 증명하는지가 결과를 크게 바꾼다는 관점이다.

한국 회사 예시:

| junior 개발자에게 필요한 것 | agent harness의 대응 |
|----------------------------|----------------------|
| 이슈 설명서 | `Task interface` |
| 코드베이스 안내서 | `Context manager` |
| 실행 권한 | `Permission boundary` |
| 테스트/완료 기준 | `Verification protocol` |
| 실패 로그 | `Observability layer` |
| 보고 양식 | `Intervention logger`, verification report |
| 재시도 규칙 | `Agent loop`, failure attribution |

즉 "잘 말하기"보다 **일이 돌아가는 시스템을 설계하기**가 중요해졌다.

## 3. 기본 Agent Loop

```text
Goal
 -> Plan
 -> Retrieve context
 -> Use tools
 -> Observe results
 -> Diagnose failure
 -> Patch/change
 -> Verify
 -> Decide: stop or continue
```

실무에서는 아래처럼 구체화한다.

```text
1. issue를 읽고 성공 조건을 checklist로 바꾼다.
2. 관련 파일과 문서를 찾는다.
3. 최소 변경을 만든다.
4. test/lint/build를 실행한다.
5. 실패하면 log를 근거로 failure attribution을 작성한다.
6. 다시 수정한다.
7. 검증 증거가 충분하면 종료하고 report를 남긴다.
```

Claude Code 분석 논문도 agentic coding system의 중심을 `model call -> tool execution -> repeat` while-loop로 설명한다. 다만 실제 난이도는 loop 한 줄보다 permission, context compaction, MCP, plugins, skills, hooks, subagents, worktree isolation 같은 주변 시스템에 있다.

## 4. Harness Components

2026년 AI Harness Engineering 논문은 harness 책임을 11개로 나눈다.

| 구성요소 | 역할 | 없을 때 생기는 문제 |
|---|---|---|
| `Task interface` | 목표, 요구사항, 성공기준 정의 | 엉뚱한 문제 해결 |
| `Context manager` | 필요한 파일/문서 선별 | wrong-file inspection |
| `Tool registry` | 사용 가능한 tool/command 선언 | 위험 명령, 반복 실패 |
| `Project memory` | 아키텍처, 테스트 규칙, 과거 실패 저장 | 매번 재탐색 |
| `Task state` | 현재 가설, 본 파일, 다음 단계 유지 | 작업 drift |
| `Observability layer` | logs, traces, runtime output 노출 | 실패 원인 불명 |
| `Failure attribution` | 실패 원인 분류 | 랜덤 패치 |
| `Verification protocol` | 요구사항별 증거 생성 | "된 것 같음"으로 종료 |
| `Permission boundary` | 위험 작업 승인/차단 | 삭제, 과범위 수정 |
| `Entropy auditor` | 유지보수 부담 감지 | dependency churn, residue |
| `Intervention logger` | 인간 개입 기록 | 실제 자동화 수준 과대평가 |

## 5. 핵심 특징

- **반복성**: agent는 한 번 답하고 끝나는 것이 아니라 관찰·행동·검증을 반복한다.
- **검증 우선**: 완료 기준은 "모델이 됐다고 말함"이 아니라 test, trace, eval, review evidence다.
- **상태 관리**: 긴 작업에서는 `Task state`가 없으면 같은 파일을 반복해서 보거나 목표가 drift한다.
- **권한 경계**: `rm`, migration, deploy, secret 접근 같은 행동은 명확한 permission boundary가 필요하다.
- **관찰 가능성**: trace와 log가 있어야 실패 원인을 model, tool, context, environment 중 어디로 돌릴지 판단할 수 있다.
- **사람 개입 설계**: `human-in-the-loop`는 불완전한 자동화를 인정하고 승인 지점을 명시하는 방식이다.

## 6. 관련 노트

- [[study/tech/ai/lazy-codex]] - 거짓 완료를 검증 루프로 잡는 사례
- [[study/tech/ai/model-context-protocol-mcp]] - tool/context 연결 계층
- [[study/tech/ai/codex]] - coding agent 사용 맥락
