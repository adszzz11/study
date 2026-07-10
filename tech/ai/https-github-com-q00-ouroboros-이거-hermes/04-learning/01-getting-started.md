---
date: 2026-06-17
tags:
  - tech
  - ai
  - ouroboros
  - getting-started
  - hermes
status: learning
type: tech-tool-study
---

# 04-1. Getting Started

## 목표

첫 실습의 목표는 Ouroboros를 "coding agent"가 아니라 **spec-first workflow wrapper**로 체감하는 것이다.

완료하면 다음을 설명할 수 있어야 한다.

- `ouroboros init`이 vague prompt를 어떻게 Seed로 바꾸는가
- `Seed`에 goal, constraints, acceptance criteria가 어떻게 들어가는가
- `ouroboros run`이 backend runtime에게 무엇을 넘기는가
- Hermes runtime을 붙이면 역할 분담이 어떻게 달라지는가

## 준비물

| 항목 | 필요 이유 |
|---|---|
| Python `>= 3.12` | Ouroboros runtime |
| `pipx` | CLI tool 격리 설치 |
| Git repo | agent가 작업할 코드베이스 |
| 선택: Hermes | Hermes runtime 실습 |
| 선택: MCP server | external context/tool 실습 |

## 설치

```bash
pipx install 'ouroboros-ai[all]'
ouroboros setup
```

설치 후 확인:

```bash
ouroboros --help
ouroboros setup --help
ouroboros init --help
ouroboros run --help
```

## 첫 Seed 만들기

일부러 약간 vague한 prompt를 넣고, interview가 어떤 질문을 하는지 본다.

```bash
ouroboros init "Build a local-first task management CLI"
```

관찰할 포인트:

- 어떤 hidden assumptions를 질문하는가?
- storage, platform, UX, error handling, test 기준을 묻는가?
- acceptance criteria가 관찰 가능한 문장으로 바뀌는가?
- `Ambiguity Score`가 낮아지기 전까지 execution을 막는가?

예상 Seed 구조:

```yaml
goal: "Build a local-first task management CLI"
constraints:
  - "Local-first storage"
  - "No hosted backend required"
acceptance_criteria:
  - "User can add a task from the terminal"
  - "User can list pending tasks"
  - "User can mark a task complete"
exit_conditions:
  - "CLI tests pass"
  - "Acceptance criteria verified"
```

## 실행

Seed가 생성되면 실행한다.

```bash
ouroboros run seed.yaml
```

실행 중 확인할 것:

- 어떤 backend runtime이 선택되는가?
- mechanical checks로 lint/build/test가 먼저 실행되는가?
- semantic verification에서 acceptance criteria가 다시 참조되는가?
- session resume 또는 event store 위치가 표시되는가?

## Hermes와 같이 보기

Hermes가 설치되어 있다면 runtime을 Hermes로 맞춰본다.

```bash
hermes
hermes model
ouroboros setup --runtime hermes
ouroboros run seed.yaml --runtime hermes
```

역할 분담:

| 역할 | 담당 |
|---|---|
| 요구사항 명확화 | Ouroboros |
| Seed / acceptance criteria | Ouroboros |
| 실행 surface | Hermes |
| command/file/test 작업 | Hermes backend |
| evaluation gate | Ouroboros |

## 실습 체크리스트

- [ ] README와 architecture 문서에서 `Seed` 정의 읽기
- [ ] `ouroboros setup` 실행
- [ ] vague prompt로 `ouroboros init` 실행
- [ ] interview 질문을 기록
- [ ] 생성된 `seed.yaml`에서 goal/constraints/acceptance criteria 표시
- [ ] `ouroboros run seed.yaml` 실행
- [ ] mechanical checks 로그 확인
- [ ] Hermes runtime으로 한 번 더 실행

## 실패했을 때 볼 것

| 증상 | 확인 |
|---|---|
| Python version error | `python --version`, `pipx runpip ouroboros-ai show` |
| runtime not found | `ouroboros setup --runtime ...`와 backend CLI 설치 여부 |
| Seed가 너무 빈약함 | prompt를 더 구체화하기보다 interview 질문에 충실히 답하기 |
| test가 없음 | acceptance criteria 중 mechanical check로 바꿀 수 있는 항목을 test로 추가 |

## 연결 노트

- [[../01-overview]] - Seed와 ambiguity gate의 의미
- [[../02-ecosystem]] - Hermes, Codex CLI, Claude Code runtime 비교
- [[study/tech/ai/model-context-protocol-mcp]] - MCP server/tool을 붙이는 다음 단계

→ 다음: [[02-deep-dive]]
