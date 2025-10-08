---
tags:
  - ELK/Server
  - Logstash
  - Pipeline
  - Kotlin
  - SpringBoot
created: 2025-10-06
updated: 2025-10-06
---

# Logstash 파이프라인 (Kotlin + Spring Boot)

> [!info] 개요
> Kotlin + Spring Boot 애플리케이션의 로그를 수집, 파싱, 처리하는 Logstash 설정

## 🏗️ 파이프라인 구조

```mermaid
graph LR
    A[Spring Boot App] -->|TCP| B[Logstash Input]
    B --> C[Filter: Grok/JSON]
    C --> D[Filter: Date]
    D --> E[Filter: Mutate]
    E --> F[Output: Elasticsearch]

    style A fill:#6db33f
    style F fill:#005571
```

---

## ⚙️ 기본 설정

### logstash.conf

```ruby
# /etc/logstash/conf.d/spring-boot.conf

input {
  # Logback TCP Appender로부터 수신
  tcp {
    port => 5000
    codec => json_lines
    type => "spring-boot-logs"
  }

  # Filebeat로부터 수신 (백업)
  beats {
    port => 5044
    type => "filebeat-logs"
  }
}

filter {
  # Spring Boot 로그만 처리
  if [type] == "spring-boot-logs" {

    # 이미 JSON이므로 별도 파싱 불필요
    # Logstash Encoder가 구조화된 JSON 전송

    # 타임스탬프 파싱
    date {
      match => [ "@timestamp", "ISO8601" ]
      target => "@timestamp"
    }

    # 필드 정리
    mutate {
      # 불필요한 필드 제거
      remove_field => [ "host", "port", "@version" ]

      # 필드명 변경 (선택)
      rename => {
        "logger_name" => "logger"
        "thread_name" => "thread"
      }

      # 애플리케이션 태그 추가
      add_tag => [ "spring-boot", "kotlin" ]
    }

    # Exception 스택 트레이스 처리
    if [stack_trace] {
      mutate {
        add_tag => [ "has_exception" ]
      }
    }

    # 로그 레벨별 태그
    if [level] == "ERROR" {
      mutate {
        add_tag => [ "error" ]
      }
    } else if [level] == "WARN" {
      mutate {
        add_tag => [ "warning" ]
      }
    }

    # GeoIP (선택)
    if [client_ip] {
      geoip {
        source => "client_ip"
        target => "geoip"
      }
    }
  }
}

output {
  # Elasticsearch로 전송
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "spring-boot-logs-%{+YYYY.MM.dd}"

    # 인증 (Elasticsearch 8.x)
    user => "elastic"
    password => "${ELASTIC_PASSWORD}"

    # ILM 사용
    ilm_enabled => true
    ilm_rollover_alias => "spring-boot-logs"
    ilm_pattern => "000001"
    ilm_policy => "spring-boot-logs-policy"
  }

  # 디버깅용 (개발 환경)
  if [level] == "ERROR" {
    stdout {
      codec => rubydebug
    }
  }
}
```

---

## 📝 Filter 플러그인 상세

### 1. JSON Filter

Logback Logstash Encoder가 이미 JSON을 전송하므로 대부분 불필요하지만, 일반 파일에서 읽는 경우:

```ruby
filter {
  # JSON 파싱 (Filebeat에서 수집한 경우)
  if [type] == "filebeat-logs" {
    json {
      source => "message"
      target => "parsed"
    }

    # 파싱된 필드를 루트로 이동
    mutate {
      rename => {
        "[parsed][level]" => "level"
        "[parsed][message]" => "log_message"
        "[parsed][logger_name]" => "logger"
      }
    }
  }
}
```

### 2. Grok Filter (일반 로그 파일용)

```ruby
filter {
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{NUMBER:pid} --- \[%{DATA:thread}\] %{DATA:logger} : %{GREEDYDATA:log_message}"
    }
  }

  # Spring Boot 기본 로그 패턴
  # 2025-10-06 10:30:45.123 INFO 12345 --- [nio-8080-exec-1] c.e.m.UserController : User login
}
```

### 3. MDC 필드 추출

```ruby
filter {
  # MDC 필드가 루트에 있는 경우
  if [requestId] {
    mutate {
      add_field => { "request_id" => "%{requestId}" }
      remove_field => [ "requestId" ]
    }
  }

  if [userId] {
    mutate {
      add_field => { "user_id" => "%{userId}" }
      remove_field => [ "userId" ]
    }
  }
}
```

### 4. Exception 처리

```ruby
filter {
  # 스택 트레이스 해시 생성 (중복 제거용)
  if [stack_trace] {
    fingerprint {
      source => ["stack_trace"]
      target => "exception_fingerprint"
      method => "MD5"
    }
  }

  # Exception 타입 추출
  if [thrown][message] {
    mutate {
      add_field => {
        "exception_message" => "%{[thrown][message]}"
        "exception_class" => "%{[thrown][exception_class]}"
      }
    }
  }
}
```

---

## 🔄 멀티 파이프라인

### pipelines.yml

```yaml
# /etc/logstash/pipelines.yml

# Spring Boot 로그 파이프라인
- pipeline.id: spring-boot-logs
  path.config: "/etc/logstash/conf.d/spring-boot.conf"
  pipeline.workers: 2
  pipeline.batch.size: 125

# Actuator 메트릭 파이프라인
- pipeline.id: spring-boot-metrics
  path.config: "/etc/logstash/conf.d/spring-boot-metrics.conf"
  pipeline.workers: 1
  pipeline.batch.size: 50
```

### spring-boot-metrics.conf

```ruby
input {
  http {
    port => 8080
    codec => json
    type => "actuator-metrics"
  }
}

filter {
  if [type] == "actuator-metrics" {
    # 메트릭 처리
    mutate {
      add_tag => [ "metrics", "actuator" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "spring-boot-metrics-%{+YYYY.MM.dd}"
  }
}
```

---

## 📊 로그 샘플 데이터

### Logback Encoder에서 전송되는 JSON

```json
{
  "@timestamp": "2025-10-06T10:30:45.123+09:00",
  "level": "INFO",
  "logger_name": "com.example.myapp.controller.UserController",
  "thread_name": "http-nio-8080-exec-1",
  "message": "User login successful",
  "app_name": "user-service",
  "profile": "production",
  "instance": "server-01",
  "requestId": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "userId": "user-123",
  "sessionId": "SESSION-456",
  "level_value": 20000,
  "stack_trace": null
}
```

### Elasticsearch에 저장되는 형태

```json
{
  "@timestamp": "2025-10-06T01:30:45.123Z",
  "level": "INFO",
  "logger": "com.example.myapp.controller.UserController",
  "thread": "http-nio-8080-exec-1",
  "message": "User login successful",
  "app_name": "user-service",
  "profile": "production",
  "instance": "server-01",
  "request_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "user_id": "user-123",
  "session_id": "SESSION-456",
  "tags": ["spring-boot", "kotlin"]
}
```

---

## ⚡ 성능 튜닝

### logstash.yml

```yaml
# /etc/logstash/logstash.yml

# 파이프라인 설정
pipeline.workers: 4  # CPU 코어 수와 동일
pipeline.batch.size: 125
pipeline.batch.delay: 50

# 큐 설정
queue.type: persisted
queue.max_bytes: 1gb
path.queue: /var/lib/logstash/queue

# JVM 설정
# /etc/logstash/jvm.options
-Xms2g
-Xmx2g
```

---

## 🧪 테스트

### 로컬 테스트

```bash
# Logstash 설정 파일 테스트
/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/spring-boot.conf --config.test_and_exit

# 샘플 데이터로 테스트
echo '{"@timestamp":"2025-10-06T10:30:45.123Z","level":"INFO","message":"Test log"}' | \
  nc localhost 5000
```

### Logstash 디버깅

```bash
# stdout으로 출력하여 확인
output {
  stdout {
    codec => rubydebug
  }
}

# 로그 확인
tail -f /var/log/logstash/logstash-plain.log
```

---

## 🔗 관련 문서

- [[README|← Server 관점 개요]]
- [[../01-Client/01-Kotlin-SpringBoot-로깅-설정|← Kotlin 로깅 설정]]
- [[03-Elasticsearch-설치-및-구성|Elasticsearch 설치 →]]

---

## 📚 참고 자료

- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Logstash Configuration Examples](https://www.elastic.co/guide/en/logstash/current/config-examples.html)
- [Logstash Filter Plugins](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html)

---

#ELK/Server #Logstash #Pipeline #Kotlin #SpringBoot
