---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Evidence, Sampling, and Cost

## Evidence Model

Claude-video의 output은 원본 video가 아니다. 선택된 JPEG frame과 timestamped transcript의 조합이며, 답변 품질은 어떤 frame·구간을 context에 넣었는지에 크게 좌우된다.

```text
wide video
  → first pass: transcript / efficient로 topic·timestamp 후보 찾기
  → narrow window: balanced로 시각 evidence 재수집
  → answer: timestamp + transcript + visible state를 함께 인용
```

## Sampling Controls

| Control | 효과 | 권장 사용 |
|---|---|---|
| `--start`, `--end` | 분석 window 축소 | 화면 질문·긴 영상에 항상 우선 적용 |
| `--timestamps` | 알고 있는 후보 시점 주변 집중 | bug report, chapter, 특정 event 검증 |
| `--resolution` | frame detail과 image token의 균형 | 작은 UI text에는 높이고, 요약에는 낮춤 |
| `efficient` | 최대 50 frames의 빠른 탐색 | 첫 pass 또는 transcript 보조 |
| `balanced` | 최대 100 frames의 scene-aware 분석 | 기본 선택, UI/slide 흐름 분석 |
| `token-burner` | visual coverage 확장 | 좁힌 구간에서만, 비용 허용 시 |

실제 지원 flag와 default는 release에 따라 바뀔 수 있으므로 실행 시 Skill contract를 기준으로 한다.

## Transcript Fallback

1. native caption이 있으면 이를 먼저 사용한다.
2. 없으면 media에서 mono 16 kHz audio를 추출한다.
3. Groq `whisper-large-v3` 또는 OpenAI `whisper-1`로 timestamped transcript를 만든다.

fallback의 비용은 STT 요청뿐 아니라 audio가 외부 provider에 전송되는 위험까지 포함한다. provider, retention, 지역, 비밀정보 포함 여부를 확인하지 못하면 local-only 또는 captions-only 경로를 선택한다.

## Failure Modes

| 증상 | 가능한 원인 | 대응 |
|---|---|---|
| 중요한 UI 상태가 답에 없음 | sampling 사이 event 또는 duplicate removal | window를 좁히고 `balanced`/`token-burner`로 재실행 |
| 발화 내용이 틀림 | caption 품질 저하 또는 STT 오인식 | 원본 audio와 timestamp를 사람이 검증 |
| 비용·latency 과다 | 긴 구간, 높은 resolution, 많은 frames | two-pass pattern과 windowing 적용 |
| 접근/다운로드 실패 | URL 권한, 플랫폼 정책, `yt-dlp` 제약 | 권한을 확인하고 허용된 source만 사용 |

## Sources

- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
- https://console.groq.com/docs/speech-to-text
- https://developers.openai.com/api/docs/guides/speech-to-text
