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

## Q&A

**Q:** Ruflo의 구체적인 사용례를 리서치해 제안하고, 기존 Orca workflow와 함께 최대 효과를 내는 방법을 설명해 달라.

**A:** 추천하는 방향은 **반복되는 작업 하나에서 검증된 지식을 재사용하고, 독립적으로 나눌 수 있는 조사·test만 병렬화하는 것**이다. 이 study에서는 당장 `study 업데이트 검증`을 실험할 수 있고, 실제 개발 repository에서는 `반복 bug 수정`을 우선 추천한다. 최대 효과는 agent 수보다 **재조사 시간, 재발 bug, 사람이 고치는 시간의 감소**로 판단한다.

아래는 [[05-projects|Projects]]와 [[04-learning/02-deep-dive|Deep Dive]], 앞선 Orca Q&A를 구체화한 **사용례 설계와 실험 계획**이다. 2026-09-09 공식 문서를 추가 확인했으며, Ruflo를 설치하거나 이 시나리오를 실행해 성능을 측정한 결과는 아니다.

### 리서치에서 확인한 기능과 적용 범위

- **Memory:** 공식 AgentDB 문서는 저장·검색, pattern 재사용, session 기능을 설명한다. 단, `memory_*`와 `embeddings_search`는 namespace를 사용하지만 `agentdb_pattern-*`와 `agentdb_hierarchical-*` 등은 namespace 인자를 무시한다. project별 분리를 이름만으로 보장하지 말고 사용하는 경로의 동작을 검증해야 한다. [AgentDB 공식 문서](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md)
- **Workflow:** 공식 문서는 pause/resume을 지원하는 MCP `workflow_*` 경로와 Claude Code용 native `Workflow` JS 경로를 구분한다. plugin smoke test를 모으고 실패한 항목의 원인을 병렬 조사하는 예제도 제공한다. 이 예제의 `sweep → diagnose failures → report` 구조를 아래 사용례에 응용할 수 있다. native 경로가 모든 coding client에서 그대로 동작한다고 가정하지 않는다. [Workflows 공식 문서](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-workflows/README.md)
- **Swarm:** 역할별 coordination과 worktree isolation을 설명한다. Orca가 이미 agent 실행을 관리한다면 Ruflo swarm을 동시에 coordinator로 둘 필요는 없다. 처음에는 기존 실행 방식에 memory만 연결하는 구성이 합리적이다. 마지막 문장은 앞선 Q&A와 기능 구성을 바탕으로 한 설계 판단이다. [Swarm 공식 문서](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-swarm/README.md)

### 사용례 1: 반복 bug를 해결하는 project memory

**상황 예시:** webhook을 재전송하거나 worker가 retry하면 같은 주문이 두 번 처리되는 서비스. 이는 가상의 개발 사례이며 이 study repository에 해당 서비스가 있다는 뜻은 아니다.

1. 첫 작업에서 중복 처리의 재현 조건과 failing regression test를 확보한다.
2. 구현 담당은 idempotency 처리와 transaction 경계를 수정하고, reviewer는 순차 재전송뿐 아니라 동시 요청·중간 실패도 검토한다.
3. 수정 전 실패와 수정 후 통과를 확인한 뒤, 원인·적용 조건·test evidence·commit을 memory에 저장한다.
4. 다음 유사 작업에서 해당 memory를 검색하고, 현재 code와 맞는지 확인한 뒤 재사용한다. 다른 database나 transaction 구조라면 그대로 적용하지 않는다.

**산출물:** 검증 가능한 patch, regression test, 짧은 failure-pattern record. **기대 효과:** 다음 bug에서 원인 탐색과 edge case 누락을 줄이는 것. 첫 작업은 memory 정리 비용 때문에 더 느릴 수 있으므로 후속 작업까지 평가한다.

다음은 저장할 내용의 예시이며 Ruflo API schema가 아니다. 실제 결과로 채우기 전에는 검증된 memory로 등록하지 않는다.

```yaml
record_type: verified_failure_pattern
project: example-orders
symptom: Duplicate processing after webhook retries
applicability: Same event identity and compatible transaction model
decision: Atomically claim the event before applying its effects
evidence:
  repository_commit: <verified-commit-sha>
  regression_test: <actual-test-path-and-case>
  before_result: <observed-failure>
  after_result: <observed-pass>
review_after: <review-date>
```

### 사용례 2: Test-gap audit를 regression 방어로 연결

**상황 예시:** API client의 timeout·retry·pagination 동작을 바꿨는데 정상 응답 test만 있다.

- Researcher는 실제 구현과 contract를 읽어 timeout, 중복 응답, 마지막 page, rate limit의 기대 동작을 정리한다.
- Tester는 이 근거를 받아 누락된 test를 작성한다. 여러 tester를 쓰는 경우 unit/integration test 파일의 소유권을 나눈다.
- Reviewer는 test가 구현을 그대로 따라 쓰는지, 실패를 제대로 감지하는지, 기존 suite와 함께 통과하는지 확인한다.

**순서:** contract 확인 → 독립된 test 작성 → 통합 검증. 의존 단계까지 동시에 실행하지 않는다. 처음에는 동시 worker 2개 이내로 시작한다.

**산출물:** 근거가 있는 test-gap 목록, test patch, 실행 결과, 제외한 항목과 이유. **Memory:** 다른 module에도 적용되는 검증된 failure pattern만 저장한다. **평가:** coverage 증가량보다 실제로 잡은 regression과 false positive, review 시간을 본다. 이 사례는 [[05-projects|Test-gap swarm]]의 구체화다.

### 사용례 3: 이 공개 study의 업데이트 검증

**상황:** `tech/ai/ruflo/` 노트의 version, 명령, API 설명이 공식 문서와 달라졌는지 반복 점검한다.

1. Researcher는 기존 claim을 추출해 `claim / note path / source URL / checked date / verdict` 표를 만든다.
2. 독립적으로 확인 가능한 영역만 나눈다. 예를 들어 release·설치 경로와 memory·workflow 동작을 각각 조사한다.
3. Reviewer는 `main` 문서, npm 배포 version, plugin compatibility가 같은 기준인지 확인하고, 차이를 오류로 단정하지 않고 구분한다.
4. Editor 한 명이 확인된 항목만 수정안으로 모은다. memory에는 원문 전체 대신 검증한 claim, 근거 URL, 적용 version, 재확인 조건을 남긴다.

**산출물:** 출처가 연결된 변경 후보표와 작은 문서 diff. **기대 효과:** 다음 업데이트에서 근거를 다시 찾는 시간과 오래된 설명의 재사용을 줄인다. version·가격·명령처럼 바뀌는 정보는 memory가 있어도 공식 source를 다시 확인한다. 이 저장소의 공개 문서 반영은 English documentation 규칙을 따르며, 이번 한국어 Q&A는 요청에 따른 local 변경으로 유지한다.

### 효과를 높이는 운영 방식

```text
Orca의 기존 작업 실행
  → 현재 task와 관련된 Ruflo memory 검색
  → code/source와 대조해 적용 가능한 근거 선택
  → 구현 또는 독립적인 조사·test 수행
  → test/source 검증과 review
  → 검증된 lesson만 memory에 저장
  → 다음 유사 작업에서 효과 측정
```

1. **하나의 실행 책임자:** task 배정·retry·종료는 한 coordinator가 소유한다. Ruflo workflow를 도입하더라도 Orca와 같은 task를 중복 배정하지 않는다. worktree별 memory가 자동 공유된다고 가정하지 말고 backend 위치와 scope를 명시한다.
2. **작업 계약부터 고정:** 입력, 수정 가능한 파일, 산출물 형식, 완료 조건을 정한다. 병렬화는 파일·산출물이 독립적일 때만 사용하고 최종 integration 검증을 둔다.
3. **작게 검색하고 선별 저장:** 첫 실험에서는 검색 결과를 최대 3건으로 제한한다. 현재 version에 맞는지 확인하고, 근거 없는 결론과 raw transcript는 저장하지 않는다. 3건은 추천 시작값이며 제품의 최적값이 아니다.
4. **자동화는 수동 loop 검증 후:** 먼저 명시적인 검색·검토·저장으로 효과를 확인한다. 이후 hook을 붙이면 같은 결과를 수동 저장과 hook이 중복 기록하지 않도록 한 경로를 택한다. AgentDB 문서도 중복 write를 피하도록 설명한다. [Hook integration 문서](https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md#hook-integration-convention)
5. **운영 비용까지 포함:** token뿐 아니라 MCP 호출, 실행 대기, 실패 재시도, merge conflict 해결, human review 시간을 기록한다. 작은 문구 수정처럼 재사용이나 병렬화 여지가 적은 작업은 기존 방식으로 처리한다.

### 1주 pilot: 무엇이 이득인지 분리해서 측정

아래 기간과 숫자는 제안한 실험 설정이며 공식 benchmark가 아니다.

| 단계 | 실행 | 확인할 것 |
|---|---|---|
| Day 1 | 반복 작업군 하나, 대표 task 5개, acceptance criteria 선정 | repository commit, model, budget, test 환경 고정 |
| Day 2 | A: 기존 Orca workflow로 수행 | 성공률, 시간, token/cost, human review 기준값 |
| Day 3 | 별도 선행 task에서 검증한 memory 준비; B: 같은 workflow + memory | 평가 task의 정답이나 A의 결과가 memory에 섞이지 않는가 |
| Day 4 | B가 유망하면 C: memory + 독립 단계의 제한적 병렬화 | memory 효과와 병렬화 효과를 구분할 수 있는가 |
| Day 5 | task별 결과 비교와 실패 원인 정리 | 어떤 유형에 적용하고 어떤 유형에서 제외할 것인가 |

각 조건은 새 session과 동일한 시작 commit에서 실행하고 순서를 교차한다. 평가 중 생성한 memory는 run별로 격리해 다른 조건의 입력에 섞이지 않게 한다. 가능하면 task당 2회 이상 반복하고 중앙값과 실패 건수를 함께 본다. 5개 task는 탐색용 표본이므로 일반적인 성능 우위를 증명하지 않는다.

**채택 기준 예시:** acceptance criteria와 regression 품질을 유지하면서, 사람이 고치는 시간을 포함한 task당 총 소요 시간이 중앙값 기준 20% 이상 줄고 API 비용이 사전 budget 안에 들면 해당 작업군으로 확대한다. 20%는 우리가 정하는 목표이며 Ruflo의 보장 수치가 아니다. 품질이 나빠지거나 운영 비용이 절감분보다 크면 memory 범위를 줄이거나 기존 방식으로 돌아간다.

**바로 사용할 pilot 작업 brief:** 아래는 agent에게 전달할 입력 template이며 실행 명령이나 자동 설정 파일이 아니다.

```text
Task: <반복 작업군의 task 하나>
Baseline: <repository commit, model, 기존 workflow>
Allowed files: <수정 가능한 경로>
Acceptance criteria: <실제 test 또는 source 검증 기준>
Memory: 관련 근거 최대 3건; 현재 code/version과 대조 후 사용
Execution: coordinator 하나; 독립 작업에만 동시 worker 최대 2개
Output: 근거, diff, 검증 결과, 미해결 사항, 시간과 비용
Memory write: 검증 완료된 lesson만; 적용 조건과 evidence를 포함
Stop: 사전 budget 초과 또는 검증 기준을 충족할 수 없는 경우
```
