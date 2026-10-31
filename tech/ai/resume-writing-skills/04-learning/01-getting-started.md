---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: 사실에서 첫 draft까지

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

- 경력 사실을 재사용 가능한 source로 구조화한다.
- JD requirement와 evidence를 연결한다.
- unsupported claim 없이 tailored Resume와 Cover Letter 초안을 만든다.

## 1. 최소 fact base 만들기

`candidate.yaml`에는 검증 가능한 사실만 둔다. 민감한 식별정보는 제외한다.

```yaml
basics:
  name: "Applicant Name"
experience:
  - company: "Example Co."
    role: "Backend Engineer"
    dates: "2023-01 — 2025-06"
    projects:
      - name: "Payment API"
        action: "Implemented idempotency keys and monitoring"
        result: "Reduced duplicate-payment incidents by 40%"
        tech: [Python, PostgreSQL]
        evidence: "https://internal-or-public-evidence.example"
```

위 example의 값은 schema 설명용이다. 실제 수치·결과는 본인이 확인 가능한 source로 교체한다. metric이나 evidence가 없으면 추측해서 쓰지 말고 `needs_confirmation`으로 남긴다.

## 2. JD를 requirement table로 바꾸기

| 우선순위 | requirement | JD 표현 | evidence | 상태 |
|---|---|---|---|---|
| must-have | Python backend | Python, API design | Payment API | matched |
| must-have | 운영 경험 | reliability, monitoring | dashboard/incident record | confirm |
| preferred | Kubernetes | Kubernetes | 없음 | gap |

1. must-have와 preferred를 분리한다.
2. 책임(responsibility), domain language, tool keyword를 기록한다.
3. 각 줄에 최소 하나의 evidence를 붙인다.
4. `gap`은 keyword stuffing으로 메우지 않는다. 관련 경험이 있으면 확인 질문을 만들고, 없으면 제외하거나 학습 계획으로 분리한다.

## 3. Tailoring prompt/Skill 규칙

```text
입력의 candidate facts와 evidence matrix만 사용한다.
source에 없는 수치, 회사명, 직책, 기간, 기술을 생성하지 않는다.
JD의 must-have를 evidence가 강한 순서로 Resume에 배치한다.
근거가 불완전하면 [확인 필요: 질문]으로 표시한다.
출력 전 unsupported claim 목록과 human approval checklist를 함께 낸다.
```

## 4. 첫 산출물 검토

- Resume: standard heading, 한 column의 읽기 순서, JD coverage, 명확한 bullet을 확인한다.
- Cover Letter: Resume bullet을 반복하지 않고 role·company·evidence 연결을 설명한다.
- 둘 다: contact information, 날짜, metric, 기술, link를 지원자가 line-by-line 승인한다.

## Sources

- https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03
- https://github.com/jezweb/claude-skills/blob/main/plugins/writing/skills/resume-cover-letter/SKILL.md
