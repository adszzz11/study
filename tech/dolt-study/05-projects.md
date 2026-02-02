# 실전 프로젝트 및 Best Practices

## 프로젝트 아이디어

### 초급 프로젝트

#### 1. 개인 재무 추적기

```
목표: 개인 수입/지출 데이터를 버전 관리

스키마:
- accounts (계좌)
- transactions (거래)
- categories (카테고리)

기능:
- 월별 지출 분석
- 카테고리별 통계
- 과거 데이터 비교 (시점 쿼리)
```

**구현 단계:**

```sql
-- 1. 스키마 생성
CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    type ENUM('checking', 'savings', 'credit'),
    balance DECIMAL(12, 2) DEFAULT 0
);

CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    type ENUM('income', 'expense')
);

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT,
    category_id INT,
    amount DECIMAL(12, 2),
    description VARCHAR(200),
    date DATE,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

```bash
# 2. 월별 데이터 커밋
dolt commit -m "2024년 1월 거래 데이터"

# 3. 월간 비교
dolt diff HEAD~1 HEAD -- transactions
```

#### 2. 도서 관리 시스템

```
목표: 읽은 책 목록과 메모 관리

스키마:
- books (도서)
- reading_log (독서 기록)
- notes (메모)

기능:
- 독서 진행 상황 추적
- 메모 버전 관리
- 연도별 독서 통계
```

#### 3. 레시피 데이터베이스

```
목표: 가족 레시피 협업 관리

스키마:
- recipes (레시피)
- ingredients (재료)
- recipe_ingredients (레시피-재료 연결)
- tags (태그)

기능:
- 레시피 수정 이력
- 가족 멤버별 브랜치
- 원본 vs 변형 레시피 비교
```

---

### 중급 프로젝트

#### 4. 설정 관리 시스템

```
목표: 애플리케이션 설정을 환경별로 관리

브랜치 구조:
main (프로덕션)
├── staging
├── development
└── feature/*

스키마:
- config_entries (설정 항목)
- config_history (변경 이력)
```

**구현:**

```sql
CREATE TABLE config_entries (
    key_name VARCHAR(100) PRIMARY KEY,
    value TEXT,
    data_type VARCHAR(20),
    description VARCHAR(500),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 환경별 데이터
-- main: 프로덕션 설정
-- staging: 스테이징 설정
```

```python
# 환경별 설정 조회 API
from flask import Flask
from doltpy.core import Dolt

app = Flask(__name__)
dolt = Dolt("/path/to/config-db")

@app.route('/config/<env>')
def get_config(env):
    result = dolt.sql(
        f"SELECT * FROM config_entries AS OF '{env}'",
        result_format="json"
    )
    return result
```

#### 5. ML 데이터셋 버전 관리

```
목표: 머신러닝 학습 데이터 버전 관리

브랜치 전략:
main (최신 검증 데이터)
├── experiment/model-v1
├── experiment/model-v2
└── data/augmentation-test

스키마:
- samples (샘플 데이터)
- labels (라벨)
- metadata (메타데이터)
```

**구현:**

```python
import pandas as pd
from doltpy.core import Dolt
from doltpy.core.write import import_df

def version_dataset(dolt_repo, df, version_tag, description):
    """데이터셋 버전 저장"""
    # 브랜치 생성
    dolt_repo.branch(f"data/{version_tag}")
    dolt_repo.checkout(f"data/{version_tag}")

    # 데이터 저장
    import_df(dolt_repo, "training_data", df, ["id"], "replace")

    # 커밋 및 태그
    dolt_repo.add(".")
    dolt_repo.commit(description)

    # main으로 복귀
    dolt_repo.checkout("main")

# 사용
dolt = Dolt("/path/to/ml-data")
df = pd.read_csv("training_v2.csv")
version_dataset(dolt, df, "v2.0", "라벨 오류 수정 및 데이터 증강")
```

#### 6. API 응답 캐시 데이터베이스

```
목표: 외부 API 응답 캐시 및 이력 관리

스키마:
- api_cache (캐시)
- api_log (호출 로그)

기능:
- API 응답 변화 추적
- 특정 시점 응답 복원
- 변경 알림
```

---

### 고급 프로젝트

#### 7. 멀티테넌트 데이터 플랫폼

```
목표: 고객별 데이터 격리 및 공유

브랜치 전략:
main (템플릿)
├── tenant/customer-a
├── tenant/customer-b
└── shared (공유 데이터)

기능:
- 테넌트별 데이터 격리
- 공유 데이터 동기화
- 테넌트별 커스터마이징
```

#### 8. 데이터 카탈로그 시스템

```
목표: 조직 데이터 자산 카탈로그

스키마:
- data_sources (데이터 소스)
- schemas (스키마 정보)
- columns (컬럼 정보)
- lineage (데이터 계보)
- glossary (용어 사전)

기능:
- 스키마 변경 추적
- 데이터 계보 시각화
- 영향도 분석
```

#### 9. 규제 준수 데이터 저장소

```
목표: GDPR/CCPA 준수 데이터 관리

기능:
- 전체 데이터 변경 감사
- 특정 시점 데이터 복원
- 삭제 요청 추적
- 데이터 접근 로그
```

---

## Best Practices

### 1. 커밋 전략

#### 원자적 커밋

```bash
# 좋은 예: 관련 변경만 함께 커밋
dolt add products
dolt commit -m "신규 상품 3종 추가"

dolt add prices
dolt commit -m "Q2 가격 인상 반영"

# 나쁜 예: 무관한 변경을 함께 커밋
dolt add .
dolt commit -m "여러 변경사항"
```

#### 의미 있는 커밋 메시지

```
[타입] 간략한 설명

상세 내용:
- 변경 사항 1
- 변경 사항 2

관련: #이슈번호
```

예시:
```
[데이터] 2024년 Q1 매출 데이터 추가

- 1월~3월 매출 데이터 100,000건
- 데이터 출처: SAP ERP
- 검증: 재무팀 승인 완료

관련: #DATA-123
```

### 2. 브랜치 전략

#### Git Flow 스타일

```
main (프로덕션)
├── develop (개발)
│   ├── feature/user-segmentation
│   └── feature/product-categories
├── release/v2.0
└── hotfix/price-correction
```

#### 환경 기반

```
production
├── staging
└── development
```

#### 데이터 파이프라인

```
raw (원시 데이터)
├── cleaned (정제 데이터)
└── aggregated (집계 데이터)
```

### 3. 코드 리뷰 (데이터 리뷰)

#### PR 체크리스트

```markdown
## 데이터 변경 PR 체크리스트

### 변경 내용
- [ ] 변경 테이블 명시
- [ ] 영향받는 행 수 확인
- [ ] 변경 이유 설명

### 검증
- [ ] 데이터 타입 검증
- [ ] 참조 무결성 확인
- [ ] 비즈니스 규칙 검증

### 승인
- [ ] 데이터 오너 승인
- [ ] 보안 검토 (민감 데이터)
```

#### diff 리뷰

```sql
-- PR 리뷰 시 확인 쿼리
-- 추가된 행
SELECT * FROM dolt_diff('main', 'feature/new-data', 'users')
WHERE diff_type = 'added';

-- 수정된 행
SELECT * FROM dolt_diff('main', 'feature/new-data', 'users')
WHERE diff_type = 'modified';

-- 삭제된 행
SELECT * FROM dolt_diff('main', 'feature/new-data', 'users')
WHERE diff_type = 'removed';
```

### 4. 데이터 품질 관리

#### 검증 쿼리

```sql
-- 중복 검사
SELECT email, COUNT(*) as cnt
FROM users
GROUP BY email
HAVING cnt > 1;

-- NULL 검사
SELECT COUNT(*) as null_count
FROM orders
WHERE customer_id IS NULL;

-- 범위 검사
SELECT COUNT(*) as invalid_count
FROM products
WHERE price < 0 OR price > 10000000;

-- 참조 무결성
SELECT o.*
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
WHERE c.id IS NULL;
```

#### 커밋 전 검증 스크립트

```python
def validate_before_commit(dolt_repo):
    """커밋 전 데이터 검증"""
    checks = [
        ("중복 이메일", "SELECT COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1"),
        ("음수 가격", "SELECT COUNT(*) FROM products WHERE price < 0"),
        ("고아 주문", "SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.id WHERE c.id IS NULL"),
    ]

    errors = []
    for name, query in checks:
        result = dolt_repo.sql(query, result_format="json")
        if result['rows']:
            errors.append(f"{name}: {len(result['rows'])}건 발견")

    if errors:
        raise ValueError(f"검증 실패: {errors}")

    return True
```

### 5. 백업 및 복구

#### 정기 백업

```bash
#!/bin/bash
# backup.sh

DOLT_REPO="/path/to/dolt-repo"
BACKUP_REMOTE="backup"
DATE=$(date +%Y%m%d)

cd "$DOLT_REPO"

# 태그 생성
dolt tag "backup-$DATE" HEAD

# 백업 원격 푸시
dolt push $BACKUP_REMOTE main
dolt push $BACKUP_REMOTE --tags

echo "백업 완료: backup-$DATE"
```

#### 복구

```bash
# 특정 시점으로 복구
dolt checkout backup-20240115

# 또는 특정 커밋으로
dolt reset --hard abc123def456
```

### 6. 성능 최적화

#### 인덱스 전략

```sql
-- 자주 검색하는 컬럼
CREATE INDEX idx_users_email ON users(email);

-- 자주 조인하는 FK
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- 복합 조건
CREATE INDEX idx_orders_date_status ON orders(order_date, status);
```

#### 쿼리 최적화

```sql
-- EXPLAIN으로 실행 계획 확인
EXPLAIN SELECT * FROM orders WHERE customer_id = 1;

-- 불필요한 컬럼 제외
SELECT id, name, email FROM users;  -- SELECT * 대신
```

#### 대용량 데이터 처리

```bash
# 배치 임포트
dolt table import -u --batch-size 10000 large_table data.csv

# 점진적 커밋
# 전체를 한 번에 하지 않고 청크로 나누기
```

### 7. 보안 고려사항

#### 민감 데이터 처리

```sql
-- 민감 컬럼 마스킹 뷰
CREATE VIEW users_public AS
SELECT
    id,
    name,
    CONCAT(SUBSTRING(email, 1, 3), '***') as email_masked,
    created_at
FROM users;
```

#### 접근 제어

```yaml
# SQL 서버 설정
users:
  - name: admin
    password: "secure_password"
    privileges:
      - ALL
  - name: readonly
    password: "read_password"
    privileges:
      - SELECT
```

---

## 프로젝트 템플릿

### 기본 구조

```
my-dolt-project/
├── .dolt/                 # Dolt 데이터
├── scripts/
│   ├── init.sql           # 초기 스키마
│   ├── seed.sql           # 시드 데이터
│   └── validate.py        # 검증 스크립트
├── docs/
│   ├── schema.md          # 스키마 문서
│   └── workflow.md        # 워크플로우
├── .doltignore            # 무시할 테이블
└── README.md
```

### 초기화 스크립트

```bash
#!/bin/bash
# init_project.sh

PROJECT_NAME=$1

mkdir -p "$PROJECT_NAME"/{scripts,docs}
cd "$PROJECT_NAME"

# Dolt 초기화
dolt init

# 사용자 설정
dolt config --local --add user.email "team@example.com"
dolt config --local --add user.name "Data Team"

# 초기 스키마 적용
dolt sql < scripts/init.sql

# 초기 커밋
dolt add .
dolt commit -m "프로젝트 초기화"

echo "프로젝트 생성 완료: $PROJECT_NAME"
```

---

## 실습 과제

### 종합 프로젝트: 전자상거래 데이터 플랫폼

1. **스키마 설계**
   - customers, products, orders, order_items
   - 적절한 인덱스 설정

2. **데이터 파이프라인**
   - 외부 CSV에서 데이터 임포트
   - 데이터 검증 스크립트

3. **브랜치 전략 구현**
   - main (프로덕션)
   - staging (테스트)
   - feature/* (기능 개발)

4. **협업 시뮬레이션**
   - 2개 이상의 feature 브랜치
   - PR 및 머지 연습

5. **분석 쿼리 작성**
   - 월별 매출
   - 인기 상품 TOP 10
   - 고객 세그먼트

---

## 다음 단계

- [[cheatsheet|치트시트]] - 빠른 참조
- [[04-learning/01-installation|설치 가이드]] - 처음부터 다시
