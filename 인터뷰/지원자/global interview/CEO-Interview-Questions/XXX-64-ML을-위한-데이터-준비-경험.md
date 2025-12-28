# ML을 위한 데이터 준비 경험이 있나요

## English Question

**What experience do you have preparing data for machine learning models?**

## 질문 번역

머신러닝 모델을 위한 데이터 준비 경험이 있나요?

---

## English Answer

**Direct Experience:**
At Danal, I wasn't the ML engineer, but I worked closely with data scientists on fraud detection systems. My role was building the data pipelines that fed their models.

**What I Did:**

**1. Feature Engineering Support**
- Built pipelines to compute features from raw transactions
- Real-time feature computation for online inference
- Batch feature computation for model training
- Feature versioning to track changes

**2. Data Quality for ML**
- Data validation before model input
- Drift detection (is production data different from training data?)
- Handling missing values consistently
- Outlier identification and handling

**3. Training Data Pipelines**
- Historical data extraction for training sets
- Label management (fraud/not fraud labels)
- Train/validation/test splits
- Data versioning with DVC

**Key Learnings:**

**Garbage In, Garbage Out:**
Models are only as good as their data. I spent more time on data quality than anything else.

**Feature Stores:**
Centralized feature computation prevents training-serving skew:
- Same features computed the same way
- Reusable across models

**Labeling is Hard:**
Getting accurate labels for training data is often the bottleneck.

**For Zonagent:**
Your data challenges:
- Unstructured documents need preprocessing
- Labels might be noisy (is this project "approved" or "likely to be approved"?)
- Data quality varies by municipality

I'd bring my experience in building reliable data pipelines and thinking about data quality systematically.

---

## 면접관 평가 (Aaron Kirsch 기준)

| 항목 | 평가 |
|------|------|
| **질문 확률** | 🟢 30% - 낮은 확률 |
| **답안 품질** | ⭐⭐⭐⭐ (4/5) |

**강점:**
- 솔직함 - "I wasn't the ML engineer"
- 데이터 품질 중심
- "Garbage in, garbage out" - 명확한 교훈

**주의:**
- 기술적 - Mark Jung 면접용
- Aaron은 질문하지 않을 것

**Zonagent 연결:**
- 라벨 노이즈 이해
- 지자체별 데이터 품질 차이 언급

**Aaron 버전:**
> "ML 엔지니어와 협력해서 데이터 파이프라인을 구축했고, 데이터 품질이 가장 중요하다는 것을 알고 있습니다."

---

## 한글 번역

**직접 경험:**
다날에서 ML 엔지니어는 아니었지만 사기 탐지 시스템에서 데이터 과학자와 긴밀히 협력했습니다. 제 역할은 그들의 모델에 공급하는 데이터 파이프라인 구축이었습니다.

**한 일:**

**1. 피처 엔지니어링 지원**
- 원시 트랜잭션에서 피처를 계산하는 파이프라인 구축
- 온라인 추론을 위한 실시간 피처 계산
- 모델 학습을 위한 배치 피처 계산
- 변경 추적을 위한 피처 버저닝

**2. ML을 위한 데이터 품질**
- 모델 입력 전 데이터 검증
- 드리프트 감지 (프로덕션 데이터가 훈련 데이터와 다른지?)
- 결측값 일관되게 처리
- 이상치 식별 및 처리

**3. 훈련 데이터 파이프라인**
- 훈련 세트를 위한 히스토리 데이터 추출
- 레이블 관리 (사기/비사기 레이블)
- 훈련/검증/테스트 분할
- DVC로 데이터 버저닝

**핵심 교훈:**

**쓰레기 입력, 쓰레기 출력:**
모델은 데이터만큼만 좋습니다. 다른 어떤 것보다 데이터 품질에 더 많은 시간을 보냈습니다.

**피처 스토어:**
중앙화된 피처 계산이 훈련-서빙 스큐를 방지:
- 같은 방식으로 계산된 같은 피처
- 모델 간 재사용 가능

**레이블링은 어려움:**
훈련 데이터에 대한 정확한 레이블 얻기가 종종 병목.

**Zonagent의 경우:**
데이터 도전:
- 비정형 문서는 전처리 필요
- 레이블이 노이즈 있을 수 있음 (이 프로젝트가 "승인됨" 또는 "승인될 가능성 높음"?)
- 지자체에 따라 데이터 품질 다름

신뢰할 수 있는 데이터 파이프라인 구축과 체계적 데이터 품질 사고 경험을 가져올 것입니다.
