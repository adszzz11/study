---
tags:
  - ELK/Client
  - SpringBoot
  - Actuator
  - Micrometer
  - Metrics
created: 2025-10-06
updated: 2025-10-06
---

# Spring Actuator & Metrics

> [!info] 개요
> Spring Boot Actuator와 Micrometer를 활용한 메트릭 수집 및 모니터링

## 📦 의존성

```kotlin
dependencies {
    // Spring Boot Actuator
    implementation("org.springframework.boot:spring-boot-starter-actuator")

    // Micrometer Elasticsearch Registry
    implementation("io.micrometer:micrometer-registry-elastic:1.12.0")

    // Micrometer Prometheus (선택)
    implementation("io.micrometer:micrometer-registry-prometheus")
}
```

---

## ⚙️ Actuator 설정

### application.yml

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,loggers,prometheus
      base-path: /actuator

  endpoint:
    health:
      show-details: always
      probes:
        enabled: true  # Kubernetes 용

    metrics:
      enabled: true

    loggers:
      enabled: true  # 런타임 로그 레벨 변경

  metrics:
    export:
      elasticsearch:
        enabled: true
        host: http://localhost:9200
        index: metrics
        step: 1m  # 1분마다 전송

    tags:
      application: ${spring.application.name}
      environment: ${spring.profiles.active}
```

---

## 📊 커스텀 메트릭

### 카운터 (Counter)

```kotlin
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Tags
import org.springframework.stereotype.Service

@Service
class OrderService(
    private val meterRegistry: MeterRegistry
) {

    fun createOrder(order: Order): Order {
        // 주문 생성 카운터
        meterRegistry.counter(
            "orders.created",
            Tags.of(
                "status", "success",
                "payment_method", order.paymentMethod
            )
        ).increment()

        return orderRepository.save(order)
    }

    fun cancelOrder(orderId: Long) {
        meterRegistry.counter(
            "orders.cancelled"
        ).increment()
    }
}
```

### 타이머 (Timer)

```kotlin
@Service
class PaymentService(
    private val meterRegistry: MeterRegistry
) {

    fun processPayment(orderId: Long, amount: BigDecimal) {
        meterRegistry.timer(
            "payment.process.duration",
            Tags.of("method", "credit_card")
        ).record {
            // 실제 결제 처리 로직
            paymentGateway.process(orderId, amount)
        }
    }
}
```

### 게이지 (Gauge)

```kotlin
@Component
class OrderMetrics(
    private val orderRepository: OrderRepository,
    meterRegistry: MeterRegistry
) {

    init {
        // 실시간 pending 주문 수
        Gauge.builder("orders.pending.count") {
            orderRepository.countByStatus(OrderStatus.PENDING).toDouble()
        }
            .tag("status", "pending")
            .register(meterRegistry)

        // 활성 사용자 수
        Gauge.builder("users.active.count") {
            userService.getActiveUsersCount().toDouble()
        }
            .register(meterRegistry)
    }
}
```

---

## 🏥 헬스체크

### 커스텀 Health Indicator

```kotlin
import org.springframework.boot.actuate.health.Health
import org.springframework.boot.actuate.health.HealthIndicator
import org.springframework.stereotype.Component

@Component
class DatabaseHealthIndicator(
    private val dataSource: DataSource
) : HealthIndicator {

    override fun health(): Health {
        return try {
            dataSource.connection.use { conn ->
                val isValid = conn.isValid(1)

                if (isValid) {
                    Health.up()
                        .withDetail("database", "PostgreSQL")
                        .withDetail("validConnection", true)
                        .build()
                } else {
                    Health.down()
                        .withDetail("error", "Invalid connection")
                        .build()
                }
            }
        } catch (e: Exception) {
            Health.down()
                .withDetail("error", e.message)
                .withException(e)
                .build()
        }
    }
}

@Component
class ExternalApiHealthIndicator(
    private val restTemplate: RestTemplate
) : HealthIndicator {

    override fun health(): Health {
        return try {
            val response = restTemplate.getForEntity(
                "https://api.example.com/health",
                String::class.java
            )

            if (response.statusCode.is2xxSuccessful) {
                Health.up()
                    .withDetail("api", "external-api")
                    .withDetail("status", "available")
                    .build()
            } else {
                Health.down()
                    .withDetail("status", response.statusCode)
                    .build()
            }
        } catch (e: Exception) {
            Health.down()
                .withDetail("error", e.message)
                .build()
        }
    }
}
```

---

## 📈 주요 엔드포인트

| 엔드포인트 | 설명 | 예시 |
|-----------|------|------|
| `/actuator/health` | 헬스체크 | `{"status": "UP"}` |
| `/actuator/metrics` | 사용 가능한 메트릭 목록 | - |
| `/actuator/metrics/{name}` | 특정 메트릭 상세 | `jvm.memory.used` |
| `/actuator/loggers` | 로거 목록 및 레벨 | - |
| `/actuator/loggers/{name}` | 특정 로거 조회/변경 | - |
| `/actuator/info` | 애플리케이션 정보 | 버전, 빌드 정보 |

### 런타임 로그 레벨 변경

```bash
# 현재 로그 레벨 조회
curl http://localhost:8080/actuator/loggers/com.example.myapp

# 로그 레벨 변경
curl -X POST \
  http://localhost:8080/actuator/loggers/com.example.myapp \
  -H 'Content-Type: application/json' \
  -d '{"configuredLevel": "DEBUG"}'
```

---

## 🔗 관련 문서

- [[01-Kotlin-SpringBoot-로깅-설정|← Kotlin 로깅 설정]]
- [[03-Kotlin-로깅-Best-Practices|Best Practices →]]

---

#ELK/Client #SpringBoot #Actuator #Metrics #Micrometer
