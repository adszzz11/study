# 라이프사이클 규칙 및 정책

## 라이프사이클 규칙 개요

라이프사이클 규칙을 사용하면 객체를 자동으로 관리할 수 있습니다. 예를 들어 오래된 파일 자동 삭제, 임시 파일 정리 등이 가능합니다.

### 주요 사용 사례

```
라이프사이클 규칙 활용:
├── 임시 파일 자동 삭제
│   └── 업로드 후 24시간 뒤 삭제
├── 로그 파일 관리
│   └── 30일 이후 자동 삭제
├── 백업 보관 정책
│   └── 90일 이후 삭제
├── 불완전 멀티파트 업로드 정리
│   └── 7일 이후 자동 삭제
└── 버전 관리 (베타)
    └── 이전 버전 자동 삭제
```

---

## 대시보드에서 설정

### 라이프사이클 규칙 생성

```
1. Cloudflare 대시보드 → R2

2. 버킷 선택 → Settings 탭

3. Object lifecycle rules 섹션

4. "Add rule" 클릭

5. 규칙 설정:
   ├── Rule name: 규칙 이름
   ├── Prefix filter: 접두사 필터 (선택)
   ├── Action: Delete objects
   └── Days after object creation: 일수
```

### 설정 예시

```
규칙 1: 임시 파일 삭제
├── Rule name: Delete temp files
├── Prefix: tmp/
├── Action: Delete objects
└── Days: 1

규칙 2: 로그 파일 삭제
├── Rule name: Delete old logs
├── Prefix: logs/
├── Action: Delete objects
└── Days: 30

규칙 3: 불완전 업로드 정리
├── Rule name: Abort incomplete uploads
├── Prefix: (없음 - 전체 적용)
├── Action: Abort incomplete multipart uploads
└── Days: 7
```

---

## API로 라이프사이클 설정

### Cloudflare API 사용

```bash
# 라이프사이클 규칙 조회
curl -X GET \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/r2/buckets/<BUCKET_NAME>/lifecycle" \
  -H "Authorization: Bearer <API_TOKEN>"

# 라이프사이클 규칙 설정
curl -X PUT \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/r2/buckets/<BUCKET_NAME>/lifecycle" \
  -H "Authorization: Bearer <API_TOKEN>" \
  -H "Content-Type: application/json" \
  --data '{
    "rules": [
      {
        "id": "delete-temp-files",
        "enabled": true,
        "conditions": {
          "prefix": "tmp/"
        },
        "action": {
          "type": "DeleteObject",
          "deleteAfterDays": 1
        }
      }
    ]
  }'
```

### S3 API로 설정 (호환)

```python
import boto3

r2 = boto3.client('s3',
    endpoint_url='https://<ACCOUNT_ID>.r2.cloudflarestorage.com',
    aws_access_key_id='<ACCESS_KEY>',
    aws_secret_access_key='<SECRET_KEY>'
)

# 라이프사이클 규칙 설정
lifecycle_config = {
    'Rules': [
        {
            'ID': 'delete-temp-files',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': 'tmp/'
            },
            'Expiration': {
                'Days': 1
            }
        },
        {
            'ID': 'delete-old-logs',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': 'logs/'
            },
            'Expiration': {
                'Days': 30
            }
        },
        {
            'ID': 'abort-incomplete-uploads',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': ''
            },
            'AbortIncompleteMultipartUpload': {
                'DaysAfterInitiation': 7
            }
        }
    ]
}

r2.put_bucket_lifecycle_configuration(
    Bucket='my-bucket',
    LifecycleConfiguration=lifecycle_config
)
```

```python
# 라이프사이클 규칙 조회
response = r2.get_bucket_lifecycle_configuration(Bucket='my-bucket')
for rule in response['Rules']:
    print(f"Rule: {rule['ID']}")
    print(f"  Status: {rule['Status']}")
    print(f"  Prefix: {rule['Filter'].get('Prefix', 'N/A')}")
    if 'Expiration' in rule:
        print(f"  Expiration: {rule['Expiration']['Days']} days")

# 라이프사이클 규칙 삭제
r2.delete_bucket_lifecycle(Bucket='my-bucket')
```

---

## 라이프사이클 규칙 패턴

### 패턴 1: 임시 업로드 정리

사용자 업로드 후 처리 완료되면 삭제

```python
# 구조
# uploads/temp/{session_id}/{filename}  ← 임시
# uploads/permanent/{user_id}/{filename} ← 영구

lifecycle_config = {
    'Rules': [
        {
            'ID': 'cleanup-temp-uploads',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': 'uploads/temp/'
            },
            'Expiration': {
                'Days': 1  # 24시간 후 삭제
            }
        }
    ]
}
```

### 패턴 2: 로그 보관 정책

```python
lifecycle_config = {
    'Rules': [
        # 액세스 로그: 7일 보관
        {
            'ID': 'access-logs-retention',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'logs/access/'},
            'Expiration': {'Days': 7}
        },
        # 에러 로그: 30일 보관
        {
            'ID': 'error-logs-retention',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'logs/error/'},
            'Expiration': {'Days': 30}
        },
        # 감사 로그: 365일 보관
        {
            'ID': 'audit-logs-retention',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'logs/audit/'},
            'Expiration': {'Days': 365}
        }
    ]
}
```

### 패턴 3: 백업 관리

```python
lifecycle_config = {
    'Rules': [
        # 일일 백업: 7일 보관
        {
            'ID': 'daily-backup-retention',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'backups/daily/'},
            'Expiration': {'Days': 7}
        },
        # 주간 백업: 30일 보관
        {
            'ID': 'weekly-backup-retention',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'backups/weekly/'},
            'Expiration': {'Days': 30}
        },
        # 월간 백업: 365일 보관
        {
            'ID': 'monthly-backup-retention',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'backups/monthly/'},
            'Expiration': {'Days': 365}
        }
    ]
}
```

### 패턴 4: 미디어 파일 관리

```python
lifecycle_config = {
    'Rules': [
        # 썸네일 캐시: 30일 보관
        {
            'ID': 'thumbnail-cache',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'cache/thumbnails/'},
            'Expiration': {'Days': 30}
        },
        # 변환된 비디오: 90일 보관
        {
            'ID': 'transcoded-videos',
            'Status': 'Enabled',
            'Filter': {'Prefix': 'videos/transcoded/'},
            'Expiration': {'Days': 90}
        }
    ]
}
```

---

## 버킷 정책

### 현재 지원 상태

```
R2 버킷 정책 지원 현황:
├── 퍼블릭 액세스 설정: 지원
├── CORS 정책: 지원
├── 라이프사이클 규칙: 지원
├── IAM 스타일 정책: 제한적
└── ACL: 제한적 지원
```

### API 토큰 권한 관리

```
API 토큰 권한 레벨:
├── Admin Read & Write
│   └── 모든 버킷, 모든 작업
├── Object Read & Write
│   └── 객체 CRUD, 버킷 설정 불가
├── Object Read only
│   └── 읽기만 가능
└── 버킷별 권한 제한
    └── 특정 버킷만 접근 가능
```

### 토큰 생성 예시

```
시나리오별 토큰 구성:

1. 백엔드 서버용 (전체 권한)
   ├── 권한: Admin Read & Write
   └── 버킷: 모든 버킷

2. 업로드 전용 (클라이언트)
   ├── 권한: Object Write only
   └── 버킷: uploads-bucket

3. CDN 원본용 (읽기 전용)
   ├── 권한: Object Read only
   └── 버킷: static-bucket

4. 백업 에이전트용
   ├── 권한: Object Read & Write
   └── 버킷: backup-bucket
```

---

## 이벤트 알림

R2는 객체 변경 시 이벤트 알림을 지원합니다.

### 이벤트 알림 설정

```
1. R2 → 버킷 → Settings → Event notifications

2. "Add notification" 클릭

3. 설정:
   ├── Event types:
   │   ├── object-create (생성)
   │   ├── object-delete (삭제)
   │   └── object-copy (복사)
   ├── Prefix filter: (선택)
   ├── Suffix filter: (선택)
   └── Queue: 연결할 Queue 선택
```

### Workers Queue와 연동

```typescript
// wrangler.toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

[[queues.consumers]]
queue = "r2-events"
max_batch_size = 10

// Worker에서 이벤트 처리
export default {
  async queue(batch: MessageBatch<R2EventNotification>, env: Env) {
    for (const message of batch.messages) {
      const event = message.body;

      console.log(`Event: ${event.eventType}`);
      console.log(`Bucket: ${event.bucket}`);
      console.log(`Object: ${event.object.key}`);

      // 이미지 업로드 시 썸네일 생성
      if (event.eventType === 'object-create' &&
          event.object.key.startsWith('images/')) {
        await createThumbnail(env, event.object.key);
      }

      message.ack();
    }
  }
};

async function createThumbnail(env: Env, key: string) {
  // 썸네일 생성 로직
}
```

---

## 비용 관리

### 라이프사이클로 비용 최적화

```
비용 최적화 전략:

1. 불필요한 데이터 자동 삭제
   └── 임시 파일, 캐시, 오래된 로그

2. 불완전 업로드 정리
   └── 멀티파트 업로드 실패 시 파트 삭제

3. 버전 관리 정리 (베타)
   └── 오래된 버전 자동 삭제

저장 비용 절감 예시:
├── 월 1TB 불필요 데이터 삭제
├── 절감: 1TB × $0.015 = $15/월
└── 연간: $180 절감
```

### 사용량 모니터링

```bash
# Cloudflare API로 사용량 조회
curl -X GET \
  "https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/r2/buckets/<BUCKET_NAME>/usage" \
  -H "Authorization: Bearer <API_TOKEN>"

# 응답 예시
{
  "result": {
    "payloadSize": 10737418240,  // 10GB
    "metadataSize": 1048576,     // 1MB
    "objectCount": 1000,
    "uploadCount": 500
  }
}
```

---

## 모범 사례

### 폴더 구조 설계

```
버킷 구조 권장:

my-bucket/
├── permanent/          # 영구 보관 (라이프사이클 없음)
│   ├── user-data/
│   └── documents/
├── temporary/          # 임시 (1일 후 삭제)
│   ├── uploads/
│   └── processing/
├── cache/             # 캐시 (7일 후 삭제)
│   ├── thumbnails/
│   └── transformed/
├── logs/              # 로그 (보관 기간별)
│   ├── access/        # 7일
│   ├── error/         # 30일
│   └── audit/         # 365일
└── backups/           # 백업 (기간별)
    ├── daily/         # 7일
    ├── weekly/        # 30일
    └── monthly/       # 365일
```

### 라이프사이클 규칙 팁

```
권장 사항:
├── 접두사(Prefix) 기반 규칙 설계
│   └── 폴더 구조와 라이프사이클 일치
├── 규칙 이름 명확하게 지정
│   └── "delete-temp-uploads-after-1-day"
├── 테스트 후 적용
│   └── 소규모 데이터로 먼저 테스트
└── 문서화
    └── 어떤 규칙이 왜 필요한지 기록

주의 사항:
├── 삭제된 데이터는 복구 불가
├── 규칙 적용까지 최대 24시간 소요
├── 버킷 단위로만 설정 가능
└── 너무 많은 규칙은 관리 복잡성 증가
```

---

## 다음 단계

- [[06-sdk-integration|SDK 통합]] - 프로그래밍 언어별 통합
- [[../05-projects|실전 프로젝트]] - Best Practices 적용
