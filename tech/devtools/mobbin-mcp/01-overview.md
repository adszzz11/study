---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — Overview

## What

Mobbin MCP는 Mobbin design-reference corpus를 AI client에 제공하는 first-party hosted MCP server다. client는 `https://api.mobbin.com/mcp`에 Streamable HTTP로 연결하고 OAuth로 계정을 승인한다. 로컬 server 운영이나 API key 설정은 필요하지 않다.

검색 결과는 UI reference 자체가 아니라, 그 reference를 판단에 사용할 수 있는 이미지·metadata·Mobbin 원본 링크다. Mobbin이 표방하는 corpus는 621,500+ shipped screens이며 mobile app, web app, website 레퍼런스를 포괄한다. 규모는 계속 변할 수 있으므로 도입 시 landing page에서 다시 확인한다.

## Why

일반적인 생성 모델은 UI를 빠르게 만들지만, 제품 시장에서 검증된 interaction pattern을 자동으로 인용하지는 않는다. Mobbin MCP를 사용하면 다음과 같은 질문을 evidence 기반으로 다룰 수 있다.

- biometric login에서 permission 설명은 어느 단계에 나타나는가?
- subscription cancellation은 어떤 reassurance와 대안을 제공하는가?
- B2B SaaS pricing page의 hero와 social proof는 어떤 정보 순서로 구성되는가?

핵심은 예쁜 화면 하나를 고르는 것이 아니라, 여러 사례에서 공통 패턴과 의도적인 예외를 분리한 뒤 제품 제약에 맞는 결정을 내리는 데 있다.

## Features

| Tool | 검색 대상 | 적합한 질문 |
|---|---|---|
| `search_screens` | 개별 UI screen | “fintech biometric login screen 15개를 찾아라.” |
| `search_flows` | 연속된 user flow | “subscription cancellation flow를 비교하라.” |
| `search_sections` | website section | “B2B SaaS pricing hero와 social proof 사례를 찾아라.” |

- **Read-only:** MCP를 통해 Mobbin library를 수정하지 않는다.
- **Hosted remote server:** client 설정에 endpoint를 넣고 OAuth만 수행한다.
- **Evidence links:** 후속 memo와 디자인 리뷰에서 원본 reference를 검증할 수 있다.
- **Agent Plugin:** Mobbin은 Agent Plugins 1.0.0 plugin도 배포하며, ChatGPT/Codex 설치 경로를 별도로 안내한다.

## Architecture

```text
AI client (Codex / Claude Code / Cursor)
             │ MCP, Streamable HTTP
             ▼
https://api.mobbin.com/mcp
             │ OAuth-authorized read access
             ▼
Mobbin design-reference corpus
  ├─ Screens
  ├─ Flows
  └─ Website sections
             │ images + metadata + source links
             ▼
Evidence-backed UX recommendation / implementation prompt
```

## Guardrails

reference는 UI 의사결정의 근거로만 사용한다. 특정 제품의 copy, asset, 독특한 visual composition을 그대로 가져오지 않고, 문제·패턴·제약을 자신의 product language로 재해석한다. 또한 `pdcolandrea/mobbin-mcp`는 browser cookie와 reverse-engineered internal endpoint를 이용한 비공식 구현이며 2026-05-15 archive되었다. 새 도입은 first-party server를 선택한다.

## Sources

- [Mobbin MCP](https://mobbin.com/mcp)
- [Mobbin MCP features](https://docs.mobbin.com/mcp/features)
- [Mobbin Agent Plugin](https://github.com/mobbin/mobbin-agent-plugin)
- [Archived unofficial Mobbin MCP](https://github.com/pdcolandrea/mobbin-mcp)
