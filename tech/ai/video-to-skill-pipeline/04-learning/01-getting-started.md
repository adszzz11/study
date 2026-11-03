---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 최소 재현 Skill

## 목표

2~5분 길이의 공개 tutorial 하나를 골라, caption과 선택 frame을 근거로 sandbox에서 실행할 수 있는 최소 Skill을 만든다. URL의 이용 조건과 download 권한을 먼저 확인한다.

## 절차

1. caption을 먼저 수집하고 timestamp별 procedure 초안을 작성한다.
2. 각 step에 transcript 인용 위치, 화면 증거, expected result를 붙인다.
3. 화면 텍스트·UI 상태가 중요한 구간만 frame을 재분석한다.
4. 확인할 수 없는 값은 `unknown`으로 둔다.
5. 빈 sandbox에서 한 단계씩 실행하고 output과 차이를 기록한다.

## 최소 `SKILL.md` 계약

```md
---
name: reproduce-tutorial
description: Verify and reproduce a tutorial from timestamped evidence.
---

1. Check prerequisites; do not install packages without approval.
2. Execute one step at a time.
3. Record command, output, screenshot/timestamp evidence.
4. Stop on an unverified instruction or destructive action.
5. Produce RUNBOOK.md and a verification report.
```

## 완료 조건

- 설명이 그럴듯한지가 아니라 원본과 같은 산출물이 생성된다.
- test 또는 명시한 verification command가 통과한다.
- 실행하지 않은 지시와 승인 대기 항목이 report에 분리된다.

다음: [[tech/ai/video-to-skill-pipeline/04-learning/02-deep-dive|심화]] · [[tech/ai/video-to-skill-pipeline/05-projects|Projects]]

## Sources

- https://lazyowen.com/guides/claude-youtube-skill
- https://github.com/yt-dlp/yt-dlp/blob/master/README.md
- https://support.claude.com/en/articles/12512176-what-are-skills
