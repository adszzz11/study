---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

[[tech/devtools/instagram-ai-publishing/README|README]] · [[tech/devtools/instagram-ai-publishing/04-learning/02-deep-dive|심화]]

## 주간 콘텐츠 운영 보드

경쟁 콘텐츠 조사 → swipe file → 주 3개 Reel script → 승인된 draft publishing → 주간 insights 요약을 하나의 보드로 연결한다. 콘텐츠마다 주제, hook formula, outlier multiple, 승인자, scheduled time, 결과 URL을 남긴다.

## 브랜드 voice QA pipeline

발행 전 gate에 caption linter, humanizer, 금칙어 검사, AI-generated media label 점검을 둔다. 각 검사는 수정 제안만 만들고, 발행 허용 판단은 사람이 한다.

## Multi-channel launch automation

하나의 short-form video를 Instagram Reel, YouTube Shorts, Threads 문구로 분기한다. media 형식·caption 제한·채널별 `scheduledAt`을 별도 target으로 관리하고, target별 status를 polling한다.

## 성과 기반 content iteration

Reel별 조회·저장·댓글·공유를 hook formula, 길이, CTA와 함께 기록한다. 한 번의 성과를 보편 규칙으로 단정하지 말고, 다음 주에 한 변수씩 재실험한다.

## Sources

- https://uplika.com/en/docs/agent-publish
- https://uplika.com/en/docs/instagram
- https://developers.google.com/youtube/data/reference/rest/v3/videos/insert
