---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 이력서 작성 Skills: Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

이력서 작성 Skill은 `SKILL.md`의 instructions와 선택적 `references/`, `scripts/`, `assets/`로 구성하는 Agent Skill이다. 후보자 사실 데이터와 Job Description(JD)을 입력으로 받아 Resume/CV, Cover Letter, interview STAR answer를 만들되, 근거 없는 claim은 차단하거나 질문으로 바꾼다.

## Why

일반적인 “이력서 써줘” prompt는 공고별 keyword 우선순위를 잃기 쉽고, 그럴듯한 수치나 책임을 만들어낼 위험이 있다. 결과물도 Resume, Cover Letter, PDF가 분리되어 변경 이유와 version을 추적하기 어렵다.

Skill workflow는 다음을 명시적으로 분리한다.

1. **Fact base**: 역할·회사·기간·행동·성과·기술·근거 URL을 기록한다.
2. **Requirement extraction**: JD의 must-have, preferred, responsibility, domain keyword를 구조화한다.
3. **Evidence mapping**: requirement마다 실제 evidence를 최소 하나 연결한다.
4. **Tailoring**: evidence가 있는 경험만 재배열·요약한다.
5. **QA와 승인**: truth, metrics, ATS, regional format, privacy를 점검하고 지원자가 승인한다.

## 핵심 특징

| 특징 | 실무 의미 |
|---|---|
| Portable packaging | `name`·`description`으로 discovery하고 상세 instructions는 Skill 선택 뒤 로드한다. |
| Structured source of truth | 공고마다 원본 경력을 복제하지 않고 YAML/Markdown source를 유지한다. |
| Evidence gate | source 밖의 숫자·회사명·직책·기간·기술을 쓰지 않는다. |
| JD-aware tailoring | JD 표현을 그대로 복사하지 않고 실제 경험과 연결한다. |
| Dual QA | ATS의 linear layout/keyword coverage와 recruiter의 명료성을 함께 본다. |
| Rendering 분리 | content와 design을 분리해 같은 source에서 재현 가능한 산출물을 만든다. |

## Reference architecture

```text
profile.yaml ───┐
evidence.md ────┼──→ requirement matrix ──→ tailored content
JD.md ──────────┘                                 │
                                                    ├─ ATS plain-text resume
                                                    ├─ styled PDF/HTML resume
                                                    ├─ cover letter
                                                    └─ STAR drafts
                                                          ↓
                                                human approval / submission
```

## Guardrails

- 주민번호, 금융정보, 상세 주소, 불필요한 신분·건강 정보는 source에도 넣지 않는다.
- “확인 필요”는 빈칸을 그럴듯한 text로 메우는 것보다 좋은 결과다.
- 국가·업계별 Resume/CV 관행은 별도 확인한다. 사진, 생년월일, 주소 요구를 일반화하지 않는다.
- community Skill과 ATS heuristic은 유용한 reference이지만 공식 채용 기준이 아니다.

## Sources

- https://learn.chatgpt.com/docs/build-skills
- https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md
- https://www.anthropic.com/research/skills
- https://academy.openai.com/public/resources/helping-job-seekers-with-chatgpt-2025-12-03
