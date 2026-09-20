---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Lazyweb MCP Cheatsheet

## Endpoint

| Endpoint | 인증 | 쓰임 |
|---|---|---|
| `https://www.lazyweb.com/mcp/public` | 없음 | 공개 제품 정보의 search/ask/compare/TL;DR |
| `https://www.lazyweb.com/mcp` | Bearer token | 인증된 product/growth workflow |

## 대표 도구군

| 목적 | 도구 예시 |
|---|---|
| screen 조사 | `lazyweb_search_screens` |
| flow 조사 | `lazyweb_search_flows` |
| variation 조사 | `lazyweb_search_experiments` |
| 이미지 비교 | `lazyweb_compare_image`, `lazyweb_find_similar` |
| workflow/schema 확인 | `lazyweb_get_workflows`, MCP `tools/list` |
| 후보 확정 | `lazyweb_agentic_search_finalize` |
| growth | `lazyweb_growth_score`, `lazyweb_growth_report`, `lazyweb_growth_backlog` |

> [!note] 실제 도구는 live schema 우선
> 이름, 인자, plan별 제공 여부는 release마다 달라질 수 있다. 실행 전 `tools/list`와 `lazyweb_get_workflows`를 확인한다.

## 기본 조사 순서

```text
질문 구체화
  → screens
  → flows
  → experiments
  → result_ref 유지
  → finalize
  → 관찰 / 가설 / 제약 / metric 분리
```

## Prompt 골격

```text
목표: [사용자/flow/의사결정]
조사: [대상 제품군]의 [onboarding/paywall/checkout]을 비교
출력: source와 capture date, 관찰 사실, 가설, 적용 조건을 분리
제약: [design token, a11y, legal, locale]
검증: primary metric=[…], guardrail=[…]
```

## Do / Don't

| Do | Don't |
|---|---|
| tool list·workflow를 먼저 확인 | 문서에 적힌 tool name만 믿고 호출 |
| optimized image URL 사용 | raw screenshot ID/storage URL 조합 |
| observed variation을 가설로 기록 | A/B winner나 uplift라고 단정 |
| mutation 전에 target·rollback 확인 | token이 있으니 모든 paid data에 접근된다고 가정 |
| 자사 metric으로 검증 | reference를 그대로 복제 |

## Sources

- https://www.lazyweb.com/agent-access
- https://www.lazyweb.com/product
- https://github.com/aboul3ata/lazyweb-skill
