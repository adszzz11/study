---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — Overview

> [[README|목차로 돌아가기]] · [[02-ecosystem|다음: Ecosystem]]

## What

Refero MCP는 Refero의 curated product-interface corpus를 MCP-compatible client에 연결하는 hosted HTTP server다. canonical endpoint는 `https://api.refero.design/mcp`이며, 연결 시 browser OAuth로 로그인한다. manifest에는 secret를 넣지 않는다.

공식 package는 connection을 **read-only**로 설명한다. 즉 agent에게 research context를 주입하는 server이며, repository·Figma file·제품을 임의로 수정하는 action server가 아니다.

## Why

LLM은 code와 logic에는 강해도 layout, information hierarchy, onboarding recovery, empty state의 CTA처럼 축적된 제품 디자인 판단을 기본으로 보유하지 않는다. Refero의 목표는 “그럴듯한 생성” 전에 실제 사례를 조회하고 synthesis하게 하는 것이다.

| 문제 | Research-first 대응 |
|---|---|
| generic AI UI | 유사 제품의 visual direction과 pattern을 먼저 조사 |
| 한 화면만 보고 journey 누락 | `Flows`로 단계, 오류, completion state 확인 |
| reference를 그대로 복제 | 2~3개 사례를 비교하고 유지/제외 trait를 기록 |
| 구현 후 시각 품질 drift | screenshot 기반 visual QA 수행 |

## Core Features

| 레이어 | 찾는 것 | 활용 예 |
|---|---|---|
| `Styles` | typography, color, spacing, imagery, tone | 신뢰감 있는 B2B marketing direction |
| `Screens` | 단일 UI pattern | dashboard, auth, table, modal, empty state |
| `Flows` | multi-step user journey | onboarding, checkout, cancellation, password reset |

```text
AI agent
  → browser OAuth
  → Refero hosted MCP (read-only)
  → Styles / Screens / Flows corpus
  → research note and reference lock
  → application code + visual QA
```

## MCP and Skill

- **MCP**: live corpus search와 결과 조회를 제공한다. live access에는 Refero paid plan이 필요하다.
- **`refero-design` Skill**: research → synthesis → implementation → visual QA라는 방법론과 craft guidance를 제공한다. MCP가 없어도 bundled reference는 읽을 수 있지만 live search는 할 수 없다.
- 공개 Skill에 적힌 tool name은 API 변경 또는 문서 지연으로 달라질 수 있다. 실제 client의 MCP tool discovery가 실행 시 source of truth다.

## Strengths and Boundaries

강점은 discovery부터 flow까지 한 context에서 조사한다는 점이다. 반면 corpus의 수량은 품질 또는 coverage를 보장하는 benchmark가 아니며, licensing·brand fit·accessibility·자사 token 적용은 팀이 검토해야 한다.

> [!warning] 수치와 API surface
> 2026-09 기준 landing page와 GitHub README의 screen/flow 수치가 다르다. 문서의 수치나 tool 이름을 계약·자동화의 고정 입력으로 사용하지 말고, 현재 plan과 client discovery 결과를 확인한다.

## Sources

- https://refero.design/mcp
- https://github.com/referodesign/refero_skill
- https://github.com/referodesign/refero_skill/blob/master/.mcp.json
- https://github.com/referodesign/refero_skill/issues/1
