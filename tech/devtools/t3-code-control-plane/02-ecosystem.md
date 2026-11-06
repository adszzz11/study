---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem

## 역할별 비교

| 도구 | 주 역할 | T3 Code와의 차이 |
|---|---|---|
| **T3 Code** | 여러 coding harness의 control plane | agent 자체보다 통합 UI, thread, worktree, 원격 운영에 초점 |
| **Codex** | OpenAI coding agent/CLI·app | T3 Code에서 실행할 수 있는 provider 중 하나이며 OpenAI 생태계 중심 |
| **Claude Code** | Anthropic의 terminal-first coding agent | T3 Code가 login/config를 감싸 multi-agent UI 운영을 제공 |
| **Cursor** | AI-native IDE와 Agent | editor-centric 경험과 code intelligence 중심; T3 Code는 harness-agnostic 운영면 중심 |
| **OpenCode** | 오픈소스 coding agent | 자체 terminal/desktop/web 및 다양한 provider 연결; T3 Code는 이를 포함한 harness 조율에 초점 |
| **GitHub Copilot** | GitHub/IDE 통합 AI 개발 도구 | GitHub platform과 IDE workflow에 더 밀착 |

## 선택 기준

| 상황 | 우선 고려 |
|---|---|
| 한 editor에서 code completion과 agent를 함께 쓴다 | Cursor 또는 GitHub Copilot |
| terminal-first agent 하나를 깊게 자동화한다 | Codex, Claude Code, OpenCode |
| 여러 provider를 같은 host/repo에서 task별로 비교·병렬 운영한다 | T3 Code |
| local model과 다수 provider를 agent 자체에서 고른다 | OpenCode |

T3 Code의 가치는 "어느 모델이 가장 좋은가"보다 "이미 선택한 harness들을 어떻게 안전하게 나누고, 관찰하고, 합칠 것인가"에 있다. 따라서 model gateway, IDE, code review 정책을 대체하기보다 그 사이의 운영면을 담당한다.

## 확인할 차이

- Cursor Agent는 terminal command, code edit, diff review, checkpoint를 IDE 경험 안에서 제공한다.
- OpenCode는 다양한 provider와 local model 구성을 지원한다.
- T3 Code는 provider마다 가진 tool behavior와 login을 통합하지만, provider별 정책과 capability 차이를 없애지는 않는다.

## 관련 학습

- [[tech/devtools/t3-code-control-plane/README|T3 Code]]
- [[tech/devtools/t3-code-control-plane/01-overview|Overview]]
- [[tech/devtools/t3-code-control-plane/05-projects|Projects]]

## Sources

- https://docs.cursor.com/chat/overview
- https://docs.opencode.ai/docs/providers/
- https://github.com/pingdotgg/t3code
