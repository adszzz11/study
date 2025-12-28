# 여러 시스템을 통합한 경험이 있나요

## English Question

**Tell me about your experience integrating multiple systems.**

## 질문 번역

여러 시스템을 통합한 경험을 말해주세요.

---

## English Answer

At Danal, integration was our core business. We connected merchants, banks, card networks, and internal systems.

**Scale of Integration:**
- 50+ external merchant integrations
- 10+ bank and payment network connections
- Internal microservices ecosystem

**What I Built:**

**1. Merchant Integration Framework**
- Standardized onboarding process
- Common SDK for merchant developers
- Webhook system for async notifications
- Sandbox environment for testing

**2. Bank/Card Network Connections**
- Each with different protocols (REST, SOAP, ISO 8583)
- Translation layers to normalize data formats
- Retry logic for unreliable connections
- Monitoring for SLA compliance

**Key Lessons:**

**1. Don't Trust External Systems**
- They will timeout
- They will send malformed data
- They will change without notice
- Build defensive code

**2. Idempotency is Critical**
- Networks fail; requests retry
- Every operation must be safely repeatable
- Idempotency keys for financial transactions

**3. Observability**
- Log every external call
- Track latency, error rates per integration
- Alert on degradation before failure

**4. Contract Testing**
- Document expected behavior
- Test that expectations match reality
- Consumer-driven contracts when possible

**For Zonagent:**
You're integrating with thousands of municipal data sources. Each is essentially a different "system" with different formats. The patterns I learned apply:
- Normalize at the boundary
- Expect sources to change
- Monitor each source independently
- Build robust error handling

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟡 55% - 물어볼 수도 있음 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 대규모 통합 경험 (50+ 가맹점, 10+ 은행)
- 4가지 핵심 교훈 (신뢰 안 함, 멱등성, 관측성, 계약)
- Zonagent 맥락 직접 연결

**Aaron이 좋아할 부분:**
- Zonagent 핵심 문제와 직결
- "Thousands of municipal data sources" 이해
- 경계에서 정규화 - 비즈니스 문제 해결

**중요:**
- ETL/데이터 수집 질문과 연결
- Zonagent 핵심 역량과 일치

**Aaron 버전:**
> "50개 이상 가맹점, 10개 은행과 통합한 경험이 있어서 수천 지자체 데이터 소스 통합에도 같은 패턴을 적용합니다."

---

## 한글 번역

다날에서 통합은 핵심 비즈니스였습니다. 가맹점, 은행, 카드 네트워크, 내부 시스템을 연결했습니다.

**통합 규모:**
- 50개 이상의 외부 가맹점 통합
- 10개 이상의 은행 및 결제 네트워크 연결
- 내부 마이크로서비스 생태계

**구축한 것:**

**1. 가맹점 통합 프레임워크**
- 표준화된 온보딩 프로세스
- 가맹점 개발자를 위한 공통 SDK
- 비동기 알림을 위한 웹훅 시스템
- 테스트를 위한 샌드박스 환경

**2. 은행/카드 네트워크 연결**
- 각각 다른 프로토콜 (REST, SOAP, ISO 8583)
- 데이터 형식 정규화를 위한 변환 레이어
- 신뢰할 수 없는 연결을 위한 재시도 로직
- SLA 준수를 위한 모니터링

**핵심 교훈:**

**1. 외부 시스템 신뢰하지 않기**
- 타임아웃할 것
- 잘못된 데이터 보낼 것
- 통보 없이 변경할 것
- 방어적 코드 구축

**2. 멱등성이 중요**
- 네트워크 실패; 요청 재시도
- 모든 작업은 안전하게 반복 가능해야
- 금융 거래에 멱등성 키

**3. 관측성**
- 모든 외부 호출 로깅
- 통합별 지연 시간, 오류율 추적
- 실패 전 성능 저하에 알림

**4. 계약 테스트**
- 예상 동작 문서화
- 기대가 현실과 일치하는지 테스트
- 가능하면 소비자 주도 계약

**Zonagent의 경우:**
수천 개의 지자체 데이터 소스와 통합합니다. 각각은 본질적으로 다른 형식을 가진 다른 "시스템"입니다. 배운 패턴이 적용됩니다:
- 경계에서 정규화
- 소스 변경 예상
- 각 소스 독립적으로 모니터링
- 견고한 오류 처리 구축
