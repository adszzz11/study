---
date: 2026-06-09
tags:
  - tech
  - devtools
  - claude
  - dynamic-workflows
  - deep-dive
status: learning
type: tech-tool-study
parent: "[[../README]]"
---

# Claude Dynamic Workflows - 딥다이브

> [[01-getting-started|이전: 시작하기]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. Mental Model

Dynamic Workflows의 핵심은 "Claude가 더 긴 context로 더 오래 생각한다"가 아니라, **task를 실행 가능한 orchestration script로 바꾼다**는 점이다.

```text
Prompt
  -> Claude plans workflow
  -> JavaScript harness stores state
  -> Runtime dispatches subagents
  -> Verifiers challenge results
  -> Synthesizer produces final output
```

| 레이어 | 책임 | 실패 모드 |
|--------|------|-----------|
| Prompt | 목표, scope, budget, stop condition 제공 | 목표 모호, 과도한 scope |
| Workflow script | phase, fan-out, variables, loops 표현 | agent 폭주, incomplete state |
| Runtime | concurrency, UI, control, execution | token 과소/과다 사용 |
| Subagents | 독립 단위 조사/수정/검증 | 중복 작업, shallow finding |
| Synthesizer | 결과 통합, 우선순위화 | 근거 없는 결론, 누락 |

---

## 2. Orchestration Patterns

| Pattern | 설명 | 적합한 작업 |
|---------|------|-------------|
| fan-out-and-synthesize | 여러 subagents가 독립 영역을 조사한 뒤 종합 | repo-wide audit, source review |
| adversarial verification | verifier agents가 finding을 반박하거나 증거를 요구 | security review, migration review |
| generate-and-filter | 많은 후보를 생성하고 기준에 맞는 것만 통과 | test case generation, refactor candidate |
| tournament | 여러 접근을 경쟁시켜 우수안을 선택 | architecture proposal, prompt design |
| loop-until-done | 완료 조건이 만족될 때까지 반복 | migration, flaky test triage |

### Pattern 예시

```text
Goal: migrate deprecated API usage.

Phase 1 discovery:
- fan out by package
- collect callsites with evidence

Phase 2 transformation:
- fan out by file group
- apply minimal patch

Phase 3 verification:
- run tests per worktree/file group
- verifier agents inspect risky diffs

Stop condition:
- no deprecated callsites remain
- all transformed areas have test or reviewer confirmation
```

---

## 3. Prompt 설계 체크리스트

좋은 Dynamic Workflow prompt는 실행 plan을 Claude에게 맡기되, 운영 제약은 명확히 준다.

| 항목 | 포함할 내용 | 예시 |
|------|-------------|------|
| Scope | 대상 path, module, branch | `only inspect src/auth and src/session` |
| Split criteria | 어떻게 나눌지 | `split by route group and middleware` |
| Output schema | 결과 형식 | `file, line, risk, evidence, fix` |
| Verification | 누가 무엇을 검증할지 | `use verifier agents to challenge each finding` |
| Stop condition | 언제 끝낼지 | `stop after all files are checked once and verified` |
| Budget | token/agent/time 제한 | `keep fan-out conservative; prefer smaller models for discovery` |
| Safety | 금지할 행동 | `do not modify files until synthesis is approved` |

```text
use a workflow: Audit packages/api for permission bypasses.

Split by route group. Discovery agents should report only findings with file path,
line evidence, affected role, and exploit scenario. Then run verifier agents that
try to disprove each finding. Synthesize only verifier-confirmed findings.

Do not edit files. Stop when every route group has been checked once and every
reported finding has either verifier-confirmed or verifier-rejected status.
Keep token usage conservative and report agent count by phase.
```

---

## 4. 비용/권한 설계

Dynamic Workflows는 일반 session보다 많은 token을 쓸 수 있으므로 budget과 control plane을 먼저 정해야 한다.

| 리스크 | 원인 | 완화 |
|--------|------|------|
| Token 폭주 | scope 과대, loop condition 모호 | 작은 directory로 시작, stop condition 명시 |
| Agent 과다 실행 | split 기준이 너무 세밀함 | package/route group 단위로 제한 |
| 권한 오용 | subagent가 command/tool을 넓게 사용 | first run approval, managed settings, tool restriction |
| 결과 품질 저하 | verifier 없이 synthesis | adversarial verification 추가 |
| 재사용 workflow 위험 | 저장된 workflow가 repo 변경 후 부적합 | 저장 전 path/권한/budget 검토 |

운영 원칙:

- discovery에는 smaller model routing을 우선 고려한다.
- patch 적용 전에는 report-only workflow로 시작한다.
- `/workflows`에서 phase별 token usage를 계속 본다.
- workflow 저장 전 command와 path assumption을 검토한다.

---

## 5. Skills/Subagents와 조합

Dynamic Workflows는 Skills와 Subagents를 대체하기보다 함께 쓸 때 가치가 커진다.

| 조합 | 사용 방식 |
|------|-----------|
| Workflow + Skill | workflow가 반복 절차를 실행하고, Skill이 domain-specific instruction과 scripts를 제공 |
| Workflow + Subagents | workflow가 orchestration을 맡고, subagents가 researcher/reviewer/migrator 역할 수행 |
| Workflow + Hooks | workflow 전후에 formatting, tests, audit log 같은 자동화를 붙임 |
| Workflow + LLM Wiki | source fan-out, claim extraction, contradiction flagging, wiki synthesis |

관련해서 [[study/tech/ai/thin-harness-fat-skills]]는 "harness는 얇게, reusable knowledge는 skill에 둔다"는 관점으로 읽을 수 있다.

---

## 관련 노트

- [[study/tech/ai/claude/05-skills]]
- [[study/tech/ai/claude/08-subagents]]
- [[study/tech/ai/claude/06-hooks]]
- [[study/tech/ai/llm-wiki-study]]
