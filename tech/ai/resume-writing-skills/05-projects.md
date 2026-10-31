---
date: 2026-09-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 이력서 작성 Skills: Projects

> [[README|목차로 돌아가기]]

## 1. Personal Resume Repository

`profile.yaml`을 source-of-truth로 두고 공고마다 JD, requirement matrix, tailored outputs를 분리한다.

```text
resume/
├── profile.yaml
├── evidence.md
├── base-resume.yaml
└── jobs/
    └── company-role/
        ├── jd.md
        ├── match-report.md
        ├── resume.yaml
        └── cover-letter.md
```

**완료 조건**: source 수정 한 번으로 base와 job-specific output의 변경 이유를 diff에서 설명할 수 있다.

## 2. Truth-first Resume Skill

Codex/Claude 호환 `SKILL.md`를 작성한다. mode는 `resume`, `cover-letter`, `interview-star`, `review`로 두고 모든 mode가 evidence gate와 human approval을 공유하게 한다.

**완료 조건**: unsupported metric 또는 role을 입력하면 draft가 이를 claim으로 쓰지 않고 확인 질문에 남긴다.

## 3. ATS Diff Reviewer

base와 tailored Resume를 비교해 added/removed keyword, unsupported claim, repeated buzzword, 너무 긴 bullet을 report한다.

**완료 조건**: score 하나만 출력하지 않고 각 finding에 source 위치와 수정/확인 action을 연결한다.

## 4. Career-coach Batch Workflow

동의한 candidate notes를 15분 flow로 structure화하고, 검증 가능한 bullet 3–5개와 STAR draft를 만든다.

**완료 조건**: consent, data retention, review owner가 기록되고 candidate가 모든 output을 승인한다.

## 5. Versioned PDF Pipeline

YAML → PDF/HTML/PNG render를 local command나 CI로 자동화한다. 비밀값이나 candidate 원문은 public repository에 올리지 않는다.

**완료 조건**: 같은 YAML과 pinned renderer version으로 같은 지원 산출물을 재생성하고 visual check를 통과한다.

## Sources

- https://docs.rendercv.com/user_guide/yaml_input_structure/
- https://learn.chatgpt.com/docs/build-skills
