---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen Overview

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

Hikugen은 HTML에서 Pydantic-compatible object를 얻기 위한 minimal Python library다. 사용자는 CSS selector나 XPath 대신 원하는 결과의 **schema**를 정의한다. Hikugen은 HTML과 schema를 OpenRouter LLM에 전달하여 아래 signature의 Python parser를 생성한다.

```python
def extract_data(html_content):
    # generated parsing logic
    return {"items": []}
```

생성된 함수의 `dict` 결과는 public API 계층에서 Pydantic model로 validation된다. 즉, LLM이 최종 데이터를 매번 직접 답하는 구조가 아니라 LLM이 **재실행 가능한 parsing program**을 한 번 만들도록 하는 구조다.

## Why

### Manual scraper의 비용

전통적인 scraper는 사이트마다 selector, XPath, pagination과 예외 처리를 개발자가 작성한다. 속도와 결정성은 좋지만 DOM이 바뀌면 parser가 깨지고 유지보수가 반복된다.

### Direct LLM extraction의 비용

HTML을 실행마다 LLM에 보내 JSON을 받는 방식은 유연하지만 다음 문제가 있다.

- 매 실행마다 token cost와 inference latency가 발생한다.
- 동일 입력에도 결과가 달라질 수 있다.
- 긴 문서는 context window, chunk overlap, merge logic이 필요하다.
- field 누락, type mismatch, hallucination을 별도로 검증해야 한다.

Hikugen의 절충안은 LLM 호출을 parser 생성 시점으로 옮기는 것이다. 성공한 parser를 반복 실행하면 LLM cost를 여러 page/run에 나눌 수 있다. parser 실행 또는 schema validation이 실패하면 오류를 feedback으로 제공해 code를 다시 생성한다.

## Core Components

| Component | 역할 |
|---|---|
| `HikuExtractor` | `extract()` / `extract_from_html()`을 제공하고 cache, generation, retry, quality check를 orchestration |
| `HikuCodeGenerator` | OpenRouter로 extraction code 생성, 오류 기반 regeneration, execution timeout 적용 |
| `HikuDatabase` | generated code를 SQLite에 저장하고 `cache_key + schema hash`로 조회 |
| `code_validation` | AST, import allowlist, 함수 정의와 return 존재 여부 검사 |
| `http_client` | URL fetch, connection pooling, timeout, OpenRouter request, cookie file 처리 |
| `prompts` | initial generation, error-feedback, data-quality prompt 분리 |

## Key Features

### Schema-first

Pydantic model이 output contract이자 LLM prompt의 의미 정보가 된다. 특히 `Field(description=...)`을 구체적으로 적으면 모호한 field의 의미를 전달할 수 있다.

```python
class Product(BaseModel):
    name: str = Field(description="화면에 표시된 상품명")
    price_krw: int = Field(description="할인가를 원 단위 정수로 정규화")
```

### Generated code reuse

성공한 code는 SQLite에 cache된다. 같은 `cache_key`라도 Pydantic JSON schema의 SHA-256 hash가 다르면 별도 parser로 취급되므로 output contract를 나란히 운용할 수 있다.

### Automatic regeneration

execution error나 Pydantic validation error가 나면 구체적 오류와 함께 parser를 다시 생성한다. 기본 `max_regenerate_attempts`는 `1`이다.

### Fresh-code quality validation

기본 `validate_quality=True`는 새 code의 extraction 결과를 optional LLM check에 통과시킨다. cached parser의 매 실행 결과를 계속 LLM이 검토하는 의미는 아니다.

### Pre-fetched HTML

`extract_from_html()` 덕분에 Playwright, browser service, 사내 crawler를 navigation/rendering 계층으로 두고 Hikugen을 extraction 계층으로 조합할 수 있다.

## Limits and Risks

| 영역 | 알아둘 점 | 대응 |
|---|---|---|
| Browser | navigation/headless browser 없음 | Playwright 등으로 HTML을 먼저 확보 |
| Cache | DOM drift 자동 감지 없음 | cache 삭제 또는 versioned `cache_key` |
| Security | AST allowlist와 timeout은 OS sandbox가 아님 | container, non-root user, read-only FS, egress 제한 |
| Correctness | Pydantic은 shape/type을 검증할 뿐 사실성을 보장하지 않음 | range, currency, ID 등 domain invariant 추가 |
| Scale | crawling scheduler나 distributed worker가 아님 | 별도 orchestration/crawler 사용 |
| Compliance | robots.txt, ToS, privacy/copyright를 해결하지 않음 | 수집 전에 정책과 법적 근거 검토 |

> [!warning] Generated code
> import allowlist에 `requests`가 포함될 수 있으므로 network egress가 차단된다고 가정하면 안 된다. Prompt injection 가능성이 있는 HTML을 다룬다면 별도의 execution isolation이 필요하다.

## Project Maturity

조사 기준일 `2026-07-13`에 PyPI 최신 버전은 `0.3.1`(2025-10-29 배포), 요구 Python은 `3.11+`다. GitHub에는 1 commit, 약 17 stars, 0 forks가 표시되고 별도 GitHub Releases는 없다. 기능의 아이디어는 선명하지만 운영 사례와 maintenance signal은 아직 작으므로 dependency pinning, fixture test, rollback plan을 전제로 평가한다.

## Sources

- [Hikugen PyPI — usage, parameters, constraints](https://pypi.org/project/hikugen/)
- [Hikugen Architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md#architecture)
- [GitHub repository](https://github.com/goncharom/hikugen)
- [GitHub Releases](https://github.com/goncharom/hikugen/releases)
- [Show HN discussion](https://news.ycombinator.com/item?id=45916119)

