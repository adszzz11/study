---
date: 2025-01-18
tags:
  - tech
  - core
  - http
  - methods
  - status-codes
parent: "[[README]]"
---

# HTTP - 핵심

> ⬅️ [[01-basics|이전: 기초]] | ➡️ [[03-practice|다음: 실무]]

---

## 1. HTTP 메서드

### 주요 메서드

| 메서드 | 목적 | 안전 | 멱등 | 요청 본문 | 응답 본문 |
|--------|------|------|------|----------|----------|
| **GET** | 조회 | ✅ | ✅ | ❌ | ✅ |
| **POST** | 생성 | ❌ | ❌ | ✅ | ✅ |
| **PUT** | 전체 수정 | ❌ | ✅ | ✅ | ✅ |
| **PATCH** | 부분 수정 | ❌ | ❌ | ✅ | ✅ |
| **DELETE** | 삭제 | ❌ | ✅ | ❌ | ❌ |
| **HEAD** | 헤더만 조회 | ✅ | ✅ | ❌ | ❌ |
| **OPTIONS** | 지원 메서드 조회 | ✅ | ✅ | ❌ | ✅ |

### 안전(Safe) vs 멱등(Idempotent)

```mermaid
graph TB
    subgraph "안전 (Safe)"
        GET[GET]
        HEAD[HEAD]
        OPTIONS[OPTIONS]
    end

    subgraph "멱등 (Idempotent)"
        GET2[GET]
        PUT[PUT]
        DELETE[DELETE]
    end

    subgraph "비멱등"
        POST[POST]
        PATCH[PATCH]
    end
```

- **안전**: 서버 상태를 변경하지 않음
- **멱등**: 여러 번 호출해도 결과가 동일

### 메서드 사용 예시

```http
# GET - 리소스 조회
GET /api/users/1 HTTP/1.1
Host: api.example.com

# POST - 리소스 생성
POST /api/users HTTP/1.1
Content-Type: application/json

{"name": "Alice", "email": "alice@example.com"}

# PUT - 전체 수정 (리소스 전체 교체)
PUT /api/users/1 HTTP/1.1
Content-Type: application/json

{"name": "Alice Updated", "email": "new@example.com", "age": 30}

# PATCH - 부분 수정
PATCH /api/users/1 HTTP/1.1
Content-Type: application/json

{"name": "Alice Updated"}

# DELETE - 삭제
DELETE /api/users/1 HTTP/1.1
```

---

## 2. 상태 코드

### 상태 코드 분류

```mermaid
pie title HTTP 상태 코드 분류
    "1xx 정보" : 1
    "2xx 성공" : 25
    "3xx 리다이렉션" : 15
    "4xx 클라이언트 오류" : 30
    "5xx 서버 오류" : 20
```

### 주요 상태 코드

#### 2xx 성공

| 코드 | 이름 | 설명 | 사용 케이스 |
|------|------|------|------------|
| **200** | OK | 성공 | GET 조회 성공 |
| **201** | Created | 생성됨 | POST 생성 성공 |
| **204** | No Content | 본문 없음 | DELETE 성공 |

#### 3xx 리다이렉션

| 코드 | 이름 | 설명 | 메서드 유지 |
|------|------|------|------------|
| **301** | Moved Permanently | 영구 이동 | ❌ (GET으로 변경) |
| **302** | Found | 임시 이동 | ❌ (GET으로 변경) |
| **304** | Not Modified | 캐시 사용 | - |
| **307** | Temporary Redirect | 임시 이동 | ✅ |
| **308** | Permanent Redirect | 영구 이동 | ✅ |

#### 4xx 클라이언트 오류

| 코드 | 이름 | 설명 |
|------|------|------|
| **400** | Bad Request | 잘못된 요청 문법 |
| **401** | Unauthorized | 인증 필요 |
| **403** | Forbidden | 권한 없음 (인증됨) |
| **404** | Not Found | 리소스 없음 |
| **405** | Method Not Allowed | 지원하지 않는 메서드 |
| **409** | Conflict | 충돌 (중복 등) |
| **422** | Unprocessable Entity | 유효성 검증 실패 |
| **429** | Too Many Requests | 요청 한도 초과 |

#### 5xx 서버 오류

| 코드 | 이름 | 설명 |
|------|------|------|
| **500** | Internal Server Error | 서버 내부 오류 |
| **502** | Bad Gateway | 게이트웨이 오류 |
| **503** | Service Unavailable | 서비스 이용 불가 |
| **504** | Gateway Timeout | 게이트웨이 타임아웃 |

### 401 vs 403

```mermaid
flowchart TD
    A[요청] --> B{인증됨?}
    B -->|No| C[401 Unauthorized<br>로그인 필요]
    B -->|Yes| D{권한 있음?}
    D -->|No| E[403 Forbidden<br>권한 부족]
    D -->|Yes| F[200 OK]
```

---

## 3. HTTP 헤더

### 헤더 분류

```mermaid
graph TB
    subgraph "General Headers"
        GH[Connection, Date, Cache-Control]
    end

    subgraph "Request Headers"
        RH[Host, Accept, Authorization, Cookie]
    end

    subgraph "Response Headers"
        RSH[Server, Set-Cookie, Location]
    end

    subgraph "Entity Headers"
        EH[Content-Type, Content-Length, Content-Encoding]
    end
```

### 주요 요청 헤더

| 헤더 | 설명 | 예시 |
|------|------|------|
| **Host** | 대상 서버 | `Host: api.example.com` |
| **Accept** | 원하는 응답 형식 | `Accept: application/json` |
| **Accept-Language** | 선호 언어 | `Accept-Language: ko-KR,en` |
| **Accept-Encoding** | 지원 압축 | `Accept-Encoding: gzip, br` |
| **Authorization** | 인증 정보 | `Authorization: Bearer token` |
| **Cookie** | 쿠키 전송 | `Cookie: session=abc123` |
| **User-Agent** | 클라이언트 정보 | `User-Agent: Mozilla/5.0...` |
| **Referer** | 이전 페이지 URL | `Referer: https://google.com` |

### 주요 응답 헤더

| 헤더 | 설명 | 예시 |
|------|------|------|
| **Content-Type** | 본문 타입 | `Content-Type: application/json` |
| **Content-Length** | 본문 크기 | `Content-Length: 1234` |
| **Content-Encoding** | 압축 방식 | `Content-Encoding: gzip` |
| **Location** | 리다이렉트 위치 | `Location: /new-path` |
| **Set-Cookie** | 쿠키 설정 | `Set-Cookie: session=xyz` |
| **Cache-Control** | 캐시 정책 | `Cache-Control: max-age=3600` |

### Content-Type 종류

| Content-Type | 용도 |
|--------------|------|
| `application/json` | JSON 데이터 |
| `application/x-www-form-urlencoded` | HTML 폼 데이터 |
| `multipart/form-data` | 파일 업로드 |
| `text/html` | HTML 문서 |
| `text/plain` | 일반 텍스트 |
| `application/octet-stream` | 바이너리 파일 |

---

## 4. 콘텐츠 협상 (Content Negotiation)

### 협상 흐름

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: GET /users<br>Accept: application/json
    Note over Server: JSON 형식으로 준비
    Server-->>Client: 200 OK<br>Content-Type: application/json

    Client->>Server: GET /users<br>Accept: text/xml
    Note over Server: XML 형식으로 준비
    Server-->>Client: 200 OK<br>Content-Type: text/xml
```

### Quality Value (q)

```http
Accept: text/html, application/json;q=0.9, */*;q=0.8
```

| 값 | 우선순위 |
|----|---------|
| `text/html` | 1.0 (기본) |
| `application/json;q=0.9` | 0.9 |
| `*/*;q=0.8` | 0.8 |

---

## 5. 연결 관리

### Keep-Alive

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Note over Client,Server: HTTP/1.0 (연결 매번 생성)
    Client->>Server: 요청 1
    Server-->>Client: 응답 1
    Note over Client,Server: 연결 종료
    Client->>Server: 요청 2
    Server-->>Client: 응답 2
    Note over Client,Server: 연결 종료

    Note over Client,Server: HTTP/1.1 (Keep-Alive)
    Client->>Server: 요청 1
    Server-->>Client: 응답 1
    Client->>Server: 요청 2
    Server-->>Client: 응답 2
    Client->>Server: 요청 3
    Server-->>Client: 응답 3
    Note over Client,Server: 연결 유지
```

### 파이프라이닝 vs 멀티플렉싱

```mermaid
graph LR
    subgraph "HTTP/1.1 파이프라이닝"
        direction TB
        R1[요청1] --> R2[요청2] --> R3[요청3]
        RS1[응답1] --> RS2[응답2] --> RS3[응답3]
    end

    subgraph "HTTP/2 멀티플렉싱"
        direction TB
        M1[요청1 + 응답1]
        M2[요청2 + 응답2]
        M3[요청3 + 응답3]
        M1 ~~~ M2
        M2 ~~~ M3
    end
```

---

## 6. 체크리스트

### 이해도 확인

- [ ] HTTP 메서드 5개 이상 설명 가능
- [ ] 안전/멱등 개념 이해
- [ ] 상태 코드 분류 (2xx, 3xx, 4xx, 5xx) 이해
- [ ] 401 vs 403 차이 설명 가능
- [ ] 주요 헤더 역할 이해
- [ ] Content-Type 종류 알고 있음

---

## 다음 단계

> [!tip] 다음으로
> 핵심 개념을 이해했다면 [[03-practice|실무 적용]]에서 캐시, 쿠키, 보안을 학습하세요.

---

## References

- [MDN HTTP 메서드](https://developer.mozilla.org/ko/docs/Web/HTTP/Methods)
- [HTTP Status Codes](https://httpstatuses.com/)
- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)
