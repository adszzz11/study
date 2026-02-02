# Cloudflare R2 에코시스템

## 관련 기술 스택

### Cloudflare 제품군 연동

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare Platform                       │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Workers │  │  Pages  │  │   D1    │  │   KV    │        │
│  │ 서버리스 │  │ 정적호스팅│  │   DB    │  │ Key-Value│       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
│       └────────────┴─────┬──────┴────────────┘              │
│                          │                                   │
│                    ┌─────▼─────┐                            │
│                    │    R2     │                            │
│                    │  Storage  │                            │
│                    └───────────┘                            │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  CDN    │  │  WAF    │  │  DNS    │  │ Images  │        │
│  │ 캐싱    │  │ 보안    │  │ 도메인  │  │ 이미지  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### 1. Workers (서버리스 컴퓨팅)
R2와 가장 긴밀하게 연동되는 서비스입니다.

```javascript
// Workers에서 R2 바인딩 사용
export default {
  async fetch(request, env) {
    // 파일 읽기
    const object = await env.MY_BUCKET.get("image.png");

    // 파일 쓰기
    await env.MY_BUCKET.put("new-file.txt", "content");

    // 파일 삭제
    await env.MY_BUCKET.delete("old-file.txt");

    return new Response(object.body);
  }
}
```

**활용 사례:**
- 이미지 리사이징/최적화
- 인증된 파일 다운로드
- 동적 콘텐츠 생성
- API 게이트웨이

### 2. Pages (정적 사이트 호스팅)
정적 사이트의 에셋 저장소로 R2 활용

```
Pages 사이트 구조:
├── /public (Pages에서 호스팅)
│   ├── index.html
│   └── style.css
└── /assets (R2에서 호스팅)
    ├── images/
    ├── videos/
    └── downloads/
```

### 3. D1 (서버리스 SQL 데이터베이스)
메타데이터는 D1에, 파일은 R2에 저장

```javascript
// D1에 파일 메타데이터 저장
await db.prepare(`
  INSERT INTO files (id, name, r2_key, size, created_at)
  VALUES (?, ?, ?, ?, ?)
`).bind(id, name, r2Key, size, Date.now()).run();

// R2에 실제 파일 저장
await env.BUCKET.put(r2Key, fileData);
```

### 4. KV (Key-Value 스토리지)
캐시 메타데이터, 세션 정보 등 저장

```javascript
// KV에 캐시 정보 저장
await env.CACHE_KV.put(`file:${key}:etag`, etag);

// R2에서 파일 제공
const object = await env.BUCKET.get(key);
```

### 5. Images (이미지 변환)
R2 이미지를 Cloudflare Images로 실시간 변환

```
원본 URL: https://r2.example.com/photos/original.jpg
변환 URL: https://example.com/cdn-cgi/image/width=400,format=webp/photos/original.jpg
```

---

## 오브젝트 스토리지 비교

### 주요 서비스 비교표

| 특성 | Cloudflare R2 | AWS S3 | Google Cloud Storage | Azure Blob |
|------|--------------|--------|---------------------|------------|
| **이그레스 비용** | **무료** | $0.09/GB | $0.12/GB | $0.087/GB |
| 저장 비용 (/GB/월) | $0.015 | $0.023 | $0.020 | $0.018 |
| S3 호환 | O | 원본 | O | 부분 |
| CDN 통합 | 네이티브 | CloudFront 별도 | Cloud CDN 별도 | Azure CDN 별도 |
| 무료 티어 | 10GB | 5GB (12개월) | 5GB | 5GB |
| 서버리스 통합 | Workers | Lambda | Cloud Functions | Azure Functions |
| 리전 선택 | 불가 | 가능 | 가능 | 가능 |
| 버전 관리 | 베타 | 완전 지원 | 완전 지원 | 완전 지원 |

### 비용 시나리오 비교

#### 시나리오 1: 콘텐츠 배포 서비스
```
조건: 1TB 저장, 10TB/월 다운로드

Cloudflare R2:
├── 저장: 1TB × $0.015 = $15
├── 이그레스: 10TB × $0 = $0
└── 총계: $15/월

AWS S3 + CloudFront:
├── 저장: 1TB × $0.023 = $23
├── 이그레스: 10TB × $0.085 = $850
└── 총계: $873/월

절감액: $858/월 (98% 절감)
```

#### 시나리오 2: 백업 스토리지
```
조건: 100GB 저장, 1GB/월 복원

Cloudflare R2:
├── 저장: 100GB × $0.015 = $1.50
├── 이그레스: 1GB × $0 = $0
└── 총계: $1.50/월

AWS S3 Glacier:
├── 저장: 100GB × $0.004 = $0.40
├── 복원 요청: ~$0.30
├── 이그레스: 1GB × $0.09 = $0.09
└── 총계: ~$0.79/월

R2가 더 비싸지만 즉시 접근 가능
```

### 언제 어떤 서비스를 선택할까?

```
R2 선택 권장:
├── 높은 다운로드 트래픽 예상
├── Workers 활용 계획
├── 비용 예측 가능성 중요
└── CDN 통합 필요

S3 선택 권장:
├── 버전 관리 필수
├── 특정 리전 규정 준수 필요
├── 고급 S3 기능 필요 (객체 잠금, 복제)
└── AWS 생태계 깊은 통합

GCS 선택 권장:
├── GCP 생태계 사용 중
├── BigQuery 연동 필요
└── Nearline/Coldline 스토리지 클래스 활용

Azure Blob 선택 권장:
├── Azure 생태계 사용 중
├── Microsoft 365 통합 필요
└── 하이브리드 클라우드 구성
```

---

## S3 호환성 현황

### 지원되는 S3 API

```
완전 지원:
├── GetObject, PutObject, DeleteObject
├── HeadObject, CopyObject
├── ListBuckets, ListObjectsV2
├── CreateMultipartUpload, UploadPart, CompleteMultipartUpload
├── GetBucketLocation
├── PutBucketCors, GetBucketCors, DeleteBucketCors
└── Presigned URLs

부분 지원:
├── GetObjectAcl, PutObjectAcl (제한적)
└── GetBucketAcl, PutBucketAcl (제한적)

미지원:
├── GetBucketVersioning, PutBucketVersioning (베타)
├── GetObjectLockConfiguration
├── PutBucketReplication
├── SelectObjectContent
└── S3 Inventory, S3 Analytics
```

### 호환 도구 목록

```
CLI 도구:
├── AWS CLI (완전 지원)
├── s3cmd (완전 지원)
├── rclone (완전 지원)
├── MinIO Client (mc) (완전 지원)
└── Cyberduck (완전 지원)

SDK:
├── AWS SDK (모든 언어)
├── boto3 (Python)
├── @aws-sdk/client-s3 (JavaScript/Node.js)
├── aws-sdk-go (Go)
└── AWS SDK for Java

백업 도구:
├── Restic
├── Duplicati
├── Rclone
└── CloudBerry

미디어 도구:
├── Mux
├── imgproxy
└── Thumbor
```

---

## 최신 트렌드 및 로드맵

### 2024년 주요 업데이트

```
최근 출시된 기능:
├── 이벤트 알림 (Event Notifications)
├── 버전 관리 (베타)
├── 수명 주기 규칙 (Lifecycle Rules)
├── 객체 수준 메타데이터 인덱싱
└── Super Slurper (대용량 마이그레이션)

개발 중인 기능:
├── 멀티파트 업로드 개선
├── 버전 관리 정식 출시
├── 객체 복제 (Cross-Region)
└── 향상된 분석 기능
```

### 산업 트렌드

#### 1. 이그레스 비용 경쟁
```
R2의 제로 이그레스 정책이 업계 표준 변화 촉진:
├── AWS: S3 Select 이그레스 무료화
├── Google: 일부 서비스 이그레스 절감
├── Backblaze B2: 저렴한 이그레스 유지
└── 전반적인 클라우드 이그레스 비용 하락 추세
```

#### 2. 엣지 컴퓨팅과의 통합
```
엣지에서 데이터 처리하는 패턴 증가:
├── 이미지 최적화
├── 동적 콘텐츠 생성
├── AI/ML 추론
└── 실시간 데이터 변환
```

#### 3. S3 호환 생태계 성장
```
S3 API가 사실상 업계 표준화:
├── MinIO (온프레미스 S3)
├── Wasabi (저비용 스토리지)
├── Backblaze B2 (S3 호환 추가)
└── R2 (이그레스 무료)
```

---

## 마이그레이션 고려사항

### S3에서 R2로 마이그레이션

```bash
# Super Slurper 사용 (Cloudflare 공식 도구)
# 대시보드에서 설정: R2 → 버킷 → 설정 → Data Migration

# 또는 rclone 사용
rclone sync s3:my-s3-bucket r2:my-r2-bucket \
  --progress \
  --transfers 32

# 또는 AWS CLI 사용 (소규모)
aws s3 sync s3://my-s3-bucket s3://my-r2-bucket \
  --source-region us-east-1 \
  --endpoint-url https://<ACCOUNT_ID>.r2.cloudflarestorage.com
```

### 마이그레이션 체크리스트

```
사전 준비:
├── [ ] 현재 S3 사용량 분석 (저장, 요청, 이그레스)
├── [ ] R2 미지원 기능 사용 여부 확인
├── [ ] 애플리케이션 호환성 테스트
└── [ ] 비용 절감 예상치 계산

마이그레이션 단계:
├── [ ] R2 버킷 생성 및 권한 설정
├── [ ] 데이터 복사 (Super Slurper 또는 rclone)
├── [ ] 애플리케이션 엔드포인트 변경
├── [ ] 테스트 및 검증
└── [ ] S3 버킷 정리

마이그레이션 후:
├── [ ] 모니터링 설정
├── [ ] 비용 추적
└── [ ] 성능 최적화
```

---

## 다음 단계

- [[03-references|참고 자료]] - 공식 문서 및 학습 자료
- [[04-learning/01-setup|버킷 생성]] - 실습 시작하기
