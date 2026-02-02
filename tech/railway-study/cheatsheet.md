# Railway Cheatsheet

## CLI 설치 및 인증

```bash
# 설치
npm install -g @railway/cli
# 또는
curl -fsSL https://railway.app/install.sh | sh

# 로그인
railway login

# 로그아웃
railway logout

# 버전 확인
railway --version
```

---

## 프로젝트 관리

```bash
# 새 프로젝트 생성
railway init

# 기존 프로젝트 연결
railway link

# 프로젝트 정보 확인
railway status

# 대시보드 열기
railway open

# 프로젝트 목록
railway list
```

---

## 배포

```bash
# 현재 디렉토리 배포
railway up

# 특정 디렉토리 배포
railway up --path ./src

# 배포 로그 확인
railway logs

# 실시간 로그 스트리밍
railway logs -f

# 최근 N줄 로그
railway logs --tail 100
```

---

## 환경 변수

```bash
# 변수 목록 확인
railway variables

# 변수 설정
railway variables set KEY=value

# 여러 변수 설정
railway variables set KEY1=val1 KEY2=val2

# 변수 삭제
railway variables delete KEY

# JSON 형식으로 출력
railway variables --json
```

---

## 환경 관리

```bash
# 환경 목록 확인
railway environment

# 환경 전환
railway environment production

# 환경 변수와 함께 로컬 실행
railway run npm start

# 특정 환경으로 실행
railway run --environment staging npm start
```

---

## 서비스 관리

```bash
# 서비스 추가
railway add

# 데이터베이스 추가
railway add --database postgres
railway add --database mysql
railway add --database redis
railway add --database mongo

# 서비스 전환
railway service

# 서비스 삭제 (대시보드 권장)
```

---

## railway.toml 설정

### 기본 구조

```toml
# 빌드 설정
[build]
builder = "nixpacks"
buildCommand = "npm run build"
watchPatterns = ["src/**"]

# 배포 설정
[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 100
numReplicas = 1
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### 환경별 설정

```toml
# 공통 변수
[variables]
LOG_LEVEL = "info"

# Production 환경
[environments.production.deploy]
numReplicas = 2
startCommand = "npm run start:prod"

[environments.production.variables]
NODE_ENV = "production"

# Staging 환경
[environments.staging.deploy]
numReplicas = 1

[environments.staging.variables]
NODE_ENV = "staging"
```

---

## 환경 변수 참조 문법

```bash
# 다른 서비스 변수 참조
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
REDIS_URL=${{Redis.REDIS_PRIVATE_URL}}

# 같은 서비스 내 변수 참조
API_URL=https://${{RAILWAY_STATIC_URL}}

# Railway 제공 변수
PORT                      # 서비스 포트
RAILWAY_ENVIRONMENT       # 환경 이름
RAILWAY_PROJECT_ID        # 프로젝트 ID
RAILWAY_SERVICE_ID        # 서비스 ID
RAILWAY_STATIC_URL        # 서비스 URL
RAILWAY_GIT_COMMIT_SHA    # Git 커밋 해시
RAILWAY_GIT_BRANCH        # Git 브랜치
```

---

## 데이터베이스 연결

### PostgreSQL

```javascript
// Node.js
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});
```

```python
# Python
import os
from sqlalchemy import create_engine
engine = create_engine(os.environ['DATABASE_URL'])
```

### Redis

```javascript
// Node.js
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);
```

### MongoDB

```javascript
// Node.js
const mongoose = require('mongoose');
mongoose.connect(process.env.MONGO_URL);
```

---

## 포트 설정

```javascript
// Node.js - 필수!
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0');  // 0.0.0.0 바인딩 필수
```

```python
# Python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

```go
// Go
port := os.Getenv("PORT")
if port == "" {
    port = "3000"
}
http.ListenAndServe("0.0.0.0:"+port, nil)
```

---

## 헬스체크

```javascript
// 기본 헬스체크
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// 상세 헬스체크
app.get('/health', async (req, res) => {
  const health = { status: 'healthy', checks: {} };

  try {
    await db.query('SELECT 1');
    health.checks.database = 'ok';
  } catch (e) {
    health.checks.database = 'error';
    health.status = 'unhealthy';
  }

  res.status(health.status === 'healthy' ? 200 : 503).json(health);
});
```

---

## Graceful Shutdown

```javascript
const server = app.listen(PORT);

process.on('SIGTERM', () => {
  console.log('SIGTERM received');
  server.close(() => {
    prisma.$disconnect();
    redis.quit();
    process.exit(0);
  });
});
```

---

## 크론 표현식

| 표현식 | 설명 |
|--------|------|
| `* * * * *` | 매분 |
| `0 * * * *` | 매시 정각 |
| `0 0 * * *` | 매일 자정 |
| `0 9 * * *` | 매일 오전 9시 |
| `0 9 * * 1` | 매주 월요일 오전 9시 |
| `*/15 * * * *` | 15분마다 |
| `0 0 1 * *` | 매월 1일 자정 |

---

## Private Network

```bash
# 내부 URL 형식
[service-name].railway.internal

# 예시
postgres.railway.internal
redis.railway.internal
api.railway.internal
```

---

## 문제 해결

### 일반적인 문제

| 증상 | 확인 사항 |
|------|----------|
| 빌드 실패 | 빌드 로그 확인, railway.toml 설정 |
| 배포 후 접속 불가 | PORT 환경변수, 0.0.0.0 바인딩 |
| 502 Bad Gateway | 헬스체크 경로, 서비스 시작 시간 |
| DB 연결 실패 | 환경 변수, Private URL 사용 |

### 디버깅 명령어

```bash
# 로그 확인
railway logs -f

# 환경 변수 확인
railway variables

# 상태 확인
railway status

# 대시보드 열기
railway open
```

---

## 유용한 링크

| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://docs.railway.app |
| 템플릿 갤러리 | https://railway.app/templates |
| Discord | https://discord.gg/railway |
| GitHub | https://github.com/railwayapp |
| 상태 페이지 | https://status.railway.app |

---

## 빠른 시작 요약

```bash
# 1. CLI 설치 및 로그인
npm i -g @railway/cli && railway login

# 2. 프로젝트 생성/연결
railway init  # 또는 railway link

# 3. 데이터베이스 추가
railway add --database postgres

# 4. 환경 변수 설정
railway variables set NODE_ENV=production

# 5. 배포
railway up

# 6. 로그 확인
railway logs -f
```
