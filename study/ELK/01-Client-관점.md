# ELK Stack - Client 관점

> 최종 업데이트: 2025-10-06

클라이언트 애플리케이션에서 ELK Stack으로 로그를 전송하는 방법과 아키텍처를 다룹니다.

## 목차

1. [개요](#개요)
2. [클라이언트 측 로깅의 특징](#클라이언트-측-로깅의-특징)
3. [웹 브라우저 애플리케이션](#웹-브라우저-애플리케이션)
4. [모바일 애플리케이션](#모바일-애플리케이션)
5. [아키텍처 패턴](#아키텍처-패턴)
6. [Best Practices](#best-practices)

## 개요

클라이언트 측 애플리케이션(웹 브라우저, 모바일 앱, 데스크톱 앱)에서 ELK Stack으로 로그를 전송하는 것은 서버 측 로깅과는 다른 접근 방식이 필요합니다.

### 주요 차이점

| 구분 | 서버 측 | 클라이언트 측 |
|-----|--------|------------|
| 네트워크 | 안정적 | 불안정적 (모바일 특히) |
| 대역폭 | 풍부 | 제한적 |
| 보안 | 내부 네트워크 | 공개 네트워크 |
| 직접 연결 | 가능 | **불가능/비권장** |

> **중요**: 클라이언트는 **절대 Elasticsearch나 Logstash에 직접 연결하지 않습니다**. 반드시 중간 백엔드 서버를 통해야 합니다.

## 클라이언트 측 로깅의 특징

### 1. 보안 고려사항

```
❌ 잘못된 방법: 클라이언트 → Elasticsearch (직접)
✅ 올바른 방법: 클라이언트 → 백엔드 API → ELK Stack
```

**직접 연결이 위험한 이유**:
- Elasticsearch 자격 증명이 클라이언트 코드에 노출됨
- 악의적 사용자가 임의의 데이터를 주입할 수 있음
- DDoS 공격의 대상이 될 수 있음
- 인증/권한 관리 불가능

### 2. 네트워크 제약

- **모바일**: 제한된 대역폭, 불안정한 연결
- **브라우저**: CORS 정책, 네트워크 레이턴시
- **해결책**: 백엔드 엔드포인트로 배치 전송, 로컬 버퍼링

## 웹 브라우저 애플리케이션

### 지원 프레임워크

현재 ELK와 통합 가능한 주요 JavaScript 프레임워크:

- React
- Vue.js
- Angular
- Vanilla JavaScript

### 구현 방법

#### 1. 백엔드 엔드포인트 방식 (권장)

**아키텍처**:
```
[브라우저] → [백엔드 API] → [Logstash/Elasticsearch]
```

**React 예시 구현**:

```javascript
// 로그 전송 유틸리티
class LogService {
  constructor(backendUrl) {
    this.backendUrl = backendUrl;
    this.buffer = [];
    this.flushInterval = 5000; // 5초마다 전송

    this.startAutoFlush();
  }

  log(level, message, context = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: {
        ...context,
        userAgent: navigator.userAgent,
        url: window.location.href,
        sessionId: this.getSessionId()
      }
    };

    this.buffer.push(logEntry);

    // 버퍼가 가득 차면 즉시 전송
    if (this.buffer.length >= 10) {
      this.flush();
    }
  }

  async flush() {
    if (this.buffer.length === 0) return;

    const logs = [...this.buffer];
    this.buffer = [];

    try {
      await fetch(`${this.backendUrl}/api/logs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ logs })
      });
    } catch (error) {
      // 실패한 로그는 다시 버퍼에 추가
      this.buffer.unshift(...logs);
    }
  }

  startAutoFlush() {
    setInterval(() => this.flush(), this.flushInterval);
  }

  getSessionId() {
    // 세션 ID 생성 로직
    return sessionStorage.getItem('sessionId') || this.generateSessionId();
  }
}

// React 컴포넌트에서 사용
import React, { useEffect } from 'react';

const App = () => {
  const logger = new LogService('https://your-backend.com');

  useEffect(() => {
    // 에러 리스너 설정
    window.addEventListener('error', (event) => {
      logger.log('error', event.message, {
        stack: event.error?.stack,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno
      });
    });

    // Unhandled Promise Rejection 리스너
    window.addEventListener('unhandledrejection', (event) => {
      logger.log('error', event.reason, {
        type: 'unhandledRejection',
        promise: event.promise
      });
    });
  }, []);

  return <div>Your App</div>;
};
```

**출처**:
- [Best Way to Log Client-Side/Javascript in ELK - Stack Overflow](https://stackoverflow.com/questions/53089448/best-way-to-log-client-side-javascript-in-elk-logstash)
- [Best Practices for Client-Side Logging in React | Loggly](https://www.loggly.com/blog/best-practices-for-client-side-logging-and-error-handling-in-react/)

#### 2. Vue.js 전용 라이브러리

**vuejs-logger 사용**:

```bash
npm install vuejs-logger
```

```javascript
import VueLogger from 'vuejs-logger';

const options = {
  isEnabled: true,
  logLevel: 'debug',
  stringifyArguments: false,
  showLogLevel: true,
  showMethodName: true,
  separator: '|',
  showConsoleColors: true
};

Vue.use(VueLogger, options);

// 사용
this.$log.debug('디버그 메시지');
this.$log.error('에러 발생', errorObject);
```

**출처**: [vuejs-logger - npm](https://www.npmjs.com/package/vuejs-logger)

#### 3. 서드파티 로깅 서비스 활용 (2025년 기준)

ELK를 직접 사용하는 대신, 클라이언트 특화 로깅 서비스를 중간 계층으로 사용하는 방법:

**주요 서비스**:

1. **Sentry**
   - 에러 트래킹 특화
   - React, Vue, Angular 모두 지원
   - ELK로 데이터 포워딩 가능

2. **TrackJS**
   - JavaScript 에러 로깅 전문
   - 상세한 컨텍스트 수집

3. **Datadog Browser Log Collection**
   - 브라우저 로그 수집
   - ELK와 통합 가능

4. **Elmah.io**
   - SPA (React, Angular, Vue) 지원
   - 에러 모니터링

**출처**: [Best JavaScript client-side error logging services 2025 - Slant](https://www.slant.co/topics/2615/~best-javascript-client-side-error-logging-services)

### 백엔드 API 구현 예시

클라이언트에서 받은 로그를 Logstash로 전달하는 Node.js 예시:

```javascript
// Express.js 백엔드
const express = require('express');
const winston = require('winston');
const LogstashTransport = require('winston-logstash-transport').LogstashTransport;

const app = express();
app.use(express.json());

// Winston + Logstash 설정
const logger = winston.createLogger({
  transports: [
    new LogstashTransport({
      host: 'localhost',
      port: 5000
    })
  ]
});

// 클라이언트 로그 수신 엔드포인트
app.post('/api/logs', (req, res) => {
  const { logs } = req.body;

  // 입력 검증
  if (!Array.isArray(logs)) {
    return res.status(400).json({ error: 'Invalid logs format' });
  }

  // 각 로그를 Logstash로 전송
  logs.forEach(log => {
    logger.log({
      level: log.level || 'info',
      message: log.message,
      timestamp: log.timestamp,
      context: log.context,
      source: 'client-side'
    });
  });

  res.status(200).json({ success: true });
});

app.listen(3000, () => {
  console.log('Log API server running on port 3000');
});
```

## 모바일 애플리케이션

### iOS 및 Android

모바일 애플리케이션에서 ELK로 로그를 전송하는 것은 웹보다 더 많은 제약이 있습니다.

#### 주요 도전 과제

1. **제한된 대역폭**: 셀룰러 네트워크에서 데이터 사용량 고려
2. **불안정한 연결**: 오프라인 상태 대응 필요
3. **배터리 소모**: 빈번한 네트워크 요청 최소화
4. **사용자 데이터 요금**: 과도한 로그 전송 방지

**출처**: [Why is it not popular to have a mobile application send crash log to ELK - Stack Overflow](https://stackoverflow.com/questions/62880629/why-is-it-not-popular-to-have-a-mobile-application-send-crash-log-to-elk)

#### 권장 접근 방식

**아키텍처**:
```
[모바일 앱] → [로컬 버퍼/DB] → [백엔드 API] → [ELK Stack]
              (Wi-Fi 연결시에만 전송)
```

#### 전송 방법 옵션

1. **HTTP/HTTPS REST API** (가장 일반적)
   - 백엔드 엔드포인트로 POST 요청
   - 배치 전송으로 네트워크 요청 최소화

2. **MQTT** (IoT 디바이스에 적합)
   - 경량 메시징 프로토콜
   - 불안정한 네트워크에 강함

3. **WebSocket**
   - 실시간 양방향 통신
   - 배터리 소모가 많음 (주의)

4. **Firebase**
   - Firebase → Cloud Functions → ELK
   - 간접적인 방법

**출처**: [How do i send Native apps log on ELK stack? - Stack Overflow](https://stackoverflow.com/questions/41744405/how-do-i-send-native-apps-log-on-elk-stack)

#### 모바일 로깅 라이브러리 예시

**Go Mobile Log ELK** (크로스 플랫폼):

```go
// Go로 작성된 모바일 라이브러리
// Android와 iOS에서 사용 가능

package logging

import (
    "bytes"
    "encoding/json"
    "net/http"
    "time"
)

type LogEntry struct {
    Timestamp string                 `json:"timestamp"`
    Level     string                 `json:"level"`
    Message   string                 `json:"message"`
    Context   map[string]interface{} `json:"context"`
}

type MobileLogger struct {
    apiEndpoint string
    buffer      []LogEntry
    maxBuffer   int
}

func (l *MobileLogger) Log(level, message string, context map[string]interface{}) {
    entry := LogEntry{
        Timestamp: time.Now().Format(time.RFC3339),
        Level:     level,
        Message:   message,
        Context:   context,
    }

    l.buffer = append(l.buffer, entry)

    if len(l.buffer) >= l.maxBuffer {
        l.Flush()
    }
}

func (l *MobileLogger) Flush() error {
    if len(l.buffer) == 0 {
        return nil
    }

    data, err := json.Marshal(l.buffer)
    if err != nil {
        return err
    }

    resp, err := http.Post(l.apiEndpoint, "application/json", bytes.NewBuffer(data))
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    l.buffer = l.buffer[:0] // 버퍼 클리어
    return nil
}
```

**출처**: [go-mobile-log-elk - GitHub](https://github.com/hemant24/go-mobile-log-elk)

### 모바일 전용 대안 솔루션

ELK Stack 대신 모바일에 특화된 솔루션을 사용하는 것도 일반적입니다:

1. **Firebase Crashlytics**
   - 크래시 리포트 및 로그 수집
   - 무료 제공

2. **Sentry.io**
   - iOS, Android SDK 제공
   - ELK로 데이터 포워딩 가능

3. **Bugfender**
   - 모바일 로깅 전문
   - 오프라인 지원

4. **Loggly**
   - 클라우드 로그 관리
   - 모바일 SDK 제공

**출처**:
- [Send logs to Kibana using Mobile iOS device - Elastic Discuss](https://discuss.elastic.co/t/send-logs-to-kibana-using-mobile-ios-devie-android-ios/305679)
- [Send Data from Mobile application to ELK - Elastic Discuss](https://discuss.elastic.co/t/send-data-from-mobile-application-to-elk/240157)

## 아키텍처 패턴

### 권장 아키텍처

```
┌─────────────────┐
│  Client Apps    │
│  - Browser      │
│  - Mobile       │
│  - Desktop      │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Backend API    │
│  - 인증/권한     │
│  - 데이터 검증   │
│  - 로그 변환     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Logstash      │
│   or            │
│   Filebeat      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Elasticsearch   │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│    Kibana       │
└─────────────────┘
```

### 처리 흐름

1. **클라이언트 로그 생성**
   - 에러, 경고, 정보 로그
   - 사용자 행동 추적
   - 성능 메트릭

2. **로컬 버퍼링**
   - 메모리 또는 로컬 스토리지
   - 배치 전송 준비
   - 오프라인 대응

3. **백엔드 전송**
   - HTTPS POST 요청
   - 인증 토큰 포함
   - 재시도 로직

4. **백엔드 처리**
   - 입력 검증 및 sanitization
   - 추가 메타데이터 부여
   - Logstash로 전달

5. **ELK Stack 처리**
   - Logstash 파싱 및 변환
   - Elasticsearch 인덱싱
   - Kibana 시각화

## Best Practices

### 1. 보안

✅ **Do:**
- 백엔드 API를 통해서만 로그 전송
- API 키/토큰 기반 인증 사용
- HTTPS 필수 사용
- 민감한 정보 필터링 (비밀번호, 토큰, PII)
- Rate limiting 적용

❌ **Don't:**
- 클라이언트에서 Elasticsearch 직접 접근
- 로그에 민감한 정보 포함
- 과도한 로깅으로 네트워크 부하

### 2. 성능

✅ **Do:**
- 로그 배치 전송 (5-10초 간격)
- 버퍼 크기 제한 (10-50개 로그)
- 로그 레벨 필터링 (프로덕션에서는 INFO 이상만)
- 비동기 전송
- Wi-Fi에서만 전송 (모바일의 경우)

❌ **Don't:**
- 로그마다 개별 HTTP 요청
- 무제한 버퍼링 (메모리 누수 위험)
- DEBUG 로그를 프로덕션에 전송

### 3. 데이터 품질

✅ **Do:**
- 타임스탬프 포함 (ISO 8601 형식)
- 구조화된 로그 (JSON)
- 컨텍스트 정보 포함 (사용자 ID, 세션 ID, URL)
- 일관된 로그 포맷
- 버전 정보 포함

```javascript
// 좋은 로그 예시
{
  "timestamp": "2025-10-06T10:30:45.123Z",
  "level": "error",
  "message": "Failed to load user profile",
  "context": {
    "userId": "user-123",
    "sessionId": "sess-456",
    "url": "https://app.example.com/profile",
    "userAgent": "Mozilla/5.0...",
    "appVersion": "2.3.1",
    "error": {
      "name": "NetworkError",
      "message": "Failed to fetch",
      "stack": "..."
    }
  }
}
```

### 4. 비용 최적화

✅ **Do:**
- 로그 레벨 기반 샘플링
- 중요 로그만 전송 (에러, 크리티컬 이벤트)
- 로그 수명 관리 (ILM 사용)
- 압축 전송

❌ **Don't:**
- 모든 클릭/이벤트 로깅
- 대용량 페이로드 전송
- 무한정 로그 보관

### 5. 오프라인 대응

```javascript
// 오프라인 지원 예시
class OfflineAwareLogger {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
    this.offlineQueue = this.loadOfflineQueue();

    // 온라인 상태 변경 감지
    window.addEventListener('online', () => {
      this.flushOfflineQueue();
    });
  }

  log(entry) {
    if (navigator.onLine) {
      this.sendLog(entry);
    } else {
      this.queueForLater(entry);
    }
  }

  queueForLater(entry) {
    this.offlineQueue.push(entry);
    localStorage.setItem('logQueue', JSON.stringify(this.offlineQueue));
  }

  async flushOfflineQueue() {
    if (this.offlineQueue.length === 0) return;

    const queue = [...this.offlineQueue];
    this.offlineQueue = [];

    try {
      await this.sendLogs(queue);
      localStorage.removeItem('logQueue');
    } catch (error) {
      // 실패시 다시 큐에 추가
      this.offlineQueue = queue.concat(this.offlineQueue);
    }
  }

  loadOfflineQueue() {
    const saved = localStorage.getItem('logQueue');
    return saved ? JSON.parse(saved) : [];
  }
}
```

## 요약

### 핵심 원칙

1. **절대 직접 연결 금지**: 클라이언트는 ELK Stack에 직접 연결하지 않음
2. **백엔드 API 필수**: 모든 로그는 백엔드를 경유
3. **배치 전송**: 네트워크 효율성을 위해 로그를 모아서 전송
4. **보안 우선**: 민감한 정보 필터링, HTTPS, 인증
5. **성능 고려**: 배터리, 대역폭, 비용 최적화

### 다음 단계

- [Server 관점](./02-Server-관점.md)에서 백엔드와 ELK Stack 구성 방법 학습
- [컴포넌트별 상세 프로세스](./03-컴포넌트별-상세-프로세스.md)에서 각 구성 요소 심화 학습

---

**참고 자료**:
- [Best Way to Log Client-Side/Javascript in ELK - Stack Overflow](https://stackoverflow.com/questions/53089448/best-way-to-log-client-side-javascript-in-elk-logstash)
- [Options for log collection from client applications - Elastic Discuss](https://discuss.elastic.co/t/options-for-log-collection-from-client-applications/328288)
- [Best JavaScript client-side error logging services 2025](https://www.slant.co/topics/2615/~best-javascript-client-side-error-logging-services)
- [Browser Log Collection - Datadog](https://docs.datadoghq.com/logs/log_collection/javascript/)

**최종 업데이트**: 2025-10-06
