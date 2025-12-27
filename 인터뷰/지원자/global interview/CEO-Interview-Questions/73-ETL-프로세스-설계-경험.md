# ETL 프로세스를 어떻게 설계하나요

## English Question

**How would you design an ETL process for municipal data?**

## 질문 번역

지자체 데이터를 위한 ETL 프로세스를 어떻게 설계하시겠습니까?

---

## English Answer

This is directly relevant to Zonagent's core challenge. Here's how I'd approach it:

**Understanding the Problem:**
- Thousands of municipalities with different data formats
- Mix of structured (APIs) and unstructured (PDFs, websites) data
- Data quality varies wildly
- Need for both batch and near-real-time processing

**My ETL Design:**

**1. Extract Layer**
```
Multiple Collectors → Raw Data Lake
- Web scrapers for municipal websites
- API integrations where available
- Document downloaders for PDFs, meeting minutes
- Store raw data before any transformation
```

**2. Transform Layer**
```
Raw Data → Normalized Format
- Document parsing (PDF text extraction, OCR if needed)
- Entity recognition (dates, addresses, project names)
- Data validation and quality checks
- Deduplication logic
```

**3. Load Layer**
```
Normalized Data → Production Database
- Incremental loads (only new/changed data)
- Version history for tracking changes
- Audit trail for data lineage
```

**Key Design Principles:**

**Idempotency**: Running the same job twice produces the same result. Critical for reliability.

**Checkpointing**: Save progress so failures don't require starting over.

**Monitoring**: Track success rates, data quality metrics, processing times by source.

**Alerting**: Immediate notification when a source changes format or becomes unavailable.

**From My Experience:**
At Danal, we processed transaction data from hundreds of merchants, each with different formats. The pattern is similar—build robust normalization, expect sources to change, make debugging easy.

---

## 한글 번역

이것은 Zonagent의 핵심 도전과 직접적으로 관련됩니다. 제 접근 방식:

**문제 이해:**
- 다른 데이터 형식을 가진 수천 개의 지자체
- 정형 (API)과 비정형 (PDF, 웹사이트) 데이터의 혼합
- 데이터 품질이 크게 다름
- 배치와 준실시간 처리 모두 필요

**제 ETL 설계:**

**1. 추출 레이어**
```
다중 수집기 → 원시 데이터 레이크
- 지자체 웹사이트용 웹 스크레이퍼
- 가능한 곳에서 API 통합
- PDF, 회의록용 문서 다운로더
- 변환 전에 원시 데이터 저장
```

**2. 변환 레이어**
```
원시 데이터 → 정규화된 형식
- 문서 파싱 (PDF 텍스트 추출, 필요시 OCR)
- 엔티티 인식 (날짜, 주소, 프로젝트 이름)
- 데이터 검증 및 품질 검사
- 중복 제거 로직
```

**3. 적재 레이어**
```
정규화된 데이터 → 프로덕션 데이터베이스
- 증분 적재 (새로운/변경된 데이터만)
- 변경 추적을 위한 버전 이력
- 데이터 리니지를 위한 감사 추적
```

**핵심 설계 원칙:**

**멱등성**: 같은 작업을 두 번 실행해도 같은 결과. 신뢰성에 중요.

**체크포인팅**: 진행 상황 저장으로 실패 시 처음부터 다시 시작 불필요.

**모니터링**: 성공률, 데이터 품질 메트릭, 소스별 처리 시간 추적.

**알림**: 소스가 형식을 변경하거나 사용 불가 시 즉시 알림.

**제 경험에서:**
다날에서 각기 다른 형식을 가진 수백 개의 가맹점 트랜잭션 데이터를 처리했습니다. 패턴은 유사합니다—견고한 정규화 구축, 소스 변경 예상, 디버깅 쉽게 만들기.
