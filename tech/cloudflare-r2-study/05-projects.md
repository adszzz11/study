# 실전 프로젝트 & Best Practices

## 프로젝트 1: 이미지 호스팅 서비스

### 개요
사용자가 이미지를 업로드하고 최적화된 형태로 제공하는 서비스

### 아키텍처

```
┌─────────┐     ┌─────────────────────────────────────────────────┐
│ Client  │────▶│               Cloudflare Edge                   │
└─────────┘     │  ┌─────────────┐    ┌──────────────────────┐   │
                │  │   Worker    │───▶│         R2           │   │
                │  │ (리사이징)   │    │  ┌────────────────┐  │   │
                │  └─────────────┘    │  │ images/        │  │   │
                │         │           │  │ └─ original/   │  │   │
                │         ▼           │  │ └─ optimized/  │  │   │
                │  ┌─────────────┐    │  │ └─ thumbnails/ │  │   │
                │  │   Images    │    │  └────────────────┘  │   │
                │  │ (변환 API)  │    └──────────────────────┘   │
                │  └─────────────┘                               │
                └─────────────────────────────────────────────────┘
```

### 구현

```typescript
// wrangler.toml
// [[r2_buckets]]
// binding = "IMAGES"
// bucket_name = "image-hosting"

interface Env {
  IMAGES: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // POST /upload - 이미지 업로드
    if (request.method === "POST" && url.pathname === "/upload") {
      return handleUpload(request, env);
    }

    // GET /images/:id - 이미지 조회
    if (request.method === "GET" && url.pathname.startsWith("/images/")) {
      return handleGetImage(request, env, url);
    }

    return new Response("Not Found", { status: 404 });
  },
};

async function handleUpload(request: Request, env: Env): Promise<Response> {
  const formData = await request.formData();
  const file = formData.get("image") as File;

  if (!file || !file.type.startsWith("image/")) {
    return new Response("Invalid image", { status: 400 });
  }

  // 파일 크기 제한 (10MB)
  if (file.size > 10 * 1024 * 1024) {
    return new Response("File too large", { status: 400 });
  }

  const id = crypto.randomUUID();
  const ext = file.name.split(".").pop();
  const key = `original/${id}.${ext}`;

  await env.IMAGES.put(key, file.stream(), {
    httpMetadata: {
      contentType: file.type,
    },
    customMetadata: {
      originalName: file.name,
      uploadedAt: new Date().toISOString(),
    },
  });

  return new Response(
    JSON.stringify({
      id,
      url: `/images/${id}`,
      original: `/images/${id}?size=original`,
      thumbnail: `/images/${id}?size=thumbnail`,
    }),
    { headers: { "Content-Type": "application/json" } }
  );
}

async function handleGetImage(
  request: Request,
  env: Env,
  url: URL
): Promise<Response> {
  const id = url.pathname.split("/")[2];
  const size = url.searchParams.get("size") || "optimized";
  const width = url.searchParams.get("w");
  const format = url.searchParams.get("format") || "webp";

  // 원본 찾기
  let originalKey = await findOriginalKey(env, id);
  if (!originalKey) {
    return new Response("Not Found", { status: 404 });
  }

  // 캐시된 버전 확인
  let cacheKey: string;
  if (width) {
    cacheKey = `optimized/${id}_w${width}.${format}`;
  } else if (size === "thumbnail") {
    cacheKey = `thumbnails/${id}.${format}`;
  } else if (size === "original") {
    cacheKey = originalKey;
  } else {
    cacheKey = `optimized/${id}.${format}`;
  }

  let object = await env.IMAGES.get(cacheKey);

  if (!object && size !== "original") {
    // 원본 가져와서 변환 (Cloudflare Images 또는 자체 처리)
    const original = await env.IMAGES.get(originalKey);
    if (!original) {
      return new Response("Not Found", { status: 404 });
    }

    // 여기서 이미지 변환 로직 구현
    // 예: Cloudflare Images Transform API 사용
    // 간단 예시: 원본 반환
    object = original;
  }

  if (!object) {
    return new Response("Not Found", { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("Cache-Control", "public, max-age=31536000, immutable");

  return new Response(object.body, { headers });
}

async function findOriginalKey(env: Env, id: string): Promise<string | null> {
  const extensions = ["jpg", "jpeg", "png", "gif", "webp"];
  for (const ext of extensions) {
    const key = `original/${id}.${ext}`;
    const head = await env.IMAGES.head(key);
    if (head) return key;
  }
  return null;
}
```

### 라이프사이클 규칙

```json
{
  "rules": [
    {
      "id": "cleanup-temp-uploads",
      "conditions": { "prefix": "temp/" },
      "action": { "type": "DeleteObject", "deleteAfterDays": 1 }
    },
    {
      "id": "cleanup-old-thumbnails",
      "conditions": { "prefix": "thumbnails/" },
      "action": { "type": "DeleteObject", "deleteAfterDays": 30 }
    }
  ]
}
```

---

## 프로젝트 2: 파일 공유 서비스

### 개요
만료 기간이 있는 파일 공유 링크 생성 서비스

### 구현

```typescript
interface Env {
  FILES: R2Bucket;
  METADATA: KVNamespace;
}

interface FileMetadata {
  originalName: string;
  mimeType: string;
  size: number;
  expiresAt: number;
  downloads: number;
  maxDownloads?: number;
  password?: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    switch (true) {
      case request.method === "POST" && url.pathname === "/upload":
        return handleUpload(request, env);

      case request.method === "GET" && url.pathname.startsWith("/d/"):
        return handleDownload(request, env, url);

      case request.method === "GET" && url.pathname.startsWith("/info/"):
        return handleInfo(request, env, url);

      default:
        return new Response("Not Found", { status: 404 });
    }
  },

  // 만료된 파일 정리 (Cron Trigger)
  async scheduled(event: ScheduledEvent, env: Env) {
    await cleanupExpiredFiles(env);
  },
};

async function handleUpload(request: Request, env: Env): Promise<Response> {
  const formData = await request.formData();
  const file = formData.get("file") as File;
  const expiresIn = parseInt(formData.get("expiresIn") as string) || 24; // 시간
  const maxDownloads = formData.get("maxDownloads")
    ? parseInt(formData.get("maxDownloads") as string)
    : undefined;
  const password = formData.get("password") as string | null;

  if (!file) {
    return new Response("No file provided", { status: 400 });
  }

  // 파일 크기 제한 (100MB)
  if (file.size > 100 * 1024 * 1024) {
    return new Response("File too large (max 100MB)", { status: 400 });
  }

  const id = generateShortId();
  const key = `files/${id}`;

  // R2에 파일 저장
  await env.FILES.put(key, file.stream(), {
    httpMetadata: {
      contentType: file.type,
      contentDisposition: `attachment; filename="${file.name}"`,
    },
  });

  // 메타데이터 저장
  const metadata: FileMetadata = {
    originalName: file.name,
    mimeType: file.type,
    size: file.size,
    expiresAt: Date.now() + expiresIn * 60 * 60 * 1000,
    downloads: 0,
    maxDownloads,
    password: password ? await hashPassword(password) : undefined,
  };

  await env.METADATA.put(`file:${id}`, JSON.stringify(metadata), {
    expirationTtl: expiresIn * 60 * 60,
  });

  const baseUrl = new URL(request.url).origin;

  return new Response(
    JSON.stringify({
      id,
      downloadUrl: `${baseUrl}/d/${id}`,
      infoUrl: `${baseUrl}/info/${id}`,
      expiresAt: new Date(metadata.expiresAt).toISOString(),
    }),
    { headers: { "Content-Type": "application/json" } }
  );
}

async function handleDownload(
  request: Request,
  env: Env,
  url: URL
): Promise<Response> {
  const id = url.pathname.split("/")[2];
  const password = url.searchParams.get("password");

  // 메타데이터 확인
  const metadataStr = await env.METADATA.get(`file:${id}`);
  if (!metadataStr) {
    return new Response("File not found or expired", { status: 404 });
  }

  const metadata: FileMetadata = JSON.parse(metadataStr);

  // 만료 확인
  if (Date.now() > metadata.expiresAt) {
    await env.FILES.delete(`files/${id}`);
    await env.METADATA.delete(`file:${id}`);
    return new Response("File expired", { status: 410 });
  }

  // 다운로드 횟수 확인
  if (metadata.maxDownloads && metadata.downloads >= metadata.maxDownloads) {
    return new Response("Download limit reached", { status: 403 });
  }

  // 비밀번호 확인
  if (metadata.password) {
    if (!password || !(await verifyPassword(password, metadata.password))) {
      return new Response("Invalid password", { status: 401 });
    }
  }

  // 파일 가져오기
  const object = await env.FILES.get(`files/${id}`);
  if (!object) {
    return new Response("File not found", { status: 404 });
  }

  // 다운로드 카운트 증가
  metadata.downloads++;
  await env.METADATA.put(`file:${id}`, JSON.stringify(metadata));

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set(
    "Content-Disposition",
    `attachment; filename="${metadata.originalName}"`
  );

  return new Response(object.body, { headers });
}

async function handleInfo(
  request: Request,
  env: Env,
  url: URL
): Promise<Response> {
  const id = url.pathname.split("/")[2];
  const metadataStr = await env.METADATA.get(`file:${id}`);

  if (!metadataStr) {
    return new Response("File not found", { status: 404 });
  }

  const metadata: FileMetadata = JSON.parse(metadataStr);

  return new Response(
    JSON.stringify({
      originalName: metadata.originalName,
      size: metadata.size,
      mimeType: metadata.mimeType,
      expiresAt: new Date(metadata.expiresAt).toISOString(),
      downloads: metadata.downloads,
      maxDownloads: metadata.maxDownloads,
      hasPassword: !!metadata.password,
    }),
    { headers: { "Content-Type": "application/json" } }
  );
}

async function cleanupExpiredFiles(env: Env): Promise<void> {
  const listed = await env.FILES.list({ prefix: "files/" });

  for (const obj of listed.objects) {
    const id = obj.key.replace("files/", "");
    const metadataStr = await env.METADATA.get(`file:${id}`);

    if (!metadataStr) {
      // 메타데이터 없으면 삭제
      await env.FILES.delete(obj.key);
    }
  }
}

function generateShortId(): string {
  const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let result = "";
  for (let i = 0; i < 8; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

async function hashPassword(password: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return btoa(String.fromCharCode(...new Uint8Array(hash)));
}

async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  const inputHash = await hashPassword(password);
  return inputHash === hash;
}
```

---

## 프로젝트 3: 정적 사이트 + API

### 개요
R2를 정적 파일 호스팅으로, Workers를 API로 사용하는 풀스택 구성

### 폴더 구조

```
my-project/
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── css/
│   │   └── js/
│   └── package.json
├── worker/
│   ├── src/
│   │   └── index.ts
│   ├── wrangler.toml
│   └── package.json
└── deploy.sh
```

### Worker 구현

```typescript
// worker/src/index.ts
interface Env {
  STATIC: R2Bucket;
  DATA: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // API 라우트
    if (url.pathname.startsWith("/api/")) {
      return handleAPI(request, env, url);
    }

    // 정적 파일 제공
    return handleStatic(request, env, url);
  },
};

async function handleStatic(
  request: Request,
  env: Env,
  url: URL
): Promise<Response> {
  let key = url.pathname.slice(1) || "index.html";

  // 확장자 없으면 HTML 시도
  if (!key.includes(".")) {
    key = key.endsWith("/") ? `${key}index.html` : `${key}.html`;
  }

  const object = await env.STATIC.get(key);

  if (!object) {
    // SPA fallback
    const fallback = await env.STATIC.get("index.html");
    if (fallback) {
      const headers = new Headers();
      fallback.writeHttpMetadata(headers);
      headers.set("Cache-Control", "no-cache");
      return new Response(fallback.body, { headers });
    }
    return new Response("Not Found", { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);

  // 캐시 설정
  if (key.match(/\.(js|css|png|jpg|gif|svg|woff2?)$/)) {
    headers.set("Cache-Control", "public, max-age=31536000, immutable");
  } else {
    headers.set("Cache-Control", "public, max-age=3600");
  }

  return new Response(object.body, { headers });
}

async function handleAPI(
  request: Request,
  env: Env,
  url: URL
): Promise<Response> {
  const path = url.pathname.replace("/api", "");

  // CORS
  if (request.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }

  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  };

  try {
    // API 라우트 처리
    if (path === "/items" && request.method === "GET") {
      return listItems(env, corsHeaders);
    }

    if (path === "/items" && request.method === "POST") {
      return createItem(request, env, corsHeaders);
    }

    if (path.match(/^\/items\/[\w-]+$/) && request.method === "GET") {
      const id = path.split("/")[2];
      return getItem(env, id, corsHeaders);
    }

    if (path.match(/^\/items\/[\w-]+$/) && request.method === "DELETE") {
      const id = path.split("/")[2];
      return deleteItem(env, id, corsHeaders);
    }

    return new Response(
      JSON.stringify({ error: "Not Found" }),
      { status: 404, headers: corsHeaders }
    );
  } catch (e: any) {
    return new Response(
      JSON.stringify({ error: e.message }),
      { status: 500, headers: corsHeaders }
    );
  }
}

async function listItems(env: Env, headers: Record<string, string>) {
  const listed = await env.DATA.list({ prefix: "items/" });
  const items = [];

  for (const obj of listed.objects) {
    const data = await env.DATA.get(obj.key);
    if (data) {
      items.push(JSON.parse(await data.text()));
    }
  }

  return new Response(JSON.stringify(items), { headers });
}

async function createItem(
  request: Request,
  env: Env,
  headers: Record<string, string>
) {
  const body = await request.json();
  const id = crypto.randomUUID();
  const item = { id, ...body, createdAt: new Date().toISOString() };

  await env.DATA.put(`items/${id}`, JSON.stringify(item));

  return new Response(JSON.stringify(item), { status: 201, headers });
}

async function getItem(
  env: Env,
  id: string,
  headers: Record<string, string>
) {
  const data = await env.DATA.get(`items/${id}`);

  if (!data) {
    return new Response(
      JSON.stringify({ error: "Not Found" }),
      { status: 404, headers }
    );
  }

  return new Response(await data.text(), { headers });
}

async function deleteItem(
  env: Env,
  id: string,
  headers: Record<string, string>
) {
  await env.DATA.delete(`items/${id}`);
  return new Response(JSON.stringify({ deleted: true }), { headers });
}
```

### 배포 스크립트

```bash
#!/bin/bash
# deploy.sh

# 프론트엔드 빌드
cd frontend
npm run build

# R2에 업로드 (rclone 사용)
rclone sync ./dist r2:static-bucket --progress

# Worker 배포
cd ../worker
wrangler deploy

echo "Deployment complete!"
```

---

## Best Practices

### 1. 보안

```typescript
// 입력 검증
function validateKey(key: string): boolean {
  // 경로 순회 방지
  if (key.includes("..") || key.startsWith("/")) {
    return false;
  }
  // 허용된 문자만
  if (!/^[\w\-\./]+$/.test(key)) {
    return false;
  }
  return true;
}

// 파일 타입 검증
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];

function validateFileType(type: string): boolean {
  return ALLOWED_TYPES.includes(type);
}

// 크기 제한
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

function validateFileSize(size: number): boolean {
  return size <= MAX_FILE_SIZE;
}
```

### 2. 에러 처리

```typescript
class R2Error extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code: string
  ) {
    super(message);
  }
}

async function safeGet(
  bucket: R2Bucket,
  key: string
): Promise<R2ObjectBody | null> {
  try {
    return await bucket.get(key);
  } catch (e: any) {
    console.error(`R2 get error: ${key}`, e);
    throw new R2Error("Storage error", 500, "STORAGE_ERROR");
  }
}

function errorResponse(error: R2Error): Response {
  return new Response(
    JSON.stringify({
      error: error.message,
      code: error.code,
    }),
    {
      status: error.statusCode,
      headers: { "Content-Type": "application/json" },
    }
  );
}
```

### 3. 성능 최적화

```typescript
// 캐시 활용
async function getCachedObject(
  request: Request,
  bucket: R2Bucket,
  key: string,
  ctx: ExecutionContext
): Promise<Response> {
  const cache = caches.default;
  const cacheKey = new Request(request.url, request);

  // 캐시 확인
  let response = await cache.match(cacheKey);
  if (response) {
    return response;
  }

  // R2에서 가져오기
  const object = await bucket.get(key);
  if (!object) {
    return new Response("Not Found", { status: 404 });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("Cache-Control", "public, max-age=86400");

  response = new Response(object.body, { headers });

  // 캐시 저장 (비동기)
  ctx.waitUntil(cache.put(cacheKey, response.clone()));

  return response;
}

// 조건부 요청 지원
async function handleConditionalRequest(
  request: Request,
  bucket: R2Bucket,
  key: string
): Promise<Response> {
  const ifNoneMatch = request.headers.get("If-None-Match");

  const head = await bucket.head(key);
  if (!head) {
    return new Response("Not Found", { status: 404 });
  }

  if (ifNoneMatch === head.httpEtag) {
    return new Response(null, { status: 304 });
  }

  const object = await bucket.get(key);
  const headers = new Headers();
  object!.writeHttpMetadata(headers);
  headers.set("ETag", head.httpEtag);

  return new Response(object!.body, { headers });
}
```

### 4. 모니터링 및 로깅

```typescript
// 요청 로깅
interface RequestLog {
  timestamp: string;
  method: string;
  path: string;
  status: number;
  duration: number;
  userAgent?: string;
}

async function logRequest(
  request: Request,
  response: Response,
  startTime: number,
  env: Env
): Promise<void> {
  const log: RequestLog = {
    timestamp: new Date().toISOString(),
    method: request.method,
    path: new URL(request.url).pathname,
    status: response.status,
    duration: Date.now() - startTime,
    userAgent: request.headers.get("User-Agent") || undefined,
  };

  // R2에 로그 저장 (일별 파일)
  const date = new Date().toISOString().split("T")[0];
  const logKey = `logs/${date}/${crypto.randomUUID()}.json`;

  await env.LOGS.put(logKey, JSON.stringify(log));
}
```

### 5. 비용 최적화

```
비용 최적화 체크리스트:

저장 최적화:
├── [ ] 라이프사이클 규칙으로 불필요 파일 자동 삭제
├── [ ] 압축 가능한 파일 압축 저장 (gzip, brotli)
├── [ ] 중복 파일 제거 (해시 기반 검사)
└── [ ] 적절한 이미지 포맷 사용 (WebP)

요청 최적화:
├── [ ] CDN 캐싱 활용 (Edge TTL 설정)
├── [ ] 조건부 요청 지원 (ETag, If-None-Match)
├── [ ] 불필요한 LIST 요청 최소화
└── [ ] 배치 작업으로 요청 통합

아키텍처:
├── [ ] 정적 파일은 Workers 경유하지 않고 직접 제공
├── [ ] 무거운 처리는 Queue로 비동기 처리
└── [ ] 적절한 캐시 전략 수립
```

---

## 다음 단계

- [[cheatsheet|치트시트]] - 빠른 참조
- [[04-learning/01-setup|처음부터 시작하기]] - 기초 복습
