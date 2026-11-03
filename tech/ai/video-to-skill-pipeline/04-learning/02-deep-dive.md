---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: Evidence, Safety, Evaluation

## Evidence schema

각 procedure step은 최소한 다음 정보를 가져야 한다.

```yaml
step: 3
action: "Run the build command"
timestamp: "00:01:24"
evidence:
  transcript: "..."
  frame: "frames/00-01-24.png"
command: "unknown"
expected_result: "Preview is shown"
confidence: medium
```

`command: unknown`은 실패가 아니다. 화면이나 발화가 증명하지 않는 명령을 model이 채우는 것보다 안전한 결과다.

## Budget-aware analysis

1. transcript를 색인하고 candidate timestamp를 찾는다.
2. 후보 주변의 짧은 interval만 Vision model로 분석한다.
3. UI text나 terminal output이 필요할 때만 resolution/detail을 높인다.
4. evidence와 절차를 분리 저장해 model 재호출을 줄인다.

## Security boundary

caption, frame OCR, 댓글, 영상 속 narration은 모두 untrusted input이다. Agent는 영상의 지시를 policy보다 우선하지 않으며 다음에서 멈춘다.

- package install, credential 입력, 외부 upload
- file overwrite/delete, privilege escalation, network side effect
- allowlist 밖 command 또는 evidence가 없는 parameter

사람 승인 후에만 실행하고, plugin과 script는 version pin 및 source review를 거친다.

## Evaluation

| 검사 | 증거 |
|---|---|
| Procedure fidelity | timestamp/frame과 step의 대응 |
| Reproducibility | clean sandbox에서 같은 결과 생성 |
| Safety | blocked action과 approval log |
| Regression | fixture와 verification command의 반복 통과 |

복습: [[tech/ai/video-to-skill-pipeline/01-overview|Overview]] · 빠른 참조: [[tech/ai/video-to-skill-pipeline/cheatsheet|Cheatsheet]]

## Sources

- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
- https://ai.google.dev/gemini-api/docs/video-understanding?hl=en
- https://claude.com/marketplace/plugins
