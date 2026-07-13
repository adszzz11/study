---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차]] · [[cheatsheet|다음: Cheatsheet]]

## Project Map

| 단계 | 프로젝트 | 핵심 질문 | 완료 기준 |
|---|---|---|---|
| 1 | HTML fixture extractor | schema와 parser generation이 동작하는가? | 예상 model + cache reuse test 통과 |
| 2 | DOM drift lab | cached parser가 언제 깨지는가? | v1/v2 fixture와 invalidation runbook 작성 |
| 3 | Playwright pipeline | rendering과 extraction을 분리할 수 있는가? | JS page HTML을 typed data로 변환 |
| 4 | Hardened extraction worker | generated code를 어디서 실행할 것인가? | isolation, metric, rollback 조건 문서화 |

## 1. HTML Fixture Extractor

상품 카드 3개가 든 작은 HTML을 준비하고 [[04-learning/01-getting-started|Getting Started]]의 `ProductPage`를 적용한다.

### Tasks

- [ ] 정상 상품, 품절 상품, 할인 전/후 가격이 있는 fixture 작성
- [ ] unit과 normalization rule을 `Field(description=...)`에 명시
- [ ] 첫 실행 결과를 golden JSON으로 저장
- [ ] 같은 key로 두 번째 실행해 cache hit 확인
- [ ] `price_krw >= 0`, non-empty name 같은 domain assertion 추가

```python
def test_contract(result: ProductPage) -> None:
    assert result.products
    assert all(item.name.strip() for item in result.products)
    assert all(item.price_krw >= 0 for item in result.products)
```

API 호출이 들어가는 generation test와 cached parser contract test를 분리하면 일상 test의 비용과 변동성을 줄일 수 있다.

## 2. DOM Drift Lab

같은 정보를 다른 markup으로 표현한 `fixture-v2.html`을 만든다.

```html
<!-- v1 -->
<span class="price">₩49,900</span>

<!-- v2 -->
<data class="sale-price" value="49900">49,900원</data>
```

### Experiment

1. v1에서 `catalog:desktop:ko:v1` parser를 생성한다.
2. cached parser로 v2를 실행하고 failure mode를 기록한다.
3. cache 삭제와 `:v2` key 생성 방식을 각각 실험한다.
4. 두 parser의 output diff와 rollback 가능성을 비교한다.
5. empty result도 schema상 valid할 수 있는지 확인하고 minimum-length rule을 설계한다.

### Deliverables

- HTML fixture 두 개
- expected JSON 두 개
- cache invalidation decision table
- validation/regeneration log에서 secret과 personal data를 제거하는 규칙

## 3. Playwright + Hikugen

Hikugen이 맡지 않는 browser interaction을 upstream으로 분리한다.

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com/products")
    page.wait_for_load_state("networkidle")
    html = page.content()
    browser.close()

result = extractor.extract_from_html(
    html_content=html,
    cache_key="example-products:rendered:desktop:v1",
    schema=ProductPage,
)
```

### Design Rules

- browser worker는 navigation/rendering만, extraction worker는 HTML/schema 처리만 담당한다.
- login cookie나 token을 generated code execution 환경에 전달하지 않는다.
- raw HTML 저장 여부와 retention을 데이터 민감도에 따라 결정한다.
- desktop/mobile, locale별 markup이 다르면 cache key를 분리한다.

## 4. Hardened Extraction Worker

이 프로젝트는 library 기능 구현보다 **운영 경계 설계**가 목표다.

### Threat Model

- HTML의 prompt injection text
- generated code의 unexpected network request
- infinite loop, memory exhaustion, pathological parsing
- poisoned/tampered SQLite cache
- log에 포함되는 API key, cookie, personal data

### Acceptance Criteria

- [ ] ephemeral container와 non-root user 사용
- [ ] read-only filesystem, CPU/memory/wall-time limit 적용
- [ ] default-deny network egress 검증
- [ ] input HTML hash, schema hash, cache key, code hash를 audit log에 기록
- [ ] cache hit ratio와 regeneration/failure metric 수집
- [ ] failed parser artifact를 quarantine하고 known-good parser로 rollback
- [ ] robots.txt, Terms of Service, privacy/copyright checklist 완료

## Evaluation Scorecard

PoC 후 `1(나쁨)–5(좋음)`으로 평가한다.

| 항목 | 질문 | 점수 |
|---|---|---:|
| Accuracy | golden fixture와 실제 sample에서 값이 맞는가? | /5 |
| Reuse | cache hit가 충분하고 parser가 여러 URL에 재사용되는가? | /5 |
| Recovery | DOM drift가 발생해도 탐지·rollback 가능한가? | /5 |
| Cost | direct LLM extraction보다 총 token/cost가 낮은가? | /5 |
| Security | generated code execution risk를 격리했는가? | /5 |
| Maintainability | 작은 upstream project의 risk를 감당할 수 있는가? | /5 |

security가 3 미만이면 production 채택을 중단한다. 총점보다 workload 적합성과 failure containment가 중요하다.

## Sources

- [Hikugen PyPI](https://pypi.org/project/hikugen/)
- [Hikugen Architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md)
- [Playwright Python documentation](https://playwright.dev/python/)
- [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/)

