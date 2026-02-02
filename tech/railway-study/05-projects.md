# Railway 실전 프로젝트

## 개요

이 문서에서는 Railway를 활용한 실전 프로젝트 예제와 Best Practices를 다룹니다.

---

## 프로젝트 1: 풀스택 웹 애플리케이션

### 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    Railway Project                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   Frontend   │  HTTPS  │   Backend    │             │
│  │   (Next.js)  │◀───────▶│  (Express)   │             │
│  │  Port: 3000  │         │  Port: 4000  │             │
│  └──────────────┘         └──────┬───────┘             │
│        │                         │                       │
│        │                  Private Network               │
│        │                         │                       │
│        │                 ┌───────▼───────┐             │
│        │                 │  PostgreSQL   │             │
│        │                 │  Port: 5432   │             │
│        │                 └───────────────┘             │
│        │                         │                       │
│        │                 ┌───────▼───────┐             │
│        │                 │     Redis     │             │
│        │                 │  (Cache)      │             │
│        │                 └───────────────┘             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 구현

#### Backend (Express + Prisma)

```javascript
// backend/index.js
const express = require('express');
const cors = require('cors');
const { PrismaClient } = require('@prisma/client');
const Redis = require('ioredis');

const app = express();
const prisma = new PrismaClient();
const redis = new Redis(process.env.REDIS_URL);

app.use(cors({
  origin: process.env.FRONTEND_URL,
  credentials: true
}));
app.use(express.json());

// 헬스체크
app.get('/health', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    await redis.ping();
    res.json({ status: 'healthy' });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', error: error.message });
  }
});

// CRUD API
app.get('/api/posts', async (req, res) => {
  // 캐시 확인
  const cached = await redis.get('posts:all');
  if (cached) {
    return res.json(JSON.parse(cached));
  }

  const posts = await prisma.post.findMany({
    include: { author: true },
    orderBy: { createdAt: 'desc' }
  });

  // 캐시 저장 (5분)
  await redis.set('posts:all', JSON.stringify(posts), 'EX', 300);
  res.json(posts);
});

app.post('/api/posts', async (req, res) => {
  const { title, content, authorId } = req.body;
  const post = await prisma.post.create({
    data: { title, content, authorId }
  });

  // 캐시 무효화
  await redis.del('posts:all');
  res.status(201).json(post);
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Backend running on port ${PORT}`);
});
```

#### Frontend (Next.js)

```javascript
// frontend/pages/index.js
import { useEffect, useState } from 'react';

export default function Home() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/posts`)
      .then(res => res.json())
      .then(data => {
        setPosts(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
          <small>By {post.author.name}</small>
        </article>
      ))}
    </div>
  );
}
```

#### 환경 변수 설정

```bash
# Backend 서비스
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
REDIS_URL=${{Redis.REDIS_PRIVATE_URL}}
FRONTEND_URL=https://your-frontend.up.railway.app
JWT_SECRET=your-secret-key

# Frontend 서비스
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

---

## 프로젝트 2: API + Worker + Cron

### 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    Railway Project                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  Queue  ┌──────────────┐             │
│  │   API        │────────▶│   Worker     │             │
│  │   Service    │  Redis  │   Service    │             │
│  └──────────────┘         └──────────────┘             │
│         │                        │                       │
│         │                        │                       │
│         │                 ┌──────▼───────┐             │
│         │                 │    Cron      │             │
│         │                 │   Service    │             │
│         │                 │ (Daily 9am)  │             │
│         │                 └──────────────┘             │
│         │                        │                       │
│         └────────────┬───────────┘                       │
│                      │                                   │
│              ┌───────▼───────┐                          │
│              │   PostgreSQL  │                          │
│              └───────────────┘                          │
│              ┌───────────────┐                          │
│              │     Redis     │                          │
│              │    (Queue)    │                          │
│              └───────────────┘                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 구현

#### API Service

```javascript
// api/index.js
const express = require('express');
const Queue = require('bull');

const app = express();
const emailQueue = new Queue('email', process.env.REDIS_URL);
const reportQueue = new Queue('report', process.env.REDIS_URL);

app.use(express.json());

// 이메일 발송 요청
app.post('/api/send-email', async (req, res) => {
  const { to, subject, body } = req.body;

  await emailQueue.add({
    to,
    subject,
    body,
    requestedAt: new Date().toISOString()
  }, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 }
  });

  res.json({ message: 'Email queued' });
});

// 리포트 생성 요청
app.post('/api/generate-report', async (req, res) => {
  const { type, dateRange } = req.body;

  const job = await reportQueue.add({
    type,
    dateRange,
    requestedBy: req.user?.id
  });

  res.json({ jobId: job.id, message: 'Report generation started' });
});

// 작업 상태 확인
app.get('/api/jobs/:id', async (req, res) => {
  const job = await reportQueue.getJob(req.params.id);
  if (!job) {
    return res.status(404).json({ error: 'Job not found' });
  }

  const state = await job.getState();
  const progress = job.progress();

  res.json({ id: job.id, state, progress });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0');
```

#### Worker Service

```javascript
// worker/index.js
const Queue = require('bull');
const nodemailer = require('nodemailer');

const emailQueue = new Queue('email', process.env.REDIS_URL);
const reportQueue = new Queue('report', process.env.REDIS_URL);

// 이메일 처리
emailQueue.process(async (job) => {
  const { to, subject, body } = job.data;
  console.log(`Processing email job ${job.id}`);

  const transporter = nodemailer.createTransporter({
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
  });

  await transporter.sendMail({ to, subject, html: body });
  console.log(`Email sent to ${to}`);

  return { sent: true, to };
});

// 리포트 처리
reportQueue.process(async (job) => {
  const { type, dateRange } = job.data;
  console.log(`Generating ${type} report`);

  // 진행률 업데이트
  job.progress(10);

  // 데이터 수집
  const data = await collectData(type, dateRange);
  job.progress(50);

  // 리포트 생성
  const report = await generateReport(data);
  job.progress(90);

  // 저장
  await saveReport(report);
  job.progress(100);

  return { reportId: report.id };
});

// 에러 핸들링
emailQueue.on('failed', (job, err) => {
  console.error(`Email job ${job.id} failed:`, err);
});

console.log('Worker started');
```

#### Cron Service

```javascript
// cron/daily-cleanup.js
const { PrismaClient } = require('@prisma/client');

const prisma = new PrismaClient();

async function main() {
  console.log('Daily cleanup started:', new Date().toISOString());

  try {
    // 30일 지난 로그 삭제
    const deletedLogs = await prisma.log.deleteMany({
      where: {
        createdAt: {
          lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
        }
      }
    });
    console.log(`Deleted ${deletedLogs.count} old logs`);

    // 만료된 세션 정리
    const deletedSessions = await prisma.session.deleteMany({
      where: {
        expiresAt: { lt: new Date() }
      }
    });
    console.log(`Deleted ${deletedSessions.count} expired sessions`);

    // 일일 통계 생성
    const stats = await generateDailyStats();
    await prisma.dailyStat.create({ data: stats });
    console.log('Daily stats generated');

    process.exit(0);
  } catch (error) {
    console.error('Cleanup failed:', error);
    process.exit(1);
  }
}

main();
```

```toml
# cron/railway.toml
[deploy]
startCommand = "node daily-cleanup.js"
# Cron 스케줄은 대시보드에서 설정: 0 9 * * * (매일 오전 9시)
```

---

## 프로젝트 3: 모노레포 배포

### 폴더 구조

```
my-monorepo/
├── apps/
│   ├── web/           # Next.js 프론트엔드
│   │   └── railway.toml
│   ├── api/           # Express 백엔드
│   │   └── railway.toml
│   └── admin/         # Admin 대시보드
│       └── railway.toml
├── packages/
│   ├── shared/        # 공유 유틸리티
│   └── types/         # 공유 타입
├── package.json
└── turbo.json
```

### 서비스별 설정

#### apps/web/railway.toml
```toml
[build]
builder = "nixpacks"
buildCommand = "cd ../.. && npm install && npm run build --filter=web"

[deploy]
startCommand = "npm run start"
```

#### apps/api/railway.toml
```toml
[build]
builder = "nixpacks"
buildCommand = "cd ../.. && npm install && npm run build --filter=api"

[deploy]
startCommand = "npm run start"
healthcheckPath = "/health"
```

### Railway 설정

```
각 apps/ 폴더를 별도 서비스로 배포:
1. New Service > Deploy from GitHub repo
2. Root Directory 설정: apps/web (또는 apps/api)
3. 각 서비스에 해당 환경 변수 설정
```

---

## Best Practices

### 1. 환경 분리

```
Production 환경
├── 실 사용자 트래픽
├── 자동 스케일링 활성화
├── 알림 설정 필수
└── 백업 정책 수립

Staging 환경
├── 배포 전 테스트
├── Production과 동일한 구성
└── 샘플 데이터 사용

Development 환경
├── 개발자 테스트
├── PR Preview 활용
└── 비용 최소화 설정
```

### 2. 보안

```javascript
// 헬멧 사용
const helmet = require('helmet');
app.use(helmet());

// Rate Limiting
const rateLimit = require('express-rate-limit');
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));

// 입력 검증
const { body, validationResult } = require('express-validator');
app.post('/api/users',
  body('email').isEmail(),
  body('password').isLength({ min: 8 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // ...
  }
);
```

### 3. 에러 핸들링

```javascript
// 전역 에러 핸들러
app.use((err, req, res, next) => {
  console.error('Error:', {
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method
  });

  // Sentry로 전송
  if (process.env.SENTRY_DSN) {
    Sentry.captureException(err);
  }

  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal Server Error'
      : err.message
  });
});

// 처리되지 않은 Promise 거부
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
});
```

### 4. Graceful Shutdown

```javascript
const server = app.listen(PORT);

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');

  server.close(() => {
    console.log('HTTP server closed');

    // 데이터베이스 연결 종료
    prisma.$disconnect().then(() => {
      console.log('Database disconnected');

      // Redis 연결 종료
      redis.quit().then(() => {
        console.log('Redis disconnected');
        process.exit(0);
      });
    });
  });

  // 10초 후 강제 종료
  setTimeout(() => {
    console.error('Forced shutdown');
    process.exit(1);
  }, 10000);
});
```

### 5. 로깅 표준

```javascript
const createLogger = () => {
  return {
    info: (message, meta = {}) => {
      console.log(JSON.stringify({
        level: 'info',
        message,
        timestamp: new Date().toISOString(),
        service: process.env.RAILWAY_SERVICE_ID,
        environment: process.env.RAILWAY_ENVIRONMENT,
        ...meta
      }));
    },
    error: (message, error, meta = {}) => {
      console.error(JSON.stringify({
        level: 'error',
        message,
        error: error?.message,
        stack: error?.stack,
        timestamp: new Date().toISOString(),
        service: process.env.RAILWAY_SERVICE_ID,
        ...meta
      }));
    }
  };
};

const logger = createLogger();
logger.info('Server started', { port: PORT });
logger.error('Database error', err, { query: 'SELECT ...' });
```

---

## 배포 체크리스트

### 배포 전
- [ ] 로컬에서 테스트 완료
- [ ] 환경 변수 설정 확인
- [ ] 데이터베이스 마이그레이션 준비
- [ ] 헬스체크 엔드포인트 구현

### 배포 중
- [ ] 빌드 로그 모니터링
- [ ] 배포 로그 확인
- [ ] 헬스체크 통과 확인

### 배포 후
- [ ] 주요 기능 동작 확인
- [ ] 에러 로그 모니터링
- [ ] 성능 메트릭 확인
- [ ] 알림 채널 확인

---

## 다음 단계

- [[cheatsheet|Cheatsheet]] - 빠른 명령어 참조
- [[03-references|참고 자료]] - 추가 학습 리소스
