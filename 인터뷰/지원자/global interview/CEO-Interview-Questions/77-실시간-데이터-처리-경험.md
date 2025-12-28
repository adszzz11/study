# 실시간 데이터 처리 경험을 설명해주세요

## English Question

**What's your experience with real-time data processing systems?**

## 질문 번역

실시간 데이터 처리 경험을 설명해주세요.

---

## English Answer

At Danal, real-time processing wasn't optional—payment authorization must happen in milliseconds.

**What I Built:**

**1. Transaction Processing Pipeline**
- 100K+ transactions per minute
- P99 latency under 200ms
- Zero tolerance for data loss

**Architecture:**
```
Request → Load Balancer → API Gateway → Service Mesh → Database
              ↓                              ↓
         Rate Limiting              Event Stream (Kafka)
                                           ↓
                                    Real-time Analytics
```

**2. Key Technologies Used:**
- **Kafka**: Event streaming backbone
- **Redis**: Sub-millisecond caching
- **Kubernetes**: Auto-scaling for traffic spikes
- **gRPC**: Low-latency inter-service communication

**3. Real-time Monitoring:**
- Live dashboards showing TPS, latency, error rates
- Anomaly detection for fraud patterns
- Alerting within seconds of issues

**Lessons Learned:**

**Backpressure Handling:**
When downstream can't keep up, you need to:
- Buffer intelligently
- Drop or delay non-critical work
- Alert before things break

**Exactly-Once Processing:**
- Idempotency keys for deduplication
- Transactional outbox pattern
- Careful ordering guarantees

**Graceful Degradation:**
- Fallback paths when systems fail
- Circuit breakers to prevent cascading failures
- Cached responses when source is unavailable

**For Zonagent:**
While your primary use case is batch processing (scraping municipalities), real-time matters for:
- Alerting when important documents appear
- Dashboard updates
- API responses to customers

The principles transfer directly.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟢 25% - 낮은 확률 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 100K+ TPS, P99 200ms - 인상적인 숫자
- 결제 = 실시간 필수의 명확한 예
- 3가지 교훈 (백프레셔, 멱등성, 우아한 저하)

**주의:**
- 매우 기술적 - Mark Jung 면접용
- Aaron은 질문하지 않을 것

**Zonagent 연결:**
- "Alerting when important documents appear" - 비즈니스 가치 연결

**Aaron 버전:**
> "분당 10만 건 실시간 결제 처리 경험이 있어서, 중요 문서 알림 같은 기능에 적용할 수 있습니다."

---

## 한글 번역

다날에서 실시간 처리는 선택이 아니었습니다—결제 승인은 밀리초 내에 이루어져야 합니다.

**구축한 것:**

**1. 트랜잭션 처리 파이프라인**
- 분당 10만 건 이상의 트랜잭션
- P99 지연 시간 200ms 미만
- 데이터 손실 무관용

**아키텍처:**
```
요청 → 로드 밸런서 → API 게이트웨이 → 서비스 메시 → 데이터베이스
           ↓                              ↓
       속도 제한                이벤트 스트림 (Kafka)
                                        ↓
                                 실시간 분석
```

**2. 사용한 핵심 기술:**
- **Kafka**: 이벤트 스트리밍 백본
- **Redis**: 서브 밀리초 캐싱
- **Kubernetes**: 트래픽 스파이크용 오토스케일링
- **gRPC**: 저지연 서비스 간 통신

**3. 실시간 모니터링:**
- TPS, 지연 시간, 오류율을 보여주는 라이브 대시보드
- 사기 패턴을 위한 이상 탐지
- 문제 발생 몇 초 내에 알림

**배운 교훈:**

**백프레셔 처리:**
다운스트림이 따라가지 못할 때 필요한 것:
- 지능적 버퍼링
- 비중요 작업 드롭 또는 지연
- 문제 전에 알림

**정확히 한 번 처리:**
- 중복 제거를 위한 멱등성 키
- 트랜잭셔널 아웃박스 패턴
- 신중한 순서 보장

**우아한 성능 저하:**
- 시스템 실패 시 폴백 경로
- 연쇄 실패 방지를 위한 서킷 브레이커
- 소스 불가 시 캐시된 응답

**Zonagent의 경우:**
주요 사용 사례가 배치 처리 (지자체 스크래핑)이지만 실시간이 중요한 경우:
- 중요 문서 등장 시 알림
- 대시보드 업데이트
- 고객에게 API 응답

원칙이 직접 전이됩니다.
