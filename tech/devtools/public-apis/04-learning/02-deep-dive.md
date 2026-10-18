---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 견고한 API Client

## 호출 contract를 adapter로 감싸기

OpenAPI가 있으면 schema validation, mock, generated SDK의 입력으로 사용한다. 없으면 provider별 세부 사항을 내부 interface 뒤로 숨긴다.

```ts
type Page<T> = { items: T[]; nextCursor?: string };

interface WeatherProvider {
  forecast(latitude: number, longitude: number, cursor?: string): Promise<Page<unknown>>;
}
```

## Pagination, timeout, retry

- pagination/filter/sort의 query parameter와 `nextCursor` 규칙을 명시한다.
- 각 요청에 timeout을 둔다. timeout은 retry 가능한 transport failure와 구분한다.
- `429`와 일시적 `5xx`는 `Retry-After`가 있으면 우선 존중하고 exponential backoff + jitter를 적용한다.
- `POST`는 idempotency 보장이 없으면 자동 retry하지 않는다. provider가 지원하면 idempotency key를 사용한다.

```ts
const response = await fetch(url, { signal: AbortSignal.timeout(8_000) });
if (response.status === 429) {
  // Retry-After를 읽고, rate-limit budget을 소진하지 않도록 재시도한다.
}
if (!response.ok) throw new Error(`provider failed: ${response.status}`);
```

## Browser와 BFF

CORS는 browser의 Origin 기반 정책이다. provider가 필요한 origin/headers를 허용하지 않으면 frontend에서 직접 우회하지 말고 BFF를 둔다.

```text
Browser ── session auth ──> BFF ── provider secret ──> Public API
          response cache       timeout / retry / validation
```

## Production checklist

- [ ] timeout, structured error, correlation ID, metrics
- [ ] rate-limit budget, caching, circuit breaker
- [ ] schema drift와 deprecation 감시
- [ ] fallback provider 또는 graceful degradation
- [ ] ToS·data residency·retention 검토

## Sources

- https://spec.openapis.org/oas/
- https://www.rfc-editor.org/rfc/rfc9110
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
