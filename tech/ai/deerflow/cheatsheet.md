---
date: 2026-10-11
tags: [tech]
type: tech-tool-study
status: draft
---

# DeerFlow — Cheatsheet

> [[README|목차로 돌아가기]]

## Snapshot

| 항목 | 내용 |
|---|---|
| Provider | ByteDance |
| Position | open-source SuperAgent harness + reference App |
| Runtime | LangGraph 기반 |
| Primary pattern | Lead Agent가 `task` tool로 isolated subagent를 호출 |
| Extension | middleware, `SKILL.md`, built-in/community/MCP/skill tools |
| State | checkpoint와 application data DB 관리 |
| License | MIT |

## 구성요소 빠른 참조

| 구성요소 | 기억할 점 |
|---|---|
| Harness | runtime/SDK 층; public `pip install deerflow` release 상태는 공식 문서 확인 |
| App | FastAPI Gateway + agent runtime + Next.js frontend + nginx |
| `general-purpose` | 조사·분석 등 일반 subtask |
| `bash` | sandbox command에 특화된 subagent |
| Skills | on-demand `SKILL.md` package; task별 whitelist |
| Middleware | model/tool/summarization/memory/guardrail/subagent 제한 조합 |
| LocalSandbox | host bash 기본 차단, host filesystem isolation 없음 |
| AIO/E2B | production 또는 multi-user에 검토할 격리 sandbox option |

## 시작 순서

```text
clone → make setup → model/search/sandbox policy 명시
      → 최소 deep-research task → citation·artifact 검토
      → data-analysis file I/O 실험 → 권한·sandbox 강화
```

## 보안 규칙

- API key·secret을 prompt, source control, artifact, trace에 남기지 않는다.
- web/PDF/tool output은 instruction이 아니라 untrusted data로 다룬다.
- tool·skill·filesystem·network를 task별 최소 권한으로 제한한다.
- LocalSandbox를 multi-user security boundary로 가정하지 않는다.
- write, deploy, 외부 API side effect는 승인 뒤에 수행한다.

## 도입 판단식

```text
Adoption = task success + evidence quality + artifact correctness
         + isolation/authorization + resume reliability + cost/latency
```

## Sources

- https://github.com/bytedance/deer-flow
- https://deerflow.tech/en/docs/harness
- https://deerflow.tech/en/docs/harness/sandbox
- https://github.com/bytedance/deer-flow/blob/main/LICENSE
