---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Lazyweb MCP Overview

## What

Lazyweb MCP는 AI coding agent가 실제 제품의 UI reference와 product-growth 맥락을 검색·비교·정리하도록 하는 hosted MCP다. 오픈소스 `lazyweb-skill` pack은 Codex, Claude Code, Cursor 등의 local skill root에 `/lazyweb-*` workflow를 설치하고 hosted MCP 사용을 돕는다.

## Why

generic UI 생성 대신, 구체적인 제품·목적·flow를 근거로 의사결정을 내리기 위해서다. 예를 들어 “좋은 paywall을 찾아줘”보다 “B2B SaaS에서 trial 직전 annual pricing을 어떻게 framing하는지 조사하고 자사 제약을 분리해줘”가 더 검증 가능한 조사 요청이다.

```text
업무 질문
  → screens / flows / experiments 탐색
  → 관찰 사실과 출처 기록
  → 자사 가설·제약 분리
  → design-system 적합화 및 구현
  → 실제 metric으로 실험 검증
```

## 특징

### Agent-first access

- public endpoint는 key 없이 Lazyweb 공개 정보의 search, cited answer, TL;DR, compare에 사용한다.
- authenticated endpoint는 Streamable HTTP와 Bearer token을 쓴다.
- 설치된 도구 이름과 schema는 문서에 고정하지 말고 매 세션 `lazyweb_get_workflows` 또는 MCP `tools/list`로 확인한다.

### 조사와 growth workflow

대표 도구군은 다음과 같다. 실제 availability는 account, plan, rollout에 따라 달라질 수 있다.

| 범주 | 예시 도구 | 목적 |
|---|---|---|
| 조사 | `lazyweb_search_screens`, `lazyweb_search_flows`, `lazyweb_search_experiments` | 사례와 ordered journey 탐색 |
| 이미지 | `lazyweb_compare_image`, `lazyweb_find_similar` | 현재 화면과 유사한 패턴 비교 |
| 성장 | `lazyweb_growth_score`, `lazyweb_growth_report`, `lazyweb_growth_backlog` | audit·recommendation·backlog 연결 |
| 운영 | `lazyweb_get_workflows`, `lazyweb_account`, `lazyweb_connections` | workflow·계정·연결 상태 확인 |

### 안전한 결과 처리

- 검색 결과는 stable `result_ref`로 누적하고 `lazyweb_agentic_search_finalize`로 선택을 확정하는 흐름을 따른다.
- image tool이 반환한 optimized image URL을 사용한다. raw screenshot ID나 storage URL을 조합하지 않는다.
- 조사 도구는 대체로 read 중심이나 product/backlog에는 상태 변경이 포함될 수 있다. 삭제는 exact confirmation을 요구한다.
- token이 작동해도 유료 데이터 접근 권한을 뜻하지는 않는다.

## 한계와 점검 항목

- capture는 특정 날짜·경로의 기록이며 모든 branch를 포괄하지 않을 수 있다.
- 제품의 marketing claim이나 화면 내 가격은 현재 사실로 재검증한다.
- Growth Score는 우선순위화 도구이지 conversion forecast가 아니다.
- 실제 적용 전 keyboard navigation, contrast, locale, brand/design token, legal copy와 metric instrumentation을 점검한다.

## Sources

- https://www.lazyweb.com/agent-access
- https://www.lazyweb.com/product
- https://github.com/aboul3ata/lazyweb-skill
