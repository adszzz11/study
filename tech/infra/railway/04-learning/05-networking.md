# Railway 네트워킹

## 개요

Railway는 강력한 네트워킹 기능을 제공합니다. 자동 HTTPS, 커스텀 도메인, Private Network를 통해 안전하고 유연한 네트워크 구성이 가능합니다.

---

## 도메인 설정

### Railway 제공 도메인

모든 서비스는 기본 도메인을 받을 수 있습니다.

```bash
# 형식
https://[project-name]-[random].up.railway.app

# 예시
https://my-app-production.up.railway.app
```

#### 도메인 생성
```
1. 서비스 선택 > "Settings" 탭
2. "Networking" 섹션
3. "Generate Domain" 클릭
```

### 커스텀 도메인

자신의 도메인을 연결할 수 있습니다.

#### 설정 방법
```
1. 서비스 > Settings > Networking
2. "Add Custom Domain" 클릭
3. 도메인 입력 (예: api.example.com)
4. DNS 설정 안내에 따라 레코드 추가
```

#### DNS 설정

**CNAME 레코드 (서브도메인)**
```
Type: CNAME
Name: api
Value: [your-project].up.railway.app
```

**A 레코드 (루트 도메인)**
```
Type: A
Name: @
Value: Railway에서 제공하는 IP 주소
```

#### 도메인 제공업체별 설정

| 제공업체 | 설정 위치 |
|---------|----------|
| Cloudflare | DNS > Add Record |
| Namecheap | Domain List > Manage > Advanced DNS |
| GoDaddy | DNS Management |
| Route53 | Hosted Zones > Create Record |

---

## HTTPS / SSL

### 자동 HTTPS

Railway는 모든 도메인에 대해 자동으로 SSL 인증서를 발급합니다.

```bash
# 자동 적용 사항
- Let's Encrypt 인증서 자동 발급
- 자동 갱신 (만료 전)
- HTTP → HTTPS 리다이렉트
```

### 인증서 상태 확인

```
서비스 > Settings > Networking > Domains
각 도메인 옆에 인증서 상태 표시 (🟢 Active)
```

### SSL 문제 해결

| 문제 | 해결 방법 |
|------|----------|
| 인증서 발급 지연 | DNS 전파 대기 (최대 48시간) |
| 인증서 오류 | DNS 설정 재확인 |
| Mixed Content | 모든 리소스 HTTPS로 변경 |

---

## Private Network

### 개념

같은 프로젝트 내의 서비스들은 Private Network를 통해 안전하게 통신합니다.

```
┌─────────────────────────────────────────────────────────┐
│                    Railway Project                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐           ┌─────────────┐             │
│  │   Backend   │  Private  │   Worker    │             │
│  │   Service   │◀────────▶│   Service   │             │
│  └──────┬──────┘  Network  └──────┬──────┘             │
│         │                         │                      │
│         └───────────┬─────────────┘                      │
│                     │                                    │
│              Private Network                             │
│                     │                                    │
│         ┌───────────┼───────────┐                        │
│         │           │           │                        │
│    ┌────▼────┐ ┌────▼────┐ ┌────▼────┐                 │
│    │Postgres │ │  Redis  │ │ MongoDB │                 │
│    └─────────┘ └─────────┘ └─────────┘                 │
│                                                          │
│    ※ 모든 내부 통신은 암호화됨                           │
└─────────────────────────────────────────────────────────┘
```

### Private URL 형식

```bash
# 형식
[service-name].railway.internal

# 예시
postgres.railway.internal
redis.railway.internal
backend.railway.internal
```

### Private vs Public URL

| 구분 | Private URL | Public URL |
|------|-------------|------------|
| **접근** | 프로젝트 내부만 | 인터넷 전체 |
| **성능** | 빠름 (내부 네트워크) | 상대적으로 느림 |
| **보안** | 암호화 + 격리 | HTTPS만 |
| **용도** | DB, 내부 API | 외부 서비스 |

### 환경 변수 예시

```bash
# 데이터베이스 - Private URL 사용 (권장)
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}

# 내부 서비스 통신
WORKER_URL=http://worker.railway.internal:3000

# 외부 접근이 필요한 경우만 Public
PUBLIC_API_URL=https://api.example.com
```

---

## 포트 설정

### 기본 동작

Railway는 `PORT` 환경 변수를 자동으로 주입합니다.

```javascript
// Node.js 예시
const PORT = process.env.PORT || 3000;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

### 중요: 0.0.0.0 바인딩

```javascript
// 올바른 방법
app.listen(PORT, '0.0.0.0');

// 잘못된 방법 (접속 불가)
app.listen(PORT, 'localhost');
app.listen(PORT, '127.0.0.1');
```

### 다중 포트

하나의 서비스에서 여러 포트를 노출할 수 있습니다.

```javascript
// HTTP 서버
const httpServer = app.listen(process.env.PORT || 3000);

// WebSocket은 같은 포트 사용 권장
const io = require('socket.io')(httpServer);
```

---

## 로드 밸런싱

### 자동 로드 밸런싱

Railway는 복제본(Replica) 설정 시 자동으로 로드 밸런싱합니다.

```toml
# railway.toml
[deploy]
numReplicas = 3  # 3개 인스턴스로 분산
```

### 세션 지속성 (Sticky Sessions)

세션 기반 애플리케이션의 경우:

```javascript
// Redis 세션 저장소 사용 권장
const session = require('express-session');
const RedisStore = require('connect-redis').default;

app.use(session({
  store: new RedisStore({ client: redisClient }),
  // ...
}));
```

---

## 네트워크 보안

### 접근 제어

```javascript
// IP 화이트리스트 (애플리케이션 레벨)
const allowedIPs = process.env.ALLOWED_IPS?.split(',') || [];

app.use((req, res, next) => {
  const clientIP = req.ip;
  if (allowedIPs.length && !allowedIPs.includes(clientIP)) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
});
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15분
  max: 100, // IP당 100 요청
  standardHeaders: true,
  legacyHeaders: false,
});

app.use(limiter);
```

### CORS 설정

```javascript
const cors = require('cors');

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true
}));
```

---

## 헬스체크

### 설정

```toml
# railway.toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 100  # 밀리초
```

### 엔드포인트 구현

```javascript
app.get('/health', (req, res) => {
  // 기본 체크
  res.json({ status: 'healthy' });
});

// 상세 체크
app.get('/health/detailed', async (req, res) => {
  const checks = {
    server: 'healthy',
    database: 'unknown',
    redis: 'unknown'
  };

  try {
    await db.query('SELECT 1');
    checks.database = 'healthy';
  } catch (e) {
    checks.database = 'unhealthy';
  }

  try {
    await redis.ping();
    checks.redis = 'healthy';
  } catch (e) {
    checks.redis = 'unhealthy';
  }

  const allHealthy = Object.values(checks).every(s => s === 'healthy');
  res.status(allHealthy ? 200 : 503).json(checks);
});
```

---

## 트래픽 라우팅

### Path 기반 라우팅

하나의 도메인에서 여러 서비스로 라우팅 (API Gateway 패턴):

```javascript
// API Gateway 서비스
const { createProxyMiddleware } = require('http-proxy-middleware');

// /api/* → Backend 서비스
app.use('/api', createProxyMiddleware({
  target: 'http://backend.railway.internal:3000',
  changeOrigin: true
}));

// /auth/* → Auth 서비스
app.use('/auth', createProxyMiddleware({
  target: 'http://auth.railway.internal:3000',
  changeOrigin: true
}));
```

### 서브도메인 라우팅

```
api.example.com → Backend 서비스
app.example.com → Frontend 서비스
admin.example.com → Admin 서비스
```

각 서비스에 해당 커스텀 도메인을 설정합니다.

---

## 문제 해결

### 일반적인 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 502 Bad Gateway | 서비스 시작 전 요청 | 헬스체크 설정 확인 |
| 503 Service Unavailable | 서비스 다운 | 로그 확인, 재배포 |
| Connection refused | 잘못된 포트/호스트 | PORT 환경변수 사용 |
| SSL 오류 | DNS 미전파 | 전파 대기 (최대 48시간) |

### 디버깅

```bash
# 서비스 로그 확인
railway logs

# 네트워크 연결 테스트 (서비스 내에서)
curl http://other-service.railway.internal:3000/health
```

---

## 체크리스트

- [ ] PORT 환경변수로 포트 설정
- [ ] 0.0.0.0으로 바인딩
- [ ] 헬스체크 엔드포인트 구현
- [ ] 데이터베이스는 Private URL 사용
- [ ] 커스텀 도메인 DNS 설정 완료
- [ ] HTTPS 인증서 활성화 확인
- [ ] CORS 및 Rate Limiting 설정

---

## 다음 단계

- [[06-monitoring|모니터링]] - 트래픽 모니터링
- [[../05-projects|실전 프로젝트]] - 네트워크 구성 예제
- [[../cheatsheet|Cheatsheet]] - 네트워크 관련 명령어
