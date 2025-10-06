# Client Best Practices

> 최종 업데이트: 2025-10-06

클라이언트 측 로깅의 보안, 성능, 데이터 품질 관련 모범 사례를 다룹니다.

## 목차

1. [보안](#보안)
2. [성능 최적화](#성능-최적화)
3. [데이터 품질](#데이터-품질)
4. [비용 최적화](#비용-최적화)
5. [오프라인 대응](#오프라인-대응)
6. [로그 구조 설계](#로그-구조-설계)

## 보안

### ✅ Do: 반드시 해야 할 것

#### 1. 백엔드 API를 통해서만 전송

```
❌ 직접 연결
Client → Elasticsearch

✅ 올바른 방식
Client → Backend API → ELK Stack
```

**이유**:
- 자격 증명 보호
- 악의적 데이터 주입 방지
- 인증/권한 관리 가능
- Rate limiting 적용

#### 2. HTTPS 필수 사용

```javascript
// ✅ 올바른 예시
const apiUrl = 'https://api.example.com/logs';

// ❌ 잘못된 예시
const apiUrl = 'http://api.example.com/logs';  // HTTP는 안전하지 않음
```

#### 3. 민감한 정보 필터링

**필터링 대상**:
- 비밀번호
- API 키/토큰
- 신용카드 번호
- 주민등록번호
- 개인 식별 정보 (PII)

```javascript
function sanitizeLog(log) {
  const sanitized = { ...log };
  const sensitivePatterns = [
    /password/i,
    /token/i,
    /api[_-]?key/i,
    /secret/i,
    /credit[_-]?card/i,
    /ssn/i,
    /\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}/  // 카드 번호 패턴
  ];

  function redactSensitive(obj, path = '') {
    if (typeof obj !== 'object' || obj === null) return;

    Object.keys(obj).forEach(key => {
      const currentPath = path ? `${path}.${key}` : key;

      // 키 이름 검사
      if (sensitivePatterns.some(pattern => pattern.test(key))) {
        obj[key] = '[REDACTED]';
        return;
      }

      // 값이 객체면 재귀적 검사
      if (typeof obj[key] === 'object') {
        redactSensitive(obj[key], currentPath);
      }

      // 문자열 값 패턴 검사
      if (typeof obj[key] === 'string') {
        sensitivePatterns.forEach(pattern => {
          if (pattern.test(obj[key])) {
            obj[key] = '[REDACTED]';
          }
        });
      }
    });
  }

  redactSensitive(sanitized);
  return sanitized;
}

// 사용
const log = {
  user: { password: '12345', email: 'user@example.com' },
  apiKey: 'secret-key'
};

const safe = sanitizeLog(log);
// { user: { password: '[REDACTED]', email: 'user@example.com' }, apiKey: '[REDACTED]' }
```

#### 4. 인증 토큰 사용

```javascript
// API 호출시 인증 토큰 포함
async function sendLogs(logs) {
  const token = getAuthToken();  // JWT, OAuth 등

  await fetch('https://api.example.com/logs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ logs })
  });
}
```

#### 5. Rate Limiting

서버 측에서 구현:

```javascript
// Express.js 예시
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15분
  max: 100,  // 최대 100개 요청
  message: 'Too many log requests',
  standardHeaders: true,
  legacyHeaders: false,
});

app.post('/api/logs', limiter, handleLogs);
```

### ❌ Don't: 절대 하지 말아야 할 것

1. **클라이언트에서 Elasticsearch 직접 접근**
2. **로그에 민감한 정보 포함**
3. **HTTP 사용 (HTTPS 필수)**
4. **하드코딩된 자격 증명**
5. **사용자 입력값 검증 없이 로깅**

## 성능 최적화

### ✅ Do

#### 1. 로그 배치 전송

```javascript
class LogBatcher {
  constructor(apiUrl, options = {}) {
    this.apiUrl = apiUrl;
    this.buffer = [];
    this.maxSize = options.maxSize || 10;
    this.flushInterval = options.flushInterval || 5000;  // 5초

    this.startAutoFlush();
  }

  add(log) {
    this.buffer.push(log);

    if (this.buffer.length >= this.maxSize) {
      this.flush();
    }
  }

  async flush() {
    if (this.buffer.length === 0) return;

    const logsToSend = this.buffer.splice(0, this.buffer.length);

    try {
      await fetch(this.apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ logs: logsToSend })
      });
    } catch (error) {
      // 실패시 버퍼에 다시 추가
      this.buffer.unshift(...logsToSend);
    }
  }

  startAutoFlush() {
    setInterval(() => this.flush(), this.flushInterval);

    // 페이지 종료시 남은 로그 전송
    window.addEventListener('beforeunload', () => {
      if (this.buffer.length > 0) {
        navigator.sendBeacon(
          this.apiUrl,
          JSON.stringify({ logs: this.buffer })
        );
      }
    });
  }
}
```

#### 2. 로그 레벨 필터링

```javascript
const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  CRITICAL: 4
};

class Logger {
  constructor() {
    // 프로덕션에서는 INFO 이상만
    this.minLevel = process.env.NODE_ENV === 'production'
      ? LOG_LEVELS.INFO
      : LOG_LEVELS.DEBUG;
  }

  log(level, message, context) {
    if (LOG_LEVELS[level] < this.minLevel) {
      return;  // 로그 레벨이 낮으면 무시
    }

    // 로그 처리
    this.sendLog({ level, message, context });
  }

  debug(msg, ctx) {
    this.log('DEBUG', msg, ctx);
  }

  info(msg, ctx) {
    this.log('INFO', msg, ctx);
  }

  error(msg, ctx) {
    this.log('ERROR', msg, ctx);
  }
}
```

#### 3. 비동기 전송

```javascript
// ✅ 비동기 전송 (UI 블로킹 없음)
async function sendLog(log) {
  // 백그라운드에서 전송
  fetch('/api/logs', {
    method: 'POST',
    body: JSON.stringify(log),
    keepalive: true  // 페이지 종료 후에도 완료
  }).catch(err => {
    // 조용히 실패 처리
    console.error('Log send failed', err);
  });
}

// ❌ 동기 전송 (UI 블로킹)
function sendLogSync(log) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/api/logs', false);  // false = 동기
  xhr.send(JSON.stringify(log));
}
```

#### 4. 샘플링 (고빈도 이벤트)

```javascript
class SamplingLogger {
  constructor(sampleRate = 0.1) {  // 10%만 로깅
    this.sampleRate = sampleRate;
  }

  log(level, message, context) {
    // 랜덤 샘플링
    if (Math.random() > this.sampleRate) {
      return;  // 샘플링 비율에 따라 스킵
    }

    this.sendLog({ level, message, context });
  }

  // 에러는 항상 로깅
  error(message, context) {
    this.sendLog({ level: 'ERROR', message, context });
  }
}
```

### ❌ Don't

1. **로그마다 개별 HTTP 요청** → 배치 전송 사용
2. **무제한 버퍼링** → 메모리 누수 위험
3. **DEBUG 로그를 프로덕션에 전송** → 불필요한 트래픽
4. **동기 전송으로 UI 블로킹** → 비동기 사용
5. **과도한 로깅** → 샘플링 사용

## 데이터 품질

### ✅ 좋은 로그 구조

```javascript
const goodLog = {
  // 필수 필드
  timestamp: "2025-10-06T10:30:45.123Z",  // ISO 8601 형식
  level: "ERROR",
  message: "Failed to load user profile",

  // 컨텍스트 정보
  context: {
    // 사용자 정보
    userId: "user-123",
    sessionId: "sess-456",

    // 환경 정보
    url: "https://app.example.com/profile",
    userAgent: "Mozilla/5.0...",
    appVersion: "2.3.1",
    environment: "production",

    // 에러 정보
    error: {
      name: "NetworkError",
      message: "Failed to fetch",
      stack: "Error: Failed to fetch\n    at ...",
      code: "ERR_NETWORK"
    },

    // 추가 메타데이터
    requestId: "req-789",
    duration: 1234,  // ms
    component: "UserProfile"
  }
};
```

### 일관된 필드 명명 규칙

```javascript
// ✅ 일관된 명명
{
  user_id: "123",
  session_id: "456",
  request_id: "789"
}

// ❌ 비일관적 명명
{
  userId: "123",
  session_id: "456",
  RequestID: "789"
}
```

### 구조화된 로깅

```javascript
// ✅ 구조화된 로그 (JSON)
logger.error("User authentication failed", {
  userId: "123",
  reason: "invalid_password",
  attempts: 3
});

// ❌ 비구조화된 로그 (문자열)
logger.error("User 123 authentication failed due to invalid password, attempt 3");
```

## 비용 최적화

### 1. 로그 수명 관리

```javascript
// 중요도에 따른 보관 기간
const RETENTION_POLICY = {
  DEBUG: 1,      // 1일
  INFO: 7,       // 7일
  WARN: 30,      // 30일
  ERROR: 90,     // 90일
  CRITICAL: 365  // 1년
};
```

### 2. 로그 압축

```javascript
import pako from 'pako';

async function sendCompressedLogs(logs) {
  const json = JSON.stringify({ logs });
  const compressed = pako.gzip(json);

  await fetch('/api/logs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Encoding': 'gzip'
    },
    body: compressed
  });
}
```

### 3. 중요 로그만 전송

```javascript
const LOGGABLE_EVENTS = new Set([
  'user_login',
  'user_logout',
  'payment_completed',
  'error_occurred',
  'critical_action'
]);

function shouldLog(eventType) {
  return LOGGABLE_EVENTS.has(eventType);
}
```

## 오프라인 대응

### IndexedDB를 사용한 오프라인 저장

```javascript
class OfflineLogger {
  constructor() {
    this.dbName = 'LogsDB';
    this.storeName = 'logs';
    this.db = null;
    this.init();

    // 온라인 상태 변경 감지
    window.addEventListener('online', () => this.syncLogs());
  }

  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'id', autoIncrement: true });
        }
      };
    });
  }

  async log(entry) {
    if (navigator.onLine) {
      await this.sendLog(entry);
    } else {
      await this.saveOffline(entry);
    }
  }

  async saveOffline(entry) {
    const transaction = this.db.transaction([this.storeName], 'readwrite');
    const store = transaction.objectStore(this.storeName);
    store.add(entry);
  }

  async syncLogs() {
    const logs = await this.getAllOfflineLogs();

    for (const log of logs) {
      try {
        await this.sendLog(log);
        await this.deleteOfflineLog(log.id);
      } catch (error) {
        console.error('Failed to sync log', error);
        break;  // 실패시 중단
      }
    }
  }

  async getAllOfflineLogs() {
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      const request = store.getAll();

      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async deleteOfflineLog(id) {
    const transaction = this.db.transaction([this.storeName], 'readwrite');
    const store = transaction.objectStore(this.storeName);
    store.delete(id);
  }

  async sendLog(log) {
    const response = await fetch('/api/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(log)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
  }
}
```

## 로그 구조 설계

### 표준 로그 포맷

```typescript
interface LogEntry {
  // 기본 정보
  timestamp: string;        // ISO 8601
  level: 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'CRITICAL';
  message: string;

  // 식별자
  userId?: string;
  sessionId: string;
  requestId?: string;

  // 환경
  environment: 'development' | 'staging' | 'production';
  appVersion: string;
  platform: 'web' | 'mobile' | 'desktop';

  // 위치
  url: string;
  component?: string;
  function?: string;

  // 디바이스/브라우저
  userAgent: string;
  device?: {
    type: string;
    os: string;
    browser: string;
  };

  // 에러 (있는 경우)
  error?: {
    name: string;
    message: string;
    stack?: string;
    code?: string;
  };

  // 성능
  duration?: number;        // ms
  memory?: number;          // bytes

  // 커스텀 컨텍스트
  context?: Record<string, any>;
}
```

## 체크리스트

### 보안 체크리스트

- [ ] HTTPS 사용
- [ ] 백엔드 API를 통한 전송
- [ ] 민감한 정보 필터링
- [ ] 인증 토큰 사용
- [ ] Rate limiting 구현
- [ ] 입력값 검증

### 성능 체크리스트

- [ ] 배치 전송 구현
- [ ] 로그 레벨 필터링
- [ ] 비동기 전송
- [ ] 버퍼 크기 제한
- [ ] 샘플링 적용 (고빈도 이벤트)

### 데이터 품질 체크리스트

- [ ] ISO 8601 타임스탬프
- [ ] 구조화된 로그 (JSON)
- [ ] 일관된 필드 명명
- [ ] 충분한 컨텍스트 정보
- [ ] 버전 정보 포함

### 오프라인 체크리스트

- [ ] 로컬 저장소 구현
- [ ] 온라인 상태 감지
- [ ] 자동 동기화
- [ ] 재시도 로직
- [ ] 저장소 크기 제한

## 참고 자료

- [Best Practices for Client-Side Logging in React | Loggly](https://www.loggly.com/blog/best-practices-for-client-side-logging-and-error-handling-in-react/)
- [Options for log collection from client applications - Elastic Discuss](https://discuss.elastic.co/t/options-for-log-collection-from-client-applications/328288)

**최종 업데이트**: 2025-10-06
