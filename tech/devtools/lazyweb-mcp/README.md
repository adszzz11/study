---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Lazyweb MCP

> **한 줄 정의**: Lazyweb MCP는 AI coding agent에 실제 제품의 UI screen·user flow·growth 사례를 제공해, 근거 기반의 UX/growth 조사와 구현을 돕는 hosted Model Context Protocol 서버 및 skill pack이다.

## Overview

AI가 만든 UI는 종종 학습 데이터의 평균처럼 보인다. Lazyweb은 출시된 제품의 screen, ordered flow, 관찰된 variation을 조사 맥락으로 제공하고 이를 growth audit, recommendation, backlog로 연결하려 한다.

두 접근면을 구분해야 한다.

| 접근면 | Endpoint | 용도 | 인증 |
|---|---|---|---|
| Public discovery | `https://www.lazyweb.com/mcp/public` | Lazyweb 제품 정보, source가 있는 답변·비교·요약 | 불필요 |
| Product MCP | `https://www.lazyweb.com/mcp` | screen/flow/experiment 및 growth workflow | Bearer token, plan별 entitlement |

> [!warning] 증거의 한계
> 화면 캡처와 detected variation은 가설의 출발점이다. 관찰된 변화가 A/B test였는지, 어떤 성과를 냈는지는 별도 검증 없이는 단정하지 않는다. capture date, 자사 metric, accessibility·법적 요건을 함께 확인한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why와 두 endpoint의 역할 이해
- [ ] [[02-ecosystem|Ecosystem]] — Mobbin, 21st, Figma와 선택 기준 비교
- [ ] [[03-references|References]] — 공식 문서와 source hierarchy 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — public MCP 연결과 첫 조사 기록
- [ ] [[04-learning/02-deep-dive|Deep dive]] — workflow, result_ref, image URL, 권한 경계 이해
- [ ] [[05-projects|Projects]] — signup/paywall·competitive brief·growth audit 적용
- [ ] [[cheatsheet|Cheatsheet]] — 도구군과 조사 checklist 빠른 복습

## When To Use

- onboarding, pricing, paywall, checkout처럼 conversion에 영향을 주는 flow를 조사할 때
- agent가 사례 조사 → 가설 → implementation ticket 초안을 연결하게 할 때
- 경쟁사 UX를 PM·designer·engineer가 공유할 evidence-backed brief로 만들 때
- 자사 화면을 실제 제품의 유사 패턴과 비교해 design QA 기준을 만들 때

## When Not To Use

- backend-only 작업이나 UI 사례가 의사결정에 도움 되지 않는 일반 coding 작업일 때
- 특정 conversion uplift를 보장하는 도구가 필요할 때
- 사내 Figma나 design system이 유일한 source of truth여야 할 때
- 민감한 URL·화면을 제3자 hosted service에 전달할 수 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- https://www.lazyweb.com/agent-access
- https://www.lazyweb.com/product
- https://www.lazyweb.com/mcp-install
- https://github.com/aboul3ata/lazyweb-skill
