---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - deep-dive
  - evaluation
status: learning
type: tech-tool-study
---

# 04-2. Deep Dive

## Mental model

Ouroboros를 깊게 이해하려면 세 가지를 분리해서 봐야 한다.

| 개념 | 한 줄 |
|---|---|
| `Seed` | workflow constitution. 실행자가 따라야 하는 immutable contract |
| `Runtime` | 실제로 codebase를 읽고 수정하는 executor |
| `Evaluation` | 작업이 끝났다고 말할 수 있는 gate |

## Seed schema를 분석하는 법

Seed를 볼 때는 "좋은 prompt인가?"보다 "실행 가능한 contract인가?"를 본다.

```yaml
goal:
  statement: "Build a local-first task management CLI"
  non_goals:
    - "No cloud sync in v1"
constraints:
  technical:
    - "Python >= 3.12"
    - "SQLite storage"
  product:
    - "Terminal-first UX"
acceptance_criteria:
  mechanical:
    - "Unit tests cover add/list/complete"
    - "CLI exits non-zero on invalid command"
  semantic:
    - "Completed tasks no longer appear in default pending list"
ontology:
  Task:
    fields: ["id", "title", "status", "created_at", "completed_at"]
exit_conditions:
  - "All tests pass"
  - "Acceptance criteria reviewed"
```

좋은 Seed의 특징:

- goal과 non-goal이 둘 다 있다.
- constraint가 기술 선택을 실제로 제한한다.
- acceptance criteria가 관찰 가능하다.
- ontology가 domain object를 명명한다.
- exit condition이 "agent가 만족했다"가 아니라 "검증 가능하다"로 쓰인다.

## Ambiguity Score

Ambiguity gate는 실행을 늦추는 장치가 아니라 실패한 실행을 줄이는 장치다.

| 신호 | 모호성 증가 |
|---|---|
| "좋게", "적당히", "깔끔하게" | 평가 기준 불명확 |
| "Hermes랑 비슷하게" | 비교 축 불명확 |
| "운영 가능하게" | SLO, deployment, rollback 조건 없음 |
| "AI agent처럼" | autonomy, tool permission, memory 범위 없음 |

모호성을 낮추는 질문:

- 사용자는 누구인가?
- 가장 중요한 workflow 1개는 무엇인가?
- 하지 않을 것은 무엇인가?
- 실패하면 안 되는 constraint는 무엇인가?
- 완료 여부를 command/test/log/UI에서 어떻게 확인하는가?

## Double Diamond를 적용하는 법

| 단계 | 산출물 | 예 |
|---|---|---|
| Discover | open questions | "task storage는 file인가 SQLite인가?" |
| Define | Seed / acceptance criteria | "`task add`, `task list`, `task done` required" |
| Design | implementation options | Typer + SQLite, Click + JSON 등 |
| Deliver | patch + verification | tests, CLI transcript, event log |

핵심은 Discover/Define에서 빨리 코딩하지 않는 것이다. coding agent에게 중요한 것은 prompt 길이가 아니라 **실행 가능한 decision**이다.

## Evaluation pipeline 설계

### 1. Mechanical checks

Mechanical checks는 가장 싸고 재현 가능한 검증이다.

```bash
ruff check .
pytest
mypy .
python -m build
```

적용 원칙:

- acceptance criteria 중 자동화 가능한 것은 test로 내린다.
- build/lint/test가 없는 repo면 최소 smoke test를 만든다.
- mechanical failure가 있으면 semantic review 전에 고친다.

### 2. Semantic verification

Semantic verification은 "테스트는 통과하지만 요구사항은 빗나간" 경우를 잡는다.

예:

```text
Acceptance criterion:
- Completed tasks no longer appear in default pending list.

Semantic check:
- Create task A.
- Mark task A complete.
- Run default list.
- Verify task A is absent.
```

### 3. Multi-model consensus

Multi-model consensus는 고비용 검토 단계다. 모든 작업에 필요한 것은 아니지만, 다음 경우에 유용하다.

- 보안/권한/데이터 손실 위험이 있는 변경
- architecture decision이 큰 변경
- acceptance criteria가 자연어 의미에 많이 의존
- runtime 하나의 blind spot이 걱정되는 경우

## Event sourcing / replayability

Ouroboros의 append-only event store는 단순 로그보다 강한 의미를 가진다.

| event | 의미 |
|---|---|
| interview question/answer | hidden assumption이 어떻게 드러났는지 |
| seed crystallized | 어느 spec이 immutable baseline이 되었는지 |
| runtime action | 어떤 executor가 무엇을 했는지 |
| check result | 어떤 mechanical/semantic gate가 통과/실패했는지 |
| evolution | 다음 iteration에서 무엇이 바뀌었는지 |

활용:

- failed session resume
- "왜 이렇게 구현했나?" audit
- retrospective로 prompt/spec 개선
- 같은 Seed를 다른 runtime에서 replay

## Runtime adapter 관점

Ouroboros가 여러 runtime을 지원한다는 것은 "모든 agent가 동일하다"는 뜻이 아니다. 같은 Seed라도 runtime 특성에 따라 전략이 달라진다.

| runtime | 유리한 상황 |
|---|---|
| Claude Code | codebase navigation, skills/hooks, MCP가 중요한 작업 |
| Codex CLI | local terminal execution, approval-mode가 중요한 작업 |
| Gemini CLI | large-context repository exploration |
| OpenCode | provider-agnostic open workflow |
| Hermes | long-running personal/infra automation, memory/skills/gateway 활용 |

## 학습 과제

- [ ] 같은 vague prompt를 `init`하고 interview 질문을 저장한다.
- [ ] 생성된 Seed에서 acceptance criteria를 mechanical/semantic으로 분류한다.
- [ ] mechanical check가 없는 criterion 하나를 test로 바꿔본다.
- [ ] 같은 Seed를 Hermes와 다른 runtime에서 실행했을 때 차이를 기록한다.
- [ ] event store에서 replay/audit에 필요한 event를 찾아본다.

## 관련 노트

- [[study/tech/ai/lazy-codex]] - independent verification, false completion 방지
- [[study/tech/ai/litellm]] - multi-model consensus와 provider routing
- [[study/tech/ai/model-context-protocol-mcp]] - external tools/context 연결

→ 다음: [[../05-projects]]
