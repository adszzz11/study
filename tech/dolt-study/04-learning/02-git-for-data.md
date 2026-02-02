# Git 명령어와 데이터 버전 관리

## Git과 Dolt 명령어 비교

| Git | Dolt | 설명 |
|-----|------|------|
| `git init` | `dolt init` | 저장소 초기화 |
| `git status` | `dolt status` | 상태 확인 |
| `git add` | `dolt add` | 스테이징 |
| `git commit` | `dolt commit` | 커밋 |
| `git log` | `dolt log` | 로그 확인 |
| `git diff` | `dolt diff` | 차이점 확인 |
| `git branch` | `dolt branch` | 브랜치 관리 |
| `git checkout` | `dolt checkout` | 브랜치/커밋 이동 |
| `git merge` | `dolt merge` | 머지 |
| `git clone` | `dolt clone` | 복제 |
| `git push` | `dolt push` | 원격 푸시 |
| `git pull` | `dolt pull` | 원격 풀 |
| `git remote` | `dolt remote` | 원격 저장소 관리 |
| `git reset` | `dolt reset` | 리셋 |

---

## 커밋 작업

### 변경사항 확인

```bash
# 상태 확인
dolt status

# 출력 예시:
# On branch main
# Changes not staged for commit:
#   (use "dolt add <table>" to update what will be committed)
#   (use "dolt checkout <table>" to discard changes in working directory)
#
#        modified:   products
#
# Untracked tables:
#   (use "dolt add <table>" to include in what will be committed)
#
#        new table:  orders
```

### 스테이징

```bash
# 특정 테이블 스테이징
dolt add products

# 모든 변경사항 스테이징
dolt add .

# 스테이징 취소
dolt reset products
```

### 커밋

```bash
# 메시지와 함께 커밋
dolt commit -m "제품 가격 업데이트"

# 상세 메시지 작성 (에디터 열림)
dolt commit

# 스테이징 없이 바로 커밋 (추적 중인 테이블만)
dolt commit -am "빠른 수정"
```

### 커밋 메시지 규칙 (권장)

```
[타입] 간략한 설명

상세 설명 (선택)
- 변경 사항 1
- 변경 사항 2

관련 이슈: #123
```

타입 예시:
- `[추가]` 새 테이블/데이터
- `[수정]` 데이터 수정
- `[삭제]` 데이터/테이블 삭제
- `[스키마]` 스키마 변경
- `[수정]` 오류 수정

---

## 로그 확인

### 기본 로그

```bash
dolt log
```

출력:
```
commit abc123def456 (HEAD -> main)
Author: Your Name <your@email.com>
Date:   2024-01-15 10:30:00 +0900

    제품 가격 업데이트

commit 789xyz000111
Author: Your Name <your@email.com>
Date:   2024-01-14 15:20:00 +0900

    products 테이블 생성
```

### 로그 옵션

```bash
# 한 줄씩 출력
dolt log --oneline

# 최근 5개만
dolt log -n 5

# 특정 테이블의 변경만
dolt log -- products

# 그래프 형태
dolt log --graph --oneline
```

### SQL로 로그 조회

```sql
-- dolt_log 시스템 테이블
SELECT * FROM dolt_log;

-- 최근 10개 커밋
SELECT commit_hash, committer, message, date
FROM dolt_log
LIMIT 10;
```

---

## Diff (차이점 확인)

### 기본 diff

```bash
# 워킹 디렉토리 vs 스테이징 영역
dolt diff

# 특정 테이블만
dolt diff products
```

### 커밋 간 비교

```bash
# 이전 커밋과 현재
dolt diff HEAD~1 HEAD

# 특정 커밋 간
dolt diff abc123 def456

# 브랜치 간
dolt diff main feature/new-data
```

### diff 출력 형식

```bash
# 기본 (텍스트)
dolt diff

# SQL 형식
dolt diff --sql

# 통계만
dolt diff --stat
```

### SQL diff 출력 예시

```sql
-- dolt diff --sql 출력
DELETE FROM products WHERE id = 3;
UPDATE products SET price = 1600000 WHERE id = 1;
INSERT INTO products (id, name, price) VALUES (5, '모니터', 350000);
```

### SQL로 diff 조회

```sql
-- 두 커밋 간 차이
SELECT *
FROM dolt_diff('HEAD~1', 'HEAD', 'products');

-- 특정 컬럼만
SELECT from_id, to_id, from_price, to_price, diff_type
FROM dolt_diff('HEAD~1', 'HEAD', 'products');
```

diff_type 값:
- `added`: 새로 추가된 행
- `removed`: 삭제된 행
- `modified`: 수정된 행

---

## 시점 쿼리 (Time Travel)

### AS OF 구문

```sql
-- 특정 커밋 시점의 데이터
SELECT * FROM products AS OF 'abc123def456';

-- 상대적 참조
SELECT * FROM products AS OF 'HEAD~3';

-- 브랜치 시점
SELECT * FROM products AS OF 'feature/old-prices';

-- 타임스탬프
SELECT * FROM products AS OF '2024-01-01 00:00:00';
```

### 시점 간 조인

```sql
-- 현재와 과거 데이터 비교
SELECT
    current.name,
    current.price as current_price,
    old.price as old_price,
    current.price - old.price as price_change
FROM products AS current
JOIN products AS OF 'HEAD~5' AS old
    ON current.id = old.id
WHERE current.price != old.price;
```

---

## 리셋

### Soft Reset (스테이징 취소)

```bash
# 특정 테이블 언스테이지
dolt reset products

# 모든 테이블 언스테이지
dolt reset
```

### Hard Reset (변경사항 폐기)

```bash
# 마지막 커밋 상태로 복원
dolt reset --hard

# 특정 커밋으로 복원 (주의!)
dolt reset --hard HEAD~2
```

### 특정 테이블만 복원

```bash
# 특정 커밋에서 테이블 복원
dolt checkout HEAD~1 -- products

# 다른 브랜치에서 테이블 가져오기
dolt checkout feature -- products
```

---

## Blame (변경 책임 추적)

### CLI blame

```bash
dolt blame products
```

### SQL blame

```sql
-- 각 행의 마지막 수정 정보
SELECT * FROM dolt_blame_products;

-- 특정 행의 변경 이력
SELECT commit_hash, committer, message
FROM dolt_blame_products
WHERE id = 1;
```

---

## 히스토리 조회

### 테이블 히스토리

```sql
-- products 테이블의 전체 변경 이력
SELECT * FROM dolt_history_products;

-- 특정 행의 이력
SELECT commit_hash, committer_date, name, price
FROM dolt_history_products
WHERE id = 1
ORDER BY committer_date DESC;
```

### 커밋 조상 확인

```sql
-- 특정 커밋의 조상들
SELECT * FROM dolt_commit_ancestors WHERE commit_hash = 'abc123';

-- 두 커밋의 공통 조상
SELECT * FROM dolt_merge_base('main', 'feature');
```

---

## 시스템 테이블 요약

| 테이블 | 설명 |
|--------|------|
| `dolt_log` | 커밋 로그 |
| `dolt_diff()` | 두 커밋 간 diff (테이블 함수) |
| `dolt_commit_diff_<table>` | 테이블별 diff |
| `dolt_history_<table>` | 테이블 전체 이력 |
| `dolt_blame_<table>` | 행별 마지막 수정자 |
| `dolt_branches` | 브랜치 목록 |
| `dolt_commits` | 모든 커밋 |
| `dolt_status` | 현재 상태 |

---

## 실습 과제

### 과제 1: 이력 추적 연습

1. 새 저장소 생성 및 테이블 만들기
2. 데이터 5회 수정, 각각 커밋
3. `dolt log`로 이력 확인
4. `dolt diff`로 각 커밋 간 차이 확인

### 과제 2: 시점 쿼리 연습

1. 과거 특정 시점의 데이터 조회 (AS OF)
2. 현재와 과거 데이터 비교 조인
3. 특정 행의 변경 이력 추적 (dolt_history)

### 과제 3: 복원 연습

1. 잘못된 데이터 변경 시뮬레이션
2. `dolt reset --hard`로 복원
3. 특정 테이블만 과거 버전으로 복원

---

## 다음 단계

- [[03-sql-operations|SQL 작업]]
- [[04-branching-merging|브랜칭과 머지]]
