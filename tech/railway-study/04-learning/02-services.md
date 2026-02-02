# Railway 서비스 유형

## 개요

Railway에서는 다양한 유형의 서비스를 실행할 수 있습니다. 각 서비스는 독립적인 컨테이너에서 실행되며, 용도에 따라 다르게 설정합니다.

---

## 서비스 유형

### 1. Web Service (웹 서비스)

외부에서 HTTP(S)로 접근 가능한 서비스입니다.

#### 특징
- 퍼블릭 도메인 제공
- 자동 HTTPS
- 로드 밸런싱
- 헬스체크 지원

#### 설정 예시
```toml
# railway.toml
[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 100
```

#### 코드 예시 (Node.js)
```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => res.send('Hello!'));
app.get('/health', (req, res) => res.json({ status: 'ok' }));

// 중요: 0.0.0.0으로 바인딩
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

---

### 2. Worker Service (워커 서비스)

백그라운드 작업을 처리하는 서비스입니다. HTTP 요청을 받지 않습니다.

#### 특징
- 외부 접근 불필요
- 큐 처리, 배치 작업에 적합
- 도메인 할당 없음

#### 사용 사례
- 메시지 큐 소비자 (RabbitMQ, Redis Queue)
- 이메일 발송 워커
- 데이터 처리 파이프라인
- 스크래핑/크롤링

#### 코드 예시 (Node.js with Bull)
```javascript
const Queue = require('bull');

const emailQueue = new Queue('email', process.env.REDIS_URL);

// 워커 프로세스
emailQueue.process(async (job) => {
  const { to, subject, body } = job.data;
  console.log(`Sending email to ${to}`);

  // 이메일 발송 로직
  await sendEmail(to, subject, body);

  return { sent: true };
});

console.log('Email worker started');

// 종료 처리
process.on('SIGTERM', async () => {
  await emailQueue.close();
  process.exit(0);
});
```

#### 설정
```toml
# railway.toml
[deploy]
startCommand = "node worker.js"
# healthcheckPath 설정하지 않음 (워커는 HTTP 없음)
```

---

### 3. Cron Job (크론 잡)

정해진 스케줄에 따라 실행되는 서비스입니다.

#### 특징
- 스케줄 기반 실행
- 실행 후 자동 종료
- 비용 효율적

#### 크론 표현식
```
┌─────────────── 분 (0-59)
│ ┌───────────── 시 (0-23)
│ │ ┌─────────── 일 (1-31)
│ │ │ ┌───────── 월 (1-12)
│ │ │ │ ┌─────── 요일 (0-6, 일요일=0)
│ │ │ │ │
* * * * *
```

#### 일반적인 예시
| 표현식 | 설명 |
|--------|------|
| `0 * * * *` | 매시 정각 |
| `0 0 * * *` | 매일 자정 |
| `0 9 * * 1` | 매주 월요일 오전 9시 |
| `*/15 * * * *` | 15분마다 |
| `0 0 1 * *` | 매월 1일 자정 |

#### 설정 방법
```toml
# railway.toml
[deploy]
startCommand = "node cron-job.js"

# 크론 스케줄은 대시보드에서 설정
# Settings > Cron Schedule
```

#### 코드 예시
```javascript
// cron-job.js
async function main() {
  console.log('Cron job started:', new Date().toISOString());

  try {
    // 작업 수행
    await performDailyCleanup();
    await generateDailyReport();

    console.log('Cron job completed successfully');
    process.exit(0);
  } catch (error) {
    console.error('Cron job failed:', error);
    process.exit(1);
  }
}

main();
```

---

## 서비스 구성 전략

### 단일 서비스 (모놀리식)

간단한 애플리케이션에 적합합니다.

```
┌─────────────────────────────────────┐
│            Web Service              │
│  ┌─────────┐  ┌─────────┐          │
│  │   API   │  │  Worker │          │
│  │ Routes  │  │ (같은   │          │
│  │         │  │ 프로세스)│          │
│  └─────────┘  └─────────┘          │
└─────────────────────────────────────┘
```

### 멀티 서비스 (분리형)

규모가 커지면 서비스를 분리합니다.

```
┌──────────────────────────────────────────────────┐
│                 Railway Project                   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Web    │  │  Worker  │  │   Cron   │       │
│  │ Service  │  │ Service  │  │   Job    │       │
│  │  (API)   │  │  (Queue) │  │ (Daily)  │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │              │
│       └─────────────┼─────────────┘              │
│                     │                            │
│              Private Network                     │
│                     │                            │
│       ┌─────────────┼─────────────┐              │
│       │             │             │              │
│  ┌────▼────┐   ┌────▼────┐  ┌────▼────┐        │
│  │ Postgres│   │  Redis  │  │  Redis  │        │
│  │  (Main) │   │ (Cache) │  │ (Queue) │        │
│  └─────────┘   └─────────┘  └─────────┘        │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## 서비스 간 통신

### Private Network 사용

같은 프로젝트 내 서비스는 Private Network로 통신합니다.

```javascript
// Web Service에서 Worker Service 호출 (비권장)
// 일반적으로 메시지 큐를 통해 통신

// Redis Queue 사용 예시
const Queue = require('bull');

// Web Service: 작업 추가
const emailQueue = new Queue('email', process.env.REDIS_URL);
await emailQueue.add({ to: 'user@example.com', subject: 'Hello' });

// Worker Service: 작업 처리
emailQueue.process(async (job) => {
  await sendEmail(job.data);
});
```

### 서비스 디스커버리

Railway는 Private Network에서 서비스 이름으로 접근 가능합니다.

```bash
# 환경 변수로 주입되는 내부 URL 형식
# RAILWAY_PRIVATE_DOMAIN=service-name.railway.internal

# 예: API 서비스에서 Worker 서비스 호출
curl http://worker-service.railway.internal:3000/internal-endpoint
```

---

## 모범 사례

### Web Service
```javascript
// 1. 환경변수로 포트 설정
const PORT = process.env.PORT || 3000;

// 2. 헬스체크 엔드포인트 구현
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

// 3. Graceful Shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
```

### Worker Service
```javascript
// 1. 재시도 로직 구현
const queue = new Queue('tasks', {
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000
    }
  }
});

// 2. 에러 핸들링
queue.on('failed', (job, err) => {
  console.error(`Job ${job.id} failed:`, err);
  // 알림 전송 등
});

// 3. 메트릭 수집
queue.on('completed', (job) => {
  console.log(`Job ${job.id} completed`);
});
```

### Cron Job
```javascript
// 1. 멱등성 보장
async function dailyCleanup() {
  // 이미 처리된 데이터는 건너뛰기
  const lastRun = await getLastRunTimestamp();
  // ...
}

// 2. 실행 시간 로깅
const start = Date.now();
await performTask();
console.log(`Task completed in ${Date.now() - start}ms`);

// 3. 명확한 종료 코드
process.exit(0); // 성공
process.exit(1); // 실패
```

---

## 서비스 설정 옵션

### railway.toml 전체 예시

```toml
# 빌드 설정
[build]
builder = "nixpacks"
buildCommand = "npm run build"
watchPatterns = ["src/**"]

# 배포 설정
[deploy]
numReplicas = 1
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### 환경별 설정
```toml
# Production 환경
[environments.production.deploy]
numReplicas = 2
startCommand = "npm run start:prod"

# Staging 환경
[environments.staging.deploy]
numReplicas = 1
startCommand = "npm run start:staging"
```

---

## 다음 단계

- [[03-databases|데이터베이스]] - PostgreSQL, Redis 추가
- [[04-environment|환경 변수]] - 서비스별 설정 관리
- [[05-networking|네트워킹]] - Private Network 상세 설정
