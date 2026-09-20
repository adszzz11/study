---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP

> **한 줄 정의**: Mobbin MCP는 AI agent가 Mobbin의 실제 출시 UI 레퍼런스를 검색하여 화면·user flow·웹 section 설계와 코드 생성의 근거로 쓰게 하는 hosted Model Context Protocol server다.

## Overview

AI coding agent는 UI를 만들 수 있지만, 좋은 checkout·onboarding·paywall이 실제 제품에서 어떤 방식으로 작동하는지의 근거를 기본으로 갖지는 않는다. Mobbin MCP는 이런 공백을 shipped product의 screen, flow, website section으로 보완한다. 즉 프롬프트의 추측에만 의존하지 않고 경쟁 제품의 패턴을 조사·비교·종합하는 workflow를 만든다.

- **연결 방식:** Streamable HTTP endpoint `https://api.mobbin.com/mcp`에 연결하고 최초 OAuth를 완료한다.
- **조사 단위:** `search_screens`, `search_flows`, `search_sections`로 단일 화면, 연속 경험, 웹 section을 나눠 찾는다.
- **결과물:** 이미지, metadata, Mobbin 원본 링크를 바탕으로 설계 권고안이나 구현 prompt를 만든다.
- **경계:** 도구는 read-only다. reference를 의사결정 근거로 쓰되 타사 layout·copy·asset을 복제하지 않는다.
- **접근 조건:** Mobbin은 Pro·Team에 MCP 제공을 안내하며 plugin 문서는 Enterprise도 언급한다. 실제 entitlement는 도입 전 현재 billing 화면에서 확인한다.

## Learning Path

- [ ] [[tech/devtools/mobbin-mcp/01-overview|1. Overview]] — What/Why, 기능, read-only 경계 이해하기
- [ ] [[tech/devtools/mobbin-mcp/02-ecosystem|2. Ecosystem]] — Figma·Refero·21st MCP와 역할 나누기
- [ ] [[tech/devtools/mobbin-mcp/03-references|3. References]] — 공식 문서와 비공식 구현을 구분하기
- [ ] [[tech/devtools/mobbin-mcp/04-learning/01-getting-started|4. Getting started]] — endpoint 등록과 OAuth, 첫 검색 실행하기
- [ ] [[tech/devtools/mobbin-mcp/04-learning/02-deep-dive|5. Deep dive]] — evidence-backed UX 결정 workflow 설계하기
- [ ] [[tech/devtools/mobbin-mcp/05-projects|6. Projects]] — paywall·KYC·checkout 사례에 적용하기
- [ ] [[tech/devtools/mobbin-mcp/cheatsheet|7. Cheatsheet]] — 검색 prompt와 점검 목록 빠르게 복습하기

## When To Use

- 새 기능의 UX를 정하기 전에 실제 시장의 유사 flow와 예외 사례를 조사할 때
- agent에게 구현을 맡기기 전, UI hierarchy와 interaction의 설계 근거를 함께 제공할 때
- paywall, onboarding, checkout처럼 conversion과 trust가 중요한 흐름을 비교할 때
- 외부 레퍼런스 조사와 내부 design-system 구현을 별도 도구로 분리할 때

## When Not To Use

- 이미 확정된 내부 Figma frame을 정확히 구현하거나 업데이트하는 일이 중심일 때는 Figma MCP가 더 직접적이다.
- 바로 설치할 React/shadcn component나 template이 필요할 때는 21st MCP 같은 code catalog를 우선 검토한다.
- Mobbin 계정 entitlement 또는 OAuth 사용이 불가능한 환경일 때
- 특정 제품의 시각 자산·문구·layout을 그대로 재현하려는 목적일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — MCP 연결 모델과 client/server 역할을 함께 학습한다.

## Sources

- [Mobbin MCP](https://mobbin.com/mcp)
- [Mobbin MCP server repository](https://github.com/mobbin/mobbin-mcp-server)
- [MCP client setup overview](https://docs.mobbin.com/mcp/clients/overview)
- [MCP feature documentation](https://docs.mobbin.com/mcp/features)
