---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-video

> **한 줄 정의**: Claude-video는 별도 Anthropic video model이 아니라, 영상 URL 또는 local file을 timestamped frames와 transcript로 변환해 Claude Code 같은 Agent가 근거 기반으로 분석하게 하는 오픈소스 Agent Skill이다.

## Overview

Claude의 image vision과 video-native input은 구분해야 한다. Claude-video는 영상을 재생해 이해시키는 대신 `yt-dlp`, `ffmpeg`, Whisper를 조합해 Claude가 읽을 수 있는 multimodal context를 만든다.

```text
video URL / local file + question
  → captions 또는 download
  → frames + timestamped transcript
  → Claude Vision / Read
  → timestamp evidence를 포함한 answer
```

- captions-first라면 빠르고 저렴하지만 화면 변화는 알 수 없다.
- 시각 질문에는 시간 구간을 좁히고 `balanced` sampling을 우선 사용한다.
- 긴 영상은 전체 요약 후 후보 timestamp를 찾고, 해당 구간을 재분석하는 two-pass pattern이 안전하다.

## Learning Path

- [ ] [[01-overview|What/Why와 제약]]: sampling-based reconstruction임을 이해한다.
- [ ] [[04-learning/01-getting-started|Getting Started]]: 짧은 공개 captioned 영상으로 `/watch`를 실행한다.
- [ ] [[04-learning/02-deep-dive|Deep Dive]]: sampling mode, transcript fallback, 비용 제어를 실습한다.
- [ ] [[02-ecosystem|Ecosystem]]: native video input 및 MCP 대안과 경계를 비교한다.
- [ ] [[05-projects|Projects]]: bug triage 또는 video QA/RAG의 작은 prototype을 만든다.
- [ ] [[cheatsheet|Cheatsheet]]: 구간·해상도·mode 선택을 빠르게 참조한다.

## When To Use

- screen recording의 오류 timestamp와 재현 단계를 구조화할 때
- 강의·웨비나·제품 demo에서 화면과 발화를 함께 인용할 때
- 광고·launch 영상의 hook, CTA, 화면 구성을 timestamp 증거와 비교할 때
- Claude Code workflow에서 즉시 video-analysis 도구를 붙이고 싶을 때

## When Not To Use

- 프레임 사이의 단발 이벤트나 빠른 동작을 누락 없이 판정해야 할 때
- 사내 영상의 다운로드·보관·외부 STT 전송이 정책상 허용되지 않을 때
- 대량 영상을 반복 처리하는 product backend가 필요하고 Gemini의 native video input이 더 적합할 때
- 저작권·서비스 약관상 원본 다운로드 권한이 불명확할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/claude/05-skills|Claude Skills]]

## Sources

- https://github.com/bradautomates/claude-video
- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
- https://platform.claude.com/docs/en/build-with-claude/vision
- https://ai.google.dev/gemini-api/docs/video-understanding
