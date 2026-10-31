---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 이력서 작성 Skills Cheatsheet

> [[README|목차로 돌아가기]]

## Core flow

```text
facts → JD requirements → evidence matrix → tailored draft
      → ATS + human QA → render → applicant approval
```

## Non-negotiable rules

| 규칙 | 적용 |
|---|---|
| Evidence-only | 수치·회사·직책·기간·기술은 candidate source에 있을 때만 사용 |
| Unknown stays unknown | 빈 부분은 `[확인 필요]` 질문으로 남김 |
| No keyword stuffing | JD keyword는 실제 experience와 연결될 때만 포함 |
| Privacy minimum | 주민번호·금융정보·상세 주소 등은 입력 금지 |
| Human owns decision | 제출 전 지원자가 line-by-line 사실성 승인 |

## Requirement matrix

```yaml
- requirement: "API design"
  priority: must_have
  jd_keywords: [REST, Python]
  evidence:
    - experience: "Payment API"
      status: verified
      source: "profile.yaml#payment-api"
  action: include
```

## Bullet patterns

```text
CAR: Challenge → Action → Result
X-Y-Z: Accomplished [X] as measured by [Y], by doing [Z].
```

결과 수치가 없으면 `Y`를 만들어내지 말고 scope·action을 정확하게 쓴다.

## Pre-submit checklist

- [ ] 날짜, 직책, 회사명, link, metric이 사실이다.
- [ ] must-have requirement마다 실제 evidence 또는 의도적인 gap 처리가 있다.
- [ ] unsupported claim·placeholder·내부 비밀정보가 없다.
- [ ] plain-text parsing과 PDF/PNG rendering을 확인했다.
- [ ] 국가·회사별 형식과 upload instruction을 확인했다.
- [ ] 지원자가 최종 version을 승인했다.

## RenderCV quick commands

```bash
rendercv new "Name"
rendercv render Name_CV.yaml
```

## Sources

- https://docs.rendercv.com/user_guide/cli_reference/
- https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03
