# Workers와 R2 바인딩

## 개요

Cloudflare Workers는 엣지에서 실행되는 서버리스 함수입니다. R2와 바인딩을 통해 직접 연결되어 S3 API보다 빠르고 효율적으로 파일에 접근할 수 있습니다.

### 아키텍처

```
┌─────────┐     ┌─────────────────────────────────────────┐
│ Client  │────▶│         Cloudflare Edge Location        │
└─────────┘     │  ┌─────────────────┐    ┌───────────┐  │
                │  │    Workers      │◀──▶│    R2     │  │
                │  │ (서버리스 코드)  │    │ (스토리지) │  │
                │  └─────────────────┘    └───────────┘  │
                │         │                              │
                │         ▼ 바인딩 (내부 연결)            │
                │    빠른 접근, 네트워크 비용 없음        │
                └─────────────────────────────────────────┘
```

---

## 프로젝트 설정

### Wrangler CLI 설치

```bash
# npm
npm install -g wrangler

# 또는 프로젝트별
npm install --save-dev wrangler

# Cloudflare 로그인
wrangler login
```

### 새 프로젝트 생성

```bash
# 프로젝트 생성
wrangler init my-r2-worker

# 프롬프트 응답:
# - Would you like to use TypeScript? Yes
# - Would you like to create a Worker at src/index.ts? Yes
# - Would you like us to write your first test? No

cd my-r2-worker
```

### wrangler.toml 설정

```toml
name = "my-r2-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# R2 버킷 바인딩
[[r2_buckets]]
binding = "MY_BUCKET"  # 코드에서 사용할 이름
bucket_name = "my-actual-bucket"  # 실제 R2 버킷 이름

# 여러 버킷 바인딩 가능
[[r2_buckets]]
binding = "BACKUP_BUCKET"
bucket_name = "backup-bucket"

# 개발용 미리보기 버킷 (선택)
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-actual-bucket"
preview_bucket_name = "my-dev-bucket"
```

---

## R2 바인딩 API

### 타입 정의

```typescript
// src/index.ts
export interface Env {
  MY_BUCKET: R2Bucket;
}

// R2Bucket 주요 메서드
interface R2Bucket {
  put(key: string, value: ReadableStream | ArrayBuffer | string, options?: R2PutOptions): Promise<R2Object>;
  get(key: string, options?: R2GetOptions): Promise<R2ObjectBody | null>;
  head(key: string): Promise<R2Object | null>;
  delete(key: string | string[]): Promise<void>;
  list(options?: R2ListOptions): Promise<R2Objects>;
  createMultipartUpload(key: string, options?: R2MultipartOptions): Promise<R2MultipartUpload>;
}
```

### 기본 CRUD 작업

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1); // URL에서 키 추출

    switch (request.method) {
      case "PUT":
        return handlePut(request, env, key);
      case "GET":
        return handleGet(env, key);
      case "DELETE":
        return handleDelete(env, key);
      default:
        return new Response("Method Not Allowed", { status: 405 });
    }
  },
};

// 파일 업로드
async function handlePut(request: Request, env: Env, key: string): Promise<Response> {
  const object = await env.MY_BUCKET.put(key, request.body, {
    httpMetadata: {
      contentType: request.headers.get("content-type") || "application/octet-stream",
    },
  });

  return new Response(JSON.stringify({
    key: object.key,
    size: object.size,
    etag: object.etag,
  }), {
    headers: { "Content-Type": "application/json" },
  });
}

// 파일 다운로드
async function handleGet(env: Env, key: string): Promise<Response> {
  const object = await env.MY_BUCKET.get(key);

  if (!object) {
    return new Response("Not Found", { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("etag", object.httpEtag);

  return new Response(object.body, { headers });
}

// 파일 삭제
async function handleDelete(env: Env, key: string): Promise<Response> {
  await env.MY_BUCKET.delete(key);
  return new Response("Deleted", { status: 200 });
}
```

### 파일 목록 조회

```typescript
async function handleList(env: Env, request: Request): Promise<Response> {
  const url = new URL(request.url);
  const prefix = url.searchParams.get("prefix") || "";
  const cursor = url.searchParams.get("cursor") || undefined;

  const listed = await env.MY_BUCKET.list({
    prefix,
    cursor,
    limit: 100,
    delimiter: "/",
  });

  return new Response(JSON.stringify({
    objects: listed.objects.map(obj => ({
      key: obj.key,
      size: obj.size,
      uploaded: obj.uploaded,
    })),
    truncated: listed.truncated,
    cursor: listed.truncated ? listed.cursor : null,
    delimitedPrefixes: listed.delimitedPrefixes,
  }), {
    headers: { "Content-Type": "application/json" },
  });
}
```

---

## 실전 예제

### 이미지 서버

```typescript
// 이미지 업로드 및 제공
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;

    // POST /upload - 이미지 업로드
    if (request.method === "POST" && path === "/upload") {
      const formData = await request.formData();
      const file = formData.get("file") as File;

      if (!file) {
        return new Response("No file provided", { status: 400 });
      }

      // 이미지 타입 검증
      if (!file.type.startsWith("image/")) {
        return new Response("Only images allowed", { status: 400 });
      }

      // 고유 키 생성
      const key = `images/${Date.now()}-${file.name}`;

      await env.MY_BUCKET.put(key, file.stream(), {
        httpMetadata: {
          contentType: file.type,
        },
        customMetadata: {
          originalName: file.name,
          uploadedAt: new Date().toISOString(),
        },
      });

      return new Response(JSON.stringify({
        url: `${url.origin}/${key}`
      }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    // GET /images/* - 이미지 제공
    if (request.method === "GET" && path.startsWith("/images/")) {
      const key = path.slice(1);
      const object = await env.MY_BUCKET.get(key);

      if (!object) {
        return new Response("Image not found", { status: 404 });
      }

      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("Cache-Control", "public, max-age=31536000");

      return new Response(object.body, { headers });
    }

    return new Response("Not Found", { status: 404 });
  },
};
```

### 인증된 다운로드

```typescript
// JWT 기반 인증된 파일 다운로드
import { verify } from "@tsndr/cloudflare-worker-jwt";

interface Env {
  MY_BUCKET: R2Bucket;
  JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    // Authorization 헤더에서 토큰 추출
    const authHeader = request.headers.get("Authorization");
    if (!authHeader?.startsWith("Bearer ")) {
      return new Response("Unauthorized", { status: 401 });
    }

    const token = authHeader.slice(7);

    try {
      // JWT 검증
      const isValid = await verify(token, env.JWT_SECRET);
      if (!isValid) {
        return new Response("Invalid token", { status: 401 });
      }

      // 파일 제공
      const object = await env.MY_BUCKET.get(key);
      if (!object) {
        return new Response("Not Found", { status: 404 });
      }

      const headers = new Headers();
      object.writeHttpMetadata(headers);

      // 다운로드 강제
      headers.set("Content-Disposition", `attachment; filename="${key.split("/").pop()}"`);

      return new Response(object.body, { headers });
    } catch (e) {
      return new Response("Unauthorized", { status: 401 });
    }
  },
};
```

### 프록시 캐싱

```typescript
// R2를 원본으로 하는 캐시 프록시
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    // 캐시 키 생성
    const cacheKey = new Request(url.toString(), request);
    const cache = caches.default;

    // 캐시 확인
    let response = await cache.match(cacheKey);
    if (response) {
      return response;
    }

    // R2에서 가져오기
    const object = await env.MY_BUCKET.get(key);
    if (!object) {
      return new Response("Not Found", { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("Cache-Control", "public, max-age=86400"); // 24시간

    response = new Response(object.body, { headers });

    // 캐시에 저장 (비동기)
    ctx.waitUntil(cache.put(cacheKey, response.clone()));

    return response;
  },
};
```

---

## 고급 기능

### 조건부 요청 처리

```typescript
async function handleConditionalGet(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const ifNoneMatch = request.headers.get("If-None-Match");
  const ifModifiedSince = request.headers.get("If-Modified-Since");

  // head로 먼저 확인
  const objectHead = await env.MY_BUCKET.head(key);
  if (!objectHead) {
    return new Response("Not Found", { status: 404 });
  }

  // ETag 비교
  if (ifNoneMatch && objectHead.httpEtag === ifNoneMatch) {
    return new Response(null, { status: 304 });
  }

  // 수정 시간 비교
  if (ifModifiedSince) {
    const modifiedSince = new Date(ifModifiedSince);
    if (objectHead.uploaded <= modifiedSince) {
      return new Response(null, { status: 304 });
    }
  }

  // 전체 객체 반환
  const object = await env.MY_BUCKET.get(key);
  const headers = new Headers();
  object!.writeHttpMetadata(headers);
  headers.set("ETag", objectHead.httpEtag);
  headers.set("Last-Modified", objectHead.uploaded.toUTCString());

  return new Response(object!.body, { headers });
}
```

### Range 요청 (부분 다운로드)

```typescript
async function handleRangeRequest(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  const rangeHeader = request.headers.get("Range");

  if (!rangeHeader) {
    // 일반 요청
    const object = await env.MY_BUCKET.get(key);
    if (!object) return new Response("Not Found", { status: 404 });

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("Accept-Ranges", "bytes");
    return new Response(object.body, { headers });
  }

  // Range 파싱
  const match = rangeHeader.match(/bytes=(\d*)-(\d*)/);
  if (!match) {
    return new Response("Invalid Range", { status: 416 });
  }

  const objectHead = await env.MY_BUCKET.head(key);
  if (!objectHead) return new Response("Not Found", { status: 404 });

  const size = objectHead.size;
  let start = match[1] ? parseInt(match[1]) : 0;
  let end = match[2] ? parseInt(match[2]) : size - 1;

  // 범위 검증
  if (start >= size || end >= size) {
    return new Response("Range Not Satisfiable", {
      status: 416,
      headers: { "Content-Range": `bytes */${size}` }
    });
  }

  // Range 요청으로 가져오기
  const object = await env.MY_BUCKET.get(key, {
    range: { offset: start, length: end - start + 1 }
  });

  const headers = new Headers();
  object!.writeHttpMetadata(headers);
  headers.set("Content-Range", `bytes ${start}-${end}/${size}`);
  headers.set("Content-Length", String(end - start + 1));
  headers.set("Accept-Ranges", "bytes");

  return new Response(object!.body, { status: 206, headers });
}
```

### 멀티파트 업로드

```typescript
// 대용량 파일 멀티파트 업로드
async function handleMultipartUpload(
  request: Request,
  env: Env,
  key: string
): Promise<Response> {
  // 멀티파트 업로드 시작
  const multipartUpload = await env.MY_BUCKET.createMultipartUpload(key);

  const uploadedParts: R2UploadedPart[] = [];
  const reader = request.body!.getReader();
  let partNumber = 1;
  const PART_SIZE = 10 * 1024 * 1024; // 10MB
  let buffer = new Uint8Array(0);

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (value) {
        // 버퍼에 추가
        const newBuffer = new Uint8Array(buffer.length + value.length);
        newBuffer.set(buffer);
        newBuffer.set(value, buffer.length);
        buffer = newBuffer;
      }

      // 파트 크기에 도달하면 업로드
      while (buffer.length >= PART_SIZE) {
        const part = buffer.slice(0, PART_SIZE);
        buffer = buffer.slice(PART_SIZE);

        const uploadedPart = await multipartUpload.uploadPart(
          partNumber,
          part
        );
        uploadedParts.push(uploadedPart);
        partNumber++;
      }

      if (done) break;
    }

    // 남은 데이터 업로드
    if (buffer.length > 0) {
      const uploadedPart = await multipartUpload.uploadPart(
        partNumber,
        buffer
      );
      uploadedParts.push(uploadedPart);
    }

    // 멀티파트 완료
    const object = await multipartUpload.complete(uploadedParts);

    return new Response(JSON.stringify({
      key: object.key,
      size: object.size,
    }), {
      headers: { "Content-Type": "application/json" }
    });

  } catch (e) {
    // 실패 시 취소
    await multipartUpload.abort();
    throw e;
  }
}
```

---

## 개발 및 배포

### 로컬 개발

```bash
# 로컬 개발 서버 실행
wrangler dev

# R2 로컬 에뮬레이션
wrangler dev --local --persist

# 원격 R2 사용하며 개발
wrangler dev --remote
```

### 배포

```bash
# 프로덕션 배포
wrangler deploy

# 특정 환경으로 배포
wrangler deploy --env staging
```

### 환경별 설정

```toml
# wrangler.toml

[env.staging]
name = "my-r2-worker-staging"
[[env.staging.r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "staging-bucket"

[env.production]
name = "my-r2-worker"
[[env.production.r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "production-bucket"
```

---

## 다음 단계

- [[04-public-access|퍼블릭 액세스 설정]] - Custom Domain 연결
- [[05-lifecycle|라이프사이클 규칙]] - 자동화된 파일 관리
