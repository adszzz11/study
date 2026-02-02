# Railway 심층 스터디 가이드

> **한 줄 정의**: 코드를 푸시하면 자동으로 빌드/배포되는 개발자 친화적인 클라우드 PaaS 플랫폼

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. GitHub 연결만 하면 자동 빌드/배포 - Dockerfile 없이도 대부분의 프레임워크 지원
2. PostgreSQL, Redis, MongoDB 등 데이터베이스를 클릭 한 번으로 프로비저닝
3. 사용량 기반 과금으로 스타트업/사이드 프로젝트에 최적

**핵심 키워드**: `#PaaS` `#배포` `#클라우드` `#Heroku대안` `#개발자경험`

**Railway가 해결하는 문제**:

```
Before Railway:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   코드 작성  │ →  │  Dockerfile │ →  │  CI/CD 설정 │ →  │  서버 관리  │
│             │    │     작성     │    │  (복잡함)   │    │  (부담됨)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

After Railway:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   코드 작성  │ →  │  git push   │ →  │   배포 완료  │
│             │    │             │    │  (자동 SSL) │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 1.2 Quick Start (30초 체험)

```bash
# 1. Railway CLI 설치
npm install -g @railway/cli

# 또는 macOS
brew install railway

# 2. 로그인
railway login

# 3. 프로젝트 초기화 및 배포
cd my-app
railway init
railway up

# 4. 브라우저에서 확인
railway open
```

**또는 웹에서 바로 시작**:
1. [railway.com](https://railway.com/) 접속
2. GitHub로 로그인
3. "New Project" → GitHub 레포 선택
4. 자동 빌드 & 배포 완료

### 1.3 왜 Railway인가?

**장점**:
- **극단적 간편함**: GitHub 연결 → 자동 배포
- **Nixpacks**: Dockerfile 없이 자동 환경 감지
- **내장 DB**: PostgreSQL, Redis, MongoDB, MySQL 원클릭 생성
- **사용량 과금**: 분 단위 과금, 유휴 시 비용 최소화
- **멋진 DX**: 깔끔한 UI, 실시간 로그, 환경 변수 관리
- **프라이빗 네트워킹**: 서비스 간 보안 통신

**단점**:
- 무료 티어 없음 (2023년 8월 폐지)
- 대규모 트래픽에는 AWS/GCP보다 비쌈
- 리전 제한 (주요 리전은 커버)
- 고급 인프라 커스터마이징 제한

**주요 사용 사례**:
- 사이드 프로젝트 빠른 배포
- 스타트업 MVP
- 백엔드 API 서버
- Discord/Slack 봇
- 스케줄 작업 (Cron)

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Railway 생태계                            │
├─────────────────────────────────────────────────────────────┤
│  [배포 방식]                                                 │
│  ├── GitHub Deploy: 레포 연결, 자동 배포                     │
│  ├── CLI Deploy: `railway up` 명령                          │
│  ├── Docker Deploy: Dockerfile 또는 이미지                   │
│  └── Template Deploy: 미리 설정된 스택                        │
│                                                              │
│  [빌드 시스템]                                               │
│  ├── Nixpacks: 자동 환경 감지 (기본)                         │
│  ├── Railpacks: Railway 최적화 빌더                         │
│  └── Dockerfile: 커스텀 빌드                                 │
│                                                              │
│  [서비스 타입]                                               │
│  ├── Web Service: HTTP 서버                                  │
│  ├── Worker: 백그라운드 작업                                 │
│  ├── Cron: 스케줄 작업                                       │
│  └── Database: PostgreSQL, Redis, MongoDB, MySQL            │
│                                                              │
│  [네트워킹]                                                  │
│  ├── Public Domain: xxx.railway.app                         │
│  ├── Custom Domain: 자체 도메인 연결                         │
│  ├── Private Networking: 서비스 간 내부 통신                  │
│  └── TCP Proxy: 비-HTTP 프로토콜                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **프레임워크** | Next.js, FastAPI, Express | 웹 앱/API |
| **DB** | PostgreSQL, Redis | 데이터 저장/캐시 |
| **오브젝트 스토리지** | Cloudflare R2, S3 | 파일 저장 |
| **모니터링** | Datadog, Sentry | 로그/에러 추적 |
| **CI/CD** | GitHub Actions | 추가 자동화 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Railway | Render | Fly.io | Vercel | Heroku |
|------|---------|--------|--------|--------|--------|
| **타입** | 범용 PaaS | 범용 PaaS | 컨테이너 | 프론트엔드 | 범용 PaaS |
| **무료 티어** | 없음 | 있음 | 제한적 | 있음 | 없음 |
| **과금** | 사용량 | 인스턴스 | 머신 시간 | 사용량 | 인스턴스 |
| **DB 내장** | 예 | 예 | 예 | 아니오 | 예 |
| **Docker** | 지원 | 지원 | 필수 | 미지원 | 지원 |
| **글로벌 배포** | 제한적 | 제한적 | 강점 | 강점 | 제한적 |

**선택 가이드**:
- **Railway**: 빠른 시작, 풀스택, 좋은 DX
- **Render**: 무료 티어 필요, 예측 가능한 비용
- **Fly.io**: 글로벌 엣지 배포, 고급 네트워킹
- **Vercel**: Next.js/프론트엔드 최적화
- **Heroku**: 엔터프라이즈, 기존 사용자

### 2.4 최신 트렌드 및 동향 (2025)

- **Object Storage 출시 (2025.09)**: S3 호환 스토리지 네이티브 지원
- **Railpacks**: Nixpacks 대체 자체 빌더
- **Volume 백업**: 자동 볼륨 백업 기능
- **Private Networking 강화**: 서비스 간 고속 내부 통신
- **Usage Dashboard**: 실시간 비용 모니터링 개선

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.railway.com](https://docs.railway.com/) | 메인 문서 |
| 🟢 대시보드 | [railway.app](https://railway.app/) | 프로젝트 관리 |
| 🟢 템플릿 | [railway.app/templates](https://railway.app/templates) | 원클릭 배포 |
| 🟡 GitHub | [github.com/railwayapp](https://github.com/railwayapp) | CLI 등 오픈소스 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Railway Quick Start](https://docs.railway.com/quick-start) - 공식 빠른 시작
- [Deploying Tutorial](https://docs.railway.com/tutorials/deploying) - 배포 가이드

**🟡 중급**:
- [Private Networking](https://docs.railway.com/guides/private-networking) - 내부 통신
- [Volumes](https://docs.railway.com/guides/volumes) - 영구 스토리지

**🔴 고급**:
- [GitHub Actions Integration](https://docs.railway.com/guides/github-actions) - CI/CD 연동
- [Scaling](https://docs.railway.com/reference/scaling) - 스케일링 전략

### 3.3 커뮤니티 및 질문할 곳

- **Discord**: [Railway 공식 디스코드](https://discord.gg/railway)
- **GitHub Discussions**: 기능 요청, 버그 리포트
- **Twitter/X**: @Railway

---

## Part 4: 상세 학습 로드맵

### 4.1 첫 배포

📌 **핵심 개념**

Railway는 GitHub 레포를 연결하면 자동으로 빌드/배포합니다. `main` 브랜치에 푸시할 때마다 새 배포가 시작됩니다.

💻 **코드 예제: Express.js 배포**

```javascript
// index.js
const express = require('express');
const app = express();

const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
    res.json({
        message: 'Hello from Railway!',
        environment: process.env.NODE_ENV
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

```json
// package.json
{
    "name": "railway-demo",
    "version": "1.0.0",
    "main": "index.js",
    "scripts": {
        "start": "node index.js"
    },
    "dependencies": {
        "express": "^4.18.2"
    }
}
```

```bash
# 배포 방법 1: CLI
cd my-express-app
railway login
railway init
railway up

# 배포 방법 2: GitHub 연결 (웹 UI)
# 1. railway.app에서 New Project
# 2. Deploy from GitHub repo 선택
# 3. 레포 선택 → 자동 배포

# 도메인 확인
railway domain
# → https://my-express-app.up.railway.app
```

**FastAPI (Python) 배포**:
```python
# main.py
from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Railway!", "env": os.getenv("ENVIRONMENT")}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

```
# requirements.txt
fastapi
uvicorn[standard]
```

```toml
# Procfile 또는 railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

✅ **체크포인트**
- [ ] GitHub 레포를 Railway에 연결할 수 있는가?
- [ ] CLI로 배포할 수 있는가?
- [ ] 배포된 URL에 접근할 수 있는가?

⚠️ **흔한 실수**
- `PORT` 환경 변수 사용 필수 (Railway가 할당)
- `0.0.0.0`에 바인딩 (localhost 아님)
- `start` 스크립트 정의 필수

🔗 **더 알아보기**: [Quick Start](https://docs.railway.com/quick-start)

---

### 4.2 데이터베이스 연결

📌 **핵심 개념**

Railway에서 PostgreSQL, Redis, MongoDB, MySQL을 원클릭으로 생성하고, 환경 변수로 연결합니다.

💻 **코드 예제: PostgreSQL 연결**

```bash
# 웹 UI에서
# 1. 프로젝트 대시보드 → "+ New" → "Database" → "PostgreSQL"
# 2. 자동으로 DATABASE_URL 환경 변수 생성

# CLI에서
railway add --database postgres
```

**Node.js (pg)**:
```javascript
// db.js
const { Pool } = require('pg');

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
        rejectUnauthorized: false
    }
});

// 테이블 생성
async function initDb() {
    const client = await pool.connect();
    try {
        await client.query(`
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        `);
    } finally {
        client.release();
    }
}

module.exports = { pool, initDb };
```

**Python (SQLAlchemy)**:
```python
# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
# Railway의 postgres:// → postgresql:// 변환
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

**Redis 연결**:
```python
import os
import redis

redis_client = redis.from_url(os.getenv("REDIS_URL"))

# 캐시 사용
redis_client.set("key", "value", ex=3600)  # 1시간 만료
value = redis_client.get("key")
```

**환경 변수 참조**:
```bash
# Railway가 자동 생성하는 변수들
DATABASE_URL=postgresql://user:pass@host:5432/railway
REDIS_URL=redis://default:pass@host:6379
PGDATABASE=railway
PGHOST=hostname
PGPASSWORD=password
PGPORT=5432
PGUSER=postgres
```

✅ **체크포인트**
- [ ] PostgreSQL을 프로비저닝할 수 있는가?
- [ ] `DATABASE_URL`로 연결할 수 있는가?
- [ ] 서비스 간 환경 변수 참조를 설정할 수 있는가?

⚠️ **흔한 실수**
- `postgres://` vs `postgresql://` 프로토콜 확인
- SSL 설정 필요할 수 있음
- Private networking 사용 시 내부 URL 사용

🔗 **더 알아보기**: [Databases](https://docs.railway.com/guides/databases)

---

### 4.3 환경 변수와 시크릿

📌 **핵심 개념**

Railway는 환경별(Production, Staging) 변수를 분리 관리하고, 서비스 간 변수 참조가 가능합니다.

💻 **코드 예제: 환경 변수 관리**

```bash
# CLI로 변수 설정
railway variables set API_KEY=secret123
railway variables set NODE_ENV=production

# 여러 변수 한번에
railway variables set API_KEY=xxx DATABASE_URL=yyy

# 변수 확인
railway variables

# 변수 삭제
railway variables unset API_KEY
```

**서비스 간 변수 참조**:
```
# 웹 UI에서 변수 값에 참조 문법 사용
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
BACKEND_URL=${{Backend.RAILWAY_PUBLIC_DOMAIN}}
```

**railway.toml 설정**:
```toml
# railway.toml
[build]
builder = "nixpacks"
buildCommand = "npm run build"

[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 5

[deploy.environment]
NODE_ENV = "production"
LOG_LEVEL = "info"
```

**환경별 분리**:
```bash
# Production 환경
railway environment production
railway variables set DEBUG=false

# Staging 환경
railway environment staging
railway variables set DEBUG=true
```

✅ **체크포인트**
- [ ] CLI로 환경 변수를 설정할 수 있는가?
- [ ] 서비스 간 변수 참조 문법을 이해하는가?
- [ ] 환경별(prod/staging) 변수를 분리할 수 있는가?

⚠️ **흔한 실수**
- 시크릿은 대시보드에서 마스킹되어 표시
- 변수 변경 시 자동 재배포 (옵션)

🔗 **더 알아보기**: [Variables](https://docs.railway.com/guides/variables)

---

### 4.4 커스텀 도메인과 네트워킹

📌 **핵심 개념**

Railway는 무료 `*.railway.app` 도메인을 제공하고, 커스텀 도메인 연결과 자동 SSL을 지원합니다.

💻 **코드 예제: 도메인 설정**

```bash
# 기본 도메인 생성
railway domain
# → https://my-app-production.up.railway.app

# 커스텀 도메인 추가 (웹 UI)
# 1. 서비스 선택 → Settings → Domains
# 2. "Custom Domain" → "api.example.com" 입력
# 3. DNS 레코드 안내에 따라 CNAME 설정

# DNS 설정 예시 (Cloudflare 등)
# Type: CNAME
# Name: api
# Target: my-app-production.up.railway.app
```

**Private Networking**:
```python
# 같은 프로젝트 내 서비스 간 통신
import os
import requests

# Private URL 사용 (외부 노출 안 됨)
BACKEND_URL = os.getenv("BACKEND_PRIVATE_URL", "http://backend.railway.internal:3000")

def call_backend():
    response = requests.get(f"{BACKEND_URL}/api/data")
    return response.json()
```

```yaml
# docker-compose 대신 Railway 서비스 연결
# Backend 서비스
# → Private Networking URL: backend.railway.internal

# Frontend 서비스
# → 환경 변수: BACKEND_URL=http://backend.railway.internal:3000
```

**TCP Proxy (비-HTTP 프로토콜)**:
```bash
# 웹 UI에서 Settings → Networking → TCP Proxy
# 예: PostgreSQL 직접 연결
# → Public TCP endpoint: railway.app:12345
```

✅ **체크포인트**
- [ ] 커스텀 도메인을 연결할 수 있는가?
- [ ] Private Networking으로 서비스 간 통신을 설정할 수 있는가?
- [ ] TCP Proxy를 사용할 수 있는가?

⚠️ **흔한 실수**
- DNS 전파에 시간 소요 (최대 48시간, 보통 몇 분)
- Private URL은 같은 프로젝트 내에서만 동작

🔗 **더 알아보기**: [Networking](https://docs.railway.com/guides/networking)

---

### 4.5 스케일링과 리소스 관리

📌 **핵심 개념**

Railway는 수직 스케일링(CPU/RAM 증가)과 수평 스케일링(복제본 증가)을 모두 지원합니다.

💻 **코드 예제: 스케일링 설정**

```toml
# railway.toml
[deploy]
# 수직 스케일링 (리소스 제한)
numReplicas = 1

# Cron 작업
# cronSchedule = "0 * * * *"  # 매 시간

[deploy.scaling]
# 수평 스케일링 (복제본)
replicas = 3
```

**웹 UI 설정**:
```
# 서비스 → Settings → Deploy

# 수직 스케일링
vCPU: 0.5 → 8 (자동 또는 수동)
Memory: 512MB → 32GB (자동 또는 수동)

# 수평 스케일링
Replicas: 1 → N
```

**Healthcheck 설정**:
```toml
# railway.toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300  # 5분

# 재시작 정책
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

```javascript
// 헬스체크 엔드포인트
app.get('/health', async (req, res) => {
    try {
        // DB 연결 확인
        await pool.query('SELECT 1');
        res.status(200).json({ status: 'healthy' });
    } catch (error) {
        res.status(503).json({ status: 'unhealthy', error: error.message });
    }
});
```

**비용 모니터링**:
```bash
# CLI로 사용량 확인
railway status

# 웹 UI → Usage 탭
# - CPU 시간
# - 메모리 사용량
# - 네트워크 전송량
# - 예상 비용
```

✅ **체크포인트**
- [ ] 복제본 수를 조절할 수 있는가?
- [ ] 헬스체크를 설정할 수 있는가?
- [ ] 비용을 모니터링할 수 있는가?

⚠️ **흔한 실수**
- 복제본 증가 시 세션 공유 문제 (Redis 사용)
- 헬스체크 실패 시 계속 재시작됨

🔗 **더 알아보기**: [Scaling](https://docs.railway.com/reference/scaling)

---

### 4.6 CI/CD와 GitHub Actions

📌 **핵심 개념**

Railway는 GitHub 푸시 시 자동 배포되지만, GitHub Actions와 연동하여 테스트 후 배포하는 것도 가능합니다.

💻 **코드 예제: GitHub Actions 통합**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run linting
        run: npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        run: railway up --service my-service
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

**Railway 토큰 생성**:
```bash
# 1. CLI에서 토큰 생성
railway login
railway tokens create

# 2. GitHub Secrets에 추가
# Settings → Secrets → RAILWAY_TOKEN
```

**Preview 환경 (PR 배포)**:
```yaml
# railway.toml
[deploy]
# PR 생성 시 자동 Preview 환경 생성
prDeploys = true
```

```yaml
# .github/workflows/preview.yml
name: Preview Deploy

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy Preview
        run: |
          npm install -g @railway/cli
          railway up --environment pr-${{ github.event.number }}
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview deployed!'
            })
```

✅ **체크포인트**
- [ ] Railway 토큰을 생성하고 GitHub에 추가할 수 있는가?
- [ ] 테스트 후 배포하는 워크플로우를 구성할 수 있는가?
- [ ] PR별 Preview 환경을 설정할 수 있는가?

⚠️ **흔한 실수**
- `RAILWAY_TOKEN` 시크릿 설정 필수
- PR 환경은 추가 비용 발생

🔗 **더 알아보기**: [GitHub Actions](https://docs.railway.com/guides/github-actions)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 단일 API 서버 | 기본 배포 |
| 🟢 | Discord 봇 | Worker 서비스 |
| 🟡 | 풀스택 앱 (Next.js + DB) | 멀티 서비스 |
| 🟡 | Cron 작업 스케줄러 | 스케줄 작업 |
| 🔴 | 마이크로서비스 아키텍처 | Private Networking |

### 5.2 단계별 구현 가이드: 풀스택 앱 배포

**목표**: Next.js + PostgreSQL + Redis 풀스택 앱

```
프로젝트 구조:
my-fullstack-app/
├── package.json
├── prisma/
│   └── schema.prisma
├── src/
│   ├── app/
│   │   ├── page.tsx
│   │   └── api/
│   │       └── users/route.ts
│   └── lib/
│       ├── prisma.ts
│       └── redis.ts
└── railway.toml
```

**Step 1: 프로젝트 설정**:
```json
// package.json
{
    "name": "fullstack-railway",
    "scripts": {
        "dev": "next dev",
        "build": "prisma generate && next build",
        "start": "next start",
        "postinstall": "prisma generate"
    },
    "dependencies": {
        "next": "14.x",
        "@prisma/client": "5.x",
        "ioredis": "5.x"
    },
    "devDependencies": {
        "prisma": "5.x"
    }
}
```

**Step 2: Prisma 설정**:
```prisma
// prisma/schema.prisma
datasource db {
    provider = "postgresql"
    url      = env("DATABASE_URL")
}

generator client {
    provider = "prisma-client-js"
}

model User {
    id        Int      @id @default(autoincrement())
    email     String   @unique
    name      String?
    createdAt DateTime @default(now())
}
```

**Step 3: DB/Redis 클라이언트**:
```typescript
// src/lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

// src/lib/redis.ts
import Redis from 'ioredis';

export const redis = new Redis(process.env.REDIS_URL!);
```

**Step 4: API 라우트**:
```typescript
// src/app/api/users/route.ts
import { prisma } from '@/lib/prisma';
import { redis } from '@/lib/redis';
import { NextResponse } from 'next/server';

export async function GET() {
    // 캐시 확인
    const cached = await redis.get('users');
    if (cached) {
        return NextResponse.json(JSON.parse(cached));
    }

    // DB 조회
    const users = await prisma.user.findMany();

    // 캐시 저장 (5분)
    await redis.set('users', JSON.stringify(users), 'EX', 300);

    return NextResponse.json(users);
}

export async function POST(request: Request) {
    const { email, name } = await request.json();

    const user = await prisma.user.create({
        data: { email, name }
    });

    // 캐시 무효화
    await redis.del('users');

    return NextResponse.json(user);
}
```

**Step 5: Railway 배포**:
```bash
# 1. Railway 프로젝트 생성
railway login
railway init

# 2. PostgreSQL 추가
railway add --database postgres

# 3. Redis 추가
railway add --database redis

# 4. 환경 변수 확인
railway variables
# DATABASE_URL, REDIS_URL 자동 생성됨

# 5. 배포
railway up

# 6. Prisma 마이그레이션
railway run npx prisma db push

# 7. 도메인 확인
railway domain
```

### 5.3 Best Practices

**프로젝트 구조**:
```
railway-project/
├── services/
│   ├── api/          # 백엔드 API
│   ├── web/          # 프론트엔드
│   └── worker/       # 백그라운드 작업
├── infrastructure/
│   └── railway.toml  # 공통 설정
└── .github/
    └── workflows/
        └── deploy.yml
```

**운영 권장사항**:

1. **환경 분리**: Production, Staging 환경 분리
2. **헬스체크**: 모든 서비스에 `/health` 엔드포인트
3. **로깅**: 구조화된 JSON 로그
4. **시크릿**: 민감 정보는 환경 변수로
5. **백업**: PostgreSQL 자동 백업 활성화

```toml
# railway.toml 권장 설정
[build]
builder = "nixpacks"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[deploy.resources]
# 시작 리소스 설정 (비용 최적화)
cpuMin = 0.25
memoryMin = 256
```

---

## 요약

Railway는 개발자 경험을 최우선으로 하는 클라우드 플랫폼입니다:

- **배포**: GitHub 연결 → 자동 빌드/배포
- **인프라**: PostgreSQL, Redis 원클릭 프로비저닝
- **네트워킹**: 자동 SSL, Private Networking
- **스케일링**: 수직/수평 스케일링, 사용량 과금

다음 단계:
1. [railway.app](https://railway.app)에서 계정 생성
2. 간단한 API 서버 배포
3. 데이터베이스 연결 테스트
