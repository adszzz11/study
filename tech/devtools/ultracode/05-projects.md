---
date: 2026-06-19
tags:
  - tech
  - devtools
  - ai
  - coding-agent
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# 울트라코드 - 실전 프로젝트

> [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 프로젝트 1. Legacy Repo Onboarding

목표: 낯선 repo의 구조와 실행 방법을 agent로 정리한다.

작업:

- architecture map 생성
- 주요 module 설명
- build/test/lint command 확인
- onboarding README 초안 작성

Prompt:

```text
이 repo를 처음 보는 개발자를 위해 onboarding note를 만들어줘.
먼저 파일을 읽고 architecture map, 주요 command, 테스트 위치, 위험한 변경 영역을 정리해줘.
파일 수정은 하지 말고 보고서만 작성해줘.
```

성공 기준:

- 실제 파일 경로 기반 설명
- 실행 가능한 command
- 추측과 확인된 사실 구분

---

## 프로젝트 2. Bug-fix Agent Workflow

목표: issue 입력에서 regression test와 patch까지 연결한다.

흐름:

```text
Issue
  -> reproduce
  -> failing test
  -> minimal patch
  -> passing test
  -> PR summary
```

Prompt:

```text
아래 버그를 먼저 재현하는 테스트를 작성해줘.
테스트가 실패하는 것을 확인한 뒤, 최소 수정으로 통과시키고 관련 테스트를 다시 실행해줘.
```

성공 기준:

- 실패 테스트가 먼저 존재
- patch가 최소 범위
- regression test가 남음

---

## 프로젝트 3. PR Review Bot

목표: changed files 기준으로 bug risk와 missing test를 점검한다.

검토 항목:

| 항목 | 질문 |
|------|------|
| Correctness | 조건 분기와 edge case가 맞는가? |
| Tests | 변경된 behavior를 테스트하는가? |
| Security | auth, validation, injection 위험은 없는가? |
| Performance | 불필요한 loop/query가 생겼는가? |
| Maintainability | 기존 convention을 따르는가? |

Prompt:

```text
이 diff를 review해줘.
칭찬보다 버그, edge case, missing test, 보안 위험을 우선순위 순으로 찾아줘.
각 finding은 파일/라인 근거와 함께 작성해줘.
```

---

## 프로젝트 4. Dependency Migration

목표: library/framework version bump와 breaking change 수정을 agent loop로 처리한다.

작업:

- release note 확인
- dependency bump
- build/test 실패 수집
- breaking change patch
- CI 통과 확인

주의:

- migration은 변경 범위가 커지기 쉽다.
- lockfile 변경을 사람이 확인해야 한다.
- full test와 build가 필요하다.

---

## 프로젝트 5. Internal Dev Assistant

목표: MCP와 내부 도구를 연결해 ticket-to-PR workflow를 만든다.

연결 후보:

- Jira ticket
- Slack thread
- GitHub issue/PR
- internal docs
- design asset
- CI logs

```text
Jira ticket -> related docs -> repo context -> patch -> test -> PR summary
```

성공 기준:

- agent가 외부 context 출처를 명시
- secret과 private data 접근 통제
- PR에 검증 결과 포함

---

## 프로젝트 6. Security Triage

목표: 취약 후보를 찾고 patch PR로 연결한다.

대상:

- auth bypass
- missing input validation
- SQL/command injection
- secret exposure
- unsafe deserialization
- open redirect

Prompt:

```text
auth와 input validation 관점에서 src/api를 audit해줘.
먼저 findings만 우선순위로 정리하고, 수정은 내가 승인한 항목만 진행해줘.
```

---

## 관련 노트

- [[study/tech/devtools/qa/what-is-qa]] - QA 관점의 검증
- [[study/tech/ai/codex/05-projects]] - Codex 실전 workflow
- [[study/tech/ai/model-context-protocol-mcp]] - MCP 기반 internal assistant
