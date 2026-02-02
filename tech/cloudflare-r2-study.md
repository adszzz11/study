# Cloudflare R2 심층 스터디 가이드

> **한 줄 정의**: AWS S3 호환 오브젝트 스토리지로, Egress(데이터 전송) 비용이 무료인 Cloudflare의 저장소 서비스

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. S3 호환 API를 제공하여 기존 S3 코드/도구를 그대로 사용 가능
2. **Egress 비용 0원** - 데이터 다운로드 시 전송 비용 없음 (S3 대비 최대 99% 절감)
3. Cloudflare Workers와 네이티브 통합으로 엣지에서 직접 접근

**핵심 키워드**: `#오브젝트스토리지` `#S3호환` `#Egress무료` `#Cloudflare` `#CDN`

**S3 vs R2 비용 비교**:

| 항목 | AWS S3 | Cloudflare R2 |
|------|--------|---------------|
| **저장** | $0.023/GB/월 | $0.015/GB/월 |
| **Class A (쓰기)** | $5/1M 요청 | $4.50/1M 요청 |
| **Class B (읽기)** | $0.40/1M 요청 | $0.36/1M 요청 |
| **Egress (전송)** | $0.09/GB | **$0 (무료)** |

**예시**: 1TB 저장, 10TB 월간 다운로드
- S3: $23 + $900 = **$923/월**
- R2: $15 + $0 = **$15/월** (98% 절감)

### 1.2 Quick Start (30초 체험)

**Cloudflare 대시보드에서**:
```
1. Cloudflare 계정 로그인
2. 좌측 메뉴 → R2 Object Storage
3. "Create bucket" 클릭
4. 버킷 이름 입력 (예: my-files)
5. 생성 완료!
```

**Wrangler CLI로**:
```bash
# 1. Wrangler 설치
npm install -g wrangler

# 2. 로그인
wrangler login

# 3. 버킷 생성
wrangler r2 bucket create my-files

# 4. 파일 업로드
wrangler r2 object put my-files/hello.txt --file ./hello.txt

# 5. 파일 다운로드
wrangler r2 object get my-files/hello.txt
```

**S3 SDK로 접근**:
```python
import boto3

# R2 클라이언트 생성
s3 = boto3.client(
    's3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<R2_ACCESS_KEY>',
    aws_secret_access_key='<R2_SECRET_KEY>'
)

# 업로드
s3.upload_file('local_file.jpg', 'my-files', 'images/photo.jpg')

# 다운로드
s3.download_file('my-files', 'images/photo.jpg', 'downloaded.jpg')
```

### 1.3 왜 R2인가?

**장점**:
- **Egress 무료**: 데이터 다운로드 비용 0원
- **S3 호환**: 기존 도구/라이브러리 그대로 사용
- **Workers 통합**: 엣지에서 직접 접근 (지연 최소화)
- **글로벌 CDN**: Cloudflare 네트워크 자동 활용
- **Apache Iceberg**: 데이터 웨어하우스 기능 (2025)
- **무료 티어**: 10GB 저장, 1천만 Class B, 1백만 Class A/월

**단점**:
- S3의 모든 기능 지원은 아님 (Lambda 트리거 등)
- 리전 선택 불가 (자동 분산)
- 복잡한 버킷 정책은 제한적
- 대용량 업로드 시 멀티파트 필요

**주요 사용 사례**:
- 정적 웹 에셋 호스팅 (이미지, JS, CSS)
- 사용자 업로드 파일 저장
- 백업 및 아카이브
- CDN 오리진
- 로그/데이터 저장

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare R2 생태계                      │
├─────────────────────────────────────────────────────────────┤
│  [접근 방식]                                                 │
│  ├── S3 API: 표준 S3 호환 REST API                          │
│  ├── Workers Binding: 엣지에서 직접 접근                     │
│  ├── Wrangler CLI: 명령줄 관리                               │
│  └── Dashboard: 웹 UI 관리                                   │
│                                                              │
│  [스토리지 클래스]                                           │
│  ├── Standard: 자주 접근하는 데이터 (기본)                   │
│  └── Infrequent Access: 드물게 접근 (저렴, 30일 최소)        │
│                                                              │
│  [기능]                                                      │
│  ├── Object Lifecycle: 자동 삭제/전환                        │
│  ├── Event Notifications: 변경 이벤트 알림                   │
│  ├── Public Buckets: 공개 URL 접근                           │
│  ├── CORS: 크로스 오리진 설정                                │
│  └── Custom Domains: 자체 도메인 연결                        │
│                                                              │
│  [통합]                                                      │
│  ├── Workers: 서버리스 함수                                  │
│  ├── Pages: 정적 사이트 호스팅                               │
│  ├── Images: 이미지 최적화                                   │
│  └── Apache Iceberg: 데이터 분석                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **CDN** | Cloudflare CDN | 캐싱, 배포 |
| **서버리스** | Cloudflare Workers | 파일 처리 |
| **프레임워크** | Next.js, Remix | 웹 앱 |
| **이미지** | Cloudflare Images | 최적화/변환 |
| **인증** | Signed URLs | 접근 제어 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Cloudflare R2 | AWS S3 | Backblaze B2 | Wasabi |
|------|---------------|--------|--------------|--------|
| **저장 비용** | $0.015/GB | $0.023/GB | $0.005/GB | $0.007/GB |
| **Egress** | 무료 | $0.09/GB | $0.01/GB | 무료* |
| **읽기 비용** | $0.36/M | $0.40/M | $0.004/M | 무료 |
| **쓰기 비용** | $4.50/M | $5.00/M | $0.004/M | 무료 |
| **S3 호환** | 예 | 네이티브 | 예 | 예 |
| **리전** | 자동 | 선택 | 선택 | 선택 |
| **CDN 통합** | 네이티브 | CloudFront | 별도 | 별도 |

*Wasabi: 다운로드가 저장량 초과 시 비용 발생

**선택 가이드**:
- **R2**: Egress 비용 중요, Workers 통합, 글로벌 배포
- **S3**: AWS 생태계, Lambda 트리거, 고급 기능
- **B2**: 저렴한 저장, 백업 용도
- **Wasabi**: 고정 비용 선호, 대용량 저장

### 2.4 최신 트렌드 및 동향 (2025)

- **Apache Iceberg 통합**: R2를 데이터 웨어하우스로 활용
- **Event Notifications GA**: Queue로 변경 이벤트 전송
- **CRC-64/NVME 체크섬**: 데이터 무결성 강화
- **SSE-C**: 고객 제공 키 암호화
- **Infrequent Access 클래스**: 30일 최소 보관 저렴한 옵션

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [developers.cloudflare.com/r2](https://developers.cloudflare.com/r2/) | 메인 문서 |
| 🟢 대시보드 | [dash.cloudflare.com](https://dash.cloudflare.com/) | R2 관리 |
| 🟡 API 레퍼런스 | [S3 API Compatibility](https://developers.cloudflare.com/r2/api/s3/) | S3 API 호환성 |
| 🟡 가격 | [cloudflare.com/r2](https://www.cloudflare.com/developer-platform/products/r2/) | 가격 정보 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [R2 Getting Started](https://developers.cloudflare.com/r2/get-started/) - 공식 시작 가이드
- [R2 Quickstart](https://developers.cloudflare.com/r2/examples/) - 예제 모음

**🟡 중급**:
- [Workers + R2](https://developers.cloudflare.com/r2/api/workers/) - Workers 통합
- [Object Lifecycle](https://developers.cloudflare.com/r2/buckets/object-lifecycles/) - 수명 주기 관리

**🔴 고급**:
- [Apache Iceberg](https://developers.cloudflare.com/r2/data-catalog/) - 데이터 분석
- [Event Notifications](https://developers.cloudflare.com/r2/buckets/event-notifications/) - 이벤트 처리

### 3.3 커뮤니티 및 질문할 곳

- **Cloudflare Community**: [community.cloudflare.com](https://community.cloudflare.com/)
- **Discord**: Cloudflare Developers
- **GitHub**: [cloudflare/workers-sdk](https://github.com/cloudflare/workers-sdk)

---

## Part 4: 상세 학습 로드맵

### 4.1 버킷 생성 및 기본 조작

📌 **핵심 개념**

R2 버킷은 S3 버킷과 동일한 개념입니다. 오브젝트(파일)를 저장하는 컨테이너입니다.

💻 **코드 예제: 버킷 관리**

```bash
# Wrangler CLI로 버킷 관리

# 버킷 목록
wrangler r2 bucket list

# 버킷 생성
wrangler r2 bucket create my-bucket

# 버킷 삭제 (비어있어야 함)
wrangler r2 bucket delete my-bucket

# 오브젝트 업로드
wrangler r2 object put my-bucket/images/photo.jpg --file ./photo.jpg

# 오브젝트 다운로드
wrangler r2 object get my-bucket/images/photo.jpg --file ./downloaded.jpg

# 오브젝트 목록
wrangler r2 object list my-bucket

# 오브젝트 삭제
wrangler r2 object delete my-bucket/images/photo.jpg
```

**Python (boto3) 사용**:
```python
import boto3
from botocore.config import Config

# R2 클라이언트 설정
r2 = boto3.client(
    's3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>',
    config=Config(signature_version='s3v4')
)

# 버킷 생성
r2.create_bucket(Bucket='my-bucket')

# 파일 업로드
r2.upload_file('local.jpg', 'my-bucket', 'images/photo.jpg')

# 파일 업로드 (바이트)
r2.put_object(
    Bucket='my-bucket',
    Key='data.json',
    Body=b'{"hello": "world"}',
    ContentType='application/json'
)

# 파일 다운로드
r2.download_file('my-bucket', 'images/photo.jpg', 'downloaded.jpg')

# 오브젝트 목록
response = r2.list_objects_v2(Bucket='my-bucket', Prefix='images/')
for obj in response.get('Contents', []):
    print(f"{obj['Key']} - {obj['Size']} bytes")

# 파일 삭제
r2.delete_object(Bucket='my-bucket', Key='images/photo.jpg')
```

**Node.js (AWS SDK v3)**:
```javascript
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';

const r2 = new S3Client({
    region: 'auto',
    endpoint: `https://${process.env.ACCOUNT_ID}.r2.cloudflarestorage.com`,
    credentials: {
        accessKeyId: process.env.R2_ACCESS_KEY,
        secretAccessKey: process.env.R2_SECRET_KEY
    }
});

// 업로드
await r2.send(new PutObjectCommand({
    Bucket: 'my-bucket',
    Key: 'images/photo.jpg',
    Body: fileBuffer,
    ContentType: 'image/jpeg'
}));

// 다운로드
const response = await r2.send(new GetObjectCommand({
    Bucket: 'my-bucket',
    Key: 'images/photo.jpg'
}));
const body = await response.Body.transformToByteArray();
```

✅ **체크포인트**
- [ ] Wrangler로 버킷을 생성할 수 있는가?
- [ ] boto3/AWS SDK로 R2에 연결할 수 있는가?
- [ ] 파일 업로드/다운로드를 할 수 있는가?

⚠️ **흔한 실수**
- `endpoint_url`에 계정 ID 포함 필수
- `region`은 `auto` 사용
- API 토큰은 "R2 Token" 권한으로 생성

🔗 **더 알아보기**: [S3 API](https://developers.cloudflare.com/r2/api/s3/)

---

### 4.2 공개 버킷과 커스텀 도메인

📌 **핵심 개념**

R2 버킷을 공개하면 누구나 URL로 접근할 수 있습니다. 커스텀 도메인을 연결하여 브랜딩도 가능합니다.

💻 **코드 예제: 공개 접근 설정**

```bash
# 대시보드에서 공개 버킷 설정
# 1. R2 → 버킷 선택 → Settings
# 2. "Public Access" 활성화
# 3. 공개 URL 생성됨: https://pub-xxx.r2.dev/path/to/file
```

**커스텀 도메인 설정**:
```
# 대시보드에서
# 1. R2 → 버킷 → Settings → Custom Domains
# 2. "Connect Domain" 클릭
# 3. 도메인 입력 (예: files.example.com)
# 4. DNS 레코드 자동 설정 (같은 Cloudflare 계정)

# 외부 DNS의 경우
# CNAME: files.example.com → pub-xxx.r2.dev
```

**접근 제어 with Workers**:
```javascript
// wrangler.toml
// [[r2_buckets]]
// binding = "MY_BUCKET"
// bucket_name = "my-bucket"

export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        const key = url.pathname.slice(1);

        // 인증 체크
        const authHeader = request.headers.get('Authorization');
        if (!isValidAuth(authHeader)) {
            return new Response('Unauthorized', { status: 401 });
        }

        // R2에서 파일 가져오기
        const object = await env.MY_BUCKET.get(key);

        if (!object) {
            return new Response('Not Found', { status: 404 });
        }

        // 응답
        const headers = new Headers();
        headers.set('Content-Type', object.httpMetadata?.contentType || 'application/octet-stream');
        headers.set('Cache-Control', 'public, max-age=31536000');

        return new Response(object.body, { headers });
    }
};
```

**Signed URL (시간 제한 접근)**:
```python
import boto3
from datetime import datetime, timedelta

r2 = boto3.client('s3', ...)

# 1시간 유효한 다운로드 URL 생성
url = r2.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'private/document.pdf'
    },
    ExpiresIn=3600  # 1시간
)

print(url)
# https://xxx.r2.cloudflarestorage.com/my-bucket/private/document.pdf?X-Amz-...
```

✅ **체크포인트**
- [ ] 공개 버킷을 설정할 수 있는가?
- [ ] 커스텀 도메인을 연결할 수 있는가?
- [ ] Signed URL을 생성할 수 있는가?

⚠️ **흔한 실수**
- 공개 버킷은 모든 파일이 공개됨 (폴더별 제어 불가)
- Signed URL 만료 시간 설정 주의

🔗 **더 알아보기**: [Public Buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/)

---

### 4.3 Workers Binding

📌 **핵심 개념**

Workers에서 R2 binding을 사용하면 엣지에서 직접 파일에 접근합니다. 네트워크 왕복 없이 빠릅니다.

💻 **코드 예제: Workers + R2**

```toml
# wrangler.toml
name = "r2-worker"
main = "src/index.js"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-files"
```

```javascript
// src/index.js
export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);

        // PUT /upload/:key
        if (request.method === 'PUT') {
            const key = url.pathname.slice(8);  // /upload/ 제거
            await env.BUCKET.put(key, request.body, {
                httpMetadata: {
                    contentType: request.headers.get('Content-Type')
                }
            });
            return new Response(`Uploaded: ${key}`, { status: 201 });
        }

        // GET /:key
        if (request.method === 'GET') {
            const key = url.pathname.slice(1);
            const object = await env.BUCKET.get(key);

            if (!object) {
                return new Response('Not Found', { status: 404 });
            }

            return new Response(object.body, {
                headers: {
                    'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
                    'ETag': object.httpEtag
                }
            });
        }

        // DELETE /:key
        if (request.method === 'DELETE') {
            const key = url.pathname.slice(1);
            await env.BUCKET.delete(key);
            return new Response('Deleted', { status: 200 });
        }

        // LIST /list?prefix=images/
        if (url.pathname === '/list') {
            const prefix = url.searchParams.get('prefix') || '';
            const listed = await env.BUCKET.list({ prefix });

            return Response.json({
                objects: listed.objects.map(obj => ({
                    key: obj.key,
                    size: obj.size,
                    uploaded: obj.uploaded
                })),
                truncated: listed.truncated
            });
        }

        return new Response('Method Not Allowed', { status: 405 });
    }
};
```

**고급 패턴: 이미지 리사이징**:
```javascript
export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        const key = url.pathname.slice(1);

        // 리사이즈 파라미터
        const width = parseInt(url.searchParams.get('w')) || null;
        const height = parseInt(url.searchParams.get('h')) || null;

        // 원본 이미지 가져오기
        const object = await env.BUCKET.get(key);
        if (!object) return new Response('Not Found', { status: 404 });

        // 리사이즈 필요 없으면 원본 반환
        if (!width && !height) {
            return new Response(object.body, {
                headers: { 'Content-Type': object.httpMetadata?.contentType }
            });
        }

        // Cloudflare Image Resizing 사용
        const imageUrl = `https://your-origin.com/${key}`;
        const resizedResponse = await fetch(imageUrl, {
            cf: {
                image: {
                    width,
                    height,
                    fit: 'contain'
                }
            }
        });

        return resizedResponse;
    }
};
```

✅ **체크포인트**
- [ ] wrangler.toml에 R2 binding을 설정할 수 있는가?
- [ ] Workers에서 put/get/delete/list를 사용할 수 있는가?
- [ ] 파일 업로드 API를 구현할 수 있는가?

⚠️ **흔한 실수**
- `object.body`는 한 번만 읽을 수 있음 (스트림)
- 대용량 파일은 Range 요청 고려

🔗 **더 알아보기**: [Workers API](https://developers.cloudflare.com/r2/api/workers/)

---

### 4.4 Object Lifecycle

📌 **핵심 개념**

Lifecycle 규칙으로 오브젝트를 자동 삭제하거나 스토리지 클래스를 전환할 수 있습니다.

💻 **코드 예제: Lifecycle 설정**

```python
import boto3

r2 = boto3.client('s3', ...)

# Lifecycle 규칙 설정
r2.put_bucket_lifecycle_configuration(
    Bucket='my-bucket',
    LifecycleConfiguration={
        'Rules': [
            {
                'ID': 'Delete old logs',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'logs/'},
                'Expiration': {'Days': 30}  # 30일 후 삭제
            },
            {
                'ID': 'Archive old backups',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'backups/'},
                'Transitions': [
                    {
                        'Days': 90,
                        'StorageClass': 'INFREQUENT_ACCESS'  # 90일 후 IA로 전환
                    }
                ]
            },
            {
                'ID': 'Clean up incomplete uploads',
                'Status': 'Enabled',
                'Filter': {'Prefix': ''},
                'AbortIncompleteMultipartUpload': {
                    'DaysAfterInitiation': 7  # 7일 후 미완료 업로드 삭제
                }
            }
        ]
    }
)

# 규칙 확인
rules = r2.get_bucket_lifecycle_configuration(Bucket='my-bucket')
print(rules)
```

**Wrangler로 설정**:
```bash
# lifecycle.json 파일 생성
cat > lifecycle.json << 'EOF'
{
    "Rules": [
        {
            "ID": "delete-old-temp",
            "Status": "Enabled",
            "Filter": {"Prefix": "temp/"},
            "Expiration": {"Days": 7}
        }
    ]
}
EOF

# 적용 (현재 S3 API 직접 사용 필요)
```

**스토리지 클래스**:
```python
# Infrequent Access 클래스로 직접 업로드
r2.put_object(
    Bucket='my-bucket',
    Key='archive/old-data.zip',
    Body=data,
    StorageClass='INFREQUENT_ACCESS'
)

# Standard → IA 전환은 Lifecycle 규칙으로
```

✅ **체크포인트**
- [ ] Lifecycle 규칙을 생성할 수 있는가?
- [ ] 자동 삭제(Expiration)를 설정할 수 있는가?
- [ ] 스토리지 클래스 전환을 이해하는가?

⚠️ **흔한 실수**
- Infrequent Access는 최소 30일 보관 필수
- 삭제 규칙은 신중하게 (복구 불가)

🔗 **더 알아보기**: [Object Lifecycles](https://developers.cloudflare.com/r2/buckets/object-lifecycles/)

---

### 4.5 Event Notifications

📌 **핵심 개념**

오브젝트 생성/삭제 시 Cloudflare Queue로 이벤트를 보내 비동기 처리가 가능합니다.

💻 **코드 예제: Event Notification 설정**

```toml
# wrangler.toml
name = "r2-processor"

[[queues.consumers]]
queue = "r2-events"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-files"
```

```javascript
// R2 이벤트 처리 Worker
export default {
    // Queue 컨슈머
    async queue(batch, env) {
        for (const message of batch.messages) {
            const event = message.body;

            console.log(`Event: ${event.action} on ${event.object.key}`);

            if (event.action === 'PutObject') {
                // 새 파일 업로드 처리
                const key = event.object.key;

                if (key.endsWith('.jpg') || key.endsWith('.png')) {
                    // 이미지 처리 (썸네일 생성 등)
                    await processImage(env, key);
                }
            }

            if (event.action === 'DeleteObject') {
                // 파일 삭제 처리
                console.log(`Deleted: ${event.object.key}`);
            }

            message.ack();
        }
    }
};

async function processImage(env, key) {
    const object = await env.BUCKET.get(key);
    if (!object) return;

    // 썸네일 키 생성
    const thumbKey = `thumbnails/${key}`;

    // 이미지 처리 (간단한 예시)
    // 실제로는 이미지 리사이징 라이브러리 사용
    await env.BUCKET.put(thumbKey, object.body, {
        httpMetadata: object.httpMetadata
    });

    console.log(`Created thumbnail: ${thumbKey}`);
}
```

**대시보드에서 설정**:
```
1. R2 → 버킷 선택 → Settings → Event notifications
2. "Add notification" 클릭
3. Queue 선택 (미리 생성 필요)
4. 이벤트 타입 선택 (object:created, object:deleted)
5. 접두사/접미사 필터 (선택)
```

**이벤트 페이로드**:
```json
{
    "account": "account-id",
    "bucket": "my-files",
    "action": "PutObject",
    "object": {
        "key": "images/photo.jpg",
        "size": 102400,
        "eTag": "abc123..."
    },
    "eventTime": "2025-01-15T10:30:00Z"
}
```

✅ **체크포인트**
- [ ] Queue를 생성하고 R2와 연결할 수 있는가?
- [ ] 이벤트를 처리하는 Worker를 작성할 수 있는가?
- [ ] 필터를 사용하여 특정 파일만 처리할 수 있는가?

⚠️ **흔한 실수**
- Queue는 R2와 같은 계정에 있어야 함
- 대량 이벤트 시 처리 지연 가능

🔗 **더 알아보기**: [Event Notifications](https://developers.cloudflare.com/r2/buckets/event-notifications/)

---

### 4.6 대용량 파일 업로드 (Multipart)

📌 **핵심 개념**

100MB 이상의 파일은 Multipart Upload로 분할 업로드합니다. 병렬 업로드로 속도가 빠릅니다.

💻 **코드 예제: Multipart Upload**

```python
import boto3
from boto3.s3.transfer import TransferConfig

r2 = boto3.client('s3', ...)

# 자동 Multipart (권장)
config = TransferConfig(
    multipart_threshold=100 * 1024 * 1024,  # 100MB 이상 시 멀티파트
    max_concurrency=10,  # 병렬 업로드
    multipart_chunksize=50 * 1024 * 1024,  # 50MB 청크
    use_threads=True
)

r2.upload_file(
    'large_file.zip',
    'my-bucket',
    'backups/large_file.zip',
    Config=config
)
```

**수동 Multipart (세밀한 제어)**:
```python
import boto3

r2 = boto3.client('s3', ...)

# 1. Multipart 시작
response = r2.create_multipart_upload(
    Bucket='my-bucket',
    Key='large_file.zip'
)
upload_id = response['UploadId']

# 2. 파트 업로드
parts = []
part_number = 1
chunk_size = 50 * 1024 * 1024  # 50MB

with open('large_file.zip', 'rb') as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break

        part_response = r2.upload_part(
            Bucket='my-bucket',
            Key='large_file.zip',
            PartNumber=part_number,
            UploadId=upload_id,
            Body=chunk
        )

        parts.append({
            'ETag': part_response['ETag'],
            'PartNumber': part_number
        })
        part_number += 1

# 3. 완료
r2.complete_multipart_upload(
    Bucket='my-bucket',
    Key='large_file.zip',
    UploadId=upload_id,
    MultipartUpload={'Parts': parts}
)

print("Upload complete!")
```

**Workers에서 Multipart**:
```javascript
export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        const key = url.pathname.slice(1);

        if (request.method === 'POST' && url.pathname === '/upload/start') {
            // 시작
            const upload = await env.BUCKET.createMultipartUpload(key);
            return Response.json({ uploadId: upload.uploadId });
        }

        if (request.method === 'PUT' && url.pathname.startsWith('/upload/part/')) {
            // 파트 업로드
            const uploadId = url.searchParams.get('uploadId');
            const partNumber = parseInt(url.searchParams.get('part'));

            const part = await env.BUCKET.uploadPart(key, uploadId, partNumber, request.body);
            return Response.json({ etag: part.etag });
        }

        if (request.method === 'POST' && url.pathname === '/upload/complete') {
            // 완료
            const { uploadId, parts } = await request.json();
            await env.BUCKET.completeMultipartUpload(key, uploadId, parts);
            return new Response('Complete');
        }

        return new Response('Not Found', { status: 404 });
    }
};
```

✅ **체크포인트**
- [ ] TransferConfig로 자동 멀티파트를 설정할 수 있는가?
- [ ] 수동 멀티파트의 3단계를 이해하는가?
- [ ] Workers에서 멀티파트를 구현할 수 있는가?

⚠️ **흔한 실수**
- 미완료 업로드는 스토리지 차지 → Lifecycle으로 정리
- 파트 번호는 1부터 시작, 연속적이어야 함

🔗 **더 알아보기**: [Multipart Upload](https://developers.cloudflare.com/r2/api/s3/api/#multipart-upload)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 정적 파일 호스팅 | 공개 버킷, CDN |
| 🟢 | 파일 업로드 API | Workers + R2 |
| 🟡 | 이미지 갤러리 | Signed URL, 썸네일 |
| 🟡 | 백업 자동화 | Lifecycle, Cron |
| 🔴 | 미디어 스트리밍 | Range 요청, 캐싱 |

### 5.2 단계별 구현 가이드: 파일 업로드 서비스

**목표**: 파일 업로드, 다운로드, 삭제 API 구현

```javascript
// src/index.js
export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        const corsHeaders = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        };

        // CORS preflight
        if (request.method === 'OPTIONS') {
            return new Response(null, { headers: corsHeaders });
        }

        // 인증 (간단한 API 키)
        const apiKey = request.headers.get('Authorization');
        if (apiKey !== `Bearer ${env.API_KEY}`) {
            return new Response('Unauthorized', { status: 401 });
        }

        const key = url.pathname.slice(1);

        try {
            // 업로드
            if (request.method === 'PUT') {
                const contentType = request.headers.get('Content-Type') || 'application/octet-stream';

                await env.BUCKET.put(key, request.body, {
                    httpMetadata: { contentType }
                });

                return Response.json(
                    { success: true, key, url: `${url.origin}/${key}` },
                    { headers: corsHeaders }
                );
            }

            // 다운로드
            if (request.method === 'GET') {
                const object = await env.BUCKET.get(key);

                if (!object) {
                    return new Response('Not Found', { status: 404, headers: corsHeaders });
                }

                const headers = new Headers(corsHeaders);
                headers.set('Content-Type', object.httpMetadata?.contentType || 'application/octet-stream');
                headers.set('Content-Length', object.size);
                headers.set('ETag', object.httpEtag);

                return new Response(object.body, { headers });
            }

            // 삭제
            if (request.method === 'DELETE') {
                await env.BUCKET.delete(key);
                return Response.json({ success: true }, { headers: corsHeaders });
            }

            return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });

        } catch (error) {
            return Response.json(
                { error: error.message },
                { status: 500, headers: corsHeaders }
            );
        }
    }
};
```

```toml
# wrangler.toml
name = "file-upload-api"
main = "src/index.js"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "uploads"

[vars]
API_KEY = "your-secret-api-key"
```

**클라이언트 사용 예시**:
```javascript
// 업로드
const response = await fetch('https://api.example.com/images/photo.jpg', {
    method: 'PUT',
    headers: {
        'Authorization': 'Bearer your-secret-api-key',
        'Content-Type': 'image/jpeg'
    },
    body: fileBlob
});

// 다운로드
const file = await fetch('https://api.example.com/images/photo.jpg', {
    headers: { 'Authorization': 'Bearer your-secret-api-key' }
});

// 삭제
await fetch('https://api.example.com/images/photo.jpg', {
    method: 'DELETE',
    headers: { 'Authorization': 'Bearer your-secret-api-key' }
});
```

### 5.3 Best Practices

**버킷 구조**:
```
my-bucket/
├── uploads/           # 사용자 업로드
│   ├── {user-id}/
│   │   └── {file-id}.{ext}
├── thumbnails/        # 자동 생성 썸네일
├── temp/              # 임시 파일 (7일 후 자동 삭제)
└── backups/           # 백업 (90일 후 IA로 전환)
```

**운영 권장사항**:

1. **버킷 분리**: 용도별 버킷 분리 (uploads, assets, logs)
2. **Lifecycle**: 임시 파일 자동 삭제, 오래된 파일 IA 전환
3. **접근 제어**: 민감 파일은 Signed URL 사용
4. **모니터링**: 사용량 대시보드 확인
5. **캐싱**: 자주 접근하는 파일은 CDN 캐시 활용

```python
# 파일 업로드 시 메타데이터 추가
r2.put_object(
    Bucket='uploads',
    Key='documents/report.pdf',
    Body=file_data,
    ContentType='application/pdf',
    Metadata={
        'uploaded-by': 'user-123',
        'original-name': 'Monthly Report.pdf',
        'upload-time': '2025-01-15T10:30:00Z'
    }
)
```

---

## 요약

Cloudflare R2는 비용 효율적인 오브젝트 스토리지입니다:

- **핵심 장점**: Egress 무료, S3 호환
- **접근 방식**: S3 API, Workers Binding, Wrangler CLI
- **통합**: Workers, Pages와 네이티브 연동
- **관리**: Lifecycle, Event Notifications

다음 단계:
1. [R2 Getting Started](https://developers.cloudflare.com/r2/get-started/) 따라하기
2. 첫 버킷 생성 및 파일 업로드
3. Workers와 연동하여 파일 API 구축
