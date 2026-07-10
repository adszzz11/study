---
date: 2026-06-23
tags: [tech, ai, agent-harness, ecosystem, comparison]
status: learning
type: tech-tool-study
---

# 02. Ecosystem — Loop / Harness 관점 비교

## 1. 큰 분류

| 영역 | 대표 도구/프레임워크 | loop/harness 관점 | 적합한 상황 |
|---|---|---|---|
| Coding agent | OpenAI Codex | 코드 작성, 리뷰, 디버깅, 반복 workflow 자동화 | repo 유지보수, feature 구현, PR 자동화 |
| Coding agent | Claude Code | `/loop`, Routines, hooks, skills, subagents, MCP | 장시간 자동화, agent team, scheduled task |
| Agent runtime | LangGraph | durable execution, human-in-the-loop, persistence | 직접 agent runtime 구축 |
| Agent framework | OpenAI Agents SDK | orchestration, tools, approvals, state를 app이 소유 | 제품 내 agent 기능 구현 |
| Context/tool standard | MCP | 외부 DB, SaaS, 파일, workflow 연결 | tool ecosystem 표준화 |
| Repo instruction | AGENTS.md | build/test/style/security 지침을 agent가 읽게 함 | 여러 coding agent 공통 설정 |
| Benchmark | SWE-bench | real GitHub issue 해결률 평가 | software engineering agent 비교 |
| Benchmark | Terminal-Bench | terminal 환경 장기 task 평가 | CLI/tool-use 능력 측정 |
| Eval loop | OpenAI Evals / Promptfoo / LangSmith | regression, rubric, judge, trace 기반 평가 | harness 개선 검증 |

## 2. Prompt engineering vs Loop engineering vs Harness engineering

| 구분 | 초점 | 예시 | 한계 |
|------|------|------|------|
| `prompt engineering` | 모델에게 무엇을 어떻게 말할지 | "단계별로 생각하고 테스트까지 해줘" | runtime, tool, permission, eval이 없으면 재현성 낮음 |
| `loop engineering` | agent가 어떤 순서로 반복할지 | `plan -> edit -> test -> diagnose -> retry` | loop가 쓸 context/tool/권한이 없으면 취약함 |
| `harness engineering` | loop가 돌아가는 기반을 어떻게 만들지 | `AGENTS.md`, trace, eval gate, tool registry | 구현 부담과 유지보수 비용이 생김 |

좋은 실무 시스템은 셋을 합친다.

```text
prompt = 업무 지시 문장
loop = 반복 업무 절차
harness = 업무 환경, 권한, 도구, 평가, 기록
```

## 3. Coding agent 비교

| 도구 | 강점 | harness 관점의 포인트 | 주의점 |
|------|------|----------------------|--------|
| OpenAI Codex | repo 안에서 파일 읽기, 수정, 명령 실행, 검증 중심 workflow | `instructions`, tools, validation checks, Codex implementation loop와 잘 맞음 | repo별 지침과 테스트 명령을 명확히 줘야 함 |
| Claude Code | `/loop`, Routines, hooks, skills, subagents, MCP가 풍부 | 반복 실행과 장시간 자동화의 제품 기능이 직접 노출됨 | permission과 hook 설계를 잘못하면 과자동화 위험 |
| Cursor / IDE agents | 편집기 문맥과 사람이 함께 보는 UX | human-in-the-loop coding에 자연스러움 | 장시간 unattended loop에는 별도 검증 체계 필요 |
| OpenHands / Devin류 | sandbox, issue-to-PR workflow | 완전한 agent runtime에 가까움 | 비용, 격리, 보안, review gate 설계가 중요 |
| LazyCodex / OmO류 | 검증 agent, durable loop, project memory | false completion을 줄이는 harness 사례 | 자체 규칙이 repo workflow와 충돌하지 않게 조정 필요 |

## 4. Runtime / Framework 비교

| 도구 | 정체성 | loop 기능 | harness 기능 |
|------|--------|-----------|--------------|
| LangGraph | 상태 있는 agent graph runtime | graph node/edge로 반복, 분기, 재시도 설계 | persistence, durable execution, human-in-the-loop |
| OpenAI Agents SDK | agent app framework | tool call, handoff, orchestration | approvals, state, tracing, guardrails를 app에서 구성 |
| MCP | context/tool protocol | loop 자체는 아님 | 외부 tool/resource/prompt를 표준 방식으로 노출 |
| AGENTS.md | repo instruction format | loop 지침을 문서로 제공 | setup/test/style/security/forbidden action을 공통화 |
| Evals / Promptfoo / LangSmith | 평가·관찰 도구 | regression loop와 improvement loop 지원 | trace-based evaluation, judge, rubric, dataset 관리 |

## 5. Benchmark 관점

| Benchmark | 무엇을 보나 | loop/harness와의 관계 |
|-----------|-------------|----------------------|
| SWE-bench | 실제 GitHub issue를 해결하는 능력 | 모델 단독보다 issue 이해, patch 생성, test feedback loop가 중요 |
| Terminal-Bench | 터미널 환경에서 긴 작업을 수행하는 능력 | CLI tool-use, persistence, observation, recovery가 중요 |
| 내부 eval suite | 내 repo의 regression과 업무 규칙 | 실제 배포/merge gate로 쓰기 좋음 |

## 6. 선택 가이드

| 상황 | 추천 접근 |
|------|-----------|
| 개인 repo에 coding agent를 잘 쓰고 싶다 | `AGENTS.md` + 명확한 test command + 변경 보고 양식부터 만든다 |
| 회사 repo에서 agent PR을 받고 싶다 | permission boundary, worktree isolation, eval gate, human review를 먼저 설계한다 |
| 제품 안에 agent 기능을 넣고 싶다 | OpenAI Agents SDK나 LangGraph처럼 state/tools/approval을 app이 소유하는 구조를 쓴다 |
| 여러 SaaS/DB/internal tool을 agent에 연결하고 싶다 | MCP server로 tool/resource를 노출하고 tool registry를 관리한다 |
| agent 성능을 지속 개선하고 싶다 | traces -> failure attribution -> evals -> harness change ranking loop를 만든다 |

## 관련 노트

- [[study/tech/ai/model-context-protocol-mcp]] - MCP는 harness의 tool/context 표준 계층
- [[study/tech/ai/lazy-codex]] - 검증 중심 coding harness 사례
- [[study/tech/ai/litellm]] - model routing과 gateway 관점
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent 생태계
