---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-video Cheatsheet

## Mental Model

```text
video ≠ Claude native input
video → captions/audio + sampled frames → Claude context
```

## Prompt Patterns

```text
/watch <URL> summarize this video

/watch <URL> --start 02:15 --end 02:45 --resolution 1024
What visible error state first appears? Cite timestamps.

/watch <LOCAL_FILE> <mode>
List the UI state transitions with timestamped evidence.
```

호스트와 release에 따라 exact syntax와 option은 다를 수 있다. 실행 전 [watch Skill contract](https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md)를 확인한다.

## Mode Selection

| Need | Mode | Remember |
|---|---|---|
| 말 중심의 빠른 요약 | `transcript` | 화면 변화는 확인하지 못함 |
| 빠른 첫 탐색 | `efficient` | 최대 50 frames, 누락 가능 |
| 일반적인 화면 분석 | `balanced` | scene-aware, 기본 선택 |
| 좁은 구간의 시각 누락 최소화 | `token-burner` | 비용과 token 증가 |

## Reliable Workflow

1. 전체 영상에는 `transcript` 또는 `efficient`로 topic와 timestamp 후보를 찾는다.
2. `--start`와 `--end`로 15–60초 구간을 자른다.
3. `balanced`로 다시 분석하고, 답변에 timestamp와 visible evidence를 요구한다.
4. 중요 판단은 원본 video에서 사람이 교차 검증한다.

## Guardrails

- API key나 private URL을 prompt, shell history, note에 남기지 않는다.
- caption 부재 시 Groq/OpenAI Whisper로 audio가 전송될 수 있다.
- `yt-dlp` download 전에 license, 약관, 접근 권한을 확인한다.
- 빠른 motion·작은 text·한 프레임 event는 sampling에서 빠질 수 있다.

## Technology Stack

Claude-video는 Python 기반 Agent Skill이며 `yt-dlp`로 영상·자막을 확보하고 `ffmpeg`로 frame·audio를 추출한다. Caption을 우선 사용하고, 부재 시 Groq 또는 OpenAI Whisper가 timestamped transcript를 만든다. Claude에 전달되는 것은 원본 video가 아니라 선택·중복 제거된 이미지와 전사문이므로 비용과 정확도는 sampling/windowing 설계에 좌우된다. Codex 등 Agent Skills host에도 이식할 수 있지만 외부 download, STT 전송, local execution 권한의 보안 검토가 필요하다.

## Sources

- https://github.com/bradautomates/claude-video
- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
- https://console.groq.com/docs/speech-to-text
- https://developers.openai.com/api/docs/guides/speech-to-text
