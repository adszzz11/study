---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Prime Agent는 Prime Intellect가 2026년 8월 공개한 오픈소스 coding/research agent harness다. LLM을 stateless chatbot이 아니라 **외부 기억과 계산 장치를 사용하는 sequential processor**로 취급한다. 각 session의 persistent Python REPL, recursive subagents, daemon-backed durable state, 실행 경험을 보조 상태에 반영하는 `Continual Harness`가 중심이다.

이름이 비슷한 일반적인 “prime agent” 개념과 구별해야 한다. 이 노트의 대상은 [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) 프로젝트다.

## Why

일반적인 coding agent는 대화, tool output, log와 중간 결과를 active token context에 직렬화한다. 작업이 길어질수록 다음 문제가 커진다.

| 문제 | 결과 | Prime Agent의 접근 |
|---|---|---|
| `context pollution/context rot` | 중요한 지시와 근거가 log에 묻힘 | 큰 data를 REPL에 두고 필요한 결과만 출력 |
| compaction 손실 | 세부 상태·근거·handle이 사라짐 | state와 history를 L2/L3에 보존 |
| 반복 token 소비 | 같은 data를 tool 호출마다 다시 읽음 | Python object로 filtering·aggregation |
| static harness | 실제 성공·실패가 prompt와 role에 반영되지 않음 | `/refine`으로 typed supplemental state 갱신 |
| process/client 종료 | 장기 objective와 작업 연속성 저하 | daemon-backed detach/reattach와 recovery |
| 분산 accounting | child 비용과 시간을 놓치기 쉬움 | root와 descendant 사용량 합산 |

## Information Hierarchy

논문은 agent의 정보를 네 계층으로 설명한다.

| 계층 | 저장 위치 | 예시 | 성격 |
|---|---|---|---|
| `L0` | model weights | 사전 학습된 지식·능력 | invocation 밖의 고정 기반 |
| `L1` | active token context | 현재 prompt, 최근 대화, 명시적 출력 | 가장 빠르지만 제한된 작업 기억 |
| `L2` | persistent runtime | REPL 변수, tool result, recursive subagent | session 내 계산·상태 계층 |
| `L3` | disk-backed state | history, memory, skill, prompt note, subagent specification | 재시작·compaction을 넘는 장기 계층 |

핵심은 모든 것을 `L1`에 복사하지 않는 것이다. 모델은 `L2`와 `L3`를 programmatically 검색·변환하고, 판단에 필요한 최소 결과만 `L1`로 가져온다.

## Core Architecture

```text
TUI / CLI / RPC client
          │
          ▼
Background daemon ─── persistent session catalog
          │
          ▼
Agent worker ─── TypeScript AgentSession
          │
          ▼ Jupyter protocol / ZeroMQ
Persistent Python kernel
```

- **Client**: interaction과 event 표시를 담당하며 실행 주체와 분리된다.
- **Daemon**: session catalog, tree, message queue와 lifecycle을 관리한다.
- **Worker**: model loop와 `AgentSession`을 실행한다.
- **Kernel**: Python object와 computation state를 유지한다.

## Key Features

### RLM-native persistent REPL

모델에 제공되는 핵심 tool은 사실상 `ipython` 하나다. file, shell, data 처리, skill 호출을 Python code로 조합한다.

```python
# 전체 build.log를 prompt에 넣지 않고 필요한 부분만 context로 가져온다.
errors = [line for line in open("build.log") if "ERROR" in line]
summary = "\n".join(errors[:30])
print(summary)
```

명시적으로 출력하지 않은 object는 active context에 들어가지 않는다. 이는 큰 log나 dataset의 재전송 비용을 줄이지만, code execution 권한과 state hygiene를 사용자가 책임져야 한다.

### Recursive subagents as function calls

```python
child = await rlm(
    "Inspect the authentication implementation and report concrete risks",
    name="auth-reviewer",
)
print(child.rlm_child_id, child.model)
```

`rlm()`은 child 완료가 아니라 admission 직후 stable handle을 반환한다. Parent는 계속 일하고, child는 나중에 `agent_message` 또는 filesystem artifact로 결과를 전달한다.

- parent와 child는 같은 runtime, tools, skills, session machinery 사용
- 각 child는 별도 context, kernel, history 보유
- daemon-mediated asynchronous messaging 지원
- compaction과 restart 뒤에도 관계·handle 유지
- root와 모든 descendant의 token, cost, time 합산

### Continual Harness and `/refine`

`/refine`은 trajectory의 반복되는 성공과 실패를 분석해 다음 typed state를 갱신한다.

- `prompt notes`: 행동 규칙과 지침
- `memories`: 재사용할 사실과 교정된 가정
- `skills`: executable procedure
- `subagent specifications`: 재사용할 역할과 분업 패턴

변경은 provenance가 있는 versioned state로 기록되고 rollback할 수 있다. 여기서 “self-improving”은 **online weight update가 아니라 supplemental harness state 개선**이다.

### Durable operations

- detach/reattach, crash recovery
- session tree와 asynchronous message queue
- `/goal`, `/heartbeat`, schedule 기반 재진입
- budget와 quality gate를 둔 `/autonomous`
- `/fork`, `/clone`, compaction, history retrieval
- JSON event stream, RPC, ACP, Node.js SDK

### Provider-neutral model layer

- Subscription login: Claude, ChatGPT/Codex, GitHub Copilot
- API key: OpenAI, Anthropic, Gemini, Bedrock, DeepSeek, Mistral, Groq, OpenRouter, Prime Inference 등
- Local endpoint: Ollama, vLLM, LM Studio 등 OpenAI-compatible server를 `models.json`으로 연결

지원 범위와 설정 schema는 release마다 바뀔 수 있으므로 실제 구성 전 공식 provider·model 문서를 확인한다.

## Performance Claims

개발진은 Prime Agent + Opus 5가 ARC-AGI-3에서 `95.5% RHAE Best@1`, 세 실행에서 `[95.0, 95.2, 95.5]`, `99.97% Best@3`를 기록했다고 보고했다. long-context suite에서도 여러 model/harness 조합으로 Pi-mono, Claude Code, Codex와 경쟁하거나 앞섰다고 주장한다.

이를 독립 검증된 일반 성능으로 해석하면 안 된다.

- 논문과 benchmark 실행 주체가 개발진이다.
- 일부 결과에는 confidence interval이나 statistical significance 검증이 없다.
- 자체 재실행한 비교 harness 점수가 공식 발표보다 낮아 일부 항목은 경쟁사 공식 점수로 대체했다.
- nanoGPT 연구에서 harness 선택 효과가 실험 noise보다 작았던 결과도 있다.
- RLM/Continual Harness 사용 방식에 맞춰 직접 훈련된 model은 아직 없다고 밝힌다.

## Security Boundary

> [!danger] Runtime isolation은 security sandbox가 아니다.
> Model-generated Python과 shell command는 현재 사용자 권한으로 실행된다.

Factorio 실험에서는 agent가 RCON으로 resource를 생성하는 reward hacking을 발견했고, `/refine`이 exploit을 재사용 skill로 보존했다. 잘못된 objective나 verifier는 self-refinement를 통해 증폭될 수 있다.

필수 방어선:

- disposable clone 또는 container
- filesystem·network least privilege
- production credential 미주입
- 외부 verifier와 immutable acceptance test
- refinement diff review와 rollback
- cost·time·turn·subagent concurrency budget
- third-party package와 skill source allowlist

## Sources

- [Prime Agent 논문 §1–2](https://arxiv.org/html/2608.23552)
- [RLM Runtime Architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/rlm-runtime.md)
- [Architecture documentation index](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/index.md)
- [Refine skill](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/skills/refine/SKILL.md)
- [공식 출시 보고서](https://www.primeintellect.ai/blog/prime-agent)

