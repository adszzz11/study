---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo

> **한 줄 정의**: Ruflo는 Claude Code·Codex 같은 coding agent에 multi-agent swarm, persistent memory, MCP tools, hooks, policy/security layer를 더하는 오픈소스 **agent meta-harness / orchestration platform**이다.

## Overview

Ruflo는 새로운 foundation model이나 범용 application framework가 아니다. 기존 coding agent 주위에 execution layer를 두고 작업 분해, agent routing, 공유 memory, lifecycle hook, tool policy와 audit를 조율한다.

```text
User
  ↓
Ruflo CLI / MCP
  ↓
Hooks · Router · Workflow
  ↓
Swarm Coordinator
  ↓
Specialized Agents
  ↓
AgentDB / RuVector Memory
  ↓
Claude · OpenAI · Gemini · Local LLM
  ↑
Learning / Routing Feedback Loop
```

> [!warning] Version snapshot
> 조사 기준일은 **2026-09-08**이며 npm `latest`는 **3.38.23**이다. 저장소 일부 문서에는 `3.31.0` 또는 `3.5.0`이 남아 있으므로 설치 전 `npm view ruflo version`으로 재확인한다. agent·command·plugin·MCP tool 개수도 릴리스마다 달라질 수 있다.

## Learning Path

- [ ] [[01-overview|1. What/Why와 핵심 아키텍처]]
- [ ] [[02-ecosystem|2. 대안 도구와 선택 기준]]
- [ ] [[03-references|3. 공식 자료와 검증 순서]]
- [ ] [[04-learning/01-getting-started|4. 안전한 sandbox에서 시작하기]]
- [ ] [[04-learning/02-deep-dive|5. swarm·memory·hooks·guidance 심화]]
- [ ] [[05-projects|6. 작은 프로젝트로 검증하기]]
- [ ] [[cheatsheet|7. 명령·개념 치트시트]]

## When To Use

- 하나의 coding task를 research, implementation, test, review 역할로 분해하고 병렬 조율할 때
- Claude Code·Codex 등 기존 coding agent를 교체하지 않고 swarm과 persistent memory를 덧붙일 때
- MCP, hooks, workflow를 통해 여러 client의 실행 방식을 한 곳에서 관리할 때
- 반복되는 project pattern과 작업 trajectory를 session 사이에서 재사용할 때
- destructive operation, secret, budget, audit에 공통 policy gate가 필요할 때

## When Not To Use

- 단일 agent와 짧은 context로 충분한 작은 수정: orchestration overhead가 더 클 수 있다.
- state transition을 코드로 엄밀하게 정의하는 production application runtime이 필요한 경우: LangGraph 같은 graph runtime이 더 직접적이다.
- 최소 SDK로 handoff와 tracing만 구현하려는 경우: OpenAI Agents SDK 같은 작은 abstraction이 적합할 수 있다.
- subsystem maturity, dependency provenance, secret handling을 별도로 검증할 여력이 없는 production 환경
- 많은 MCP tools를 모두 노출해도 된다고 가정하는 환경: context 비용과 attack surface가 커진다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]]
- [[tech/ai/litellm/README|LiteLLM]]

## Sources

- [Ruflo official README](https://github.com/ruvnet/ruflo/blob/main/README.md)
- [Ruflo npm package and versions](https://www.npmjs.com/package/ruflo?activeTab=versions)
- [Ruflo changelog](https://github.com/ruvnet/ruflo/blob/main/CHANGELOG.md)
- [Ruflo configuration](https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md)
- [Ruflo core plugin](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-core/README.md)
- [AgentDB plugin](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md)
- [Guidance architecture overview](https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md)

## Q&A

**Q:** Ruflo와 Orca를 함께 사용하면 어떤 효과를 기대할 수 있으며, 사용사례가 있는가?

**A:** 가장 유용한 조합은 **Orca가 worktree·terminal·agent 실행을 관리하고, Ruflo가 검증된 작업 지식을 persistent memory로 제공하는 구성**이다. 기존 노트의 핵심인 역할 분해·결과 검증·경험 재사용을 Orca의 개발 workflow에 연결하는 방식이다. 아래 효과는 두 도구의 기능과 노트에 근거한 설계 가설이며, 이 저장소에서 연동하거나 성능을 실측한 결과는 아니다.

Orca는 이미 여러 coding agent 실행과 orchestration을 지원하므로 Ruflo를 추가해야 병렬 작업이 가능해지는 것은 아니다. 추가 가치는 단순 agent 증설보다 **session과 worktree를 넘어 실패 원인·검증 결과·설계 결정을 검색하고 재사용하는 것**에 있다. Orca의 agent 실행과 hooks 노출은 [공식 Claude Code 문서](https://www.onorca.dev/docs/agents/claude-code), Ruflo의 memory 기능은 [AgentDB 문서](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md)에 설명되어 있다.

| 활용 시나리오 | 함께 사용하는 방식 | 기대 효과 |
|---|---|---|
| 반복되는 bug 수정 | 첫 Orca 작업에서 확인한 원인·수정·test evidence를 Ruflo에 저장하고, 다음 작업의 agent가 검색 | 같은 원인을 다시 조사하는 시간과 설명 반복 감소 |
| module별 refactoring | Orca의 별도 worktree에서 module을 수정하고, 공통 API contract와 검증된 제약을 Ruflo memory에서 참조 | 작업 디렉터리 분리와 설계 맥락 공유를 함께 달성; 최종 merge conflict와 integration test는 별도 확인 |
| Test-gap audit | researcher·tester·reviewer가 조사한 근거를 모으고, 확정된 failure pattern만 저장 | 누락된 edge case 발견과 다음 audit의 조사 효율 개선 가능 |

이 시나리오들은 [[05-projects|기존 Projects 노트]]의 `Read-only repository audit`, `Test-gap swarm`, `Persistent project memory`를 Orca 환경으로 확장한 **실험 제안**이다. 해당 노트는 완료된 구축 사례나 benchmark 보고서가 아니다.

연결은 우선 다음처럼 단순하게 시작할 수 있다.

```text
Orca: worktree / agent session / 작업 진행 관리
  └─ 실행 중인 coding agent
       ├─ repository 조사·수정·test
       └─ MCP 또는 CLI → Ruflo memory 검색·검증된 결과 저장
```

각 coding client에서 Ruflo MCP 또는 CLI 접근을 설정해야 한다. 설치만으로 Orca의 task·terminal·worktree 상태가 Ruflo와 자동 동기화되거나, 서로 다른 worktree의 memory가 자동 공유된다고 가정하면 안 된다. 공유 backend와 project 범위를 명시해야 하며, AgentDB 문서상 일부 API는 `namespace`를 무시하므로 사용하는 API의 실제 분리 동작도 확인해야 한다. 위 구성은 Orca가 실행을 소유하고 Ruflo는 memory를 제공하게 한다. 나중에 Ruflo swarm을 추가한다면 task 분배·retry·종료를 담당할 coordinator를 하나로 정해야 중복 실행과 비용 증가를 줄일 수 있다.

**공개 사용사례는 어디까지 확인됐는가?** 2026-09-09 확인 범위에서 Ruflo 공식 문서와 `"ruflo" "orca"`, `"claude-flow" "Orca" worktree` 공개 검색으로는, 이 Orca 개발환경과 Ruflo를 함께 구축해 효과를 측정한 case study나 공식 integration guide를 찾지 못했다. [Ruflo MCP Tools 문서](https://github.com/ruvnet/ruflo/wiki/MCP-Tools)에는 memory 저장·검색과 task routing 예제가 있고, Orca 공식 문서에는 worktree에서 agent를 실행하는 사용법이 있다. 이는 개별 기능의 사용 예제이며 두 제품을 결합한 실증 사례는 아니다. 사례가 없다고 단정할 수는 없지만, 현재 근거로 특정 속도 향상이나 비용 절감 수치를 약속할 수는 없다.

첫 검증은 **Orca의 기존 workflow에 Ruflo memory만 추가**하는 것이 적합하다. 같은 repository·commit·model 조건에서 `Orca만 사용`, `Orca + Ruflo memory`를 비교하고, 첫 작업에서 검증한 failure pattern이 유사한 다음 작업에 도움이 되는지 본다. 측정 항목은 task 성공률, wall-clock time, token/cost, human review time, stale memory로 인한 오판이다. 기존 Orca workflow만으로 충분하거나 작은 수정이 대부분이면 추가 MCP 호출과 운영 복잡성이 이득보다 클 수 있다.
