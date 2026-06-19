---
date: 2026-06-19
tags:
  - tech
  - devtools
  - ai
  - coding-agent
  - deep-dive
type: tech-tool-study
parent: "[[../README]]"
---

# 딥다이브 - Agentic Coding Workflow 설계

> [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

---

## 핵심 질문

AI coding agent의 품질은 모델 성능만으로 결정되지 않는다. 실무에서는 다음 네 가지 설계가 더 중요해진다.

| 설계 축 | 질문 |
|---------|------|
| Context | agent가 어떤 repo 지식을 갖고 시작하는가? |
| Permission | agent가 무엇을 읽고, 쓰고, 실행할 수 있는가? |
| Verification | 어떤 명령으로 성공을 판정하는가? |
| Handoff | 결과를 commit/PR/review로 어떻게 넘기는가? |

---

## 1. Context 설계

Agent에게 필요한 context는 “많을수록 좋다”가 아니라 “작업에 맞게 신뢰할 수 있어야 한다”에 가깝다.

| Context | 좋은 예 |
|---------|---------|
| Build command | `npm test`, `pnpm lint`, `go test ./...` |
| Architecture rule | domain layer는 infra layer를 import하지 않음 |
| Test convention | `*.test.ts`, Given/When/Then, fixture 위치 |
| Review rule | behavior change에는 regression test 필요 |
| Safety rule | migration은 dry-run 먼저 실행 |

`AGENTS.md`나 `CLAUDE.md`에는 변하지 않는 팀 규칙을 넣고, ticket prompt에는 이번 작업의 구체 조건을 넣는다.

---

## 2. Permission 설계

권한은 agent 성능과 안전성을 동시에 좌우한다.

| 권한 | 기본 정책 |
|------|-----------|
| Read files | repo 내부는 허용 |
| Write files | task 범위 또는 workspace로 제한 |
| Shell command | test/lint/build 중심으로 허용 |
| Network | dependency install, docs lookup은 승인 기반 |
| Secret | 기본 차단 |
| Destructive command | 명시 승인 없이는 금지 |

금지 예시:

```bash
rm -rf
git reset --hard
git push --force
DROP DATABASE
```

---

## 3. Verification 설계

검증은 agent workflow의 중심이다.

```text
Patch quality = Change correctness + Verification evidence + Reviewability
```

| 변경 유형 | 최소 검증 |
|----------|-----------|
| 문서 수정 | link/path 확인, markdown lint 가능하면 실행 |
| pure function | 관련 unit test |
| API behavior | unit + integration test |
| UI 변경 | screenshot 또는 browser check |
| dependency migration | full test + build + CI |
| security fix | regression test + abuse case |

Agent에게 “테스트 돌려줘”라고만 하지 말고, 어떤 테스트를 먼저 실행하고 실패 시 어떻게 좁힐지 요구한다.

---

## 4. Prompt Pattern

### Plan-only

```text
먼저 파일을 수정하지 말고 관련 파일을 탐색해줘.
영향 범위, 변경 후보, test plan, 위험 요소만 정리해줘.
```

### Scoped Patch

```text
제안한 plan 중 1번만 구현해줘.
관련 없는 refactor는 하지 말고, 변경 후 가장 작은 검증 명령을 실행해줘.
```

### Failure Loop

```text
방금 실패한 테스트 로그를 기준으로 원인을 좁혀줘.
추측으로 넓은 수정하지 말고, 실패를 재현하는 최소 변경부터 진행해줘.
```

### Review Mode

```text
이 diff를 code review 관점으로 봐줘.
버그, edge case, missing test, 보안 위험을 우선순위 순으로 지적해줘.
```

---

## 5. Extensibility

AI coding agent는 외부 시스템과 연결될수록 workflow 자동화 범위가 넓어진다.

| 확장 | 사용 예 |
|------|---------|
| MCP | Jira ticket, GitHub issue, internal docs 검색 |
| Hooks | format, policy check, prompt guard |
| Skills/plugins | 반복 workflow 패키징 |
| CI/CD | failing job 기반 patch 생성 |
| Browser tools | UI regression, screenshot verification |

관련 학습은 [[study/tech/ai/model-context-protocol-mcp]]와 [[study/tech/ai/claude/05-skills]]를 같이 보면 좋다.

---

## 6. 운영 원칙

- 작은 단위의 issue로 agent에게 맡긴다.
- 먼저 plan을 받고, 그 다음 patch를 요청한다.
- 검증 명령을 project instruction에 명시한다.
- 권한은 기본 차단, 필요한 것만 열어준다.
- PR에는 agent가 한 일과 사람이 확인한 일을 구분해 기록한다.

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent 운영 관점
- [[study/tech/ai/claude/08-subagents]] - subagent와 역할 분리
- [[study/tech/ai/thin-harness-fat-skills]] - skill 중심 자동화 설계
