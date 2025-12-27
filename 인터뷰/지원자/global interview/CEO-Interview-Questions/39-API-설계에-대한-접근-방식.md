# API 설계에 대한 접근 방식이 어떻게 되나요

## English Question

**What's your approach to API design?**

## 질문 번역

API 설계에 대한 접근 방식이 어떻게 되나요?

---

## English Answer

I follow a set of principles that I've developed through building APIs consumed by both internal teams and external partners:

**1. Consumer-First Design**
Start with the question: "What does the caller actually need?"
- Don't expose internal implementation details
- Provide exactly the data needed, not everything you have
- Make common use cases easy, edge cases possible

**2. Consistency**
- Consistent naming conventions across all endpoints
- Standard error response format
- Predictable pagination, filtering, and sorting patterns
- Versioning strategy from day one

**3. Documentation as First-Class Citizen**
- OpenAPI/Swagger specs maintained alongside code
- Examples for every endpoint
- Clear error code explanations
- Changelog for breaking changes

**4. Reliability**
- Idempotency for mutating operations
- Graceful degradation when dependencies fail
- Rate limiting to protect the system
- Meaningful HTTP status codes

**5. Observability**
- Request tracing across services
- Latency monitoring per endpoint
- Error rate tracking
- Usage analytics to understand real consumption patterns

**In Practice:**
At Danal, I designed APIs consumed by hundreds of merchants. When you can't fix every consumer's integration, you learn to make APIs that are hard to misuse. Clear contracts, helpful error messages, and predictable behavior.

---

## 한글 번역

내부 팀과 외부 파트너 모두가 사용하는 API를 구축하면서 개발한 원칙을 따릅니다:

**1. 소비자 우선 설계**
질문으로 시작합니다: "호출자가 실제로 필요한 것은 무엇인가?"
- 내부 구현 세부사항을 노출하지 않음
- 가진 모든 것이 아닌 정확히 필요한 데이터 제공
- 일반적인 사용 사례는 쉽게, 엣지 케이스는 가능하게

**2. 일관성**
- 모든 엔드포인트에서 일관된 명명 규칙
- 표준 오류 응답 형식
- 예측 가능한 페이지네이션, 필터링, 정렬 패턴
- 첫날부터 버전 관리 전략

**3. 문서화를 일급 시민으로**
- 코드와 함께 유지되는 OpenAPI/Swagger 스펙
- 모든 엔드포인트에 대한 예제
- 명확한 오류 코드 설명
- 브레이킹 체인지에 대한 변경 로그

**4. 신뢰성**
- 변경 작업에 대한 멱등성
- 의존성 실패 시 우아한 저하
- 시스템 보호를 위한 속도 제한
- 의미 있는 HTTP 상태 코드

**5. 관찰 가능성**
- 서비스 간 요청 추적
- 엔드포인트별 지연 모니터링
- 오류율 추적
- 실제 소비 패턴을 이해하기 위한 사용 분석

**실제로:**
다날에서 수백 개의 가맹점이 사용하는 API를 설계했습니다. 모든 소비자의 통합을 수정할 수 없을 때, 잘못 사용하기 어려운 API를 만드는 법을 배웁니다. 명확한 계약, 도움이 되는 오류 메시지, 예측 가능한 동작.
