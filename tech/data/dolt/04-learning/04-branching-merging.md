# 브랜칭과 머지

## 브랜치 개념

### 왜 브랜칭인가?

```
main (프로덕션 데이터)
  │
  ├── feature/new-pricing (가격 실험)
  │
  ├── analysis/q4-report (분석용 데이터 변경)
  │
  └── fix/data-correction (오류 수정)
```

브랜칭이 유용한 경우:
- **실험**: 기존 데이터에 영향 없이 변경 테스트
- **협업**: 각자의 작업 공간 분리
- **환경 분리**: dev/staging/production
- **분석**: 분석용 데이터 가공

---

## 브랜치 기본 작업

### 브랜치 목록

```bash
# 로컬 브랜치
dolt branch

# 원격 포함 모든 브랜치
dolt branch -a

# 상세 정보
dolt branch -v
```

### 브랜치 생성

```bash
# 새 브랜치 생성 (이동 안 함)
dolt branch feature/new-data

# 생성하고 이동
dolt checkout -b feature/new-data

# 특정 커밋에서 브랜치 생성
dolt branch fix/hotfix abc123
```

### 브랜치 이동

```bash
# 다른 브랜치로 이동
dolt checkout feature/new-data

# 이전 브랜치로 돌아가기
dolt checkout -
```

### 브랜치 삭제

```bash
# 머지된 브랜치 삭제
dolt branch -d feature/merged

# 강제 삭제 (머지 안 됨 주의!)
dolt branch -D feature/abandoned
```

### 브랜치 이름 변경

```bash
dolt branch -m old-name new-name
```

---

## SQL에서 브랜치 작업

### 브랜치 조회

```sql
-- 브랜치 목록
SELECT * FROM dolt_branches;

-- 현재 브랜치
SELECT active_branch();
```

### 브랜치 생성 및 이동

```sql
-- 브랜치 생성
CALL dolt_branch('feature/new');

-- 체크아웃
CALL dolt_checkout('feature/new');

-- 생성 후 체크아웃
CALL dolt_checkout('-b', 'feature/quick');
```

### 다른 브랜치 데이터 조회

```sql
-- 다른 브랜치의 데이터 조회 (AS OF)
SELECT * FROM products AS OF 'feature/new-pricing';

-- 현재와 다른 브랜치 비교
SELECT
    main.name,
    main.price as main_price,
    feat.price as feature_price
FROM products AS main
JOIN products AS OF 'feature/new-pricing' AS feat
    ON main.id = feat.id
WHERE main.price != feat.price;
```

---

## 머지 (Merge)

### 기본 머지

```bash
# feature 브랜치를 main에 머지
dolt checkout main
dolt merge feature/new-data

# 머지 메시지 직접 지정
dolt merge feature/new-data -m "feature/new-data 브랜치 머지"
```

### SQL에서 머지

```sql
-- main 브랜치에서 실행
CALL dolt_merge('feature/new-data');
```

### 머지 결과

```bash
# 성공 시
Updating abc123..def456
Fast-forward

# 또는
Merge made by the 'ort' strategy.
 products | 3 +++
 1 table changed, 3 rows added(+)
```

---

## 머지 유형

### 1. Fast-forward 머지

```
main:    A---B
              \
feature:       C---D

머지 후:
main:    A---B---C---D
```

- main에서 분기 후 main에 변경 없음
- 커밋 히스토리가 선형으로 유지

### 2. 3-way 머지

```
main:    A---B---E
              \
feature:       C---D

머지 후:
main:    A---B---E---M (머지 커밋)
              \     /
feature:       C---D
```

- 양쪽 브랜치 모두 변경됨
- 머지 커밋 생성

### 머지 옵션

```bash
# Fast-forward만 허용 (충돌 가능성 있으면 실패)
dolt merge --ff-only feature

# Fast-forward 가능해도 머지 커밋 생성
dolt merge --no-ff feature

# 머지하지 않고 변경사항만 가져오기
dolt merge --squash feature
```

---

## 충돌 해결

### 충돌 발생 조건

같은 행(row)을 양쪽 브랜치에서 수정했을 때:

```sql
-- main 브랜치
UPDATE products SET price = 1500 WHERE id = 1;

-- feature 브랜치
UPDATE products SET price = 1600 WHERE id = 1;
```

### 충돌 확인

```bash
# 머지 시도
dolt merge feature
# CONFLICT (content): Merge conflict in products
# Automatic merge failed; fix conflicts and then commit the result.

# 상태 확인
dolt status
# You have unmerged tables.
#   (fix conflicts and run "dolt commit")
#
# Unmerged paths:
#   both modified:   products
```

### 충돌 내용 확인

```sql
-- 충돌 테이블
SELECT * FROM dolt_conflicts;

-- 상세 충돌 내용
SELECT * FROM dolt_conflicts_products;
```

출력 예시:
```
base_id | base_price | our_id | our_price | their_id | their_price
--------|------------|--------|-----------|----------|------------
1       | 1000       | 1      | 1500      | 1        | 1600
```

- `base`: 공통 조상
- `our`: 현재 브랜치 (main)
- `their`: 머지하려는 브랜치 (feature)

### 충돌 해결

#### 방법 1: 직접 수정

```sql
-- 원하는 값으로 직접 수정
UPDATE products SET price = 1550 WHERE id = 1;

-- 충돌 해결됨 표시
CALL dolt_conflicts_resolve('products');
```

#### 방법 2: 특정 버전 선택

```sql
-- 현재 브랜치(ours) 값 선택
CALL dolt_conflicts_resolve('--ours', 'products');

-- 머지 브랜치(theirs) 값 선택
CALL dolt_conflicts_resolve('--theirs', 'products');
```

### 머지 완료

```bash
# 충돌 해결 후 커밋
dolt add .
dolt commit -m "feature 브랜치 머지 - 충돌 해결"
```

### 머지 취소

```bash
# 충돌 상태에서 머지 취소
dolt merge --abort
```

---

## 실전 워크플로우

### Feature Branch 워크플로우

```bash
# 1. 새 기능 브랜치 생성
dolt checkout -b feature/product-categories

# 2. 작업 수행
dolt sql -q "ALTER TABLE products ADD COLUMN category_id INT"
dolt sql -q "CREATE TABLE categories (id INT PRIMARY KEY, name VARCHAR(50))"

# 3. 커밋
dolt add .
dolt commit -m "카테고리 기능 추가"

# 4. main으로 돌아가서 머지
dolt checkout main
dolt merge feature/product-categories

# 5. 브랜치 정리
dolt branch -d feature/product-categories
```

### 환경별 브랜치

```bash
# 브랜치 구조
main        # 프로덕션
staging     # 스테이징
dev         # 개발

# 개발 -> 스테이징
dolt checkout staging
dolt merge dev

# 스테이징 -> 프로덕션
dolt checkout main
dolt merge staging
```

### 분석용 브랜치

```bash
# 분석 브랜치 생성
dolt checkout -b analysis/q4-2024

# 분석용 데이터 가공
dolt sql -q "DELETE FROM orders WHERE date < '2024-01-01'"
dolt sql -q "UPDATE products SET price = price * 1.1"

# 분석 수행 (머지하지 않음)
# ...

# 분석 완료 후 폐기
dolt checkout main
dolt branch -D analysis/q4-2024
```

---

## 브랜치 비교

### diff로 비교

```bash
# 두 브랜치 간 차이
dolt diff main feature/new-data

# 특정 테이블만
dolt diff main feature/new-data -- products
```

### SQL로 비교

```sql
-- 브랜치 간 행 차이
SELECT * FROM dolt_diff('main', 'feature/new-data', 'products');

-- 스키마 차이
SELECT * FROM dolt_schema_diff('main', 'feature/new-data', 'products');
```

---

## 고급 기능

### Cherry-pick (특정 커밋만 가져오기)

```bash
# 특정 커밋만 현재 브랜치에 적용
dolt cherry-pick abc123
```

### Rebase

```bash
# feature 브랜치를 main 위로 리베이스
dolt checkout feature
dolt rebase main
```

### Stash (임시 저장)

```bash
# 작업 중인 변경사항 임시 저장
dolt stash

# 목록 확인
dolt stash list

# 복원
dolt stash pop
```

---

## 실습 과제

### 과제 1: 기본 브랜칭

1. 새 저장소에서 products 테이블 생성
2. `feature/new-products` 브랜치 생성
3. 브랜치에서 새 상품 추가
4. main으로 머지

### 과제 2: 충돌 해결

1. 두 브랜치에서 같은 행 수정
2. 머지 시도하여 충돌 발생
3. 충돌 확인 및 해결
4. 머지 완료

### 과제 3: 환경별 브랜치 관리

1. main, staging, dev 브랜치 생성
2. dev에서 작업
3. dev -> staging -> main 순차 머지
4. 각 단계에서 데이터 확인

---

## 다음 단계

- [[05-dolthub|DoltHub]]
- [[06-integration|프로그래밍 언어 통합]]
