---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## Comparison

Hikugen을 crawler 전체와 일대일로 비교하면 범위를 오해하기 쉽다. Hikugen은 **HTML → typed data** 구간에 집중하며 browser와 crawl orchestration은 외부 도구에 맡긴다.

| 도구 | 핵심 방식 | Browser / Crawl | Structured extraction | LLM 비용 특성 | Hikugen 대신 적합한 경우 |
|---|---|---:|---|---|---|
| **Hikugen** | LLM이 Python parser를 생성하고 SQLite에 code cache | 제한적 HTTP fetch; navigation/headless browser 없음 | Pydantic schema | 초기 생성·실패·선택적 품질검사 때 발생 | 반복되는 유사 HTML을 작고 재사용 가능한 local parser로 바꾸고 싶을 때 |
| **Crawl4AI** | Browser crawling + HTML/Markdown pipeline + extraction strategies | 강함; browser와 multi-page/parallel crawl | CSS, XPath, Regex, LLM + Pydantic schema | LLM strategy는 chunk 단위 호출 가능; non-LLM strategy도 제공 | JS-rendered page, crawl, Markdown/RAG ingestion까지 한 stack에서 처리할 때 |
| **ScrapeGraphAI** | managed API와 graph/agent 기반 semantic extraction | managed crawl, multi-page 기능 제공 | prompt + Pydantic/Zod output schema | semantic extraction request에 따른 API/credit 비용 | 인프라를 운영하지 않고 semantic extraction과 site crawl을 API로 쓰고 싶을 때 |
| **Firecrawl** | managed/self-host crawl, scrape, map 및 extraction API | 강함; crawl/map/browser 기능 | JSON schema 기반 extraction | extraction/agent 사용량 및 service credit 중심 | URL discovery, rendering, crawl과 data/Markdown delivery가 모두 필요할 때 |
| **Playwright + Beautiful Soup** | browser automation + 직접 작성한 deterministic parser | 매우 강한 browser control; crawl은 직접 구성 | 직접 작성한 model/validator | LLM 비용 없음 | selector가 안정적이고 throughput, auditability, 정확한 제어가 중요할 때 |
| **Direct LLM extraction** | HTML/chunk마다 LLM이 최종 JSON 생성 | 별도 fetch/browser 필요 | JSON/Pydantic structured output | 거의 모든 extraction마다 inference | page 구조가 매번 달라 parser reuse 이점이 작거나 semantic reasoning 자체가 필요할 때 |

## Cost Model

```text
반복되는 HTML 구조
├─ parser를 오래 재사용 가능
│  ├─ selector 작성 가능 → manual parser
│  └─ selector 작성 비용이 큼 → Hikugen 후보
└─ 구조가 매번 크게 다름
   ├─ semantic reasoning 필요 → direct LLM / ScrapeGraphAI
   └─ crawl·rendering도 필요 → Crawl4AI / Firecrawl
```

Hikugen의 경제성은 `generation cost ÷ successful cache reuse count`로 생각할 수 있다. DOM이 자주 변해 regeneration이 반복되거나 `cache_key`가 지나치게 세분화되면 이점이 사라진다. 반대로 product detail처럼 template이 같고 URL만 다른 page가 많으면 parser code reuse 효과가 커진다.

## Composition Patterns

### Playwright + Hikugen

JavaScript rendering, login, scroll은 Playwright가 맡고 최종 HTML만 Hikugen에 넘긴다.

```text
Playwright: navigate → authenticate → render → page.content()
                                      ↓
Hikugen:                 schema → generate/cache parser → validate
```

이 조합은 책임이 분명하지만 generated code execution isolation은 별도로 설계해야 한다.

### Crawler + deterministic validation

Hikugen 결과 뒤에 business rule validation을 둔다.

```python
result = extractor.extract_from_html(...)
assert result.price_krw >= 0
assert result.currency == "KRW"
assert result.product_id in source_html
```

Pydantic validation과 domain validation은 서로 대체하지 않는다.

## Selection Checklist

- [ ] target page가 같은 template을 반복해서 쓰는가?
- [ ] Pydantic으로 output contract를 표현할 수 있는가?
- [ ] HTML fetch/rendering은 단순 HTTP이거나 이미 다른 계층이 담당하는가?
- [ ] generated code를 inspect하고 sandbox에서 실행할 수 있는가?
- [ ] DOM drift를 감지할 fixture/monitoring과 cache versioning이 있는가?
- [ ] 초기 library의 작은 community와 maintenance risk를 감수할 수 있는가?

네 개 이상이 `Yes`라면 Hikugen PoC의 조건이 좋다. browser/crawl 질문이 `No`라면 먼저 Crawl4AI, Firecrawl 또는 Playwright를 평가한다.

## Sources

- [Hikugen PyPI](https://pypi.org/project/hikugen/)
- [Hikugen architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md)
- [Crawl4AI LLM extraction strategy](https://docs.crawl4ai.com/extraction/llm-strategies/)
- [Crawl4AI LLM-free extraction](https://docs.crawl4ai.com/extraction/no-llm-strategies/)
- [ScrapeGraphAI SmartScraper](https://docs.scrapegraphai.com/services/smartscraper)
- [ScrapeGraphAI SmartCrawler](https://docs.scrapegraphai.com/services/smartcrawler)
- [Firecrawl documentation](https://docs.firecrawl.dev/)
- [Playwright Python documentation](https://playwright.dev/python/)

