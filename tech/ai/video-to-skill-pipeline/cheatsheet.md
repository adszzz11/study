---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Video-to-Skill Cheatsheet

## Stack

`Python 3 + yt-dlp + FFmpeg`로 영상·caption·frame을 확보하고, caption이 없으면 Whisper 계열 STT를 사용한다. Gemini Video Understanding 또는 Claude Vision이 timestamp별 시청각 증거를 해석한다. 결과는 `SKILL.md`, 보조 scripts, fixtures, `RUNBOOK.md`, test checklist로 패키징한다. source pinning, 최소 권한, 외부 upload 고지, command approval, 재현 test를 운영 통제로 둔다.

## Pipeline

```text
caption → timestamp index → candidate interval → key frames
→ evidence table → procedure → SKILL.md → sandbox test → approval
```

## Before execution

- [ ] 영상 사용 권한, upload/retention 정책, 민감정보를 확인했다.
- [ ] source/plugin version을 pin했고 script를 검토했다.
- [ ] destructive/network/package command allowlist와 approval owner를 정했다.
- [ ] clean sandbox와 verification command를 준비했다.

## During extraction

- [ ] step마다 timestamp, transcript/frame evidence, expected result를 적는다.
- [ ] 확인되지 않은 parameter는 `unknown`으로 남긴다.
- [ ] transcript-first로 후보를 좁힌 뒤 필요한 frame만 분석한다.

## After execution

- [ ] command, output, screenshot/timestamp, deviation을 `RUNBOOK.md`에 남겼다.
- [ ] fixture와 test가 통과했다.
- [ ] 차이·차단된 지시·승인 대기 항목을 verification report에 분리했다.

관련: [[tech/ai/video-to-skill-pipeline/README|README]] · [[tech/ai/video-to-skill-pipeline/03-references|References]]

## Sources

- https://github.com/yt-dlp/yt-dlp/blob/master/README.md
- https://ai.google.dev/gemini-api/docs/video-understanding?hl=en
- https://github.com/bradautomates/claude-video/blob/main/README.md
