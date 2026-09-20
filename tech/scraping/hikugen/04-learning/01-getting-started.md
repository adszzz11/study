---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen Getting Started

> [[03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

고정 HTML에서 상품 목록을 Pydantic model로 추출하고, 같은 `cache_key`의 generated parser를 재사용한다.

## Requirements

- Python `3.11+`
- OpenRouter API key
- 외부 URL 대신 시작하기에 사용할 작은 HTML fixture

```bash
uv init hikugen-lab
cd hikugen-lab
uv add hikugen
export OPENROUTER_API_KEY="..."
```

`pip install hikugen`도 가능하지만 재현성을 위해 package version과 lockfile을 함께 관리한다.

## Define the Schema

```python
from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(description="상품 카드에 표시된 상품명")
    price_krw: int = Field(
        ge=0,
        description="통화 기호와 쉼표를 제거한 현재 가격, 한국 원화 정수",
    )
    in_stock: bool = Field(description="현재 구매 가능 여부")


class ProductPage(BaseModel):
    products: list[Product] = Field(description="페이지에 있는 모든 상품 카드")
```

`description`은 문서 장식이 아니라 code generation prompt에 전달되는 semantic hint다. 이름이 모호한 field일수록 source, unit, normalization rule을 명시한다.

## Extract from HTML

```python
import os

from hikugen import HikuExtractor


html = """
<main>
  <article class="product">
    <h2>기계식 키보드</h2>
    <span class="price">₩129,000</span>
    <span class="stock">재고 있음</span>
  </article>
  <article class="product">
    <h2>USB-C 허브</h2>
    <span class="price">₩49,900</span>
    <span class="stock sold-out">품절</span>
  </article>
</main>
"""

extractor = HikuExtractor(
    api_key=os.environ["OPENROUTER_API_KEY"],
    model="google/gemini-2.5-flash",
)

result = extractor.extract_from_html(
    html_content=html,
    cache_key="shop-product-list:v1",
    schema=ProductPage,
)

for product in result.products:
    print(product.model_dump())
```

예상 shape:

```python
{"name": "기계식 키보드", "price_krw": 129000, "in_stock": True}
{"name": "USB-C 허브", "price_krw": 49900, "in_stock": False}
```

값은 LLM이나 parser 결과에 따라 달라질 수 있으므로 예상 output을 guarantee로 취급하지 않는다.

## Extract from URL

단순 HTTP fetch로 충분한 page라면 `extract()`를 쓴다.

```python
result = extractor.extract(
    url="https://example.com/products",
    schema=ProductPage,
    cache_key="example-products:v1",
    use_cached_code=True,
    max_regenerate_attempts=1,
    validate_quality=True,
)
```

authenticated request는 Netscape-format cookie file을 `cookies_path`로 전달할 수 있다. login flow 자체는 Hikugen의 역할이 아니다.

## Cache Lifecycle

같은 page template에는 안정된 논리 key를 사용한다. URL마다 key를 만들면 같은 parser를 재사용할 기회를 잃고, 서로 다른 template에 key를 공유하면 잘못된 parser가 실행될 수 있다.

```python
# DOM template 변경 후 해당 key의 code 제거
deleted = extractor.clear_cache_for_key("shop-product-list:v1")
print(f"deleted={deleted}")

# 개발 환경에서 전체 초기화
total = extractor.clear_all_cache()
print(f"deleted_total={total}")
```

운영에서는 삭제보다 `shop-product-list:v2`처럼 versioned key가 rollback과 비교에 유리하다.

## First-run Checklist

- [ ] 실제 page가 아닌 작은 fixture로 schema와 field description을 먼저 검증한다.
- [ ] 첫 실행은 `validate_quality=True`로 생성 결과를 관찰한다.
- [ ] 두 번째 실행에서 같은 key/schema의 cache reuse를 확인한다.
- [ ] field 누락, 잘못된 가격, empty list를 test assertion으로 만든다.
- [ ] schema를 바꿔 schema hash별 parser 분리를 확인한다.
- [ ] DOM fixture를 변경해 regeneration/cache invalidation 절차를 연습한다.
- [ ] generated code는 격리된 개발 환경에서만 먼저 실행한다.

## Common Problems

| 증상 | 가능한 원인 | 대응 |
|---|---|---|
| API request 실패 | key/model identifier/credit 문제 | OpenRouter 설정과 model availability 확인 |
| Pydantic validation error | field 의미 불명확 또는 parser bug | `Field(description=...)` 강화, regeneration error 확인 |
| 오래된 값/빈 결과 | cached parser와 DOM drift | fixture 비교 후 cache key version 증가 |
| JS content 누락 | HTTP response에 rendered content 없음 | Playwright로 render 후 `extract_from_html()` 사용 |
| 매번 LLM 호출 | key/schema가 계속 변하거나 extraction 실패 | cache naming과 validation log 점검 |

## Sources

- [Hikugen PyPI — Quick Start and parameters](https://pypi.org/project/hikugen/)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [OpenRouter documentation](https://openrouter.ai/docs)

