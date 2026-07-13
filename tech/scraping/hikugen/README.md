---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen

> **한 줄 정의**: URL/HTML과 Pydantic schema를 입력받아 LLM이 Python extraction code를 생성하고, 이를 검증·실행·캐시하여 type-safe structured data를 추출하는 경량 AI web scraping library.

## Overview

Hikugen은 LLM을 매번 JSON을 만드는 extractor가 아니라 **parser generator**로 사용한다. 대표 HTML과 Pydantic schema로 `extract_data(html_content)` 함수를 만든 뒤 AST/import 규칙을 검사하고, 실행 결과를 schema로 검증한다. 성공한 code는 SQLite에 저장되어 같은 구조의 페이지에서 일반 Python parser처럼 재사용된다.

```text
URL 또는 HTML + Pydantic schema
            ↓
     cache lookup ── hit ──→ cached Python code
            │ miss
            ↓
 OpenRouter code generation
            ↓
 AST validation → execution → Pydantic validation
            ↓ 실패
 error-feedback regeneration
```

핵심 범위는 **주어진 HTML의 structured extraction**이다. navigation, login flow, JavaScript rendering, headless browser, distributed crawling은 직접 담당하지 않는다. 최신 공개 버전은 조사 기준일 현재 `0.3.1`이며 Python `3.11+`, MIT License다. 저장소 규모와 release history를 고려하면 production crawling platform보다는 초기 단계의 experimental library로 보는 편이 안전하다.

## Learning Path

- [ ] [[01-overview|1. Overview — What, Why, 특징과 한계]]
- [ ] [[02-ecosystem|2. Ecosystem — 대안과 선택 기준]]
- [ ] [[03-references|3. References — 공식 자료와 읽기 순서]]
- [ ] [[04-learning/01-getting-started|4. Getting Started — 설치와 첫 extraction]]
- [ ] [[04-learning/02-deep-dive|5. Deep Dive — cache, regeneration, security]]
- [ ] [[05-projects|6. Projects — 단계별 실습]]
- [ ] [[cheatsheet|7. Cheatsheet — API 빠른 참조]]

## When To Use

- 같은 DOM pattern을 가진 여러 페이지를 반복 수집하며 LLM cost와 latency를 amortize하고 싶을 때
- 기대 결과를 Pydantic model로 명확히 표현할 수 있을 때
- selector를 직접 만들 시간은 부족하지만, 생성된 parser를 검토·격리 실행할 수 있을 때
- Playwright나 기존 crawler가 가져온 HTML에 schema extraction 계층만 덧붙일 때
- 작은 PoC, 내부 도구, low-volume batch에서 AI-generated parser의 가능성을 검증할 때

## When Not To Use

- login, click, infinite scroll, JavaScript rendering 등 browser interaction이 핵심일 때
- sitemap discovery, scheduling, proxy rotation, distributed crawling이 필요한 대규모 수집
- untrusted page의 prompt injection 영향을 받은 generated code를 격리 없이 production host에서 실행해야 할 때
- millisecond-level latency, 완전한 deterministic behavior 또는 엄격한 audit가 필수일 때
- DOM 변경을 자동 감지하고 parser를 스스로 versioning해야 할 때
- schema의 type뿐 아니라 값의 사실성까지 library가 보장해야 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Scraping]]
- [[tech/scraping/playwright/README|Playwright]]
- [[tech/scraping/firecrawl/README|Firecrawl]]

## Sources

- [Hikugen on PyPI](https://pypi.org/project/hikugen/)
- [goncharom/hikugen](https://github.com/goncharom/hikugen)
- [Architecture (CLAUDE.md)](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md)
- [Show HN: Hikugen](https://news.ycombinator.com/item?id=45916119)
- [MIT License](https://github.com/goncharom/hikugen/blob/master/LICENSE)
