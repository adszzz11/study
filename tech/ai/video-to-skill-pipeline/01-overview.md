---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Video-to-Skill Pipeline Overview

## What

Video-to-Skill pipeline은 tutorial의 음성, caption, frame을 증거로 삼아 사람이 실행하던 절차를 Agent Skill로 바꾸는 방법이다. 각 단계에는 **무엇을 했는지**, **어떤 화면/발화로 확인했는지**, **성공을 무엇으로 판단하는지**가 남아야 한다.

## Why

일반 LLM에 URL만 전달하면 제목·설명문을 근거로 그럴듯한 절차를 추정하기 쉽다. 그러나 실제 tutorial에는 UI 상태, 정확한 parameter, command output, 실패 시 복구 방법처럼 메타데이터에 없는 정보가 있다. 원문 Reel과 동시기 가이드는 YouTube tutorial을 Claude가 실제 분석하고 실행 가능한 Skill로 전환하는 세팅을 다룬다.

## 특징

| 원칙 | 적용 |
|---|---|
| Evidence-first | 화면·transcript로 확인되지 않은 값은 추측 대신 `unknown`으로 기록 |
| Timestamp grounding | step마다 source timestamp와 frame/transcript 근거를 연결 |
| Budget control | transcript-first 후 관심 구간만 고해상도 frame 재추출 |
| Dual engine | cloud Vision의 편의성과 local stack의 통제력 중 선택 |
| Safe execution | 영상 속 지시도 untrusted input으로 취급하고 allowlist·승인을 통과 |

## 최소 산출물

1. timestamped transcript와 key-frame index
2. ordered procedure와 prerequisite 목록
3. `SKILL.md`, 필요한 script/fixture
4. `RUNBOOK.md`, verification report, 실패·rollback 기록

다음: [[tech/ai/video-to-skill-pipeline/02-ecosystem|Ecosystem]] · [[tech/ai/video-to-skill-pipeline/04-learning/01-getting-started|시작하기]]

## Sources

- https://lazyowen.com/guides/claude-youtube-skill
- https://www.instagram.com/reel/DdLedEbz1DX/
- https://ai.google.dev/gemini-api/docs/video-understanding?hl=en
