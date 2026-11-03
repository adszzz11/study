---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — Claude Code 기반 LinkedIn workflow

## What

Claude Code를 orchestration layer로 삼아 Markdown context, `SKILL.md`, 허가된 도구 연결을 콘텐츠 운영 절차에 묶는 방식이다. 입력은 주제만이 아니라 `voice.md`, `audience.md`, `proof-points.md`, 기존 우수 게시물과 금지 표현이다.

## Why

단발성 chat은 빠르지만 작성자마다 맥락과 검수 기준이 달라지기 쉽다. 파일 기반 context와 정해진 review contract는 brand voice를 재현하고, 근거 없는 claim과 과장된 CTA를 줄인다. 성과가 좋았던 문장을 정답으로 고정하지 않고, 같은 주제의 여러 angle을 가설로 기록하는 것도 중요하다.

## 핵심 특징

| 구성 | 역할 | 운영 원칙 |
|---|---|---|
| Context repository | 브랜드·제품·고객 근거 보관 | 검증 가능한 source와 금지 표현을 분리 |
| `linkedin-post` Skill | 초안 생성과 검수 출력 표준화 | hook 3개, 초안 2개, claim 목록을 고정 |
| MCP | CRM·문서·analytics의 허가된 연결 | least privilege와 데이터 범위 통제 |
| Approval queue | 외부 게시 전 final gate | 사람 승인 또는 공식 API만 통과 |
| Feedback loop | 다음 brief 개선 | 주간 단위로 가설과 성과를 함께 기록 |

## 안전 경계

LinkedIn은 scraper, browser extension, bot을 이용한 무단 데이터 수집과 메시지·게시·댓글·좋아요의 자동 활동을 제한한다. 따라서 이 노트의 workflow는 **content assistance**를 다루며, 개인 계정 조작이나 대량 engagement 실행은 포함하지 않는다.

## Related Notes

- [[tech/ai/claude-linkedin-workflows/README|README]]
- [[tech/ai/claude-linkedin-workflows/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/skills
- https://ac.linkedin.com/legal/user-agreement
- https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en
