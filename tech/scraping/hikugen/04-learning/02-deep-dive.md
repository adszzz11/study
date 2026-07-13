---
date: 2026-07-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Hikugen Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차]] · [[../05-projects|다음: Projects]]

## Execution Pipeline

```text
1. URL fetch 또는 pre-fetched HTML 입력
2. cache_key와 Pydantic JSON schema hash 계산
3. SQLite lookup
   ├─ hit  → cached code
   └─ miss → schema + HTML context로 OpenRouter code generation
4. AST/import/function/return validation
5. timeout이 적용된 extract_data(html_content) 실행
6. 반환 dict를 Pydantic model로 validation
7. fresh code라면 optional LLM quality validation
8. 실패 시 error feedback을 포함해 제한 횟수만큼 regeneration
```

이 pipeline에는 서로 다른 세 종류의 validation이 있다.

| 단계 | 보장하려는 것 | 보장하지 않는 것 |
|---|---|---|
| Static code validation | 허용 import, 요구 함수와 return 같은 code shape | runtime safety, syscall/network 차단 |
| Pydantic validation | output field, type, 선언한 constraint | source와 값의 사실성 |
| LLM quality check | fresh result의 의미적 plausibility | deterministic proof, cached run의 지속 검증 |

## Cache Identity

`HikuDatabase`는 `cache_key + SHA-256(Pydantic JSON schema)`를 복합 identity로 사용한다.

```text
(catalog:v1, hash(ProductListV1)) → parser A
(catalog:v1, hash(ProductListV2)) → parser B
(catalog:v2, hash(ProductListV2)) → parser C
```

### Good cache key

- URL 자체보다 **DOM template family**를 나타낸다.
- migration을 위해 `:v1`, `:v2` version suffix를 둔다.
- locale, mobile/desktop처럼 markup이 달라지는 축을 포함한다.
- tenant나 credential을 key에 직접 넣어 secret을 노출하지 않는다.

예: `store-product-detail:desktop:ko-KR:v3`

### Cache invalidation signal

Hikugen이 DOM drift를 자동 탐지하지 않으므로 외부 signal을 둔다.

- golden HTML fixture에서 contract test 실패
- extraction empty-rate 또는 validation error-rate 상승
- source selector/snippet fingerprint 변화
- 필수 field의 domain invariant 위반
- deploy된 frontend version 변경

## Regeneration Strategy

무제한 regeneration은 비용을 키우고 장애를 숨긴다. 기본 1회를 기준으로 오류를 분류한다.

| 오류 | regeneration 기대효과 | 더 나은 대응 |
|---|---:|---|
| parser syntax/runtime bug | 높음 | error feedback으로 1회 재생성 |
| 일부 selector drift | 중간 | 새 cache version + fixture test |
| HTTP 401/403/timeout | 낮음 | fetch/auth/network 계층 수정 |
| JS render 전 HTML | 낮음 | browser에서 rendered HTML 확보 |
| schema 자체가 모순 | 낮음 | model/constraint 수정 |
| source에 값이 없음 | 낮음 | optional field 또는 business rule 재설계 |

`max_regenerate_attempts`를 늘리기 전에 실패 class와 token spend를 log한다.

## Security Boundary

> [!danger] AST validation ≠ sandbox
> AST inspection, import allowlist, isolated namespace와 30초 timeout은 유용한 guardrail이지만 process/container isolation을 대신하지 않는다.

위험 경로는 **untrusted HTML → prompt context → generated code → local execution**이다. HTML 내부의 prompt-like text가 generation에 영향을 줄 수 있고, 허용된 library의 기능만으로도 network/file/resource abuse 가능성이 남을 수 있다. 특히 문서상 `requests` import가 허용되므로 egress가 원천 차단되었다고 볼 수 없다.

### Production hardening

```text
job queue
   ↓
ephemeral container / VM
   ├─ non-root user
   ├─ read-only root filesystem + isolated temp
   ├─ no secrets except scoped API credential
   ├─ default-deny egress; 필요한 host만 allow
   ├─ CPU / memory / process / wall-time limit
   └─ generated code + input hash + result audit log
```

- generation과 execution worker를 분리한다.
- generated code를 artifact로 보관하고 review/deny rule을 추가한다.
- application/database credential이 있는 host process에서 실행하지 않는다.
- cache DB를 executable artifact store로 보고 access와 integrity를 관리한다.
- malicious HTML, huge DOM, pathological regex/parser를 test corpus에 포함한다.

## Correctness Beyond Types

```python
def validate_product(product: Product, html: str) -> None:
    assert 0 <= product.price_krw <= 100_000_000
    assert product.name.strip()
    assert product.name in html
```

실전에서는 다음 evidence를 함께 저장하는 schema를 고려한다.

```python
class PriceEvidence(BaseModel):
    value_krw: int = Field(ge=0)
    source_text: str = Field(description="가격을 읽은 원문 snippet")
```

source snippet은 완전한 증명은 아니지만 hallucination과 normalization error를 추적하기 쉽게 한다. 가격, 날짜, currency, identifier에는 range, format, cross-field invariant를 추가한다.

## Observability

최소한 다음 metric/log를 수집한다.

| Signal | 이유 |
|---|---|
| cache hit ratio | amortization이 실제로 일어나는지 확인 |
| generation/regeneration count | DOM drift와 비용 증가 탐지 |
| Pydantic validation failure rate | parser/schema mismatch 탐지 |
| domain validation failure rate | type-correct but wrong value 탐지 |
| execution duration/timeout | pathological parser 탐지 |
| template/schema/code hash | 어느 artifact가 결과를 만들었는지 추적 |
| model identifier와 token usage | cost와 재현성 분석 |

HTML 원문과 extracted personal data를 log할 때는 privacy와 retention policy를 적용한다.

## Architecture Review Questions

- [ ] generated code를 누가 승인하고 어떤 환경에서 실행하는가?
- [ ] parser artifact와 input/output의 lineage를 재구성할 수 있는가?
- [ ] cache rollback과 invalidation 기준이 명시되어 있는가?
- [ ] schema validation 이후 domain validation이 있는가?
- [ ] LLM/provider 장애 때 cached parser만으로 계속할지 정책이 있는가?
- [ ] robots.txt, ToS, copyright, personal data 처리를 검토했는가?

## Sources

- [Hikugen Architecture](https://github.com/goncharom/hikugen/blob/master/CLAUDE.md#architecture)
- [Hikugen PyPI — workflow and execution constraints](https://pypi.org/project/hikugen/)
- [Python `ast` module](https://docs.python.org/3/library/ast.html)
- [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/)

