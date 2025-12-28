# 서로 다른 소스의 불일치한 데이터 형식을 어떻게 처리하나요

## English Question

**How do you handle inconsistent data formats across different sources?**

## 질문 번역

서로 다른 소스에서 불일치한 데이터 형식을 어떻게 처리하나요?

---

## English Answer

This is a problem I've dealt with extensively in payment processing. Here's my approach:

**1. Define a Canonical Schema**
First, decide what your internal representation looks like. All external formats get normalized to this canonical form. This decouples your core logic from source-specific variations.

Example: In payments, we have different formats from Visa, Mastercard, local banks. But internally, a transaction is a transaction—same fields, same types.

**2. Source-Specific Adapters**
Each external source gets its own adapter that:
- Parses the source format
- Maps fields to the canonical schema
- Handles source-specific edge cases
- Logs transformation failures for review

**3. Validation Layer**
After transformation, validate aggressively:
- Required fields present?
- Values in expected ranges?
- Relationships between fields make sense?

Invalid records go to a quarantine for human review, not into the main pipeline.

**4. Monitoring for Drift**
Sources change without warning. I track:
- Percentage of records failing validation
- New field values we haven't seen before
- Changes in data volume patterns

Sudden spikes trigger alerts before bad data pollutes the system.

**5. Documentation**
Maintain a living document of each source's quirks. When a new engineer joins, they shouldn't have to rediscover why source X sends dates in a weird format.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟢 30% - 낮은 확률 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 5단계 체계적 접근
- "Canonical Schema" - 정규화 전략
- "Source-Specific Adapters" - 확장 가능한 설계
- 문서화 중요성 언급

**주의:**
- 기술 면접 (Mark Jung)용 질문
- Aaron에게는 너무 기술적

**Aaron에게 요약 버전:**
> "각 소스마다 다른 형식을 하나의 표준으로 변환합니다. 결제 네트워크에서 이런 경험이 많습니다."

---

## 한글 번역

이것은 결제 처리에서 광범위하게 다룬 문제입니다. 제 접근 방식:

**1. 정규 스키마 정의**
먼저 내부 표현이 어떻게 생겼는지 결정합니다. 모든 외부 형식이 이 정규 형태로 정규화됩니다. 이것은 핵심 로직을 소스별 변형에서 분리합니다.

예: 결제에서 Visa, Mastercard, 로컬 은행에서 다른 형식이 있습니다. 하지만 내부적으로 트랜잭션은 트랜잭션입니다—같은 필드, 같은 타입.

**2. 소스별 어댑터**
각 외부 소스는 자체 어댑터가 있어:
- 소스 형식 파싱
- 필드를 정규 스키마에 매핑
- 소스별 엣지 케이스 처리
- 검토를 위해 변환 실패 로깅

**3. 검증 레이어**
변환 후 적극적으로 검증:
- 필수 필드 존재?
- 값이 예상 범위 내?
- 필드 간 관계가 의미 있음?

유효하지 않은 레코드는 메인 파이프라인이 아닌 격리 구역으로 가서 인간 검토를 받습니다.

**4. 드리프트 모니터링**
소스는 경고 없이 변경됩니다. 추적하는 것:
- 검증 실패 레코드 비율
- 이전에 본 적 없는 새 필드 값
- 데이터 볼륨 패턴 변화

갑작스러운 급증은 나쁜 데이터가 시스템을 오염시키기 전에 알림을 트리거합니다.

**5. 문서화**
각 소스의 특이점에 대한 살아있는 문서를 유지합니다. 새 엔지니어가 합류할 때 소스 X가 이상한 형식으로 날짜를 보내는 이유를 다시 발견할 필요가 없어야 합니다.
