---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# Aside - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 1. QA smoke test agent

Local web app을 열고 주요 화면을 탐색한다.

```bash
aside "Open localhost:3000 and run a smoke test"
```

| 항목 | 설계 |
|------|------|
| Mode | `Guard` 또는 local 환경 한정 `Full access` |
| Input | local URL, test account, 금지 action |
| Output | screenshot, issue list, reproduction step |
| Approval | destructive test data 변경 전 확인 |

Prompt 예시:

```text
Open localhost:3000 and run a smoke test for login, dashboard, and settings.
Save screenshots and a markdown issue report under ./artifacts/smoke-test.
Do not delete data or change billing settings without asking.
```

---

## 2. Vendor research

Ultrabrowse로 pricing, SOC2/security docs, API docs를 citation 포함 비교한다.

| 항목 | 설계 |
|------|------|
| Mode | `Read only` |
| Input | vendor list, 비교 기준, required citations |
| Output | comparison table, source links, risk note |
| Approval | 불필요. 단, account signup이나 contact form 제출은 금지 |

```text
Use Ultrabrowse to compare Vendor A, Vendor B, and Vendor C.
Focus on pricing, SOC2/security docs, API limits, and enterprise features.
Return a citation-heavy markdown table and note any missing evidence.
```

---

## 3. Back-office automation

Payroll, invoice portal, CRM, support dashboard에서 파일 다운로드, 요약, draft 생성을 수행한다.

| 업무 | 예 |
|------|----|
| Payroll | paystub PDF 다운로드, 월별 폴더 정리 |
| Invoice portal | invoice PDF 다운로드, total amount CSV 생성 |
| CRM | account page 확인, renewal note draft |
| Support dashboard | high-priority ticket 요약, response draft |

권장 rule:

```text
Ask before sending messages, changing ticket status, submitting forms,
updating payroll settings, deleting files, or using payment autofill.
```

---

## 4. Hiring workflow

Candidate page, calendar, email, ATS를 오가며 interview notes와 follow-up draft를 만든다.

| 단계 | Aside task |
|------|------------|
| Candidate review | ATS profile과 resume 확인 |
| Calendar check | interview schedule 확인 |
| Notes | interview notes markdown 작성 |
| Follow-up | email draft 생성, 전송 전 approval |

산출물:

```text
artifacts/hiring/
├── candidate-summary.md
├── interview-notes.md
└── follow-up-draft.md
```

---

## 5. Recurring ops

Cron routine 또는 heartbeat routine으로 반복 업무를 실행한다.

| Routine | 예 | Artifact |
|---------|----|----------|
| Weekly dashboard summary | 매주 월요일 KPI dashboard 요약 | `weekly-summary.md` |
| Ongoing vendor watch | 가격/보안 문서 변경 확인 | `vendor-watch.md` |
| Support health check | high-priority queue 확인 | `support-health.md` |
| Compliance research | SOC2/security page 주기적 재확인 | `compliance-notes.md` |

Routine 설계 템플릿:

```text
Trigger:
Scope:
Allowed sites:
Working folder:
Approval gates:
Output artifact:
Failure / wait behavior:
```

---

## 프로젝트 선택 기준

| 상황 | 추천 프로젝트 |
|------|---------------|
| 개발자 | QA smoke test agent |
| 구매/보안 검토 | Vendor research |
| 운영팀 | Back-office automation |
| People team | Hiring workflow |
| 반복 보고 | Recurring ops |

## 관련 노트

- [[../agent-orchestration/README|Agent orchestration]] - 반복 agent task 운영
- [[../../devtools/qa/danal-auto-testing-tool|Auto testing tool]] - QA 자동화 관점
- [[../llm-wiki-study/README|LLM wiki study]] - artifact를 지식 노트로 축적하는 방식
