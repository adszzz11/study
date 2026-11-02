---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템 스터디

> **한 줄 정의**: LLM에 명확한 context, tools, memory, approval을 연결하여 콘텐츠·리서치·개발·업무를 반복 실행 가능한 시스템으로 만드는 방법이다.

## Overview

이 스터디는 Lazy Owen의 공개 프로필과 가이드 79편에서 반복되는 Claude Code, ChatGPT, MCP, Skills, n8n, 생성형 영상, SNS 운영 관점을 하나의 시스템 설계 관점으로 묶는다. Instagram 릴스 전체 음성·영상은 로그인 제한 때문에 완전 재생으로 검증하지 않았으며, 따라서 모든 릴스를 청취했다는 주장은 하지 않는다.

- 핵심 전환: 일회성 대화에서 context·tool·검증·기억이 있는 업무 시스템으로 전환한다.
- 원칙: 판단은 Agent에, 저장·변환·schedule·retry는 deterministic workflow에 둔다.
- 안전: 외부 발송·금전·배포·삭제·고객 응대는 draft와 human approval 뒤에만 실행한다.

## Learning Path

- [ ] [[tech/ai/ai-agent-automation-systems/01-overview|Overview]] — 문제, 구조, 핵심 특징을 이해한다.
- [ ] [[tech/ai/ai-agent-automation-systems/02-ecosystem|Ecosystem 비교]] — Agent, MCP, workflow와 도구 선택을 구분한다.
- [ ] [[tech/ai/ai-agent-automation-systems/04-learning/01-getting-started|시작하기]] — 작은 read-only briefing을 만든다.
- [ ] [[tech/ai/ai-agent-automation-systems/04-learning/02-deep-dive|심화]] — memory, approval, evaluation을 설계한다.
- [ ] [[tech/ai/ai-agent-automation-systems/05-projects|Projects]] — 업무별 최소 실행 단위를 적용한다.
- [ ] [[tech/ai/ai-agent-automation-systems/03-references|References]] — 공식 문서와 공개 가이드를 확인한다.
- [ ] [[tech/ai/ai-agent-automation-systems/cheatsheet|Cheatsheet]] — 설계·운영 체크리스트로 복습한다.

## When To Use

- 여러 도구와 최신 정보가 필요한 리서치·콘텐츠·개발 업무를 반복할 때
- 결과물을 사람이 검수한 뒤 발행하거나 실행해야 할 때
- 실행 기록, 비용, 실패 원인을 남겨 계속 개선해야 할 때

## When Not To Use

- 입력과 출력이 고정된 단순 변환이면 일반 code나 workflow가 더 적합할 때
- approval, 최소 권한, 로그를 마련할 수 없는데 write action이 필요한 때
- 품질 기준과 source 검증 없이 자동 게시부터 시작하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://lazyowen.com/guides
- https://lazyowen.com/challenge
- https://docs.anthropic.com/en/docs/mcp
- https://n8n.io/ai-agents/

