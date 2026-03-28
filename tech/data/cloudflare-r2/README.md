# Cloudflare R2 학습 가이드

## 개요

Cloudflare R2는 S3 호환 오브젝트 스토리지 서비스로, **이그레스(데이터 전송) 비용이 무료**라는 혁신적인 가격 정책을 제공합니다. AWS S3 API와 100% 호환되어 기존 도구와 SDK를 그대로 사용할 수 있습니다.

## 목차

### 기초 학습
- [[01-overview|01. 개요]] - 핵심 개념, 장단점, 사용 사례
- [[02-ecosystem|02. 에코시스템]] - 관련 기술, 비교, 트렌드
- [[03-references|03. 참고 자료]] - 공식 문서, 학습 자료, 커뮤니티

### 실습 가이드
- [[04-learning/01-setup|01. 버킷 생성 및 기본 설정]]
- [[04-learning/02-s3-api|02. S3 호환 API 사용]]
- [[04-learning/03-workers|03. Workers와 R2 바인딩]]
- [[04-learning/04-public-access|04. 퍼블릭 액세스 및 Custom Domain]]
- [[04-learning/05-lifecycle|05. 라이프사이클 규칙 및 정책]]
- [[04-learning/06-sdk-integration|06. AWS SDK, boto3 통합]]

### 실전 & 참조
- [[05-projects|05. 실전 프로젝트]] - Best Practices
- [[cheatsheet|치트시트]] - 빠른 참조

---

## Quick Start

### 1단계: Cloudflare 계정 및 버킷 생성
```bash
# Cloudflare 대시보드 접속
# https://dash.cloudflare.com/

# R2 → 버킷 생성 → 버킷 이름 입력 → 생성
```

### 2단계: API 토큰 생성
```bash
# R2 → 개요 → API 토큰 관리 → API 토큰 생성
# 권한: 오브젝트 읽기 및 쓰기
# Access Key ID와 Secret Access Key 저장
```

### 3단계: AWS CLI로 연결
```bash
# AWS CLI 설정
aws configure --profile r2
# Access Key ID: <R2 Access Key>
# Secret Access Key: <R2 Secret Key>
# Region: auto
# Output format: json

# 버킷 목록 확인
aws s3 ls --endpoint-url https://<ACCOUNT_ID>.r2.cloudflarestorage.com --profile r2
```

### 4단계: 파일 업로드
```bash
# 파일 업로드
aws s3 cp ./myfile.txt s3://my-bucket/ \
  --endpoint-url https://<ACCOUNT_ID>.r2.cloudflarestorage.com \
  --profile r2
```

---

## 학습 플랜

### Week 1: 기초 (2-3일)
- [ ] R2 개념 및 S3와의 차이점 이해
- [ ] Cloudflare 계정 생성 및 대시보드 탐색
- [ ] 첫 번째 버킷 생성
- [ ] API 토큰 생성 및 AWS CLI 연결

### Week 2: 핵심 기능 (3-4일)
- [ ] S3 API로 CRUD 작업 수행
- [ ] 퍼블릭 액세스 설정
- [ ] Custom Domain 연결
- [ ] CORS 설정

### Week 3: Workers 통합 (3-4일)
- [ ] Cloudflare Workers 기초 학습
- [ ] R2 바인딩 설정
- [ ] Workers로 이미지 리사이징 구현
- [ ] 인증된 업로드/다운로드 구현

### Week 4: 실전 프로젝트 (4-5일)
- [ ] 라이프사이클 규칙 설정
- [ ] SDK 통합 (Node.js, Python)
- [ ] 미니 프로젝트 완성
- [ ] 모니터링 및 비용 분석

---

## 핵심 장점 요약

| 특징 | 설명 |
|------|------|
| 이그레스 무료 | 데이터 전송 비용 $0 (AWS S3 대비 최대 90% 절감) |
| S3 호환 | 기존 S3 도구/SDK 그대로 사용 가능 |
| Workers 통합 | 서버리스 엣지 컴퓨팅과 네이티브 연동 |
| 무료 티어 | 10GB 저장, Class A 1,000만/Class B 1억 연산 무료 |
| 글로벌 분산 | Cloudflare 네트워크 활용한 빠른 액세스 |

---

## 관련 문서

- [Cloudflare R2 공식 문서](https://developers.cloudflare.com/r2/)
- [R2 가격 정책](https://developers.cloudflare.com/r2/pricing/)
- [Workers 공식 문서](https://developers.cloudflare.com/workers/)
