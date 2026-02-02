# Railway 모니터링

## 개요

Railway는 기본적인 모니터링 기능을 제공합니다. 로깅, 메트릭, 알림을 통해 서비스 상태를 파악하고 문제를 빠르게 해결할 수 있습니다.

---

## 로깅

### 로그 확인 방법

#### 대시보드
```
1. 프로젝트 > 서비스 선택
2. "Deployments" 탭
3. 배포 선택 > "View Logs"
```

#### CLI
```bash
# 실시간 로그 스트리밍
railway logs

# 최근 로그만 확인
railway logs --tail 100

# 특정 서비스 로그
railway logs --service my-service
```

### 로그 유형

| 유형 | 설명 | 확인 위치 |
|------|------|----------|
| **Build Logs** | 빌드 과정 로그 | Deployments > Build Logs |
| **Deploy Logs** | 런타임 로그 | Deployments > Deploy Logs |
| **Database Logs** | DB 서비스 로그 | Database Service > Logs |

### 효과적인 로깅

#### 구조화된 로그 (JSON)

```javascript
// 추천: JSON 형식 로그
const log = (level, message, meta = {}) => {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level,
    message,
    ...meta,
    service: process.env.RAILWAY_SERVICE_ID
  }));
};

// 사용
log('info', 'User logged in', { userId: 123 });
log('error', 'Database connection failed', { error: err.message });
```

#### 로그 레벨

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console()
  ]
});

logger.info('Server started', { port: PORT });
logger.warn('High memory usage', { usage: '85%' });
logger.error('Request failed', { error: err.message });
```

### 로그 검색

대시보드에서 로그 필터링:
- 시간 범위 선택
- 텍스트 검색
- 로그 레벨 필터

---

## 메트릭

### 기본 메트릭

Railway 대시보드에서 확인 가능한 메트릭:

| 메트릭 | 설명 | 단위 |
|--------|------|------|
| **CPU** | CPU 사용량 | % |
| **Memory** | 메모리 사용량 | MB |
| **Network In** | 인바운드 트래픽 | MB |
| **Network Out** | 아웃바운드 트래픽 | MB |
| **Disk** | 디스크 사용량 | MB |

### 메트릭 확인

```
1. 프로젝트 > 서비스 선택
2. "Metrics" 탭
3. 시간 범위 선택 (1h, 24h, 7d, 30d)
```

### 애플리케이션 메트릭 수집

#### Node.js (prom-client)

```javascript
const promClient = require('prom-client');

// 기본 메트릭 수집
promClient.collectDefaultMetrics();

// 커스텀 메트릭
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

// 미들웨어
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });
  next();
});

// 메트릭 엔드포인트
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});
```

#### Python (prometheus_client)

```python
from prometheus_client import Counter, Histogram, generate_latest
from flask import Flask, Response
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency')

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_COUNT.labels(request.method, request.endpoint, response.status_code).inc()
    REQUEST_LATENCY.observe(latency)
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')
```

---

## 스케일링

### 수동 스케일링

#### 대시보드
```
1. 서비스 > Settings
2. "Scaling" 섹션
3. Replicas 수 조정
```

#### railway.toml
```toml
[deploy]
numReplicas = 3
```

### 리소스 제한

```toml
# railway.toml
[deploy]
# 메모리 제한 (MB)
memorySoftLimit = 512

# vCPU 제한
# Railway는 자동 할당, 직접 제어 제한적
```

### 스케일링 전략

#### 언제 스케일 업?
| 지표 | 임계값 | 조치 |
|------|--------|------|
| CPU > 80% | 5분 이상 지속 | 레플리카 추가 |
| Memory > 85% | 지속적 | 메모리 증가 또는 최적화 |
| 응답 시간 > 500ms | 평균 | 레플리카 추가 |

#### 스케일링 고려사항
```
┌─────────────────────────────────────────────────────────┐
│                   스케일링 의사결정                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  CPU 바운드?                                             │
│       │                                                  │
│       ├── Yes ──▶ 레플리카 추가 (수평 확장)              │
│       │                                                  │
│       └── No                                             │
│            │                                             │
│  메모리 바운드?                                          │
│       │                                                  │
│       ├── Yes ──▶ 메모리 최적화 또는 증가                │
│       │                                                  │
│       └── No                                             │
│            │                                             │
│  I/O 바운드?                                             │
│       │                                                  │
│       ├── Yes ──▶ 캐싱 추가, DB 최적화                   │
│       │                                                  │
│       └── 아키텍처 검토 필요                              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 알림 설정

### Railway 기본 알림

Railway는 다음 이벤트에 대해 알림을 제공합니다:
- 배포 성공/실패
- 서비스 다운
- 빌드 실패

### 외부 알림 서비스 연동

#### Slack 웹훅

```javascript
const axios = require('axios');

async function sendSlackAlert(message) {
  const webhookUrl = process.env.SLACK_WEBHOOK_URL;

  await axios.post(webhookUrl, {
    text: message,
    attachments: [{
      color: 'danger',
      fields: [{
        title: 'Service',
        value: process.env.RAILWAY_SERVICE_ID,
        short: true
      }, {
        title: 'Environment',
        value: process.env.RAILWAY_ENVIRONMENT,
        short: true
      }]
    }]
  });
}

// 에러 발생 시 알림
process.on('uncaughtException', (error) => {
  sendSlackAlert(`Uncaught Exception: ${error.message}`);
});
```

#### Discord 웹훅

```javascript
async function sendDiscordAlert(message) {
  const webhookUrl = process.env.DISCORD_WEBHOOK_URL;

  await axios.post(webhookUrl, {
    content: message,
    embeds: [{
      title: 'Alert',
      color: 15158332, // Red
      fields: [{
        name: 'Service',
        value: process.env.RAILWAY_SERVICE_ID,
        inline: true
      }]
    }]
  });
}
```

---

## 외부 모니터링 도구 연동

### Datadog

```javascript
// dd-trace 패키지 사용
const tracer = require('dd-trace').init({
  service: 'my-railway-app',
  env: process.env.RAILWAY_ENVIRONMENT
});

// 환경 변수 설정
// DD_API_KEY=your-api-key
// DD_SITE=datadoghq.com
```

### Sentry (에러 트래킹)

```javascript
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.RAILWAY_ENVIRONMENT,
  release: process.env.RAILWAY_GIT_COMMIT_SHA
});

// 에러 캡처
app.use(Sentry.Handlers.errorHandler());
```

### Uptime 모니터링

외부 서비스로 가동시간 모니터링:
- UptimeRobot (무료)
- Better Uptime
- Pingdom

```
설정: 헬스체크 엔드포인트 URL 등록
예: https://your-app.up.railway.app/health
```

---

## 비용 모니터링

### 사용량 확인

```
1. 대시보드 > Settings > Usage
2. 현재 사용량 및 예상 비용 확인
```

### 비용 최적화

#### 리소스 최적화
```javascript
// 메모리 사용 최적화
const v8 = require('v8');
const heapStats = v8.getHeapStatistics();
console.log(`Heap used: ${heapStats.used_heap_size / 1024 / 1024} MB`);

// 연결 풀 최적화
const pool = new Pool({
  max: 10,  // 필요한 만큼만
  idleTimeoutMillis: 30000
});
```

#### 유휴 서비스 관리
```toml
# 개발 환경에서 유휴 시 슬립
# 대시보드에서 설정 가능
```

---

## 헬스체크 모니터링

### 상세 헬스체크

```javascript
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {}
  };

  // 데이터베이스 체크
  try {
    await pool.query('SELECT 1');
    health.checks.database = { status: 'healthy' };
  } catch (error) {
    health.checks.database = { status: 'unhealthy', error: error.message };
    health.status = 'degraded';
  }

  // Redis 체크
  try {
    await redis.ping();
    health.checks.redis = { status: 'healthy' };
  } catch (error) {
    health.checks.redis = { status: 'unhealthy', error: error.message };
    health.status = 'degraded';
  }

  // 메모리 체크
  const memUsage = process.memoryUsage();
  health.checks.memory = {
    heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024) + 'MB',
    heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024) + 'MB'
  };

  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});
```

---

## 문제 해결 가이드

### 일반적인 문제

| 증상 | 가능한 원인 | 확인 방법 | 해결 |
|------|-------------|----------|------|
| 느린 응답 | 메모리 부족 | 메트릭 확인 | 리소스 증가 |
| 간헐적 500 | 메모리 누수 | 시간별 메모리 추이 | 코드 검토 |
| 타임아웃 | DB 연결 부족 | DB 연결 수 | 풀 크기 조정 |
| 크래시 | 처리되지 않은 예외 | 로그 확인 | 에러 핸들링 |

### 디버깅 체크리스트

- [ ] 로그에서 에러 메시지 확인
- [ ] 메트릭에서 리소스 사용량 확인
- [ ] 최근 배포 변경사항 확인
- [ ] 헬스체크 엔드포인트 응답 확인
- [ ] 외부 서비스 (DB, API) 상태 확인

---

## 체크리스트

- [ ] 구조화된 로깅 구현
- [ ] 헬스체크 엔드포인트 구현
- [ ] 메트릭 수집 설정
- [ ] 알림 채널 연동 (Slack/Discord)
- [ ] 에러 트래킹 (Sentry) 연동
- [ ] 비용 알림 설정
- [ ] Uptime 모니터링 설정

---

## 다음 단계

- [[../05-projects|실전 프로젝트]] - 모니터링이 적용된 프로젝트 예제
- [[../cheatsheet|Cheatsheet]] - 모니터링 관련 명령어
