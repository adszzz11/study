---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - overview
  - repairable-agents
type: tech-tool-study
parent: "[[README]]"
---

# Hankweave - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - Hankweave란?

Hankweave는 Southbridge.AI가 공개한 **repairable agents runtime**이다. `hank.json`에 선언된 AI workflow를 codon 단위로 실행하고, 각 codon을 checkpoint, event journal, sentinel, budget, workspace isolation으로 감싸 긴 agent 작업을 재현·디버그·수리 가능하게 만든다.

공식 README와 docs 기준으로 Hankweave는 "coding agent" 자체가 아니다. Claude Code, Codex, Gemini CLI, Pi, OpenCode 같은 기존 harness를 재구현하지 않고 shim으로 호출하며, Hankweave는 orchestration, isolation, state management, event logging을 담당한다.

```text
Developer
  -> hank.json
      -> Hankweave runtime
          -> Codon 1: gather
          -> checkpoint
          -> Codon 2: verify
          -> sentinel observes event stream
          -> checkpoint / rollback
          -> Codon 3: synthesize
```

## 2. Why - 왜 필요한가?

Hankweave의 문제의식은 long-horizon agent가 커질수록 실패 원인이 단순히 "모델이 약해서"가 아니라 **작업 상태와 행동을 사람이 이해하고 고칠 수 없어서**라는 데 있다.

| 문제 | 일반 agent 실행 | Hankweave 접근 |
|------|----------------|----------------|
| Context drift | 긴 대화에 과거 판단과 오류가 누적 | codon boundary와 `continuationMode: "fresh"`로 context firewalling |
| 재현성 부족 | tool call과 중간 산출물이 흩어짐 | structured JSONL event journal, checkpoint |
| 복구 어려움 | 실패 후 어디서 재시작할지 불명확 | Git commit 기반 snapshot, rollback |
| 비용 폭주 | long run 중 token/cost 감시가 약함 | codon budget, runtime `--max-cost`, sentinel |
| 품질 감시 | main agent가 자기 실패를 놓침 | secondary agent인 sentinel이 event stream 관찰 |

Southbridge는 이를 **brownfield AI engineering** 문제로 설명한다. 새 agent를 만드는 것보다 이미 운영 중인 agent workflow를 유지보수, 이관, 개선, 재실행하는 일이 더 어렵다는 관점이다.

## 3. 핵심 개념

| 개념 | English | 설명 |
|------|---------|------|
| Hank | Declarative AI program | `hank.json`에 정의되는 workflow. codon sequence, model, prompt, context flow, requirement, override를 담는다. |
| Codon | Agent task unit | 하나의 agent 작업 단위. prompt, model, tracked files, rig setup, output files, failure policy, budget, sentinel 설정을 캡슐화한다. |
| Context firewalling | Controlled forgetting | codon 간 context를 분리하고 필요한 handoff만 file로 명시한다. |
| Checkpoint | Snapshot | codon 완료 시 Git commit 기반 snapshot을 만들어 rollback/resume 기준점을 제공한다. |
| Sentinel | Observer agent | main agent와 별도로 event stream을 관찰해 drift, convention violation, cost spike, missing citation 등을 감지한다. |
| Harness abstraction | Shim layer | Claude Code, Codex, Gemini CLI 같은 harness를 직접 재구현하지 않고 실행·관찰 가능한 primitive로 다룬다. |

## 4. 핵심 특징

### Declarative workflow

`hank.json`은 agent workflow를 코드 안의 ad hoc loop가 아니라 선언적 program으로 만든다. 실행 순서, prompt, model, file boundary, output, budget, requirements가 문서화된 실행 단위가 된다.

```json
{
  "codons": [
    {
      "id": "gather",
      "prompt": "prompts/gather.md",
      "continuationMode": "fresh",
      "outputFiles": ["work/gather.md"],
      "budget": { "maxDollars": 2.0 }
    }
  ]
}
```

### Context firewalling

`continuationMode: "fresh"`는 이전 codon의 대화 context를 그대로 이어받지 않는다. 필요한 handoff는 file로 남기고 다음 codon이 그 file을 읽게 한다. 이는 agent가 "잊어야 할 것"을 통제하는 context engineering 패턴이다.

### Checkpoint와 rollback

codon 완료 시점에 checkpoint를 만들면, 긴 workflow가 중간에 실패해도 특정 지점으로 돌아갈 수 있다. Hankweave는 Git commit 기반 snapshot을 repairability의 핵심 primitive로 사용한다.

### Sentinel

Sentinel은 main agent가 아니라 event stream을 보는 secondary agent다. 예를 들어 citation이 빠졌는지, 비용이 급증했는지, style convention을 어겼는지, 작업 목표에서 drift가 생겼는지를 별도 관찰자로 기록한다.

### Preflight validation

Hankweave는 token을 쓰기 전에 API key, model availability, file path, rig config, sentinel schema 같은 조건을 검사한다. long run에서 초반 설정 오류로 비용을 낭비하지 않기 위한 장치다.

### Runtime/infra

- WebSocket packet stream
- structured JSONL event journal
- LLM proxy
- workspace isolation
- read-only data mounting
- isolated execution directory
- budget enforcement
- Docker/CI execution

## 5. 장점과 한계

| 장점 | 설명 |
|------|------|
| Repairability | 실패한 agent workflow를 codon/checkpoint/event 단위로 조사하고 수리할 수 있다. |
| Harness reuse | Claude Code, Codex, Gemini CLI 등 기존 harness를 그대로 활용한다. |
| Reproducibility | file handoff, checkpoint, event journal로 long run을 추적한다. |
| Cost control | codon budget과 runtime budget guardrail을 둔다. |
| 운영 친화성 | headless, Docker, CI, volume 기반 execution state 관리가 가능하다. |

| 한계/주의점 | 설명 |
|-------------|------|
| Alpha maturity | 2026-06-24 기준 `release/alpha` package metadata가 `0.6.2`를 표시한다. 운영 도입 전 API churn을 감안해야 한다. |
| Harness 의존 | 실제 agent 능력과 tool behavior는 호출되는 harness에 크게 의존한다. |
| Workflow 설계 비용 | codon boundary, handoff files, sentinel schema를 설계해야 한다. |
| Git 기반 checkpoint | repo 상태 관리와 generated artifact 정책을 명확히 해야 한다. |

## 관련 노트

- [[study/tech/ai/agent-orchestration]] - agent workflow runtime의 큰 맥락
- [[study/tech/ai/lazy-codex]] - harness 실행과 검증 루프 관점 비교
- [[study/tech/ai/codex]] - Hankweave가 호출할 수 있는 coding agent harness

## References

- [Southbridge Hankweave 공식 소개](https://www.southbridge.ai/hankweave)
- [Hankweave Documentation](https://hankweave.southbridge.ai/)
- [Hanks concept](https://hankweave.southbridge.ai/concepts/hanks/)
- [Codons concept](https://hankweave.southbridge.ai/concepts/codons/)
- [Sentinels concept](https://hankweave.southbridge.ai/concepts/sentinels/)
