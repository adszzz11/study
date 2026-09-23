---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-video: What, Why, Features

## What

`bradautomates/claude-video`는 Agent Skill 형태의 video-analysis pipeline이다. Claude에 원본 video를 native input으로 전달하는 제품 기능이 아니라, Agent가 얻은 visual·audio evidence를 Claude의 image vision과 text context로 전달한다.

## Why

영상에는 말로 설명되지 않는 UI 상태, 오류 banner, pointer 이동, slide 전환이 있다. transcript만으로는 이 정보를 잃고, 일정 간격의 frame만 뽑으면 중요한 장면을 놓친다. Claude-video는 captions-first와 scene-aware frame extraction을 결합해 이 간극을 줄인다.

## Pipeline

```text
URL 또는 local video + question
  → yt-dlp: native captions 우선, 필요 시 media download
  → ffmpeg: keyframe / scene-change frame extraction
  → transcript: captions 또는 Groq/OpenAI Whisper fallback
  → near-duplicate frame 제거 + frame/token budget
  → timestamped JPEG frames + transcript
  → Claude Read/Vision: evidence-grounded answer
```

## Key Features

| Mode | Frame 전략 | 적합한 질문 | Trade-off |
|---|---|---|---|
| `transcript` | frame을 최소화하고 captions 중심 | 발화 요약, 키워드 탐색 | 화면 변화를 놓침 |
| `efficient` | keyframe 중심, 최대 50 frames | 빠른 탐색 | 장면 사이 이벤트 누락 가능 |
| `balanced` | scene-aware, 최대 100 frames | 일반적인 화면·발화 분석 | 기본보다 비용 증가 |
| `token-burner` | scene frame cap 완화 | 시각적 누락을 줄일 긴 영상 | image token·처리 시간 증가 |

`--start`, `--end`, `--timestamps`는 단순 최적화가 아니라 정확도와 비용을 함께 제어하는 핵심 장치다. 정지 slide나 변화가 적은 screen recording은 near-duplicate removal로 중복 context를 줄인다.

## Limits and Safety

- 결과는 video-native understanding이 아니라 sampling-based reconstruction이다.
- 작은 자막, 빠른 animation, sampling 사이의 한 프레임짜리 이벤트는 놓칠 수 있다.
- captions가 없으면 mono 16 kHz audio를 추출하여 Groq `whisper-large-v3` 또는 OpenAI `whisper-1`에 전사 요청할 수 있다.
- 외부 STT fallback은 음성 데이터 전송을 수반할 수 있으므로 API key, retention, data residency 정책을 먼저 확인한다.
- `yt-dlp` 다운로드 전에는 저작권, 플랫폼 약관, 사내 영상 접근 권한을 검토한다.

## Sources

- https://github.com/bradautomates/claude-video
- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
- https://platform.claude.com/docs/en/build-with-claude/vision
- https://github.com/yt-dlp/yt-dlp
