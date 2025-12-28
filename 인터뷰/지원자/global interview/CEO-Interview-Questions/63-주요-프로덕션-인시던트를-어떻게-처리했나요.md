# 주요 프로덕션 인시던트를 어떻게 처리했나요

## English Question

**How did you handle a critical production incident?**

## 질문 번역

주요 프로덕션 인시던트를 어떻게 처리했나요?

---

## English Answer

Let me walk you through a real incident from last year's holiday peak.

**The Incident:**
At 11 PM on a holiday eve, our transaction success rate dropped from 99.9% to 85%. This was during peak shopping hours—every minute of downtime meant significant revenue loss for our merchants.

**Immediate Response (First 15 minutes):**

**1. Assess the Blast Radius**
- Which services affected?
- Which merchants impacted?
- Is it getting worse?

**2. Communicate**
- Alerted the on-call team
- Notified management with initial assessment
- Started a war room channel

**3. Stabilize First**
Instead of debugging immediately, we rolled back the most recent deployment (even though we weren't sure it was the cause). Success rate recovered to 98%.

**Investigation (Next 2 hours):**
- Reviewed logs from the rolled-back version
- Found the issue: A new caching layer was hitting a race condition under high load
- The bug only manifested at traffic levels higher than our staging environment

**Resolution:**
- Kept the rollback in place
- Fixed the race condition
- Added load testing that matched production traffic patterns
- Deployed the fix during low-traffic hours the next week

**Post-Mortem:**
- What went wrong (technical root cause)
- Why we didn't catch it earlier (testing gaps)
- What we'll change (improved load testing, better staging parity)
- Blameless—focused on systems, not individuals

**Key Takeaway:**
During incidents, stability beats diagnosis. Restore service first, then investigate.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟡 55% - 물어볼 수도 있음 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 명확한 시간 구조 (첫 15분, 다음 2시간)
- "Stabilize first, then investigate" - 성숙한 접근
- Blameless post-mortem 언급
- 비즈니스 임팩트 이해 (매출 손실)

**Aaron이 좋아할 부분:**
- 위기 대응 능력
- 커뮤니케이션 (관리자 알림, 워룸)
- "Stability beats diagnosis" - 실용적

**주의:**
- 기술적 용어 (race condition, caching layer) 간소화 필요
- Aaron에게는 "위기 관리" 측면 강조

**Aaron 버전:**
> "명절 피크에 결제 성공률이 급락했을 때, 먼저 서비스를 안정화하고 나서 원인을 조사했습니다. 위기 때는 안정성이 우선입니다."

---

## 한글 번역

작년 명절 피크의 실제 인시던트를 설명하겠습니다.

**인시던트:**
명절 전야 밤 11시에 트랜잭션 성공률이 99.9%에서 85%로 떨어졌습니다. 쇼핑 피크 시간이었고—다운타임 1분마다 가맹점에 상당한 매출 손실을 의미했습니다.

**즉각 대응 (첫 15분):**

**1. 피해 범위 평가**
- 어떤 서비스가 영향받았나?
- 어떤 가맹점이 영향받았나?
- 악화되고 있나?

**2. 커뮤니케이션**
- 온콜 팀에 알림
- 초기 평가로 관리자에게 알림
- 워룸 채널 시작

**3. 먼저 안정화**
즉시 디버깅하는 대신, 가장 최근 배포를 롤백했습니다 (원인인지 확실하지 않았지만). 성공률이 98%로 회복.

**조사 (다음 2시간):**
- 롤백된 버전의 로그 검토
- 이슈 발견: 새 캐싱 레이어가 높은 부하에서 레이스 컨디션에 걸림
- 버그가 스테이징 환경보다 높은 트래픽 수준에서만 나타남

**해결:**
- 롤백 유지
- 레이스 컨디션 수정
- 프로덕션 트래픽 패턴에 맞는 부하 테스트 추가
- 다음 주 저트래픽 시간에 수정 배포

**사후 분석:**
- 무엇이 잘못되었나 (기술적 근본 원인)
- 왜 일찍 잡지 못했나 (테스팅 갭)
- 무엇을 바꿀 것인가 (개선된 부하 테스트, 더 나은 스테이징 동등성)
- 비난 없음—개인이 아닌 시스템에 집중

**핵심 교훈:**
인시던트 중에는 진단보다 안정성. 먼저 서비스 복원, 그다음 조사.
