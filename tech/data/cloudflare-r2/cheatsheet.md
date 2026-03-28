# Cloudflare R2 치트시트

## 빠른 참조

### 엔드포인트

```
S3 API: https://<ACCOUNT_ID>.r2.cloudflarestorage.com
퍼블릭: https://pub-<BUCKET_ID>.r2.dev/<KEY>
```

### 가격

| 항목 | 가격 | 무료 한도 |
|------|------|----------|
| 저장 | $0.015/GB/월 | 10GB |
| Class A (쓰기) | $4.50/백만 | 1,000만/월 |
| Class B (읽기) | $0.36/백만 | 1억/월 |
| 이그레스 | **$0** | 무제한 |

---

## AWS CLI

### 초기 설정

```bash
# 프로필 설정
aws configure --profile r2
# Access Key: <R2_ACCESS_KEY_ID>
# Secret Key: <R2_SECRET_ACCESS_KEY>
# Region: auto
# Format: json

# 환경 변수
export R2_ENDPOINT="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"

# 별칭 (선택)
alias r2='aws s3 --endpoint-url $R2_ENDPOINT --profile r2'
```

### 기본 명령어

```bash
# 버킷 목록
aws s3 ls --endpoint-url $R2_ENDPOINT --profile r2

# 객체 목록
aws s3 ls s3://bucket-name/ --endpoint-url $R2_ENDPOINT --profile r2

# 업로드
aws s3 cp file.txt s3://bucket/path/ --endpoint-url $R2_ENDPOINT --profile r2

# 다운로드
aws s3 cp s3://bucket/file.txt ./ --endpoint-url $R2_ENDPOINT --profile r2

# 동기화
aws s3 sync ./local s3://bucket/remote --endpoint-url $R2_ENDPOINT --profile r2

# 삭제
aws s3 rm s3://bucket/file.txt --endpoint-url $R2_ENDPOINT --profile r2

# 재귀 삭제
aws s3 rm s3://bucket/folder/ --recursive --endpoint-url $R2_ENDPOINT --profile r2
```

---

## Python (boto3)

### 클라이언트 설정

```python
import boto3

r2 = boto3.client('s3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>'
)
```

### CRUD 작업

```python
# 업로드
r2.put_object(Bucket='bucket', Key='key', Body=b'data')
r2.upload_file('./file.txt', 'bucket', 'key')

# 다운로드
response = r2.get_object(Bucket='bucket', Key='key')
data = response['Body'].read()

# 메타데이터
head = r2.head_object(Bucket='bucket', Key='key')

# 삭제
r2.delete_object(Bucket='bucket', Key='key')

# 목록
response = r2.list_objects_v2(Bucket='bucket', Prefix='folder/')
for obj in response.get('Contents', []):
    print(obj['Key'])

# Presigned URL
url = r2.generate_presigned_url('get_object',
    Params={'Bucket': 'bucket', 'Key': 'key'},
    ExpiresIn=3600)
```

---

## JavaScript (AWS SDK v3)

### 클라이언트 설정

```javascript
import { S3Client } from "@aws-sdk/client-s3";

const r2 = new S3Client({
  region: "auto",
  endpoint: "https://<ACCOUNT_ID>.r2.cloudflarestorage.com",
  credentials: {
    accessKeyId: "<ACCESS_KEY>",
    secretAccessKey: "<SECRET_KEY>",
  },
});
```

### CRUD 작업

```javascript
import {
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  ListObjectsV2Command,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

// 업로드
await r2.send(new PutObjectCommand({
  Bucket: "bucket", Key: "key", Body: "data"
}));

// 다운로드
const response = await r2.send(new GetObjectCommand({
  Bucket: "bucket", Key: "key"
}));
const data = await response.Body.transformToString();

// 삭제
await r2.send(new DeleteObjectCommand({
  Bucket: "bucket", Key: "key"
}));

// 목록
const list = await r2.send(new ListObjectsV2Command({
  Bucket: "bucket", Prefix: "folder/"
}));

// Presigned URL
const url = await getSignedUrl(r2,
  new GetObjectCommand({ Bucket: "bucket", Key: "key" }),
  { expiresIn: 3600 }
);
```

---

## Workers 바인딩

### wrangler.toml

```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "actual-bucket-name"
```

### 기본 작업

```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}

export default {
  async fetch(request: Request, env: Env) {
    // 업로드
    await env.MY_BUCKET.put("key", "data", {
      httpMetadata: { contentType: "text/plain" }
    });

    // 다운로드
    const obj = await env.MY_BUCKET.get("key");
    if (obj) {
      const headers = new Headers();
      obj.writeHttpMetadata(headers);
      return new Response(obj.body, { headers });
    }

    // 메타데이터
    const head = await env.MY_BUCKET.head("key");

    // 삭제
    await env.MY_BUCKET.delete("key");

    // 목록
    const list = await env.MY_BUCKET.list({
      prefix: "folder/",
      limit: 100
    });

    return new Response("OK");
  }
}
```

---

## CORS 설정

```json
[
  {
    "AllowedOrigins": ["https://example.com"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3600
  }
]
```

---

## 라이프사이클 규칙

```python
r2.put_bucket_lifecycle_configuration(
    Bucket='bucket',
    LifecycleConfiguration={
        'Rules': [
            {
                'ID': 'delete-old-logs',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'logs/'},
                'Expiration': {'Days': 30}
            },
            {
                'ID': 'abort-incomplete-uploads',
                'Status': 'Enabled',
                'Filter': {'Prefix': ''},
                'AbortIncompleteMultipartUpload': {
                    'DaysAfterInitiation': 7
                }
            }
        ]
    }
)
```

---

## Wrangler CLI

```bash
# 설치
npm install -g wrangler

# 로그인
wrangler login

# 버킷 목록
wrangler r2 bucket list

# 버킷 생성
wrangler r2 bucket create my-bucket

# 객체 조회
wrangler r2 object get my-bucket/key

# 객체 업로드
wrangler r2 object put my-bucket/key --file ./local-file.txt

# 객체 삭제
wrangler r2 object delete my-bucket/key

# 로컬 개발
wrangler dev

# 배포
wrangler deploy
```

---

## 일반적인 에러

| 에러 | 원인 | 해결 |
|------|------|------|
| AccessDenied | 권한 부족 | API 토큰 권한 확인 |
| NoSuchBucket | 버킷 없음 | 버킷 이름 확인 |
| NoSuchKey | 객체 없음 | 키 경로 확인 |
| SignatureDoesNotMatch | 자격 증명 오류 | Access/Secret Key 확인 |
| EntityTooLarge | 파일 크기 초과 | 멀티파트 업로드 사용 |

---

## 유용한 링크

- [R2 공식 문서](https://developers.cloudflare.com/r2/)
- [R2 가격](https://developers.cloudflare.com/r2/pricing/)
- [Workers 문서](https://developers.cloudflare.com/workers/)
- [대시보드](https://dash.cloudflare.com/)
- [시스템 상태](https://www.cloudflarestatus.com/)

---

## 주요 제한사항

```
객체 크기: 최대 5TB (단일), 5GB (파트)
버킷 이름: 3-63자, 소문자/숫자/하이픈
객체 키: 최대 1024바이트
메타데이터: 최대 2KB
버킷 수: 계정당 1,000개 (기본)
동시 업로드: 파트 최대 10,000개
```
