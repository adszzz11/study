---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 사내 tutorial → Runbook 변환기

교육 영상을 timestamp 기반 SOP, FAQ, verification checklist로 변환한다. 접근 제어와 retention policy를 설계하고, 초안은 담당자가 승인한다.

## UI 구현 패턴 라이브러리

디자인 tutorial에서 component 구조, CSS token, interaction evidence를 추출해 팀 Skill로 배포한다. pixel-level 일치를 주장하기보다 fixture와 visual regression 기준을 정한다.

## DevOps 교육 재현 Agent

설치·배포 영상에서 command, output, rollback을 분리한다. production 명령은 실행하지 않고 sandbox/dry-run evidence와 승인 gate를 둔다.

## Research-to-implementation pipeline

공개 conference talk·demo를 분석하여 재현 repo, fixture, benchmark를 만든다. 발표자의 주장과 실제 demo 관찰을 구분해 기록한다.

## Video QA Agent

product demo의 transcript와 frame을 검사해 누락된 안내, 잘못된 화면, 민감정보 노출 후보를 찾는다. 탐지는 human review queue로 전달한다.

기획 전 [[tech/ai/video-to-skill-pipeline/02-ecosystem|Ecosystem]]을 비교하고, 구현 전 [[tech/ai/video-to-skill-pipeline/04-learning/02-deep-dive|심화]]의 안전 경계를 적용한다.

## Sources

- https://support.claude.com/en/articles/12512176-what-are-skills
- https://claude.com/marketplace/plugins
- https://ai.google.dev/gemini-api/docs/video-understanding?hl=en
