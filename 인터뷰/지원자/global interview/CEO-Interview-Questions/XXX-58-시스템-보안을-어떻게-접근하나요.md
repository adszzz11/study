# 시스템 보안을 어떻게 접근하나요

## English Question

**How do you approach system security in your development work?**

## 질문 번역

개발 작업에서 시스템 보안을 어떻게 접근하나요?

---

## English Answer

Working in payments, security wasn't optional—it was regulated. PCI-DSS compliance shaped my security mindset.

**Layers of Security I Apply:**

**1. Application Security**
- Input validation on all external data
- Parameterized queries (never string concatenation for SQL)
- Output encoding to prevent XSS
- CSRF protection on state-changing operations
- Dependency scanning for known vulnerabilities

**2. Authentication & Authorization**
- Token-based auth with proper expiration
- Role-based access control (RBAC)
- Principle of least privilege
- Audit logging for sensitive operations

**3. Data Protection**
- Encryption at rest and in transit
- Sensitive data masking in logs
- Secure credential management (never in code)
- Data retention policies

**4. Infrastructure Security**
- Network segmentation (public/private subnets)
- Security groups as whitelist, not blacklist
- Regular patching and updates
- Immutable infrastructure where possible

**5. Operational Security**
- Secrets rotation
- Access reviews
- Incident response procedures
- Security monitoring and alerting

**For Zonagent:**
You're handling municipal data—some might be public, but your customers' strategies are definitely sensitive. I'd want to understand:
- What data is most sensitive?
- Who needs access to what?
- What are the compliance requirements?

Then build security into the architecture from the start, not bolted on later.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟢 35% - 낮은 확률 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- PCI-DSS 경험 - 높은 보안 기준
- 5개 레이어 체계적 접근
- Zonagent 고객 데이터 보안 언급

**Aaron이 좋아할 부분:**
- 결제 = 민감한 데이터 경험
- "Build security from the start" - 올바른 마인드셋
- 고객 전략 보호 이해

**주의:**
- 기술 용어가 많음 (RBAC, CSRF 등)
- Aaron보다 Mark 면접용

**Aaron 버전:**
> "결제 시스템에서 PCI-DSS 준수로 보안을 배웠고, 처음부터 보안을 아키텍처에 구축합니다."

---

## 한글 번역

결제 분야에서 일하면서 보안은 선택이 아니라 규제였습니다. PCI-DSS 준수가 제 보안 마인드셋을 형성했습니다.

**적용하는 보안 레이어:**

**1. 애플리케이션 보안**
- 모든 외부 데이터에 입력 검증
- 파라미터화된 쿼리 (SQL에 문자열 연결 절대 금지)
- XSS 방지를 위한 출력 인코딩
- 상태 변경 작업에 CSRF 보호
- 알려진 취약점에 대한 의존성 스캔

**2. 인증 & 권한 부여**
- 적절한 만료와 함께 토큰 기반 인증
- 역할 기반 액세스 제어 (RBAC)
- 최소 권한 원칙
- 민감한 작업에 감사 로깅

**3. 데이터 보호**
- 저장 및 전송 중 암호화
- 로그에서 민감한 데이터 마스킹
- 안전한 자격 증명 관리 (코드에 절대 포함 금지)
- 데이터 보존 정책

**4. 인프라 보안**
- 네트워크 세분화 (퍼블릭/프라이빗 서브넷)
- 블랙리스트가 아닌 화이트리스트로서의 보안 그룹
- 정기적 패칭과 업데이트
- 가능한 곳에서 불변 인프라

**5. 운영 보안**
- 시크릿 로테이션
- 액세스 리뷰
- 인시던트 대응 절차
- 보안 모니터링과 알림

**Zonagent의 경우:**
지자체 데이터를 다룹니다—일부는 공개일 수 있지만 고객의 전략은 분명히 민감합니다. 이해하고 싶은 것:
- 어떤 데이터가 가장 민감한지?
- 누가 무엇에 접근해야 하는지?
- 컴플라이언스 요구사항은 무엇인지?

그런 다음 나중에 덧붙이는 것이 아니라 처음부터 아키텍처에 보안을 구축합니다.
