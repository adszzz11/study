---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code 기반 LinkedIn 콘텐츠·운영 워크플로

> **한 줄 정의**: Claude Code의 Skills·MCP·파일 기반 context로 LinkedIn 콘텐츠 운영을 보조하고, 외부 행동은 human-in-the-loop 또는 승인된 공식 API에 한정하는 workflow다.

## Overview

이 workflow의 목적은 게시물을 한 번 빨리 쓰는 일이 아니라 `brand voice`, 제품 근거, 고객 언어, 성과 기록을 재사용 가능한 context로 만들어 콘텐츠 운영의 품질을 누적하는 데 있다. Claude Code는 context repository를 읽고 `SKILL.md` 절차를 실행하며, MCP를 통해 허가된 CRM·문서·analytics를 연결할 수 있다.

```text
승인된 내부 context → 조사·사실 확인 → hook/초안 → linter 검수
                                                   ↓
                                      사람 승인 또는 공식 API 게시
                                                   ↓
                                    성과 기록 → 다음 주 brief 갱신
```

핵심 경계는 명확하다. AI는 조사·초안·검수 보조를 맡고, 개인 계정의 browser bot·scraping·대량 DM·engagement 자동화는 설계에서 제외한다.

## Learning Path

- [ ] [[tech/ai/claude-linkedin-workflows/01-overview|Overview]] — What/Why와 안전한 운영 원칙
- [ ] [[tech/ai/claude-linkedin-workflows/02-ecosystem|Ecosystem]] — Claude Code, automation 도구, 공식 API 비교
- [ ] [[tech/ai/claude-linkedin-workflows/04-learning/01-getting-started|시작하기]] — context repository와 첫 2주 loop
- [ ] [[tech/ai/claude-linkedin-workflows/04-learning/02-deep-dive|Deep Dive]] — Skill, MCP, publishing boundary 설계
- [ ] [[tech/ai/claude-linkedin-workflows/05-projects|Projects]] — 적용 가능한 프로젝트 아이디어
- [ ] [[tech/ai/claude-linkedin-workflows/03-references|References]] — 공식 문서와 정책 근거
- [ ] [[tech/ai/claude-linkedin-workflows/cheatsheet|Cheatsheet]] — 운영 checklist와 prompt contract

## When To Use

- 여러 작성자가 같은 brand voice와 검증된 proof point를 일관되게 써야 할 때
- 초안, 검수, 승인, 성과 회고를 주간 운영 과정으로 만들 때
- 조직 Page에 공식 API 기반 게시 흐름을 검토할 때

## When Not To Use

- 개인 LinkedIn 계정에서 browser automation으로 게시·댓글·좋아요·DM을 대량 실행하려 할 때
- LinkedIn scraping으로 prospect data를 수집하려 할 때
- 출처와 사람 검수 없이 AI 초안을 즉시 외부에 게시하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/claude-code-skill-workflows/README|Claude Code Skills 워크플로]]

## Sources

- https://www.instagram.com/reel/DeiiZIhAIpL/
- https://code.claude.com/docs/en/overview
- https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-02
