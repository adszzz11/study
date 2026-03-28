---
date: 2025-01-18
tags:
  - tech
  - practice
  - http
  - cache
  - security
parent: "[[README]]"
---

# HTTP - 실무

> ⬅️ [[02-core|이전: 핵심]] | ➡️ [[04-advanced|다음: 고급]]

---

## 1. 캐시 (Cache)

### 캐시 동작 원리

```mermaid
flowchart TD
    A[요청] --> B{캐시 있음?}
    B -->|No| C[서버 요청]
    B -->|Yes| D{유효?}
    D -->|Yes| E[캐시 응답<br>304 Not Modified]
    D -->|No| F{조건부 요청}
    F --> G[서버 검증]
    G -->|변경됨| H[새 응답 + 캐시 갱신]
    G -->|동일| E
    C --> I[응답 + 캐시 저장]
```

### Cache-Control 헤더

| 디렉티브 | 설명 | 예시 |
|---------|------|------|
| `max-age` | 캐시 유효 시간 (초) | `max-age=3600` (1시간) |
| `no-cache` | 항상 서버 검증 필요 | 매번 조건부 요청 |
| `no-store` | 캐시 저장 금지 | 민감한 데이터 |
| `private` | 브라우저만 캐시 | 사용자별 데이터 |
| `public` | 공유 캐시 허용 | CDN 캐시 가능 |
| `must-revalidate` | 만료 후 반드시 검증 | 신선도 보장 |

```http
# 1시간 캐시, CDN 허용
Cache-Control: public, max-age=3600

# 매번 검증, 개인 데이터
Cache-Control: private, no-cache

# 캐시 금지 (민감 정보)
Cache-Control: no-store
```

### 조건부 요청

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: GET /image.png
    Server-->>Client: 200 OK<br>ETag: "abc123"<br>Last-Modified: Tue, 01 Jan 2025

    Note over Client: 캐시에 저장

    Client->>Server: GET /image.png<br>If-None-Match: "abc123"
    Server-->>Client: 304 Not Modified

    Client->>Server: GET /image.png<br>If-Modified-Since: Tue, 01 Jan 2025
    Server-->>Client: 304 Not Modified
```

| 요청 헤더 | 검증 방식 | 응답 헤더 |
|----------|----------|----------|
| `If-None-Match` | ETag 비교 | `ETag` |
| `If-Modified-Since` | 날짜 비교 | `Last-Modified` |

---

## 2. 쿠키 (Cookie)

### 쿠키 설정

```http
# 응답에서 쿠키 설정
Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure; SameSite=Lax

# 요청에서 쿠키 전송
Cookie: sessionId=abc123; userId=456
```

### 쿠키 속성

| 속성 | 설명 | 보안 영향 |
|------|------|----------|
| `HttpOnly` | JavaScript 접근 차단 | XSS 방어 |
| `Secure` | HTTPS만 전송 | 도청 방지 |
| `SameSite` | 크로스 사이트 제한 | CSRF 방어 |
| `Domain` | 쿠키 전송 도메인 | 범위 제한 |
| `Path` | 쿠키 전송 경로 | 범위 제한 |
| `Expires/Max-Age` | 만료 시간 | 수명 관리 |

### SameSite 옵션

```mermaid
graph TB
    subgraph "SameSite=Strict"
        S1[같은 사이트만 전송]
    end

    subgraph "SameSite=Lax (기본)"
        L1[같은 사이트 + 안전한 크로스 사이트<br>GET 링크 클릭 등]
    end

    subgraph "SameSite=None"
        N1[모든 크로스 사이트<br>Secure 필수]
    end
```

---

## 3. 인증

### 인증 방식 비교

| 방식 | 저장 위치 | 확장성 | 보안 |
|------|----------|--------|------|
| **Session** | 서버 | 낮음 | 높음 |
| **JWT** | 클라이언트 | 높음 | 중간 |
| **OAuth 2.0** | 외부 서버 | 높음 | 높음 |

### JWT 인증 흐름

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Resource

    Client->>Server: 1. POST /login (credentials)
    Server-->>Client: 2. JWT Token

    Note over Client: 토큰 저장

    Client->>Resource: 3. GET /api/data<br>Authorization: Bearer JWT
    Resource-->>Client: 4. Protected Data
```

### Authorization 헤더 형식

```http
# Basic 인증 (Base64)
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=

# Bearer 토큰 (JWT, OAuth)
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# API Key
X-API-Key: your-api-key-here
```

---

## 4. CORS (Cross-Origin Resource Sharing)

### CORS 필요성

```mermaid
graph LR
    subgraph "Same Origin"
        A1[https://example.com] --> B1[https://example.com/api]
    end

    subgraph "Cross Origin"
        A2[https://app.com] -->|CORS 필요| B2[https://api.com]
    end

    style A2 fill:#ff6b6b
    style B2 fill:#ff6b6b
```

### Preflight 요청

```mermaid
sequenceDiagram
    participant Browser
    participant Server

    Note over Browser,Server: 단순 요청 (Simple Request)
    Browser->>Server: GET /data<br>Origin: https://app.com
    Server-->>Browser: 200 OK<br>Access-Control-Allow-Origin: *

    Note over Browser,Server: Preflight 필요한 요청
    Browser->>Server: OPTIONS /data<br>Origin: https://app.com<br>Access-Control-Request-Method: POST
    Server-->>Browser: 204 No Content<br>Access-Control-Allow-Origin: https://app.com<br>Access-Control-Allow-Methods: POST

    Browser->>Server: POST /data<br>Origin: https://app.com
    Server-->>Browser: 200 OK
```

### CORS 헤더

| 헤더 | 설명 |
|------|------|
| `Access-Control-Allow-Origin` | 허용 출처 |
| `Access-Control-Allow-Methods` | 허용 메서드 |
| `Access-Control-Allow-Headers` | 허용 헤더 |
| `Access-Control-Allow-Credentials` | 인증 정보 허용 |
| `Access-Control-Max-Age` | Preflight 캐시 시간 |

---

## 5. 보안 헤더

### 주요 보안 헤더

```http
# XSS 방어
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'

# 클릭재킹 방어
X-Frame-Options: DENY

# MIME 스니핑 방지
X-Content-Type-Options: nosniff

# HTTPS 강제
Strict-Transport-Security: max-age=31536000; includeSubDomains

# Referrer 정책
Referrer-Policy: strict-origin-when-cross-origin
```

### Content-Security-Policy (CSP)

| 디렉티브 | 제어 대상 |
|---------|----------|
| `default-src` | 기본 정책 |
| `script-src` | JavaScript |
| `style-src` | CSS |
| `img-src` | 이미지 |
| `connect-src` | XHR, fetch, WebSocket |
| `frame-src` | iframe |

---

## 6. 실무 설정 예시

### Nginx 캐시 설정

```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /api/ {
    add_header Cache-Control "no-store";
}
```

### Spring Security 설정

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .headers(headers -> headers
            .frameOptions(frame -> frame.deny())
            .xssProtection(xss -> xss.disable())
            .contentSecurityPolicy(csp -> csp
                .policyDirectives("default-src 'self'"))
            .httpStrictTransportSecurity(hsts -> hsts
                .maxAgeInSeconds(31536000)
                .includeSubDomains(true))
        )
        .cors(cors -> cors.configurationSource(corsConfigurationSource()));
    return http.build();
}
```

### Express.js CORS 설정

```javascript
const cors = require('cors');

app.use(cors({
    origin: ['https://app.example.com'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400
}));
```

---

## 7. 체크리스트

### 실무 점검

- [ ] 정적 리소스 캐시 설정 (1년 + immutable)
- [ ] API 응답 캐시 정책 정의
- [ ] 쿠키 보안 속성 설정 (HttpOnly, Secure, SameSite)
- [ ] CORS 설정 검토
- [ ] CSP 헤더 설정
- [ ] HSTS 활성화

---

## 다음 단계

> [!tip] 다음으로
> 실무 기법을 익혔다면 [[04-advanced|고급]]에서 HTTP/2, HTTP/3를 학습하세요.

---

## References

- [MDN HTTP Caching](https://developer.mozilla.org/ko/docs/Web/HTTP/Caching)
- [MDN CORS](https://developer.mozilla.org/ko/docs/Web/HTTP/CORS)
- [OWASP Secure Headers](https://owasp.org/www-project-secure-headers/)
