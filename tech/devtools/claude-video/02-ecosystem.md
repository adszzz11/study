---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and Alternatives

## Comparison

| 선택지 | 접근 | 강점 | 주의점 |
|---|---|---|---|
| `bradautomates/claude-video` | Skill + Python + `yt-dlp`/`ffmpeg`/Whisper | 단순한 `/watch`, 여러 Agent host 지원, captions-first | sampling 품질과 외부 도구 설치를 검토해야 함 |
| `claude-video-plus` | 원본 fork, question-aware evidence retrieval | 질문 중심으로 context를 줄이는 실험적 확장 | upstream과 별개 프로젝트이며 benchmark 주장은 독립 검증 필요 |
| `claude-video-vision` | MCP Server + TypeScript | local Whisper/Gemini/OpenAI 선택, 구조 분석·cache·drill-down | Node/MCP 운영 복잡도 증가 |
| Gemini API Video Understanding | native video input | File API/YouTube URL, timestamp Q&A, 장영상용 agentic mode | Claude가 아닌 Gemini 모델·플랫폼으로 전환 |
| 직접 구현 | `ffmpeg` + Claude Vision API | data residency, sampling·저장·비용 정책 완전 제어 | ingestion, retries, observability를 직접 구축 |

## Decision Guide

| 요구 | 우선 검토할 선택지 | 이유 |
|---|---|---|
| Claude Code에서 한두 개 영상을 빠르게 분석 | Claude-video | Agent Skill workflow에 직접 연결 |
| 영상 분석을 서비스 backend에서 대량 반복 | Gemini API Video Understanding | native video input과 platform 기능이 더 직접적 |
| local 처리, cache, provider 선택이 중요 | claude-video-vision 또는 직접 구현 | 실행·보관·모델 경계를 세밀하게 제어 |
| 질문별 최소 evidence만 필요 | claude-video-plus | retrieval 중심 실험을 평가할 출발점 |

## Boundary

Gemini의 native video input은 모델이 video를 처리하는 플랫폼 기능이다. 반면 Claude-video는 frames와 transcript라는 재구성된 evidence를 Claude에게 보내는 developer tool이다. 이 차이는 latency, 비용, 누락 위험, data handling 책임이 어디에 있는지를 바꾼다.

## Sources

- https://github.com/bradautomates/claude-video
- https://github.com/abe238/claude-video-plus
- https://github.com/jordanrendric/claude-video-vision
- https://ai.google.dev/gemini-api/docs/video-understanding
