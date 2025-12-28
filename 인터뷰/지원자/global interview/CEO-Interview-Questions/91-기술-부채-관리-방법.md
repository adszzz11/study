# 기술 부채를 어떻게 관리하나요

## English Question

**How do you manage technical debt?**

## 질문 번역

기술 부채를 어떻게 관리하나요?

---

## English Answer

Technical debt is inevitable. The question is whether you manage it intentionally or let it accumulate accidentally.

**My Framework:**

**1. Track It Explicitly**
- Maintain a tech debt backlog (separate from features)
- Each item has: description, impact, effort estimate
- Review quarterly: is this getting better or worse?

**2. Categorize by Type**

| Type | Example | Priority |
|------|---------|----------|
| **Safety** | Security vulnerabilities | Immediate |
| **Velocity** | Slow builds, flaky tests | High |
| **Scalability** | Won't handle 10x load | Plan ahead |
| **Maintenance** | Outdated dependencies | Scheduled |
| **Cosmetic** | Inconsistent naming | When convenient |

**3. Pay It Down Continuously**
- 20% of sprint capacity for debt reduction
- Every PR should leave code slightly better
- "Boy Scout Rule": leave the campground cleaner than you found it

**4. Make Trade-offs Visible**
When taking on new debt:
- "We can ship faster if we skip X, but we'll need to address it within Y weeks"
- Document the decision
- Set a calendar reminder to revisit

**5. Prevent Where Possible**
- Code review catches debt before it merges
- Linting and automated checks
- Architecture discussions before building

**At Danal:**
We had decades of accumulated debt. I couldn't fix it all, but I:
- Prioritized debt that caused actual incidents
- Made progress visible to leadership
- Built team habits around continuous improvement

**For Startups:**
Some debt is fine—you're optimizing for learning, not perfection. But safety and velocity debt should be addressed quickly.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟡 50% - 물어볼 수도 있음 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 5단계 체계적 프레임워크
- 유형별 분류표 - 명확한 우선순위
- "20% sprint capacity for debt" - 구체적
- 스타트업 맥락 이해

**Aaron이 좋아할 부분:**
- "Some debt is fine" - 스타트업 현실적
- "Safety and velocity debt" 구분
- 비즈니스와 기술 균형

**중요:**
- 45번과 비슷하지만 더 체계적
- 스타트업 CEO가 관심 가질 수 있는 주제

**핵심 문구:**
> "You're optimizing for learning, not perfection."

---

## 한글 번역

기술 부채는 불가피합니다. 문제는 의도적으로 관리하느냐 우연히 축적되게 두느냐입니다.

**제 프레임워크:**

**1. 명시적으로 추적**
- 기술 부채 백로그 유지 (기능과 별도)
- 각 항목: 설명, 영향, 노력 추정
- 분기별 리뷰: 나아지고 있나 나빠지고 있나?

**2. 유형별 분류**

| 유형 | 예시 | 우선순위 |
|------|------|---------|
| **안전** | 보안 취약점 | 즉시 |
| **속도** | 느린 빌드, 불안정한 테스트 | 높음 |
| **확장성** | 10배 부하 처리 못함 | 미리 계획 |
| **유지보수** | 오래된 의존성 | 예정됨 |
| **외관** | 일관성 없는 네이밍 | 편할 때 |

**3. 지속적으로 상환**
- 부채 감소에 스프린트 용량의 20%
- 모든 PR은 코드를 약간 더 좋게 남겨야
- "보이스카웃 규칙": 캠프장을 발견했을 때보다 더 깨끗하게 남기기

**4. 트레이드오프 가시화**
새 부채를 질 때:
- "X를 건너뛰면 더 빨리 출시할 수 있지만 Y주 내에 해결해야 함"
- 결정 문서화
- 재검토하기 위해 캘린더 알림 설정

**5. 가능한 곳에서 예방**
- 코드 리뷰가 병합 전 부채 포착
- 린팅과 자동화된 검사
- 구축 전 아키텍처 토론

**다날에서:**
수십 년의 축적된 부채가 있었습니다. 전부 고칠 수 없었지만:
- 실제 인시던트를 야기한 부채 우선순위
- 진전을 리더십에 가시화
- 지속적 개선 주변에 팀 습관 구축

**스타트업의 경우:**
일부 부채는 괜찮습니다—완벽이 아닌 학습에 최적화 중. 하지만 안전과 속도 부채는 빨리 해결해야 합니다.
