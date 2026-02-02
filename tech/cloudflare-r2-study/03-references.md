# Cloudflare R2 참고 자료

## 공식 문서

### Cloudflare 공식
- [R2 Documentation](https://developers.cloudflare.com/r2/) - R2 공식 문서 (영문)
- [R2 API Reference](https://developers.cloudflare.com/r2/api/) - S3 API 호환성 문서
- [R2 Pricing](https://developers.cloudflare.com/r2/pricing/) - 가격 정책 상세
- [R2 Examples](https://developers.cloudflare.com/r2/examples/) - 공식 예제 코드

### Workers 관련
- [Workers Documentation](https://developers.cloudflare.com/workers/) - Workers 공식 문서
- [R2 Bindings](https://developers.cloudflare.com/r2/api/workers/workers-api-reference/) - Workers R2 바인딩 API

### 관련 서비스
- [Pages Documentation](https://developers.cloudflare.com/pages/)
- [D1 Documentation](https://developers.cloudflare.com/d1/)
- [KV Documentation](https://developers.cloudflare.com/kv/)

---

## 학습 자료

### 공식 튜토리얼
- [Getting Started with R2](https://developers.cloudflare.com/r2/get-started/)
- [Migrating from S3](https://developers.cloudflare.com/r2/data-migration/sippy/)
- [Configure CORS](https://developers.cloudflare.com/r2/buckets/cors/)
- [Public Buckets](https://developers.cloudflare.com/r2/buckets/public-buckets/)

### 영상 강의

#### Cloudflare 공식 채널
- [Cloudflare TV - R2 소개](https://cloudflare.tv/)
- [R2 발표 영상 (Developer Week 2022)](https://www.youtube.com/cloudflare)

#### 추천 YouTube 영상
```
초급:
├── "Cloudflare R2 Tutorial - Zero Egress Object Storage"
├── "How to Use Cloudflare R2 with AWS S3 API"
└── "R2 vs S3 Cost Comparison"

중급:
├── "Cloudflare Workers + R2 Full Stack Tutorial"
├── "Building a CDN with R2 and Workers"
└── "Image Optimization with R2"

고급:
├── "Migrating Petabytes to R2"
├── "R2 Performance Optimization"
└── "Building SaaS on Cloudflare Stack"
```

### 블로그 포스트

#### Cloudflare 공식 블로그
- [Announcing Cloudflare R2 Storage](https://blog.cloudflare.com/introducing-r2-object-storage/)
- [R2 is now Generally Available](https://blog.cloudflare.com/r2-ga/)
- [Building a Global File Storage](https://blog.cloudflare.com/)

#### 기술 블로그 추천
```
한국어:
├── 44bits.io - "Cloudflare R2 소개"
├── 개발자 개인 블로그들
└── Velog, Tistory R2 관련 포스트

영어:
├── Dev.to - "Getting Started with R2"
├── Medium - "R2 vs S3 Deep Dive"
├── Hashnode - R2 튜토리얼들
└── freeCodeCamp - 관련 강좌
```

---

## 커뮤니티

### Discord
- [Cloudflare Workers Discord](https://discord.gg/cloudflaredev) - 공식 개발자 커뮤니티
  - `#r2-storage` 채널에서 R2 관련 질문/토론
  - 빠른 응답, 활발한 커뮤니티

### 포럼
- [Cloudflare Community](https://community.cloudflare.com/) - 공식 포럼
  - Developers 카테고리에서 R2 관련 토픽
- [Stack Overflow](https://stackoverflow.com/questions/tagged/cloudflare-r2) - `cloudflare-r2` 태그

### GitHub
- [Cloudflare Workers Examples](https://github.com/cloudflare/workers-sdk) - 공식 예제 저장소
- [R2 Examples](https://github.com/cloudflare/r2-examples) - R2 전용 예제 (존재시)
- [Wrangler](https://github.com/cloudflare/workers-sdk/tree/main/packages/wrangler) - CLI 도구

### Reddit
- [r/CloudFlare](https://www.reddit.com/r/CloudFlare/) - Cloudflare 커뮤니티
- [r/selfhosted](https://www.reddit.com/r/selfhosted/) - 셀프호스팅 (R2 활용 사례)

---

## 도구 및 라이브러리

### CLI 도구

```bash
# Wrangler (Cloudflare 공식)
npm install -g wrangler
wrangler r2 bucket list
wrangler r2 object get my-bucket/my-key

# AWS CLI
pip install awscli
aws s3 ls --endpoint-url https://<ACCOUNT_ID>.r2.cloudflarestorage.com

# rclone
brew install rclone  # macOS
rclone sync local-folder r2:my-bucket

# MinIO Client
brew install minio/stable/mc  # macOS
mc alias set r2 https://<ACCOUNT_ID>.r2.cloudflarestorage.com ACCESS_KEY SECRET_KEY
mc ls r2/my-bucket
```

### SDK 라이브러리

#### JavaScript/TypeScript
```javascript
// @aws-sdk/client-s3 (추천)
npm install @aws-sdk/client-s3

// 또는 aws-sdk v2
npm install aws-sdk
```

#### Python
```python
# boto3 (추천)
pip install boto3

# 또는 aioboto3 (비동기)
pip install aioboto3
```

#### Go
```go
// aws-sdk-go-v2
go get github.com/aws/aws-sdk-go-v2
go get github.com/aws/aws-sdk-go-v2/service/s3
```

#### Java
```xml
<!-- AWS SDK for Java v2 -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
</dependency>
```

### GUI 클라이언트

```
무료:
├── Cyberduck (macOS, Windows) - https://cyberduck.io/
├── WinSCP (Windows) - https://winscp.net/
└── S3 Browser (Windows) - https://s3browser.com/

유료:
├── Transmit (macOS) - https://panic.com/transmit/
├── CloudBerry Explorer - https://www.msp360.com/explorer/
└── S3cmd GUI - 다양한 옵션
```

---

## 관련 도서

### 클라우드 스토리지 일반
```
├── "클라우드 네이티브 패턴" - 전반적인 클라우드 아키텍처
├── "AWS 인 액션" - S3 관련 챕터 (호환성 참고용)
└── "Infrastructure as Code" - IaC 패턴 이해
```

### 웹 개발 / 서버리스
```
├── "서버리스 웹 애플리케이션 개발"
├── "실전 서버리스 아키텍처"
└── Workers/엣지 컴퓨팅 관련 자료
```

---

## 인증 및 자격증

### Cloudflare 공식
- Cloudflare 인증 프로그램은 현재 제한적
- [Cloudflare University](https://www.cloudflare.com/learning/) - 학습 자료

### 관련 자격증
```
AWS 자격증 (S3 호환성 이해에 도움):
├── AWS Cloud Practitioner
├── AWS Solutions Architect Associate
└── AWS Developer Associate

일반 클라우드:
├── Google Cloud Professional Cloud Architect
└── Azure Administrator Associate
```

---

## 유용한 외부 도구

### 마이그레이션
- [rclone](https://rclone.org/) - 멀티 클라우드 동기화 도구
- [Super Slurper](https://developers.cloudflare.com/r2/data-migration/super-slurper/) - Cloudflare 공식

### 모니터링
- [Cloudflare Analytics](https://dash.cloudflare.com/) - 내장 분석
- [Grafana + Prometheus](https://grafana.com/) - 커스텀 모니터링

### 백업
- [Restic](https://restic.net/) - R2 호환 백업 도구
- [Duplicati](https://www.duplicati.com/) - GUI 백업 도구

---

## 자주 참조하는 링크

### Quick Reference
| 용도 | 링크 |
|------|------|
| 대시보드 | https://dash.cloudflare.com/ |
| R2 가격 계산기 | https://developers.cloudflare.com/r2/pricing/ |
| API 레퍼런스 | https://developers.cloudflare.com/r2/api/ |
| 시스템 상태 | https://www.cloudflarestatus.com/ |
| 지원 티켓 | https://support.cloudflare.com/ |

### 엔드포인트 형식
```
S3 API 엔드포인트:
https://<ACCOUNT_ID>.r2.cloudflarestorage.com

퍼블릭 버킷 URL:
https://pub-<BUCKET_ID>.r2.dev/<KEY>

커스텀 도메인:
https://cdn.yourdomain.com/<KEY>
```

---

## 다음 단계

- [[04-learning/01-setup|버킷 생성 및 기본 설정]] - 실습 시작
- [[cheatsheet|치트시트]] - 빠른 참조
