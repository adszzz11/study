---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Install

```bash
# Python 3.11+
uv add hikugen
export OPENROUTER_API_KEY="..."
```

## Minimal Schema

```python
from pydantic import BaseModel, Field


class Item(BaseModel):
    title: str = Field(description="화면에 표시된 제목")
    price: int = Field(ge=0, description="통화 기호를 제거한 정수 가격")


class Page(BaseModel):
    items: list[Item] = Field(description="페이지의 모든 item")
```

## Initialize

```python
import os
from hikugen import HikuExtractor

extractor = HikuExtractor(
    api_key=os.environ["OPENROUTER_API_KEY"],
    model="google/gemini-2.5-flash",  # PyPI 문서의 기본 model
)
```

## Extract

```python
# URL
result = extractor.extract(
    url="https://example.com/items",
    schema=Page,
    cache_key="items:desktop:v1",
    use_cached_code=True,
    max_regenerate_attempts=1,
    validate_quality=True,
)

# pre-fetched HTML
result = extractor.extract_from_html(
    html_content=html,
    cache_key="items:desktop:v1",
    schema=Page,
)
```

## Cache

```python
deleted = extractor.clear_cache_for_key("items:desktop:v1")
total = extractor.clear_all_cache()
```

| 상황 | 권장 action |
|---|---|
| 같은 template, 같은 schema | 같은 `cache_key` 재사용 |
| 같은 template, schema 변경 | 같은 key 가능; schema hash로 분리 |
| DOM template 변경 | `:v2` key로 새 parser 생성 |
| 개발 중 전체 reset | `clear_all_cache()` |
| rollback 필요 | 이전 versioned key 유지 |

## Parameters

| Parameter | 의미 | 기본값/메모 |
|---|---|---|
| `url` | fetch할 URL | `extract()`에서 사용 |
| `html_content` | 이미 확보한 HTML | `extract_from_html()`에서 사용 |
| `schema` | Pydantic `BaseModel` class | output contract |
| `cache_key` | parser cache의 논리 key | template family + version 권장 |
| `use_cached_code` | cache code 사용 여부 | `True` |
| `cookies_path` | Netscape-format cookie file | optional |
| `max_regenerate_attempts` | 실패 후 재생성 최대 횟수 | `1` |
| `validate_quality` | fresh code 결과의 LLM quality check | `True` |

## Generated Code Contract

```python
def extract_data(html_content):
    ...
    return {"items": [...]}
```

- 정확한 함수 signature 필요
- `dict` 반환 필요
- AST와 import allowlist 검사
- 허용 import: 문서상 stdlib, `requests`, `bs4`, `pydantic`
- code execution timeout: 30초
- 반환 `dict`는 public API에서 Pydantic model로 validation

## Cache Key Pattern

```text
{site-or-task}:{template}:{viewport}:{locale}:v{n}

shop:product-detail:desktop:ko-KR:v3
```

URL마다 다른 key를 쓰기보다 같은 DOM template끼리 공유한다. secret, cookie, personal identifier는 key에 넣지 않는다.

## Validation Layers

```text
AST/import check
      ↓
runtime + timeout
      ↓
Pydantic shape/type/constraint
      ↓
domain invariant + source evidence  ← 직접 추가
```

```python
assert result.items
assert all(item.price >= 0 for item in result.items)
assert all(item.title in html for item in result.items)
```

## Troubleshooting

| 문제 | 먼저 확인할 것 |
|---|---|
| JS content 없음 | Playwright `page.content()` → `extract_from_html()` |
| stale/empty output | DOM drift, cache key version, minimum list constraint |
| repeated LLM cost | cache hit ratio, key/schema 안정성, regeneration count |
| wrong but type-valid value | domain invariant, source snippet, fixture test |
| generated code risk | container, non-root, read-only FS, egress/CPU/memory limit |
| 401/403 | cookie/fetch 계층; regeneration으로 해결하지 않기 |

## Decision Shortcut

```text
render/navigation 필요? ─ Yes → Playwright/Crawl4AI/Firecrawl upstream
          │ No
반복 template인가? ───── No  → direct LLM/semantic extractor 검토
          │ Yes
generated code 격리 가능? No  → manual CSS/XPath parser
          │ Yes
                       Hikugen PoC
```

## Sources

- [Hikugen PyPI](https://pypi.org/project/hikugen/)
- [Hikugen Architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)

