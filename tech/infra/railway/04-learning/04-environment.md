# Railway 환경 변수 및 시크릿 관리

## 개요

환경 변수는 애플리케이션 설정, API 키, 데이터베이스 연결 정보 등을 안전하게 관리하는 방법입니다. Railway는 강력한 환경 변수 관리 기능을 제공합니다.

---

## 환경 변수 설정 방법

### 1. 대시보드에서 설정

```
1. 프로젝트 > 서비스 선택
2. "Variables" 탭 클릭
3. "New Variable" 클릭
4. Key와 Value 입력
5. 자동 재배포 (또는 수동 배포)
```

### 2. Raw Editor

여러 변수를 한 번에 설정할 때 유용합니다.

```bash
# Raw Editor 형식
NODE_ENV=production
API_KEY=sk-xxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://default:pass@host:6379
```

### 3. CLI로 설정

```bash
# 단일 변수 설정
railway variables set NODE_ENV=production

# 여러 변수 설정
railway variables set API_KEY=xxx SECRET_KEY=yyy

# 변수 확인
railway variables

# 변수 삭제
railway variables delete API_KEY
```

### 4. railway.toml에서 설정

```toml
# railway.toml
# 주의: 민감한 정보는 여기에 넣지 마세요!

[variables]
NODE_ENV = "production"
LOG_LEVEL = "info"
```

---

## Railway 자동 주입 변수

Railway가 자동으로 제공하는 변수들:

| 변수 | 설명 | 예시 |
|------|------|------|
| `PORT` | 서비스 포트 | 3000 |
| `RAILWAY_ENVIRONMENT` | 환경 이름 | production |
| `RAILWAY_PROJECT_ID` | 프로젝트 ID | xxxxxxxx |
| `RAILWAY_SERVICE_ID` | 서비스 ID | xxxxxxxx |
| `RAILWAY_DEPLOYMENT_ID` | 배포 ID | xxxxxxxx |
| `RAILWAY_STATIC_URL` | 정적 URL | xxx.up.railway.app |
| `RAILWAY_GIT_COMMIT_SHA` | Git 커밋 해시 | abc1234 |
| `RAILWAY_GIT_BRANCH` | Git 브랜치 | main |

### 데이터베이스 연결 변수 (자동)

데이터베이스 추가 시 자동 주입:

```bash
# PostgreSQL
DATABASE_URL=postgresql://...
PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE

# MySQL
MYSQL_URL=mysql://...
MYSQLHOST, MYSQLPORT, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE

# Redis
REDIS_URL=redis://...
REDISHOST, REDISPORT, REDISUSER, REDISPASSWORD

# MongoDB
MONGO_URL=mongodb://...
MONGOHOST, MONGOPORT, MONGOUSER, MONGOPASSWORD
```

---

## 변수 참조 문법

### 서비스 간 변수 참조

다른 서비스의 변수를 참조할 수 있습니다.

```bash
# 문법: ${{ServiceName.VariableName}}

# 예: API 서비스에서 DB 서비스의 URL 참조
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Private URL 참조
DATABASE_PRIVATE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
```

### 자기 참조

```bash
# 같은 서비스 내 변수 참조
# 문법: ${{VariableName}}

BASE_URL=https://${{RAILWAY_STATIC_URL}}
API_ENDPOINT=${{BASE_URL}}/api
```

### 예시: 멀티 서비스 설정

```bash
# Backend 서비스
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
REDIS_URL=${{Redis.REDIS_PRIVATE_URL}}
JWT_SECRET=my-secret-key

# Frontend 서비스
NEXT_PUBLIC_API_URL=https://${{Backend.RAILWAY_STATIC_URL}}
```

---

## 환경별 변수 관리

### 환경 분리

Railway는 환경(Environment)별로 독립된 변수를 관리합니다.

```
Project
├── Production Environment
│   ├── DATABASE_URL=prod-db-url
│   └── API_KEY=prod-api-key
├── Staging Environment
│   ├── DATABASE_URL=staging-db-url
│   └── API_KEY=staging-api-key
└── Development Environment
    ├── DATABASE_URL=dev-db-url
    └── API_KEY=dev-api-key
```

### 환경 생성

```
1. 대시보드 > 프로젝트 선택
2. 상단 환경 드롭다운 > "New Environment"
3. 이름 입력 (예: staging)
4. 기존 환경 복사 또는 새로 시작
```

### railway.toml 환경별 설정

```toml
# 공통 설정
[variables]
LOG_LEVEL = "info"

# Production 환경
[environments.production.variables]
NODE_ENV = "production"
LOG_LEVEL = "warn"

# Staging 환경
[environments.staging.variables]
NODE_ENV = "staging"
LOG_LEVEL = "debug"
```

---

## 시크릿 관리 모범 사례

### DO (권장)

```bash
# 1. 대시보드에서 직접 설정 (가장 안전)
# 2. 의미 있는 이름 사용
DATABASE_URL=...
STRIPE_SECRET_KEY=...
JWT_SECRET=...

# 3. 환경별 분리
# Production: STRIPE_SECRET_KEY=sk_live_xxx
# Development: STRIPE_SECRET_KEY=sk_test_xxx

# 4. 참조 문법 활용
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
```

### DON'T (금지)

```bash
# 1. 코드에 하드코딩 금지
const apiKey = "sk-xxxxx";  # 절대 금지!

# 2. Git에 커밋 금지
# .env 파일을 커밋하지 마세요

# 3. railway.toml에 시크릿 넣지 않기
# [variables]
# API_KEY = "sk-xxxxx"  # 금지!

# 4. 로그에 출력 금지
console.log(process.env.API_KEY);  # 금지!
```

### .gitignore 설정

```gitignore
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
```

---

## 코드에서 환경 변수 사용

### Node.js

```javascript
// 직접 접근
const dbUrl = process.env.DATABASE_URL;
const port = process.env.PORT || 3000;

// dotenv (로컬 개발용)
require('dotenv').config();

// 필수 변수 검증
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

### Python

```python
import os
from dotenv import load_dotenv

# 로컬 개발용
load_dotenv()

# 환경 변수 접근
database_url = os.environ.get('DATABASE_URL')
port = int(os.environ.get('PORT', 5000))

# 필수 변수 검증
required_vars = ['DATABASE_URL', 'SECRET_KEY']
for var in required_vars:
    if not os.environ.get(var):
        raise ValueError(f"Missing required environment variable: {var}")
```

### Go

```go
package main

import (
    "os"
    "log"
)

func main() {
    dbURL := os.Getenv("DATABASE_URL")
    if dbURL == "" {
        log.Fatal("DATABASE_URL is required")
    }

    port := os.Getenv("PORT")
    if port == "" {
        port = "3000"
    }
}
```

---

## 로컬 개발 연동

### railway run 명령어

```bash
# Railway 환경 변수로 로컬 명령어 실행
railway run npm start

# 특정 환경 지정
railway run --environment staging npm start
```

### 환경 변수 내보내기

```bash
# 환경 변수 확인
railway variables

# JSON 형식으로 내보내기
railway variables --json > env.json

# .env 형식으로 변환 (직접 스크립트 필요)
```

### 로컬 .env 파일

```bash
# .env.local (gitignore에 추가)
DATABASE_URL=postgresql://localhost:5432/myapp
REDIS_URL=redis://localhost:6379
API_KEY=test-api-key
NODE_ENV=development
```

---

## 변수 디버깅

### 변수 확인

```bash
# CLI로 확인
railway variables

# 서비스 로그에서 확인 (개발 환경에서만!)
console.log('Environment:', process.env.RAILWAY_ENVIRONMENT);
```

### 일반적인 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 변수가 undefined | 설정 안 됨 또는 오타 | 대시보드에서 확인 |
| 이전 값 사용 | 재배포 필요 | 배포 트리거 |
| 참조 실패 | 서비스 이름 오류 | `${{ServiceName.VAR}}` 확인 |
| 특수문자 문제 | URL 인코딩 필요 | 특수문자 이스케이프 |

### 특수문자 처리

```bash
# 비밀번호에 특수문자가 있는 경우
# @, #, %, & 등은 URL 인코딩 필요

# 원본: p@ssw#rd
# 인코딩: p%40ssw%23rd

# Node.js에서 처리
const password = encodeURIComponent('p@ssw#rd');
```

---

## 보안 체크리스트

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는가?
- [ ] 프로덕션 시크릿이 대시보드에만 저장되어 있는가?
- [ ] 환경별로 다른 시크릿을 사용하고 있는가?
- [ ] 로그에 시크릿이 노출되지 않는가?
- [ ] 필수 환경 변수 검증 로직이 있는가?
- [ ] API 키가 필요한 최소 권한만 가지고 있는가?

---

## 다음 단계

- [[05-networking|네트워킹]] - 도메인 및 네트워크 설정
- [[06-monitoring|모니터링]] - 로그에서 환경 변수 확인
- [[../05-projects|실전 프로젝트]] - 환경 변수 활용 예제
