# 성능 최적화 경험을 말해주세요

## English Question

**Tell me about a time you optimized system performance.**

## 질문 번역

성능 최적화 경험을 말해주세요.

---

## English Answer

Here's a significant one from Danal.

**The Problem:**
Our payment authorization latency was creeping up. P99 went from 150ms to 400ms over several months. Merchants started complaining.

**Discovery Phase:**

**1. Measure Everything**
- Added detailed timing to each step
- Built a flame graph of the full request path
- Identified: database queries were the main culprit

**2. Root Cause Analysis**
Not one big problem, but several:
- N+1 queries in merchant validation
- Missing indexes on frequently-queried columns
- Connection pool exhaustion under load
- Unnecessary data fetched (SELECT *)

**Optimization Actions:**

**1. Query Optimization**
- Batch queries to eliminate N+1
- Added compound indexes for common query patterns
- Switched to column-specific SELECTs

**2. Caching**
- Added Redis cache for merchant config (rarely changes)
- Cache hit rate: 95%+ for hot data
- Reduced database load by 60%

**3. Connection Management**
- Tuned connection pool size
- Added connection pooler (PgBouncer)
- Reduced connection overhead

**4. Architecture Change**
- Moved expensive validation to async
- Only critical path remains synchronous
- Precomputed frequently-accessed data

**Results:**
- P99 latency: 400ms → 120ms
- Database load: reduced 60%
- Throughput: increased 40%

**What I Learned:**
Optimization is about measurement first. Don't guess—profile. The obvious bottleneck is often not the real one.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟢 35% - 낮은 확률 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 구체적 숫자 (P99 400ms → 120ms, 60% 부하 감소)
- 체계적 접근 (발견, 분석, 조치, 결과)
- 4가지 최적화 영역

**주의:**
- 매우 기술적 - Mark Jung 면접용
- Aaron은 질문하지 않을 것

**Aaron 버전:**
> "결제 지연을 400ms에서 120ms로 줄이고 처리량을 40% 증가시켰습니다. 측정 먼저, 추측 금지가 원칙입니다."

**핵심 문구:**
> "Don't guess—profile."

---

## 한글 번역

다날에서 중요한 것 하나입니다.

**문제:**
결제 승인 지연이 증가하고 있었습니다. P99가 몇 달에 걸쳐 150ms에서 400ms로. 가맹점들이 불평하기 시작.

**발견 단계:**

**1. 모든 것 측정**
- 각 단계에 상세 타이밍 추가
- 전체 요청 경로의 플레임 그래프 구축
- 식별: 데이터베이스 쿼리가 주 원인

**2. 근본 원인 분석**
하나의 큰 문제가 아닌 여러 개:
- 가맹점 검증에서 N+1 쿼리
- 자주 쿼리되는 컬럼에 누락된 인덱스
- 부하에서 커넥션 풀 고갈
- 불필요한 데이터 페치 (SELECT *)

**최적화 조치:**

**1. 쿼리 최적화**
- N+1 제거를 위한 배치 쿼리
- 일반적인 쿼리 패턴에 복합 인덱스 추가
- 컬럼 특정 SELECT로 전환

**2. 캐싱**
- 가맹점 설정에 Redis 캐시 추가 (거의 변경 안 됨)
- 핫 데이터에 캐시 히트율: 95%+
- 데이터베이스 부하 60% 감소

**3. 커넥션 관리**
- 커넥션 풀 크기 튜닝
- 커넥션 풀러 추가 (PgBouncer)
- 커넥션 오버헤드 감소

**4. 아키텍처 변경**
- 비싼 검증을 비동기로 이동
- 중요 경로만 동기로 유지
- 자주 접근되는 데이터 사전 계산

**결과:**
- P99 지연: 400ms → 120ms
- 데이터베이스 부하: 60% 감소
- 처리량: 40% 증가

**배운 것:**
최적화는 먼저 측정입니다. 추측하지 말고 프로파일. 명백한 병목은 종종 진짜가 아닙니다.
