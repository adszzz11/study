# S3 호환 API 사용

## S3 API 기본 개념

### 엔드포인트 구조

```
R2 S3 API 엔드포인트:
https://<ACCOUNT_ID>.r2.cloudflarestorage.com

예시:
https://a1b2c3d4e5f6g7h8i9j0.r2.cloudflarestorage.com
```

### 인증 방식

R2는 AWS Signature Version 4 인증을 사용합니다.

```
요청 헤더에 포함:
├── Authorization: AWS4-HMAC-SHA256 Credential=...
├── x-amz-date: 20240101T000000Z
└── x-amz-content-sha256: <hash>
```

---

## 객체 작업 (Object Operations)

### PutObject - 파일 업로드

```bash
# AWS CLI
aws s3api put-object \
  --bucket my-bucket \
  --key "folder/file.txt" \
  --body ./local-file.txt \
  --content-type "text/plain" \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 메타데이터 포함
aws s3api put-object \
  --bucket my-bucket \
  --key "image.png" \
  --body ./image.png \
  --content-type "image/png" \
  --metadata '{"author":"john","version":"1.0"}' \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
# Python (boto3)
import boto3

r2 = boto3.client('s3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>'
)

# 파일 업로드
r2.put_object(
    Bucket='my-bucket',
    Key='folder/file.txt',
    Body=b'Hello R2!',
    ContentType='text/plain'
)

# 파일에서 업로드
with open('local-file.txt', 'rb') as f:
    r2.put_object(
        Bucket='my-bucket',
        Key='uploaded.txt',
        Body=f
    )
```

```javascript
// Node.js (@aws-sdk/client-s3)
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const r2 = new S3Client({
  region: "auto",
  endpoint: "https://<ACCOUNT_ID>.r2.cloudflarestorage.com",
  credentials: {
    accessKeyId: "<ACCESS_KEY>",
    secretAccessKey: "<SECRET_KEY>",
  },
});

await r2.send(new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "folder/file.txt",
  Body: "Hello R2!",
  ContentType: "text/plain",
}));
```

### GetObject - 파일 다운로드

```bash
# AWS CLI
aws s3api get-object \
  --bucket my-bucket \
  --key "folder/file.txt" \
  ./downloaded.txt \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# Range 요청 (부분 다운로드)
aws s3api get-object \
  --bucket my-bucket \
  --key "large-file.zip" \
  --range "bytes=0-1023" \
  ./partial.bin \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
# Python
response = r2.get_object(Bucket='my-bucket', Key='folder/file.txt')
content = response['Body'].read()
print(content.decode('utf-8'))

# 스트리밍 다운로드 (대용량 파일)
response = r2.get_object(Bucket='my-bucket', Key='large-file.zip')
with open('downloaded.zip', 'wb') as f:
    for chunk in response['Body'].iter_chunks():
        f.write(chunk)
```

```javascript
// Node.js
import { GetObjectCommand } from "@aws-sdk/client-s3";

const response = await r2.send(new GetObjectCommand({
  Bucket: "my-bucket",
  Key: "folder/file.txt",
}));

const content = await response.Body.transformToString();
console.log(content);
```

### HeadObject - 메타데이터 조회

```bash
aws s3api head-object \
  --bucket my-bucket \
  --key "file.txt" \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
response = r2.head_object(Bucket='my-bucket', Key='file.txt')
print(f"Size: {response['ContentLength']}")
print(f"Type: {response['ContentType']}")
print(f"ETag: {response['ETag']}")
print(f"LastModified: {response['LastModified']}")
```

### DeleteObject - 파일 삭제

```bash
# 단일 삭제
aws s3api delete-object \
  --bucket my-bucket \
  --key "file.txt" \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 다중 삭제
aws s3api delete-objects \
  --bucket my-bucket \
  --delete '{"Objects":[{"Key":"file1.txt"},{"Key":"file2.txt"}]}' \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
# 단일 삭제
r2.delete_object(Bucket='my-bucket', Key='file.txt')

# 다중 삭제
r2.delete_objects(
    Bucket='my-bucket',
    Delete={
        'Objects': [
            {'Key': 'file1.txt'},
            {'Key': 'file2.txt'},
            {'Key': 'folder/file3.txt'},
        ]
    }
)
```

### CopyObject - 파일 복사

```bash
aws s3api copy-object \
  --bucket my-bucket \
  --key "new-location/file.txt" \
  --copy-source "my-bucket/old-location/file.txt" \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
# 같은 버킷 내 복사
r2.copy_object(
    Bucket='my-bucket',
    Key='backup/file.txt',
    CopySource='my-bucket/original/file.txt'
)

# 메타데이터 변경하며 복사
r2.copy_object(
    Bucket='my-bucket',
    Key='file.txt',
    CopySource='my-bucket/file.txt',
    MetadataDirective='REPLACE',
    ContentType='application/json',
    Metadata={'new-key': 'new-value'}
)
```

---

## 버킷 작업 (Bucket Operations)

### ListBuckets - 버킷 목록

```bash
aws s3api list-buckets \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
response = r2.list_buckets()
for bucket in response['Buckets']:
    print(f"{bucket['Name']} - {bucket['CreationDate']}")
```

### ListObjectsV2 - 객체 목록

```bash
# 기본 목록
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 접두사 필터
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --prefix "images/" \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 페이지네이션
aws s3api list-objects-v2 \
  --bucket my-bucket \
  --max-keys 100 \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

```python
# 기본 목록
response = r2.list_objects_v2(Bucket='my-bucket')
for obj in response.get('Contents', []):
    print(f"{obj['Key']} - {obj['Size']} bytes")

# 접두사 필터
response = r2.list_objects_v2(
    Bucket='my-bucket',
    Prefix='images/',
    Delimiter='/'
)

# 폴더 (CommonPrefixes)
for prefix in response.get('CommonPrefixes', []):
    print(f"Folder: {prefix['Prefix']}")

# 파일
for obj in response.get('Contents', []):
    print(f"File: {obj['Key']}")

# 페이지네이션 (모든 객체 가져오기)
paginator = r2.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket='my-bucket'):
    for obj in page.get('Contents', []):
        print(obj['Key'])
```

---

## Presigned URLs - 서명된 URL

### 업로드용 Presigned URL

```python
# 업로드 URL 생성 (PUT)
url = r2.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'uploads/user-file.txt',
        'ContentType': 'text/plain'
    },
    ExpiresIn=3600  # 1시간
)
print(url)

# 클라이언트에서 업로드
# curl -X PUT -H "Content-Type: text/plain" --data-binary "@file.txt" "<presigned_url>"
```

```javascript
// Node.js
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { PutObjectCommand } from "@aws-sdk/client-s3";

const url = await getSignedUrl(r2, new PutObjectCommand({
  Bucket: "my-bucket",
  Key: "uploads/user-file.txt",
  ContentType: "text/plain",
}), { expiresIn: 3600 });
```

### 다운로드용 Presigned URL

```python
# 다운로드 URL 생성 (GET)
url = r2.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'files/document.pdf'
    },
    ExpiresIn=3600
)

# 응답 헤더 커스터마이징
url = r2.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'files/document.pdf',
        'ResponseContentDisposition': 'attachment; filename="download.pdf"',
        'ResponseContentType': 'application/pdf'
    },
    ExpiresIn=3600
)
```

### Presigned POST - 폼 업로드

```python
# 브라우저 폼 업로드용 Presigned POST
post = r2.generate_presigned_post(
    Bucket='my-bucket',
    Key='uploads/${filename}',
    Fields={
        'Content-Type': 'image/png'
    },
    Conditions=[
        {'Content-Type': 'image/png'},
        ['content-length-range', 0, 10485760],  # 최대 10MB
    ],
    ExpiresIn=3600
)

# HTML 폼에서 사용
# <form action="{post['url']}" method="post" enctype="multipart/form-data">
#   <input type="hidden" name="key" value="uploads/${filename}">
#   ... fields ...
#   <input type="file" name="file">
# </form>
```

---

## 멀티파트 업로드

대용량 파일(100MB 이상)은 멀티파트 업로드 권장

### CLI 자동 멀티파트

```bash
# s3 cp/sync는 자동으로 멀티파트 처리
aws s3 cp ./large-file.zip s3://my-bucket/ \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 멀티파트 임계값 조정
aws configure set s3.multipart_threshold 100MB --profile r2
aws configure set s3.multipart_chunksize 50MB --profile r2
```

### 수동 멀티파트 업로드

```python
# 1. 멀티파트 업로드 시작
response = r2.create_multipart_upload(
    Bucket='my-bucket',
    Key='large-file.zip',
    ContentType='application/zip'
)
upload_id = response['UploadId']

# 2. 파트 업로드
parts = []
part_size = 50 * 1024 * 1024  # 50MB

with open('large-file.zip', 'rb') as f:
    part_number = 1
    while True:
        data = f.read(part_size)
        if not data:
            break

        response = r2.upload_part(
            Bucket='my-bucket',
            Key='large-file.zip',
            UploadId=upload_id,
            PartNumber=part_number,
            Body=data
        )
        parts.append({
            'PartNumber': part_number,
            'ETag': response['ETag']
        })
        part_number += 1

# 3. 멀티파트 완료
r2.complete_multipart_upload(
    Bucket='my-bucket',
    Key='large-file.zip',
    UploadId=upload_id,
    MultipartUpload={'Parts': parts}
)
```

### 멀티파트 관리

```python
# 진행 중인 멀티파트 업로드 목록
response = r2.list_multipart_uploads(Bucket='my-bucket')
for upload in response.get('Uploads', []):
    print(f"{upload['Key']} - {upload['UploadId']}")

# 멀티파트 업로드 취소
r2.abort_multipart_upload(
    Bucket='my-bucket',
    Key='large-file.zip',
    UploadId='<upload_id>'
)

# 업로드된 파트 목록
response = r2.list_parts(
    Bucket='my-bucket',
    Key='large-file.zip',
    UploadId='<upload_id>'
)
```

---

## CORS 설정

### CORS 규칙 설정

```bash
# CORS 규칙 적용
aws s3api put-bucket-cors \
  --bucket my-bucket \
  --cors-configuration file://cors.json \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

cors.json:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://example.com", "https://*.example.com"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag", "x-amz-meta-*"],
      "MaxAgeSeconds": 3600
    }
  ]
}
```

```python
# Python으로 CORS 설정
r2.put_bucket_cors(
    Bucket='my-bucket',
    CORSConfiguration={
        'CORSRules': [
            {
                'AllowedOrigins': ['https://example.com'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE'],
                'AllowedHeaders': ['*'],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3600
            }
        ]
    }
)

# CORS 규칙 조회
response = r2.get_bucket_cors(Bucket='my-bucket')
print(response['CORSRules'])

# CORS 규칙 삭제
r2.delete_bucket_cors(Bucket='my-bucket')
```

---

## 에러 핸들링

### 일반적인 에러

```python
from botocore.exceptions import ClientError

try:
    r2.get_object(Bucket='my-bucket', Key='nonexistent.txt')
except ClientError as e:
    error_code = e.response['Error']['Code']

    if error_code == 'NoSuchKey':
        print("파일이 존재하지 않습니다")
    elif error_code == 'AccessDenied':
        print("접근 권한이 없습니다")
    elif error_code == 'NoSuchBucket':
        print("버킷이 존재하지 않습니다")
    else:
        print(f"오류: {error_code}")
```

### 재시도 설정

```python
from botocore.config import Config

# 재시도 설정
config = Config(
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    },
    connect_timeout=5,
    read_timeout=60
)

r2 = boto3.client('s3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>',
    config=config
)
```

---

## 다음 단계

- [[03-workers|Workers와 R2 바인딩]] - 서버리스 통합
- [[04-public-access|퍼블릭 액세스 설정]] - 공개 URL 구성
