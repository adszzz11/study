# API 연동 가이드

## 1. 개요

본 문서는 Konda 프로젝트의 API 연동 방식을 정의합니다. App이 BE(비금융)와 BE(금융)를 각각 호출하며, 두 BE 간 직접 통신도 필요 시 발생할 수 있습니다.

---

## 2. API 아키텍처

### 2.1 전체 구조

```
┌─────────────────────────────────────────────────────────────┐
│                       Konda App                              │
│                    (iOS / Android)                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│   BE - 비금융 API    │    │    BE - 금융 API     │
│     (외주사)         │    │      (내부)          │
│                     │    │                     │
│  • 사용자 관리       │    │  • 계좌 조회         │
│  • 콘텐츠 API       │    │  • 거래 내역         │
│  • 일반 서비스       │    │  • 결제 처리         │
│                     │    │  • 자산 관리         │
└─────────────────────┘    └─────────────────────┘
          │                           │
          └───────── ↔ ───────────────┘
            (필요 시 직접 통신 가능)
```

### 2.2 API 연동 방식

| 연동 | 방식 | 설명 |
|------|------|------|
| App ↔ BE(비금융) | REST API | HTTPS 직접 통신 |
| App ↔ BE(금융) | REST API | HTTPS 직접 통신 |
| BE(비금융) ↔ BE(금융) | REST API | 필요 시 직접 통신 |

### 2.3 필요 시 연동

비금융 데이터와 금융 데이터를 함께 사용해야 하는 경우:

```
1. App에서 BE(비금융) API 호출
2. App에서 BE(금융) API 호출
3. App에서 두 응답 조합하여 화면 표시
```

---

## 3. API 명세서 작성 가이드

### 3.1 명세서 형식

OpenAPI (Swagger) 3.0 형식을 권장합니다.

```yaml
openapi: 3.0.0
info:
  title: Konda API
  version: 1.0.0
  description: Konda 비금융 API

servers:
  - url: https://api.konda.com/v1
    description: Production
  - url: https://api-staging.konda.com/v1
    description: Staging

paths:
  /users/{userId}:
    get:
      summary: 사용자 정보 조회
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 성공
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: 사용자 없음

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
```

### 3.2 API 문서 위치

- GitHub Wiki 또는 별도 API 문서 페이지
- Swagger UI 제공 (개발/스테이징 환경)

### 3.3 API 명세 항목

| 항목 | 설명 | 필수 |
|------|------|------|
| Endpoint | API 경로 | O |
| Method | HTTP 메서드 | O |
| Description | 기능 설명 | O |
| Request Parameters | 요청 파라미터 | O |
| Request Body | 요청 본문 (POST/PUT) | △ |
| Response | 응답 형식 및 예시 | O |
| Error Codes | 에러 코드 및 메시지 | O |
| Authentication | 인증 방식 | O |

---

## 4. API 설계 원칙

### 4.1 URL 설계

```
# 리소스 기반 URL
GET    /users           # 사용자 목록
GET    /users/{id}      # 특정 사용자
POST   /users           # 사용자 생성
PUT    /users/{id}      # 사용자 수정
DELETE /users/{id}      # 사용자 삭제

# 중첩 리소스
GET    /users/{id}/posts         # 사용자의 게시물 목록
GET    /users/{id}/posts/{postId} # 특정 게시물

# 버전 관리
/v1/users
/v2/users
```

### 4.2 HTTP 메서드

| 메서드 | 용도 | 멱등성 |
|--------|------|--------|
| GET | 조회 | O |
| POST | 생성 | X |
| PUT | 전체 수정 | O |
| PATCH | 부분 수정 | X |
| DELETE | 삭제 | O |

### 4.3 응답 형식

#### 성공 응답
```json
{
  "success": true,
  "data": {
    "id": "user_123",
    "name": "홍길동",
    "email": "hong@example.com"
  }
}
```

#### 목록 응답 (페이지네이션)
```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "totalItems": 150,
      "totalPages": 8
    }
  }
}
```

#### 에러 응답
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "사용자를 찾을 수 없습니다.",
    "details": {}
  }
}
```

### 4.4 HTTP 상태 코드

| 코드 | 의미 | 사용 상황 |
|------|------|----------|
| 200 | OK | 성공 (조회, 수정) |
| 201 | Created | 성공 (생성) |
| 204 | No Content | 성공 (삭제) |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 권한 없음 |
| 404 | Not Found | 리소스 없음 |
| 409 | Conflict | 충돌 (중복 등) |
| 500 | Internal Server Error | 서버 오류 |

---

## 5. API 버전 관리

### 5.1 버전 정책

- URL 경로에 버전 포함: `/v1/`, `/v2/`
- 메이저 변경 시 새 버전 생성
- 이전 버전은 최소 3개월 유지 후 deprecation

### 5.2 버전 변경 기준

| 변경 유형 | 버전 변경 |
|----------|----------|
| 필드 추가 (optional) | 버전 유지 |
| 필드 삭제 | 메이저 버전 증가 |
| 필드 타입 변경 | 메이저 버전 증가 |
| 엔드포인트 삭제 | 메이저 버전 증가 |
| 새 엔드포인트 추가 | 버전 유지 |

### 5.3 Deprecation 알림

```
1. 3개월 전 deprecation 예고 (문서 + Slack)
2. 1개월 전 최종 알림
3. 이전 버전 종료
```

---

## 6. 인증/인가

### 6.1 인증 방식

| 영역 | 인증 방식 | 토큰 위치 |
|------|----------|----------|
| BE(비금융) | JWT Bearer Token | Authorization Header |
| BE(금융) | JWT Bearer Token | Authorization Header |

### 6.2 토큰 형식

```
Authorization: Bearer <access_token>
```

### 6.3 토큰 갱신

```
1. Access Token 만료 시
2. Refresh Token으로 새 Access Token 발급
3. 새 토큰으로 재요청
```

---

## 7. 에러 코드 체계

### 7.1 에러 코드 형식

```
[영역]_[에러유형]

예시:
- AUTH_TOKEN_EXPIRED
- USER_NOT_FOUND
- PAYMENT_INSUFFICIENT_BALANCE
```

### 7.2 공통 에러 코드

| 코드 | HTTP | 설명 |
|------|------|------|
| INVALID_REQUEST | 400 | 잘못된 요청 형식 |
| VALIDATION_ERROR | 400 | 유효성 검사 실패 |
| AUTH_REQUIRED | 401 | 인증 필요 |
| AUTH_TOKEN_EXPIRED | 401 | 토큰 만료 |
| ACCESS_DENIED | 403 | 접근 권한 없음 |
| RESOURCE_NOT_FOUND | 404 | 리소스 없음 |
| CONFLICT | 409 | 리소스 충돌 |
| INTERNAL_ERROR | 500 | 서버 내부 오류 |

---

## 8. API 개발 협업

### 8.1 API 변경 프로세스

```
1. API 변경 필요성 논의 (Slack #proj-konda-dev)
2. API 명세 초안 작성
3. App 팀과 리뷰
4. 명세 확정
5. 개발 및 배포
6. App 팀에 알림
```

### 8.2 API 변경 알림 형식

```markdown
**[API 변경 알림]**

## 변경 유형
- [ ] 신규 API
- [ ] API 수정
- [ ] API 삭제 예정 (Deprecation)

## 변경 내용
- 엔드포인트: `GET /api/v1/users`
- 변경 사항: [상세 설명]

## 영향 범위
- App: [영향 있음/없음]
- 필요 조치: [App에서 해야 할 작업]

## 배포 일정
- 스테이징: YYYY-MM-DD
- 프로덕션: YYYY-MM-DD

@App개발팀
```

---

## 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|-------|----------|
| 1.0 | YYYY-MM-DD | [작성자] | 최초 작성 |
