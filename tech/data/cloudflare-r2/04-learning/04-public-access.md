# 퍼블릭 액세스 및 Custom Domain

## 퍼블릭 액세스 개요

R2 버킷의 파일을 공개적으로 제공하는 방법은 두 가지입니다:

```
┌─────────────────────────────────────────────────────────────┐
│                    퍼블릭 액세스 방법                        │
│                                                              │
│  1. R2.dev 서브도메인                                        │
│     https://pub-xxxxx.r2.dev/path/to/file                   │
│     └── 빠른 설정, Cloudflare 제공 도메인                    │
│                                                              │
│  2. Custom Domain                                            │
│     https://cdn.yourdomain.com/path/to/file                 │
│     └── 자체 도메인, 브랜딩, Cache Rules 적용 가능          │
└─────────────────────────────────────────────────────────────┘
```

---

## R2.dev 퍼블릭 URL 설정

### 대시보드에서 활성화

```
1. Cloudflare 대시보드 → R2
2. 버킷 선택 → Settings 탭
3. Public access 섹션
4. "Allow Access" 또는 "R2.dev subdomain" 활성화
5. 확인 체크박스 선택 → Enable
```

### URL 구조

```
https://pub-<BUCKET_UNIQUE_ID>.r2.dev/<OBJECT_KEY>

예시:
https://pub-a1b2c3d4e5f6.r2.dev/images/photo.jpg
https://pub-a1b2c3d4e5f6.r2.dev/documents/report.pdf
```

### 제한사항

```
R2.dev 퍼블릭 URL 제한:
├── Cloudflare CDN 캐싱 제한적
├── 사용자 정의 Cache 규칙 불가
├── Rate Limiting 기본값 적용
├── 커스텀 응답 헤더 불가
└── 브랜딩/도메인 일관성 부족
```

---

## Custom Domain 설정

### 사전 요구사항

```
필수 조건:
├── Cloudflare에 등록된 도메인
│   (또는 NS 레코드가 Cloudflare로 설정된 도메인)
├── R2 버킷 생성 완료
└── Workers 유료 플랜 (무료 플랜도 가능하지만 제한)
```

### 대시보드에서 설정

```
1. R2 → 버킷 선택 → Settings 탭

2. Custom Domains 섹션 → "Connect Domain" 클릭

3. 도메인 입력:
   ├── 서브도메인: cdn.yourdomain.com
   ├── 또는 전체: storage.yourdomain.com
   └── 또는 경로 기반: yourdomain.com/storage

4. DNS 레코드 자동 생성 확인

5. "Connect Domain" 클릭

6. SSL 인증서 자동 프로비저닝 (몇 분 소요)
```

### DNS 설정 확인

```
자동 생성되는 DNS 레코드:

타입: CNAME
이름: cdn (cdn.yourdomain.com)
대상: <bucket-name>.<account-id>.r2.cloudflarestorage.com
프록시: 활성화 (주황색 구름)
```

### URL 구조

```
Custom Domain 설정 후:

https://cdn.yourdomain.com/<OBJECT_KEY>

예시:
https://cdn.yourdomain.com/images/photo.jpg
https://cdn.yourdomain.com/videos/intro.mp4
```

---

## Cache Rules 설정

Custom Domain을 사용하면 Cloudflare Cache Rules를 적용할 수 있습니다.

### 대시보드에서 Cache Rules

```
1. 도메인 선택 → Rules → Cache Rules

2. "Create rule" 클릭

3. Rule 설정:
   ├── Rule name: R2 Static Assets Cache
   ├── When: (hostname eq "cdn.yourdomain.com")
   ├── Then:
   │   ├── Cache eligibility: Eligible for cache
   │   ├── Edge TTL: 30 days
   │   └── Browser TTL: 7 days
   └── Deploy
```

### 파일 타입별 캐시 설정

```
규칙 1: 이미지 - 장기 캐시
├── When: (http.request.uri.path.extension in {"jpg" "jpeg" "png" "gif" "webp" "svg"})
├── Edge TTL: 365 days
└── Browser TTL: 30 days

규칙 2: CSS/JS - 중기 캐시
├── When: (http.request.uri.path.extension in {"css" "js"})
├── Edge TTL: 30 days
└── Browser TTL: 7 days

규칙 3: 문서 - 단기 캐시
├── When: (http.request.uri.path.extension in {"pdf" "doc" "docx"})
├── Edge TTL: 1 day
└── Browser TTL: 1 hour
```

---

## 보안 설정

### CORS 설정

```json
// 대시보드 → R2 → 버킷 → Settings → CORS Policy

[
  {
    "AllowedOrigins": [
      "https://yourdomain.com",
      "https://www.yourdomain.com"
    ],
    "AllowedMethods": [
      "GET",
      "HEAD"
    ],
    "AllowedHeaders": [
      "Content-Type",
      "Range"
    ],
    "ExposeHeaders": [
      "Content-Length",
      "Content-Range",
      "ETag"
    ],
    "MaxAgeSeconds": 86400
  }
]
```

### Hotlink Protection (핫링크 방지)

```
Cloudflare WAF Rules로 설정:

1. 도메인 → Security → WAF → Custom rules

2. Rule 설정:
   Name: Block Hotlinking
   When: (http.host eq "cdn.yourdomain.com") and
         (not http.referer contains "yourdomain.com") and
         (http.request.uri.path.extension in {"jpg" "png" "gif"})
   Then: Block
```

### 액세스 제한 (특정 경로)

```
민감한 파일 보호:

규칙: /private/ 경로 차단
When: (http.request.uri.path contains "/private/")
Then: Block

또는 Workers로 인증 구현
```

---

## Workers를 통한 Custom Domain

더 세밀한 제어가 필요하면 Workers를 통해 R2를 제공할 수 있습니다.

### Worker 코드

```typescript
// src/index.ts
interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    // 빈 경로 처리
    if (!key) {
      return new Response("Not Found", { status: 404 });
    }

    // 객체 가져오기
    const object = await env.MY_BUCKET.get(key);

    if (!object) {
      return new Response("Not Found", { status: 404 });
    }

    // 응답 헤더 설정
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("ETag", object.httpEtag);

    // 캐시 헤더 추가
    const extension = key.split('.').pop()?.toLowerCase();
    if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(extension || '')) {
      headers.set("Cache-Control", "public, max-age=31536000, immutable");
    } else if (['css', 'js'].includes(extension || '')) {
      headers.set("Cache-Control", "public, max-age=2592000");
    } else {
      headers.set("Cache-Control", "public, max-age=86400");
    }

    // CORS 헤더
    headers.set("Access-Control-Allow-Origin", "https://yourdomain.com");

    return new Response(object.body, { headers });
  },
};
```

### Custom Domain을 Worker에 연결

```
1. Workers & Pages → Worker 선택 → Settings → Triggers

2. Custom Domains → Add Custom Domain

3. 도메인 입력: cdn.yourdomain.com

4. 자동으로 DNS 레코드 생성 및 SSL 발급
```

---

## 실전 구성 예시

### 정적 웹사이트 호스팅

```
구조:
my-website-bucket/
├── index.html
├── about.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── images/
    ├── logo.png
    └── banner.jpg

Custom Domain: www.yourdomain.com
```

Worker 코드 (SPA 지원):
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    let key = url.pathname.slice(1) || "index.html";

    // 확장자 없으면 .html 추가
    if (!key.includes('.')) {
      key = key.endsWith('/') ? `${key}index.html` : `${key}.html`;
    }

    let object = await env.MY_BUCKET.get(key);

    // 404 시 index.html 반환 (SPA)
    if (!object && !key.match(/\.(css|js|png|jpg|gif|svg|ico)$/)) {
      object = await env.MY_BUCKET.get("index.html");
    }

    if (!object) {
      return new Response("Not Found", { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);

    return new Response(object.body, { headers });
  },
};
```

### CDN 구성 (멀티 버킷)

```typescript
interface Env {
  IMAGES_BUCKET: R2Bucket;
  VIDEOS_BUCKET: R2Bucket;
  DOCUMENTS_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;

    let bucket: R2Bucket;
    let key: string;

    if (path.startsWith("/images/")) {
      bucket = env.IMAGES_BUCKET;
      key = path.slice(8);
    } else if (path.startsWith("/videos/")) {
      bucket = env.VIDEOS_BUCKET;
      key = path.slice(8);
    } else if (path.startsWith("/docs/")) {
      bucket = env.DOCUMENTS_BUCKET;
      key = path.slice(6);
    } else {
      return new Response("Not Found", { status: 404 });
    }

    const object = await bucket.get(key);

    if (!object) {
      return new Response("Not Found", { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);

    return new Response(object.body, { headers });
  },
};
```

---

## 트러블슈팅

### 일반적인 문제

```
문제: SSL 인증서 오류
├── 원인: 인증서 프로비저닝 미완료
└── 해결: 몇 분 대기, DNS 프로파게이션 확인

문제: 403 Forbidden
├── 원인: 퍼블릭 액세스 비활성화
└── 해결: 버킷 Settings에서 Public access 확인

문제: 404 Not Found
├── 원인: 객체 키 불일치
└── 해결: 대소문자 확인, 경로 확인

문제: CORS 오류
├── 원인: CORS 정책 미설정
└── 해결: 버킷 CORS 설정 추가

문제: 캐시 안 됨
├── 원인: R2.dev는 캐시 제한적
└── 해결: Custom Domain 사용
```

### 캐시 퍼지

```bash
# Cloudflare API로 캐시 퍼지
curl -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/purge_cache" \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://cdn.yourdomain.com/path/to/file.jpg"]}'

# 전체 퍼지
curl -X POST "https://api.cloudflare.com/client/v4/zones/<ZONE_ID>/purge_cache" \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'
```

---

## 다음 단계

- [[05-lifecycle|라이프사이클 규칙]] - 자동 파일 관리
- [[06-sdk-integration|SDK 통합]] - 애플리케이션 통합
