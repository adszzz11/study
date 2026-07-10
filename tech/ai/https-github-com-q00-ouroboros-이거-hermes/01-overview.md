---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - spec-first
  - agent-os
status: learning
type: tech-tool-study
---

# 01. Overview — What / Why / 특징

## What

`Q00/ouroboros`는 coding agent 위에 얹는 **specification-first Agent OS/workflow engine**이다.

```text
vague prompt
  -> Socratic interview
  -> immutable Seed spec
  -> acceptance criteria
  -> execution by backend runtime
  -> evaluation gate
  -> evolution / replay
```

여기서 backend runtime은 Claude Code, Codex CLI, OpenCode, Hermes, Gemini, Kiro, Copilot, Pi 같은 agent가 될 수 있다. Ouroboros의 초점은 코드를 직접 잘 쓰는 것보다, agent가 실행할 수밖에 없는 **정확한 contract**를 만드는 데 있다.

## Why

AI coding agent는 이미 다음 작업을 잘한다.

- codebase 읽기와 검색
- 파일 생성/수정
- shell command 실행
- lint/build/test 수행
- MCP tool 호출
- git/PR workflow 일부 자동화

하지만 실제 실패는 종종 agent의 손이 느려서가 아니라, **요구사항이 실행 가능한 형태로 정리되지 않아서** 생긴다.

| 문제 | agent가 흔히 하는 행동 | 결과 |
|---|---|---|
| 목표가 vague함 | missing requirement를 추측 | 나중에 scope drift 발생 |
| constraint가 숨겨져 있음 | architecture를 임의 선택 | 운영 조건과 충돌 |
| acceptance criteria가 없음 | "완료"를 주관적으로 판단 | false completion 또는 QA 누락 |
| 평가 기준이 뒤늦게 생김 | 구현 후에 맞추려 함 | 리팩터링 비용 증가 |

Ouroboros는 이 문제를 **input clarity problem**으로 보고, coding 전에 specification을 확정하는 흐름을 강제한다. README의 핵심 메시지도 "Stop prompting. Start specifying."와 "replayable, observable, policy-bound execution contract" 쪽에 있다.

## 핵심 아키텍처

### Agent OS stack

| 계층 | 역할 |
|---|---|
| `ouroboros` core | kernel. spec, workflow, event, evaluation의 중심 |
| `ouroboros-plugins` | UserLevel workflows. 반복 가능한 업무 흐름을 plugin으로 확장 |
| `ourocode` | terminal shell. agent workflow를 터미널에서 다루는 surface |
| backend runtime | Claude Code, Codex CLI, Hermes, Gemini CLI, OpenCode 등 실제 실행자 |

### Seed 중심 workflow

`Seed`는 interview 결과를 결정화한 immutable spec이다.

```yaml
goal: "Build a local-first task management CLI"
constraints:
  - "No external database"
  - "Runs on macOS and Linux"
acceptance_criteria:
  - "User can add/list/complete tasks from terminal"
  - "Data persists across sessions"
ontology:
  entities:
    - Task
    - Project
exit_conditions:
  - "All mechanical checks pass"
  - "Acceptance criteria verified"
```

Seed에는 보통 다음 요소가 들어간다.

- `goal`: 무엇을 만들지
- `constraints`: 기술, 운영, 보안, UX 제약
- `acceptance criteria`: 완료 여부를 판단할 관찰 가능한 조건
- `ontology schema`: domain object와 관계
- `exit conditions`: 작업을 종료할 수 있는 조건

### Ambiguity gate

Ouroboros는 모호성이 충분히 낮아지기 전까지 coding execution으로 넘어가지 않는다.

```text
if ambiguity_score > 0.2:
    continue_interview()
else:
    crystallize_seed()
    execute()
```

이 gate의 의미는 "agent에게 더 잘하라고 압박"하는 것이 아니라, **agent가 실패할 수밖에 없는 입력을 실행하지 않게 막는 것**이다.

### Double Diamond execution

Ouroboros는 acceptance criteria를 recursive decomposition하면서 Double Diamond 흐름을 따른다.

| 단계 | 초점 | 질문 |
|---|---|---|
| Discover | 문제 발산 | 무엇이 불명확한가? |
| Define | 문제 수렴 | 어떤 spec이 실행 가능한가? |
| Design | 해결 발산 | 어떤 implementation path가 가능한가? |
| Deliver | 해결 수렴 | 무엇을 만들고 어떻게 검증할 것인가? |

### Evaluation pipeline

Evaluation은 세 층으로 나뉜다.

1. **Mechanical checks**: lint, format, build, test, static analysis.
2. **Semantic verification**: acceptance criteria와 실제 동작의 의미 비교.
3. **Multi-model consensus**: 필요하면 여러 model/runtime 관점으로 결과 검토.

## Event sourcing / replayability

Ouroboros는 SQLite event store에 append-only event를 기록한다. 이 구조는 다음에 유리하다.

- session resume
- audit trail
- retrospective
- failed run replay
- policy-bound execution 추적

## Tech detail

| 영역 | 기술 |
|---|---|
| Language | Python `>= 3.12` |
| CLI | Typer |
| Data model | Pydantic |
| Persistence | SQLAlchemy, aiosqlite |
| UI | Rich, Textual |
| Optional LLM routing | LiteLLM |
| Optional tool protocol | MCP |

## 기억할 구분

- [[study/tech/ai/codex]] / Claude Code / Gemini CLI / OpenCode: **executor**
- Ouroboros: **specification and evaluation control plane**
- [[study/tech/ai/model-context-protocol-mcp]]: **external tool/context protocol**
- Hermes: **personal/infra agent runtime**, Ouroboros의 backend가 될 수 있음

→ 다음: [[02-ecosystem]]
