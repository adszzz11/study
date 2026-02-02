# Railway 데이터베이스

## 개요

Railway는 다양한 데이터베이스를 원클릭으로 프로비저닝할 수 있습니다. 모든 데이터베이스는 Private Network를 통해 안전하게 연결됩니다.

---

## 지원 데이터베이스

| 데이터베이스 | 용도 | 특징 |
|-------------|------|------|
| **PostgreSQL** | 범용 관계형 | ACID, JSON 지원, 확장성 |
| **MySQL** | 범용 관계형 | 널리 사용, 호환성 |
| **MongoDB** | 문서형 NoSQL | 유연한 스키마, 수평 확장 |
| **Redis** | 캐시/큐 | 초고속 인메모리, Pub/Sub |

---

## PostgreSQL

### 생성 방법

#### 대시보드
```
1. 프로젝트 > "New" > "Database" > "Add PostgreSQL"
2. 자동으로 프로비저닝 및 환경 변수 주입
```

#### CLI
```bash
railway add --database postgres
```

### 환경 변수

Railway가 자동으로 주입하는 변수:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
PGHOST=containers-us-west-xxx.railway.app
PGPORT=5432
PGUSER=postgres
PGPASSWORD=xxxxx
PGDATABASE=railway
```

### 연결 예시

#### Node.js (Prisma)
```javascript
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 사용
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const users = await prisma.user.findMany();
  console.log(users);
}
```

#### Node.js (pg)
```javascript
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production'
    ? { rejectUnauthorized: false }
    : false
});

const result = await pool.query('SELECT * FROM users');
```

#### Python (SQLAlchemy)
```python
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ['DATABASE_URL'])

with engine.connect() as conn:
    result = conn.execute("SELECT * FROM users")
```

### 마이그레이션

```bash
# Prisma
npx prisma migrate deploy

# Django
python manage.py migrate

# 또는 Railway에서 자동 실행
# railway.toml
[deploy]
startCommand = "npx prisma migrate deploy && npm start"
```

---

## MySQL

### 생성 방법

```
1. 프로젝트 > "New" > "Database" > "Add MySQL"
2. 환경 변수 자동 주입
```

### 환경 변수

```bash
MYSQL_URL=mysql://user:password@host:port/database
MYSQLHOST=containers-us-west-xxx.railway.app
MYSQLPORT=3306
MYSQLUSER=root
MYSQLPASSWORD=xxxxx
MYSQLDATABASE=railway
```

### 연결 예시

#### Node.js (mysql2)
```javascript
const mysql = require('mysql2/promise');

const connection = await mysql.createConnection(process.env.MYSQL_URL);
const [rows] = await connection.execute('SELECT * FROM users');
```

#### Python (PyMySQL)
```python
import pymysql
import os

connection = pymysql.connect(
    host=os.environ['MYSQLHOST'],
    user=os.environ['MYSQLUSER'],
    password=os.environ['MYSQLPASSWORD'],
    database=os.environ['MYSQLDATABASE'],
    port=int(os.environ['MYSQLPORT'])
)
```

---

## Redis

### 생성 방법

```
1. 프로젝트 > "New" > "Database" > "Add Redis"
2. 환경 변수 자동 주입
```

### 환경 변수

```bash
REDIS_URL=redis://default:password@host:port
REDISHOST=containers-us-west-xxx.railway.app
REDISPORT=6379
REDISUSER=default
REDISPASSWORD=xxxxx
```

### 사용 사례

#### 1. 캐싱
```javascript
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

// 캐시 설정
await redis.set('user:123', JSON.stringify(userData), 'EX', 3600);

// 캐시 조회
const cached = await redis.get('user:123');
if (cached) {
  return JSON.parse(cached);
}
```

#### 2. 세션 저장
```javascript
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const Redis = require('ioredis');

const redisClient = new Redis(process.env.REDIS_URL);

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}));
```

#### 3. 작업 큐 (Bull)
```javascript
const Queue = require('bull');

const emailQueue = new Queue('email', process.env.REDIS_URL);

// 작업 추가
await emailQueue.add({
  to: 'user@example.com',
  subject: 'Welcome!'
});

// 워커에서 처리
emailQueue.process(async (job) => {
  await sendEmail(job.data);
});
```

#### 4. Pub/Sub
```javascript
const Redis = require('ioredis');
const publisher = new Redis(process.env.REDIS_URL);
const subscriber = new Redis(process.env.REDIS_URL);

// 구독
subscriber.subscribe('notifications');
subscriber.on('message', (channel, message) => {
  console.log(`Received: ${message}`);
});

// 발행
publisher.publish('notifications', 'New message!');
```

---

## MongoDB

### 생성 방법

```
1. 프로젝트 > "New" > "Database" > "Add MongoDB"
2. 환경 변수 자동 주입
```

### 환경 변수

```bash
MONGO_URL=mongodb://user:password@host:port/database
MONGOHOST=containers-us-west-xxx.railway.app
MONGOPORT=27017
MONGOUSER=mongo
MONGOPASSWORD=xxxxx
```

### 연결 예시

#### Node.js (Mongoose)
```javascript
const mongoose = require('mongoose');

mongoose.connect(process.env.MONGO_URL);

const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

const user = await User.create({ name: 'John', email: 'john@example.com' });
```

#### Python (PyMongo)
```python
from pymongo import MongoClient
import os

client = MongoClient(os.environ['MONGO_URL'])
db = client.railway

users = db.users.find({})
```

---

## Private Network 연결

### 내부 연결 (권장)

같은 프로젝트 내에서는 Private Network를 사용합니다.

```bash
# 환경 변수 예시 (Private)
DATABASE_PRIVATE_URL=postgresql://user:pass@postgres.railway.internal:5432/railway
REDIS_PRIVATE_URL=redis://default:pass@redis.railway.internal:6379
```

### 외부 연결

개발 환경에서 직접 연결할 때:

```bash
# Public URL 사용 (개발용)
DATABASE_URL=postgresql://user:pass@containers-us-west-xxx.railway.app:5432/railway
```

### 연결 URL 선택

```javascript
// 환경에 따라 자동 선택
const databaseUrl = process.env.DATABASE_PRIVATE_URL || process.env.DATABASE_URL;
```

---

## 백업 및 복원

### 수동 백업

#### PostgreSQL
```bash
# 백업
pg_dump $DATABASE_URL > backup.sql

# 복원
psql $DATABASE_URL < backup.sql
```

#### MySQL
```bash
# 백업
mysqldump -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD $MYSQLDATABASE > backup.sql

# 복원
mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD $MYSQLDATABASE < backup.sql
```

#### MongoDB
```bash
# 백업
mongodump --uri=$MONGO_URL --out=backup/

# 복원
mongorestore --uri=$MONGO_URL backup/
```

### 자동 백업

Railway에서는 자동 백업 기능을 제공합니다 (Pro 플랜).

---

## 성능 최적화

### 연결 풀링

```javascript
// Node.js PostgreSQL
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,        // 최대 연결 수
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```

### 인덱스 설정

```sql
-- PostgreSQL 인덱스
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

### Redis 최적화

```javascript
// 파이프라인 사용
const pipeline = redis.pipeline();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.set('key3', 'value3');
await pipeline.exec();
```

---

## 모니터링

### 대시보드에서 확인
- 연결 수
- 쿼리 수
- 디스크 사용량
- 메모리 사용량

### 쿼리 로깅

```javascript
// Prisma 쿼리 로깅
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error']
});
```

---

## 문제 해결

### 연결 실패
| 문제 | 해결 방법 |
|------|----------|
| Connection refused | 환경 변수 확인, Private URL 사용 |
| Authentication failed | 비밀번호 확인, URL 인코딩 |
| Too many connections | 연결 풀 크기 조정, 유휴 연결 정리 |

### SSL 연결 문제
```javascript
// SSL 설정 (외부 연결 시)
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});
```

---

## 다음 단계

- [[04-environment|환경 변수]] - 데이터베이스 URL 관리
- [[05-networking|네트워킹]] - Private Network 상세 설정
- [[../05-projects|실전 프로젝트]] - 풀스택 앱 구축
