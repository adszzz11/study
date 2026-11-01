---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code 기반 Instagram 콘텐츠·발행 자동화 — Instagram Agent Skill + Uplika MCP

> **한 줄 정의**: Claude Code의 local Skill로 Instagram 콘텐츠를 기획·작성·분석하고, Uplika의 OAuth 기반 remote MCP로 사람 검토 후 Instagram·YouTube 등 채널에 발행 또는 예약하는 워크플로우다.

## Overview

이 조합은 하나의 단일 플러그인이 아니다. MIT 오픈소스인 **Instagram Agent Skill**은 Reel, caption, carousel, profile 분석과 콘텐츠 계획을 만드는 local drafting 계층이고, **Uplika**는 실제 발행·예약·성과 조회를 맡는 별도 상용 remote MCP/API 계층이다.

핵심 운영 루프는 `research → draft → human approval → publish → observe`다. AI 초안의 속도는 살리되 계정 voice, 사실성, media 규칙, 게시 시각은 사람이 최종 책임진다. Reel에서 언급된 “MIT · 39종”은 공개 저장소의 설명과 맞지 않는다. 공개 저장소는 **13 skills와 5개 local Python 도구**를 명시하며, Uplika를 하나의 MIT 패키지로 묶어 해석해서는 안 된다.

## Learning Path

- [ ] [[tech/devtools/instagram-ai-publishing/01-overview|Overview]] — 구성요소와 approval-first 아키텍처를 이해한다.
- [ ] [[tech/devtools/instagram-ai-publishing/02-ecosystem|Ecosystem]] — Skill, Uplika, Meta API, 수동 게시의 경계를 비교한다.
- [ ] [[tech/devtools/instagram-ai-publishing/04-learning/01-getting-started|시작하기]] — voice.md와 수동 리서치로 첫 draft를 만든다.
- [ ] [[tech/devtools/instagram-ai-publishing/04-learning/02-deep-dive|심화]] — OAuth scope, scheduling, polling, retry를 설계한다.
- [ ] [[tech/devtools/instagram-ai-publishing/05-projects|Projects]] — 운영 보드와 multi-channel pipeline을 적용한다.
- [ ] [[tech/devtools/instagram-ai-publishing/03-references|References]] — 원문·공식 문서의 주장과 제약을 검증한다.
- [ ] [[tech/devtools/instagram-ai-publishing/cheatsheet|Cheatsheet]] — 발행 전후 체크리스트를 빠르게 확인한다.

## When To Use

- 일정한 브랜드 voice로 Reel/Shorts 초안을 반복 생산하고 싶을 때
- 사람의 최종 승인을 유지하면서 여러 채널에 예약 발행할 때
- 계정 규모가 다른 경쟁 콘텐츠를 outlier multiple로 비교할 때

## When Not To Use

- 미검토 콘텐츠를 자동으로 즉시 게시하려는 경우
- 비공식 scraping 또는 브라우저 조작으로 성과 데이터를 수집하려는 경우
- Meta App 운영과 권한 관리를 직접 감당할 수 있고 multi-channel 계층이 불필요한 경우

## Related Notes

- [[MOCs/Index|Index]]
- [[MOCs/Devtools|Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]
- [[tech/devtools/claude-code-setup/README|Claude Code Setup]]

## Sources

- https://www.instagram.com/reel/DfKLdfYguUJ/
- https://github.com/Jakeschincariol/instagram-agent-skill
- https://uplika.com/en/docs
- https://uplika.com/en/docs/agent-publish
