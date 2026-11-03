---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 영상 튜토리얼을 재실행 가능한 Agent Skill로 전환하는 파이프라인

> **한 줄 정의**: 영상의 자막·프레임·음성을 timestamp 근거와 함께 분석하여, 검증 가능한 `SKILL.md` 기반 Agent workflow로 패키징하는 방식이다.

## Overview

이 pipeline의 산출물은 영상 요약이 아니라 특정 tutorial을 다시 실행하고 결과를 검사할 수 있는 작업 계약이다. `yt-dlp`로 media/caption을 확보하고, caption이 없으면 Whisper 계열 STT를 사용한다. FFmpeg frame, transcript, Vision model의 관찰을 결합해 prerequisites, 명령, expected result, failure/rollback을 추출한 뒤 `SKILL.md`, scripts, fixtures, `RUNBOOK.md`로 고정한다.

```text
Video → caption/STT + key frames → timestamped evidence
      → procedure extraction → SKILL.md + scripts
      → sandbox execution → test → human approval
```

## Learning Path

- [ ] [[tech/ai/video-to-skill-pipeline/01-overview|Overview]] — What/Why와 evidence-first 원칙 이해
- [ ] [[tech/ai/video-to-skill-pipeline/02-ecosystem|Ecosystem]] — managed API, Watch, local stack 비교
- [ ] [[tech/ai/video-to-skill-pipeline/04-learning/01-getting-started|시작하기]] — 짧은 공개 tutorial로 최소 Skill 만들기
- [ ] [[tech/ai/video-to-skill-pipeline/04-learning/02-deep-dive|심화]] — timestamp schema, security, evaluation 설계
- [ ] [[tech/ai/video-to-skill-pipeline/05-projects|Projects]] — 조직의 SOP와 재현 Agent로 확장
- [ ] [[tech/ai/video-to-skill-pipeline/03-references|References]] — 원문·공식 문서와 source를 검토
- [ ] [[tech/ai/video-to-skill-pipeline/cheatsheet|Cheatsheet]] — 실행 전·후 체크리스트 빠른 참조

## When To Use

- UI 조작, 명령 출력, 화면 상태가 결과 검증에 중요한 공개 tutorial
- 팀의 교육 영상에서 timestamp 기반 SOP나 Runbook을 만들 때
- sandbox에서 반복 재현하고 test 통과 여부를 확인할 수 있을 때

## When Not To Use

- 저작권·접근 권한·개인정보 처리 근거가 없는 영상
- 영상만으로 확인할 수 없는 credential, hidden setting, destructive command를 자동화해야 할 때
- 빠른 요약만 필요하고 재현 실행이나 검증 산출물이 필요 없을 때

## Related Notes

- [[MOCs/Index|Index]]
- [[MOCs/AI|AI]]
- [[tech/ai/claude/README|Claude]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol]]

## Sources

- https://www.instagram.com/reel/DdLedEbz1DX/
- https://lazyowen.com/guides/claude-youtube-skill
- https://ai.google.dev/gemini-api/docs/video-understanding?hl=en
- https://github.com/bradautomates/claude-video/blob/main/README.md
