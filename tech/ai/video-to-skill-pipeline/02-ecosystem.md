---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem Comparison

| 선택지 | 분석 방식 | 강점 | 주의점 / 적합한 경우 |
|---|---|---|---|
| `bradautomates/claude-video` Watch | Gemini 또는 local frame + caption/STT | Claude Code plugin 및 Agent Skill 설치 경로, focused analysis | third-party source review와 version pin 필요 |
| Gemini API Video Understanding | Files API, Cloud Storage, inline data, YouTube URL | multimodal 질의와 timestamp 근거, API 확장성 | upload·보관 정책과 비용 검토 필요 |
| `yt-dlp` + FFmpeg + Whisper custom | download/caption, frame extraction, STT 조합 | 데이터·모델·보존기간 통제, lock-in 최소화 | 구현·운영 부담이 큼 |
| Claude Skills/Plugins | workflow와 tool bundle 배포 | 팀 규칙과 검증 코드를 함께 배포 | marketplace plugin을 supply-chain으로 관리 |
| Notebook/문서 요약 | transcript·메모 중심 | 빠른 학습 노트 | UI 상태와 재현 절차 추출에는 약함 |

## 선택 기준

- 민감한 영상 또는 장기 보관 통제가 필요하면 local engine을 우선 검토한다.
- 빠른 discovery와 timestamp Q&A가 목표면 managed video API가 편리하다.
- 재사용 실행이 목표면 어느 engine이든 Skill contract와 sandbox test가 필수다.

`claude-video`의 focused interval, frame cap, detail 옵션은 긴 영상을 전체 frame으로 보내지 않도록 돕는다. provider가 달라도 evidence schema와 approval gate는 유지한다.

다음: [[tech/ai/video-to-skill-pipeline/03-references|References]] · [[tech/ai/video-to-skill-pipeline/04-learning/02-deep-dive|심화]]

## Sources

- https://github.com/bradautomates/claude-video
- https://github.com/bradautomates/claude-video/blob/main/README.md
- https://ai.google.dev/gemini-api/docs/video-understanding?hl=en
- https://github.com/yt-dlp/yt-dlp/blob/master/README.md
- https://claude.com/marketplace/plugins
