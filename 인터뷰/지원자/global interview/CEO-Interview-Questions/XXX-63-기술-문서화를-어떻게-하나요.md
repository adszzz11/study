# 기술 문서화를 어떻게 접근하나요

## English Question

**How do you approach technical documentation?**

## 질문 번역

기술 문서화를 어떻게 접근하나요?

---

## English Answer

Documentation was core to my role at Danal—I led "Danal Crafters," our technical writing community.

**My Documentation Philosophy:**

**1. Documentation as Product**
Treat docs like code:
- Version controlled
- Reviewed and maintained
- Tested (do the examples actually work?)
- User-focused

**2. Right Level for Right Audience**

| Type | Audience | Purpose |
|------|----------|---------|
| README | New developers | Quick start |
| API docs | Integrators | Reference |
| Architecture docs | Team | Understanding |
| Runbooks | Ops | Problem-solving |
| ADRs | Future us | Decision history |

**3. Write at the Point of Work**
- Document as you build, not after
- If you struggled to understand something, document it
- If you answered the same question twice, write it down

**4. Keep It Alive**
Dead documentation is worse than no documentation:
- Review docs during code reviews
- Scheduled documentation audits
- Delete outdated docs

**What I Built at Danal:**

- Payment API documentation for external merchants
- Internal onboarding guides for new engineers
- Architecture decision records (ADRs)
- Incident postmortem templates

**For Zonagent:**
Early-stage startup means documentation can slip. But a few key docs make huge difference:
- System architecture overview
- Local development setup
- Deployment process
- Key decision history

I'd prioritize docs that accelerate onboarding and reduce bus factor.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟡 50% - 물어볼 수도 있음 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- "Danal Crafters" 리더십 경험
- 문서화 = 제품 철학
- 스타트업 맥락 이해 ("docs can slip")

**Aaron이 좋아할 부분:**
- "Accelerate onboarding" - 스케일링 중요
- "Reduce bus factor" - 리스크 관리
- 청중별 문서 구분

**중요:**
- 문서화는 비기술자도 이해하는 가치
- 팀 성장에 필수

**팁:**
- Aaron에게 "onboarding 가속화"와 "리스크 감소" 강조

---

## 한글 번역

문서화는 다날에서 제 역할의 핵심이었습니다—기술 글쓰기 커뮤니티인 "Danal Crafters"를 이끌었습니다.

**제 문서화 철학:**

**1. 제품으로서의 문서화**
문서를 코드처럼 취급:
- 버전 관리
- 리뷰 및 유지보수
- 테스트 (예제가 실제로 작동하나?)
- 사용자 중심

**2. 적절한 청중에게 적절한 수준**

| 유형 | 청중 | 목적 |
|------|------|------|
| README | 새 개발자 | 빠른 시작 |
| API 문서 | 통합자 | 참조 |
| 아키텍처 문서 | 팀 | 이해 |
| 런북 | 운영 | 문제 해결 |
| ADR | 미래의 우리 | 결정 이력 |

**3. 작업 시점에 작성**
- 나중이 아니라 만들면서 문서화
- 이해하기 어려웠다면 문서화
- 같은 질문에 두 번 답했다면 적어두기

**4. 살아있게 유지**
죽은 문서화는 문서화가 없는 것보다 나쁨:
- 코드 리뷰 중 문서 검토
- 예정된 문서화 감사
- 오래된 문서 삭제

**다날에서 만든 것:**

- 외부 가맹점용 결제 API 문서
- 새 엔지니어를 위한 내부 온보딩 가이드
- 아키텍처 결정 기록 (ADR)
- 인시던트 포스트모템 템플릿

**Zonagent의 경우:**
초기 단계 스타트업은 문서화가 밀릴 수 있습니다. 하지만 몇 가지 핵심 문서가 큰 차이를 만듭니다:
- 시스템 아키텍처 개요
- 로컬 개발 설정
- 배포 프로세스
- 핵심 결정 이력

온보딩을 가속하고 버스 팩터를 줄이는 문서를 우선시할 것입니다.
