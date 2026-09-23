---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started

## Goal

짧고 공개된 captioned YouTube 영상에서 captions-first 경로를 확인하고, timestamp 범위를 좁힌 질문을 실행한다.

## Preconditions

- Claude-video를 지원하는 Agent Skills host와 해당 Skill 설치 상태
- `ffmpeg`, `yt-dlp` 등 원본 Skill이 요구하는 local dependency
- 공개 영상의 이용·다운로드 권한 확인

설치 방법과 host별 명령은 변경될 수 있으므로 실행 전 [원본 README](https://github.com/bradautomates/claude-video)와 [watch contract](https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md)를 확인한다.

## First Watch

Agent 대화에서 공개 영상 URL과 질문을 제공한다.

```text
/watch <PUBLIC_VIDEO_URL> summarize this video
```

확인할 것:

- caption이 발견되었는가
- 답변에 timestamp 또는 근거가 포함되는가
- 화면 evidence가 필요한 질문과 transcript 질문의 답이 어떻게 다른가

## Ask a Visual Question

화면을 묻는 질문은 구간과 해상도를 명시한다.

```text
/watch <PUBLIC_VIDEO_URL> --start 02:15 --end 02:45 --resolution 1024
At what timestamp does the error state first appear? Describe the visible UI evidence.
```

시간 범위를 30초처럼 작게 설정하면 frame budget을 중요한 장면에 집중시킬 수 있다. 답을 바로 사실로 확정하지 말고, 반환된 timestamp와 frame evidence를 사람이 다시 확인한다.

## Exercise

1. 같은 영상에 `efficient`와 `balanced`를 각각 실행한다.
2. 처리 시간, frame coverage, 답변의 timestamp 근거를 기록한다.
3. 화면 전환이 많은 구간에서 어느 mode가 더 유용했는지 비교한다.

## Safety Check

사내 녹화물은 실행 전에 다음을 확인한다.

- 외부 다운로드와 임시 file 보관 위치가 허용되는가
- captions 부재 시 STT provider로 audio가 전송될 수 있음을 승인받았는가
- API key가 shell history나 note에 기록되지 않는가

## Sources

- https://github.com/bradautomates/claude-video
- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
- https://github.com/yt-dlp/yt-dlp
