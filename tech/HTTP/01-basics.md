---
date: 2025-01-18
tags:
  - tech
  - basics
  - http
  - network
parent: "[[README]]"
---

# HTTP - 기초

> ⬅️ [[README|목차로 돌아가기]] | ➡️ [[02-core|다음: 핵심]]

---

## 1. What - 개념 정의

> **한 줄 정의**: HTTP는 웹에서 하이퍼텍스트 문서를 전송하기 위한 애플리케이션 계층 프로토콜

### HTTP 특징

| 특징 | 설명 |
|------|------|
| **클라이언트-서버** | 요청-응답 모델 |
| **무상태(Stateless)** | 각 요청이 독립적 |
| **비연결성** | 요청 후 연결 종료 (Keep-Alive로 보완) |
| **텍스트 기반** | 사람이 읽을 수 있는 형식 |

### 핵심 용어

| 용어 | 설명 |
|------|------|
| **URL** | Uniform Resource Locator - 리소스 위치 |
| **URI** | Uniform Resource Identifier - 리소스 식별자 |
| **Request** | 클라이언트 → 서버 요청 |
| **Response** | 서버 → 클라이언트 응답 |
| **Header** | 요청/응답의 메타데이터 |
| **Body** | 실제 전송 데이터 |

---

## 2. URL 구조

```
https://user:pass@www.example.com:8080/path/to/resource?query=value#fragment
└─┬─┘  └───┬───┘ └──────┬──────┘└─┬─┘└──────┬───────┘└─────┬─────┘└───┬───┘
scheme  userinfo      host     port     path           query      fragment
```

| 구성요소 | 예시 | 설명 |
|---------|------|------|
| Scheme | `https` | 프로토콜 |
| Host | `www.example.com` | 서버 도메인/IP |
| Port | `8080` | 포트 (기본: HTTP 80, HTTPS 443) |
| Path | `/path/to/resource` | 리소스 경로 |
| Query | `?query=value` | 추가 파라미터 |
| Fragment | `#section` | 문서 내 위치 (서버 전송 X) |

---

## 3. 요청/응답 구조

### HTTP 요청 (Request)

```http
POST /api/users HTTP/1.1          ← 요청 라인
Host: api.example.com             ← 헤더 시작
Content-Type: application/json
Authorization: Bearer token123
                                  ← 빈 줄 (헤더 끝)
{"name": "Alice", "age": 30}      ← 본문 (Body)
```

```mermaid
graph LR
    subgraph "HTTP Request"
        A[Request Line] --> B[Headers]
        B --> C[Empty Line]
        C --> D[Body]
    end

    A1["GET /path HTTP/1.1"] --> A
    B1["Host: example.com<br>Content-Type: ..."] --> B
    D1["JSON, Form Data, etc."] --> D
```

### HTTP 응답 (Response)

```http
HTTP/1.1 200 OK                   ← 상태 라인
Content-Type: application/json    ← 헤더 시작
Content-Length: 42
Cache-Control: max-age=3600
                                  ← 빈 줄 (헤더 끝)
{"id": 1, "name": "Alice"}        ← 본문 (Body)
```

---

## 4. TCP/IP와 HTTP

### 네트워크 흐름

```mermaid
sequenceDiagram
    participant Client
    participant DNS
    participant Server

    Client->>DNS: 1. 도메인 조회
    DNS-->>Client: IP 주소 반환

    Note over Client,Server: TCP 3-Way Handshake
    Client->>Server: 2. SYN
    Server-->>Client: 3. SYN-ACK
    Client->>Server: 4. ACK

    Note over Client,Server: HTTP 통신
    Client->>Server: 5. HTTP Request
    Server-->>Client: 6. HTTP Response

    Note over Client,Server: TCP 연결 종료
    Client->>Server: 7. FIN
    Server-->>Client: 8. FIN-ACK
```

### TCP 3-Way Handshake

| 단계 | 방향 | 설명 |
|------|------|------|
| SYN | Client → Server | 연결 요청 |
| SYN-ACK | Server → Client | 연결 수락 + 요청 |
| ACK | Client → Server | 연결 확인 |

---

## 5. HTTP 버전 비교

```mermaid
timeline
    title HTTP 버전 역사
    1991 : HTTP/0.9 (GET만 지원)
    1996 : HTTP/1.0 (헤더, 상태코드)
    1997 : HTTP/1.1 (Keep-Alive, 파이프라이닝)
    2015 : HTTP/2 (멀티플렉싱, 헤더 압축)
    2022 : HTTP/3 (QUIC 기반, UDP)
```

| 버전 | 특징 | 연결 방식 |
|------|------|----------|
| **HTTP/1.0** | 요청마다 연결 생성 | 단일 요청-응답 |
| **HTTP/1.1** | Keep-Alive 기본 | 연결 재사용 |
| **HTTP/2** | 멀티플렉싱 | 하나의 연결로 병렬 처리 |
| **HTTP/3** | QUIC (UDP 기반) | 연결 설정 최소화 |

### HTTP/1.1 Keep-Alive

```http
GET /page HTTP/1.1
Host: example.com
Connection: keep-alive    ← 연결 유지 요청
Keep-Alive: timeout=5, max=100
```

---

## 6. HTTPS

### HTTP vs HTTPS

```mermaid
graph LR
    subgraph "HTTP"
        A1[Client] -->|평문| B1[Server]
    end

    subgraph "HTTPS"
        A2[Client] -->|암호화| TLS[TLS/SSL]
        TLS -->|암호화| B2[Server]
    end

    style TLS fill:#4ecdc4
```

| 항목 | HTTP | HTTPS |
|------|------|-------|
| 포트 | 80 | 443 |
| 암호화 | 없음 | TLS/SSL |
| 인증서 | 불필요 | 필요 |
| 속도 | 빠름 | TLS 오버헤드 |
| SEO | 불리 | 유리 |

### TLS Handshake

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: 1. Client Hello (지원 암호 목록)
    Server-->>Client: 2. Server Hello + 인증서
    Client->>Client: 3. 인증서 검증
    Client->>Server: 4. 암호화 키 교환
    Server-->>Client: 5. Finished
    Note over Client,Server: 암호화된 통신 시작
```

---

## 7. 체크리스트

### 이해도 확인

- [ ] URL 구성요소 설명 가능
- [ ] HTTP 요청/응답 구조 이해
- [ ] HTTP 무상태 특성 설명 가능
- [ ] TCP 3-Way Handshake 이해
- [ ] HTTP vs HTTPS 차이 설명 가능

---

## 다음 단계

> [!tip] 다음으로
> 기초를 이해했다면 [[02-core|핵심 개념]]에서 메서드와 상태코드를 학습하세요.

---

## References

- [MDN HTTP 개요](https://developer.mozilla.org/ko/docs/Web/HTTP/Overview)
- [RFC 7230 - HTTP/1.1](https://tools.ietf.org/html/rfc7230)
- [How HTTPS Works](https://howhttps.works/)
