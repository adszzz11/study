# R2 버킷 생성 및 기본 설정

## 사전 준비

### 필요한 것
- Cloudflare 계정 (무료 가능)
- 결제 수단 등록 (무료 티어 사용해도 필요)

### Cloudflare 계정 생성
1. https://dash.cloudflare.com/sign-up 접속
2. 이메일, 비밀번호 입력
3. 이메일 인증 완료

---

## 버킷 생성하기

### 대시보드에서 생성

```
1. Cloudflare 대시보드 로그인
   https://dash.cloudflare.com/

2. 좌측 사이드바 → R2 Object Storage 클릭

3. "Create bucket" 버튼 클릭

4. 버킷 설정:
   ├── Bucket name: my-first-bucket
   │   (소문자, 숫자, 하이픈만 가능, 3-63자)
   ├── Location hint: Automatic (권장)
   │   또는 특정 리전 힌트 선택
   └── "Create bucket" 클릭
```

### 버킷 이름 규칙
```
유효한 이름:
├── my-bucket
├── user-uploads-2024
├── static-assets
└── backup-data-kr

무효한 이름:
├── My-Bucket (대문자 불가)
├── my_bucket (언더스코어 불가)
├── -mybucket (하이픈으로 시작 불가)
└── ab (3자 미만 불가)
```

---

## API 토큰 생성

### S3 API 접근용 토큰

```
1. R2 개요 페이지 → "Manage R2 API Tokens" 클릭
   또는 우측 상단 "API" 클릭

2. "Create API token" 클릭

3. 토큰 설정:
   ├── Token name: my-r2-token
   ├── Permissions:
   │   ├── Object Read (읽기)
   │   ├── Object Write (쓰기)
   │   └── 또는 Admin Read & Write (전체 권한)
   ├── Specify bucket(s):
   │   ├── Apply to all buckets (모든 버킷)
   │   └── 또는 특정 버킷만 선택
   ├── TTL: 선택사항 (만료 시간)
   └── Client IP Address Filtering: 선택사항

4. "Create API Token" 클릭

5. 중요! 표시된 정보 저장:
   ├── Access Key ID: xxxxxxxxxxxxxxxx
   ├── Secret Access Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   └── Endpoint: https://<ACCOUNT_ID>.r2.cloudflarestorage.com
```

> 주의: Secret Access Key는 한 번만 표시됩니다. 반드시 안전하게 저장하세요.

### Account ID 확인
```
대시보드 우측 사이드바 또는
R2 개요 페이지에서 Account ID 확인
```

---

## AWS CLI 설정

### AWS CLI 설치

```bash
# macOS (Homebrew)
brew install awscli

# macOS (공식 설치 프로그램)
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows (PowerShell)
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# 설치 확인
aws --version
```

### R2용 프로필 설정

```bash
# R2 전용 프로필 생성
aws configure --profile r2

# 입력 내용:
# AWS Access Key ID: <R2 Access Key ID>
# AWS Secret Access Key: <R2 Secret Access Key>
# Default region name: auto
# Default output format: json
```

### 연결 테스트

```bash
# 환경 변수로 엔드포인트 설정 (편의상)
export R2_ENDPOINT="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"

# 버킷 목록 확인
aws s3 ls --endpoint-url $R2_ENDPOINT --profile r2

# 특정 버킷 내용 확인
aws s3 ls s3://my-first-bucket --endpoint-url $R2_ENDPOINT --profile r2
```

---

## 기본 파일 작업

### 파일 업로드

```bash
# 단일 파일 업로드
aws s3 cp ./test.txt s3://my-first-bucket/ \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 특정 경로(폴더)에 업로드
aws s3 cp ./image.png s3://my-first-bucket/images/ \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 디렉토리 전체 업로드
aws s3 cp ./local-folder s3://my-first-bucket/remote-folder \
  --recursive \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 동기화 (변경된 파일만 업로드)
aws s3 sync ./local-folder s3://my-first-bucket/folder \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

### 파일 다운로드

```bash
# 단일 파일 다운로드
aws s3 cp s3://my-first-bucket/test.txt ./downloaded.txt \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 디렉토리 다운로드
aws s3 cp s3://my-first-bucket/images ./local-images \
  --recursive \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 동기화
aws s3 sync s3://my-first-bucket/folder ./local-folder \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

### 파일 목록 조회

```bash
# 버킷 내 모든 객체 나열
aws s3 ls s3://my-first-bucket/ \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 재귀적으로 모든 객체 나열
aws s3 ls s3://my-first-bucket/ \
  --recursive \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 특정 접두사(폴더)의 객체만
aws s3 ls s3://my-first-bucket/images/ \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

### 파일 삭제

```bash
# 단일 파일 삭제
aws s3 rm s3://my-first-bucket/test.txt \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 디렉토리 삭제 (재귀)
aws s3 rm s3://my-first-bucket/images/ \
  --recursive \
  --endpoint-url $R2_ENDPOINT \
  --profile r2

# 버킷 내 모든 객체 삭제
aws s3 rm s3://my-first-bucket/ \
  --recursive \
  --endpoint-url $R2_ENDPOINT \
  --profile r2
```

---

## 대시보드에서 파일 관리

### 파일 업로드 (GUI)

```
1. R2 → 버킷 선택
2. "Upload" 버튼 클릭
3. 파일 드래그 앤 드롭 또는 "Select files" 클릭
4. 업로드 진행 확인
```

### 파일 관리

```
대시보드에서 가능한 작업:
├── 파일 목록 보기
├── 파일 미리보기
├── 파일 다운로드
├── 파일 삭제
├── 메타데이터 확인
└── 폴더 생성 (접두사)
```

---

## 편의 설정

### 쉘 별칭 설정

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가

# R2 엔드포인트 환경변수
export R2_ENDPOINT="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"

# R2 명령어 별칭
alias r2='aws s3 --endpoint-url $R2_ENDPOINT --profile r2'
alias r2api='aws s3api --endpoint-url $R2_ENDPOINT --profile r2'

# 사용 예시:
# r2 ls
# r2 cp file.txt s3://my-bucket/
# r2 sync ./folder s3://my-bucket/
```

### rclone 설정 (대안)

```bash
# rclone 설치
brew install rclone  # macOS

# R2 원격 저장소 설정
rclone config

# 설정 단계:
# n) New remote
# name> r2
# Storage> s3
# provider> Cloudflare
# access_key_id> <Access Key>
# secret_access_key> <Secret Key>
# endpoint> https://<ACCOUNT_ID>.r2.cloudflarestorage.com
# acl> private

# 사용 예시
rclone ls r2:my-bucket
rclone copy ./file.txt r2:my-bucket/
rclone sync ./folder r2:my-bucket/folder
```

---

## 버킷 설정

### CORS 설정

대시보드에서:
```
1. R2 → 버킷 선택 → Settings 탭
2. CORS Policy → Edit
3. JSON 규칙 추가
```

예시 CORS 규칙:
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

### 버킷 삭제

```
주의: 버킷 삭제 전 모든 객체를 삭제해야 합니다.

1. 모든 객체 삭제
   aws s3 rm s3://my-bucket --recursive --endpoint-url $R2_ENDPOINT --profile r2

2. 대시보드 → R2 → 버킷 → ⋮ 메뉴 → Delete

또는 CLI:
aws s3api delete-bucket --bucket my-bucket --endpoint-url $R2_ENDPOINT --profile r2
```

---

## 트러블슈팅

### 자주 발생하는 오류

```
오류: Access Denied
├── 원인: API 토큰 권한 부족
└── 해결: 토큰 권한 확인 및 재생성

오류: NoSuchBucket
├── 원인: 버킷 이름 오타 또는 미존재
└── 해결: 버킷 이름 확인

오류: SignatureDoesNotMatch
├── 원인: Access Key 또는 Secret Key 오류
└── 해결: 자격 증명 재확인

오류: InvalidEndpoint
├── 원인: 엔드포인트 URL 오류
└── 해결: Account ID 확인, URL 형식 검증
```

### 연결 테스트 스크립트

```bash
#!/bin/bash
# r2-test.sh

R2_ENDPOINT="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"

echo "Testing R2 connection..."

# 버킷 목록
echo "1. Listing buckets:"
aws s3 ls --endpoint-url $R2_ENDPOINT --profile r2

# 테스트 파일 생성 및 업로드
echo "2. Creating test file..."
echo "Hello R2" > /tmp/r2-test.txt

echo "3. Uploading test file..."
aws s3 cp /tmp/r2-test.txt s3://my-first-bucket/test.txt \
  --endpoint-url $R2_ENDPOINT --profile r2

echo "4. Listing bucket contents:"
aws s3 ls s3://my-first-bucket/ --endpoint-url $R2_ENDPOINT --profile r2

echo "5. Downloading test file..."
aws s3 cp s3://my-first-bucket/test.txt /tmp/r2-test-download.txt \
  --endpoint-url $R2_ENDPOINT --profile r2

echo "6. Verifying content:"
cat /tmp/r2-test-download.txt

echo "7. Cleaning up..."
aws s3 rm s3://my-first-bucket/test.txt \
  --endpoint-url $R2_ENDPOINT --profile r2
rm /tmp/r2-test.txt /tmp/r2-test-download.txt

echo "R2 connection test completed!"
```

---

## 다음 단계

- [[02-s3-api|S3 호환 API 사용]] - API 상세 활용법
- [[03-workers|Workers와 R2 바인딩]] - 서버리스 통합
