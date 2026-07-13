---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Official Resources

| 자료 | 무엇을 확인할까 | 주의점 |
|---|---|---|
| [PyPI](https://pypi.org/project/hikugen/) | 설치, Quick Start, parameter, execution constraint, version history | 현재 가장 실용적인 user-facing 문서 |
| [GitHub repository](https://github.com/goncharom/hikugen) | source tree, dependency, issue와 activity | 조사 시점 repository history가 매우 작음 |
| [Architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md) | component, cache key/schema hash, prompt, validation flow | public API reference라기보다 개발 문서 |
| [LICENSE](https://github.com/goncharom/hikugen/blob/master/LICENSE) | MIT License 조건 | dependency license는 별도 확인 |
| [GitHub Releases](https://github.com/goncharom/hikugen/releases) | release artifact 여부 | 조사 시점 별도 release 없음; PyPI history 사용 |

## Context and Discussion

- [Show HN: Hikugen](https://news.ycombinator.com/item?id=45916119)
  - 제작자가 library scope를 navigation/crawling이 아닌 HTML extraction으로 설명한 맥락을 읽는다.
  - community comment는 설계 아이디어를 평가하는 참고자료이며 공식 guarantee가 아니다.

## Prerequisites

| 주제 | 자료 | 학습 포인트 |
|---|---|---|
| Pydantic | [Models](https://docs.pydantic.dev/latest/concepts/models/) | `BaseModel`, validation, nested model |
| Pydantic | [Fields](https://docs.pydantic.dev/latest/concepts/fields/) | `Field(description=...)`, constraint, optional field |
| Python AST | [`ast` module](https://docs.python.org/3/library/ast.html) | AST validation이 확인할 수 있는 범위와 한계 |
| SQLite | [SQLite documentation](https://www.sqlite.org/docs.html) | local code cache의 운영·백업 특성 |
| OpenRouter | [API documentation](https://openrouter.ai/docs) | API key, model identifier, request behavior |

## Alternatives

- [Crawl4AI LLM strategies](https://docs.crawl4ai.com/extraction/llm-strategies/) — chunking되는 direct LLM extraction과 비교
- [Crawl4AI LLM-free strategies](https://docs.crawl4ai.com/extraction/no-llm-strategies/) — CSS/XPath/Regex extraction과 비교
- [ScrapeGraphAI SmartScraper](https://docs.scrapegraphai.com/services/smartscraper) — managed semantic extraction과 비교
- [Firecrawl Docs](https://docs.firecrawl.dev/) — browser/crawl 포함 service와 scope 비교
- [Playwright Python](https://playwright.dev/python/) — pre-fetched rendered HTML을 만드는 upstream layer
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — generated parser가 사용할 수 있는 전통적 parsing 방식 이해

## Recommended Reading Order

1. PyPI의 **Overview → Quick Start → Parameters**로 public API를 확인한다.
2. `CLAUDE.md`의 workflow와 component를 읽고 [[04-learning/02-deep-dive|Deep Dive]]와 대조한다.
3. Pydantic field description과 constraint를 복습한다.
4. sample HTML fixture로 [[04-learning/01-getting-started|Getting Started]]를 실행한다.
5. AST validation을 sandbox로 오해하지 않도록 security boundary를 검토한다.
6. target workload를 [[02-ecosystem|Ecosystem]]의 대안과 비교한다.

## Version Snapshot

| 항목 | 조사 기준일 값 |
|---|---|
| 조사일 | 2026-07-13 |
| PyPI latest | `0.3.1` |
| latest upload | 2025-10-29 |
| Python | `>=3.11` |
| PyPI releases | `0.1.0`, `0.1.1`, `0.2.1`, `0.3.1` |
| License | MIT |
| GitHub snapshot | 1 commit, 약 17 stars, 0 forks |

> [!note] 시간에 민감한 정보
> 버전, repository activity, model default는 바뀔 수 있다. 실제 도입 시 PyPI와 source를 다시 확인하고 version을 pin한다.

## Sources

- [Hikugen PyPI](https://pypi.org/project/hikugen/)
- [goncharom/hikugen](https://github.com/goncharom/hikugen)
- [Hikugen Architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md)
- [Show HN](https://news.ycombinator.com/item?id=45916119)

