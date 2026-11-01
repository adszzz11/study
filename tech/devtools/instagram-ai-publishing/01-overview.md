---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview

[[tech/devtools/instagram-ai-publishing/README|README]]로 돌아가기.

## What

Instagram Agent Skill은 Claude Code에서 콘텐츠 조사와 초안 생성을 돕는 MIT Skill bundle이다. `ig-viral`, `ig-reel`, `ig-caption`, `ig-plan` 같은 작업으로 swipe file, 대본, caption, 콘텐츠 캘린더를 만든다. 실제 게시 권한은 갖지 않는다.

Uplika MCP는 OAuth 2.1 + PKCE로 account를 연결해 Instagram, YouTube, Threads 등에 draft, 예약, 발행, insight 조회를 수행하는 remote service다.

## Why

좋은 문장을 만드는 것만으로는 운영 품질이 보장되지 않는다. 계정 고유 voice, 경쟁 콘텐츠의 상대 성과, 채널별 media 제약, 되돌릴 수 없는 게시 직전 검토를 함께 다뤄야 한다. 두 층을 분리하면 콘텐츠 생성과 권한 위임을 독립적으로 통제할 수 있다.

## 핵심 특징

- **상대 성과 비교**: `ig-viral`은 raw views 대신 `views ÷ 최근 median views`인 outlier multiple을 쓴다. 3x 이상은 조사 신호이며, 절대적 성공 판정은 아니다.
- **구조화된 대본**: `ig-reel`은 26개 hook formula, hook score, timed beat sheet, on-screen text를 구성한다.
- **local-first drafting**: scraping이나 자동 브라우징을 기본으로 하지 않고, 사람이 관찰한 경쟁 Reel 입력을 활용한다.
- **approval gate**: account, media, caption, channel, 예약 시각을 보여 준 뒤 명시적 승인을 받아야 한다.

## Architecture

```text
Saved Reels / 수동 관찰
        ↓
ig-viral → outlier multiple swipe file
        ↓
ig-reel · ig-caption · ig-plan → voice.md + local lint
        ↓
사람 검토 및 승인
        ↓
Uplika MCP (OAuth 2.1 + PKCE)
        ↓
draft / scheduledAt / publish → Instagram · YouTube · Threads
        ↓
get_post · get_insights · retry_post
```

## Sources

- https://github.com/Jakeschincariol/instagram-agent-skill
- https://github.com/Jakeschincariol/instagram-agent-skill/blob/main/skills/ig-viral/SKILL.md
- https://uplika.com/en/docs
