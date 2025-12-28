# 정부 문서와 회의록 파싱에 어떻게 접근하시겠습니까

## English Question

**How would you approach parsing government documents and meeting minutes?**

## 질문 번역

정부 문서와 회의록 파싱에 어떻게 접근하시겠습니까?

---

## English Answer

This is a classic unstructured data problem. Here's how I'd approach it:

**1. Understand the Document Types**
First, catalog what we're dealing with:
- PDF zoning codes (often scanned, variable formatting)
- Meeting minutes (agenda items, votes, discussions)
- Approval letters
- Public hearing notices

Each type needs a different extraction strategy.

**2. Layered Extraction Approach**

**Layer 1: Document Ingestion**
- Convert PDFs to text (OCR for scanned docs)
- Handle different encodings and formats
- Preserve document structure where possible

**Layer 2: Structured Extraction**
For semi-structured content:
- Identify recurring patterns (meeting dates, agenda formats)
- Build templates for common document types
- Extract metadata (dates, addresses, case numbers)

**Layer 3: NLP for Unstructured Content**
For free-text like discussions:
- Named entity recognition (project names, people, addresses)
- Sentiment analysis (community support/opposition)
- Topic classification (what issues were discussed)

**3. Quality Pipeline**
- **Confidence scoring**: How sure are we about each extraction?
- **Human-in-the-loop**: Flag low-confidence items for review
- **Feedback integration**: Use corrections to improve extraction

**4. Practical Considerations**
- Start with the highest-volume, most-structured sources
- Build ground truth datasets for evaluation
- Iterate: perfect is the enemy of good enough

**From My Experience:**
In payments, I've parsed transaction records from diverse formats. The key is building robust pipelines that handle edge cases gracefully rather than breaking on unexpected input.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟢 40% - 낮은 확률 |
| **답안 품질** | ⭐⭐⭐⭐⭐ (5/5) |

**강점:**
- 문서 유형별 분류
- 3계층 추출 접근 (Ingestion, Structured, NLP)
- Quality Pipeline 포함
- 결제 경험 연결

**주의:**
- Aaron은 비기술자
- Mark Jung 면접용 질문

**Aaron에게 요약:**
> "다양한 형식의 정부 문서에서 필요한 정보를 자동으로 추출하는 시스템을 설계할 수 있습니다. 결제에서 비슷한 문제를 해결해봤습니다."

---

## 한글 번역

이것은 전형적인 비정형 데이터 문제입니다. 접근 방식:

**1. 문서 유형 이해**
먼저 다루는 것을 목록화:
- PDF 조닝 코드 (종종 스캔됨, 가변 포맷팅)
- 회의록 (안건, 투표, 논의)
- 승인서
- 공청회 공지

각 유형은 다른 추출 전략이 필요합니다.

**2. 계층화된 추출 접근**

**레이어 1: 문서 수집**
- PDF를 텍스트로 변환 (스캔 문서는 OCR)
- 다른 인코딩과 형식 처리
- 가능한 경우 문서 구조 보존

**레이어 2: 정형 추출**
반정형 콘텐츠:
- 반복되는 패턴 식별 (회의 날짜, 안건 형식)
- 일반적인 문서 유형에 대한 템플릿 구축
- 메타데이터 추출 (날짜, 주소, 케이스 번호)

**레이어 3: 비정형 콘텐츠를 위한 NLP**
논의 같은 자유 텍스트:
- 명명된 엔티티 인식 (프로젝트 이름, 사람, 주소)
- 감정 분석 (커뮤니티 지지/반대)
- 주제 분류 (어떤 이슈가 논의되었는지)

**3. 품질 파이프라인**
- **신뢰도 점수**: 각 추출에 대해 얼마나 확신하나?
- **휴먼 인 더 루프**: 낮은 신뢰도 항목을 검토 플래그
- **피드백 통합**: 수정을 사용하여 추출 개선

**4. 실용적 고려사항**
- 가장 볼륨이 크고 가장 정형화된 소스부터 시작
- 평가를 위한 그라운드 트루스 데이터셋 구축
- 반복: 완벽은 충분히 좋은 것의 적

**제 경험에서:**
결제에서 다양한 형식의 트랜잭션 레코드를 파싱했습니다. 핵심은 예상치 못한 입력에 깨지기보다 엣지 케이스를 우아하게 처리하는 강건한 파이프라인을 구축하는 것입니다.
