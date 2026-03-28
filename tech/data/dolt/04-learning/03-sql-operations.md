# SQL 작업

## SQL 실행 방법

### 1. SQL 쉘

```bash
# 대화형 쉘
dolt sql

# 프롬프트
my_database>
```

쉘 명령어:
- `exit` 또는 `quit`: 종료
- `\G`: 결과를 세로로 표시
- `source <file>`: SQL 파일 실행

### 2. 단일 쿼리 실행

```bash
dolt sql -q "SELECT * FROM products"
```

### 3. SQL 파일 실행

```bash
dolt sql < script.sql

# 또는
dolt sql -q "source script.sql"
```

### 4. SQL 서버 모드

```bash
# 서버 시작
dolt sql-server -P 3306

# 클라이언트 접속
mysql -h 127.0.0.1 -P 3306 -u root
```

---

## 스키마 작업

### 테이블 생성

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 지원되는 데이터 타입

| 카테고리 | 타입 |
|----------|------|
| **정수** | TINYINT, SMALLINT, MEDIUMINT, INT, BIGINT |
| **실수** | FLOAT, DOUBLE, DECIMAL |
| **문자열** | CHAR, VARCHAR, TEXT, MEDIUMTEXT, LONGTEXT |
| **날짜/시간** | DATE, TIME, DATETIME, TIMESTAMP, YEAR |
| **이진** | BINARY, VARBINARY, BLOB |
| **기타** | BOOLEAN, ENUM, SET, JSON |

### 테이블 수정

```sql
-- 컬럼 추가
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- 컬럼 수정
ALTER TABLE users MODIFY COLUMN phone VARCHAR(30);

-- 컬럼 이름 변경
ALTER TABLE users CHANGE COLUMN phone phone_number VARCHAR(30);

-- 컬럼 삭제
ALTER TABLE users DROP COLUMN phone_number;

-- 테이블 이름 변경
RENAME TABLE users TO members;

-- 테이블 삭제
DROP TABLE IF EXISTS temp_table;
```

### 스키마 확인

```sql
-- 테이블 목록
SHOW TABLES;

-- 테이블 구조
DESCRIBE users;
-- 또는
SHOW CREATE TABLE users;

-- 전체 스키마
SHOW CREATE DATABASE my_database;
```

---

## CRUD 작업

### CREATE (삽입)

```sql
-- 단일 행
INSERT INTO users (username, email, password_hash)
VALUES ('john_doe', 'john@example.com', 'hashed_password');

-- 다중 행
INSERT INTO users (username, email, password_hash) VALUES
    ('jane_doe', 'jane@example.com', 'hash1'),
    ('bob_smith', 'bob@example.com', 'hash2'),
    ('alice_kim', 'alice@example.com', 'hash3');

-- 다른 테이블에서 삽입
INSERT INTO archived_users
SELECT * FROM users WHERE is_active = FALSE;
```

### READ (조회)

```sql
-- 기본 조회
SELECT * FROM users;

-- 특정 컬럼
SELECT username, email FROM users;

-- 조건부 조회
SELECT * FROM users WHERE is_active = TRUE;

-- 정렬
SELECT * FROM users ORDER BY created_at DESC;

-- 페이지네이션
SELECT * FROM users LIMIT 10 OFFSET 20;

-- 집계
SELECT COUNT(*) FROM users;
SELECT status, COUNT(*) as count FROM posts GROUP BY status;
```

### UPDATE (수정)

```sql
-- 단일 행
UPDATE users SET email = 'new@example.com' WHERE id = 1;

-- 조건부 수정
UPDATE posts SET status = 'archived'
WHERE status = 'published' AND created_at < '2023-01-01';

-- 다중 컬럼 수정
UPDATE users
SET email = 'updated@example.com', is_active = FALSE
WHERE id = 1;
```

### DELETE (삭제)

```sql
-- 조건부 삭제
DELETE FROM users WHERE id = 1;

-- 다중 행 삭제
DELETE FROM posts WHERE status = 'draft' AND created_at < '2023-01-01';

-- 전체 삭제 (테이블 구조 유지)
DELETE FROM temp_table;
-- 또는
TRUNCATE TABLE temp_table;
```

---

## 조인

### INNER JOIN

```sql
SELECT
    u.username,
    p.title,
    p.created_at
FROM users u
INNER JOIN posts p ON u.id = p.user_id;
```

### LEFT JOIN

```sql
-- 글이 없는 사용자도 포함
SELECT
    u.username,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;
```

### 다중 테이블 조인

```sql
SELECT
    u.username,
    p.title,
    c.content as comment
FROM users u
INNER JOIN posts p ON u.id = p.user_id
INNER JOIN comments c ON p.id = c.post_id
WHERE p.status = 'published';
```

---

## 인덱스

### 인덱스 생성

```sql
-- 단일 컬럼 인덱스
CREATE INDEX idx_users_email ON users(email);

-- 복합 인덱스
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- 유니크 인덱스
CREATE UNIQUE INDEX idx_users_username ON users(username);
```

### 인덱스 확인

```sql
SHOW INDEX FROM users;
```

### 인덱스 삭제

```sql
DROP INDEX idx_users_email ON users;
```

### 인덱스 전략

```sql
-- 자주 검색하는 컬럼에 인덱스
CREATE INDEX idx_posts_status ON posts(status);

-- 조인 키에 인덱스 (FK)
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- 정렬 컬럼에 인덱스
CREATE INDEX idx_posts_created_at ON posts(created_at);

-- 복합 조건에 복합 인덱스
CREATE INDEX idx_posts_user_status_date ON posts(user_id, status, created_at);
```

---

## 트랜잭션

### 기본 트랜잭션

```sql
START TRANSACTION;

INSERT INTO users (username, email, password_hash)
VALUES ('new_user', 'new@example.com', 'hash');

INSERT INTO user_profiles (user_id, bio)
VALUES (LAST_INSERT_ID(), 'Hello!');

COMMIT;
```

### 롤백

```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;

-- 문제 발생 시
ROLLBACK;

-- 정상이면
COMMIT;
```

### Dolt 커밋과의 관계

```sql
-- SQL 트랜잭션 커밋 (데이터 반영)
COMMIT;

-- Dolt 버전 커밋 (이력 저장)
CALL dolt_commit('-am', '계좌 이체 처리');
```

---

## Dolt 전용 SQL 함수

### 버전 관리 함수

```sql
-- 현재 커밋
SELECT dolt_hashof('HEAD');

-- 브랜치 확인
SELECT active_branch();

-- 커밋
CALL dolt_commit('-m', '변경사항 저장');

-- 스테이징
CALL dolt_add('users');

-- 브랜치 생성
CALL dolt_branch('feature/new');

-- 체크아웃
CALL dolt_checkout('feature/new');

-- 머지
CALL dolt_merge('feature/new');
```

### 시스템 테이블 활용

```sql
-- 현재 상태
SELECT * FROM dolt_status;

-- 브랜치 목록
SELECT * FROM dolt_branches;

-- 최근 커밋
SELECT * FROM dolt_log LIMIT 5;

-- 테이블 변경 이력
SELECT * FROM dolt_history_users WHERE id = 1;
```

---

## 뷰 (View)

### 뷰 생성

```sql
CREATE VIEW active_users AS
SELECT id, username, email, created_at
FROM users
WHERE is_active = TRUE;

CREATE VIEW post_summary AS
SELECT
    u.username,
    p.title,
    p.status,
    p.created_at
FROM posts p
JOIN users u ON p.user_id = u.id;
```

### 뷰 사용

```sql
SELECT * FROM active_users;
SELECT * FROM post_summary WHERE status = 'published';
```

### 뷰 삭제

```sql
DROP VIEW IF EXISTS active_users;
```

---

## 고급 쿼리

### 서브쿼리

```sql
-- 가장 많은 글을 쓴 사용자
SELECT username FROM users
WHERE id = (
    SELECT user_id FROM posts
    GROUP BY user_id
    ORDER BY COUNT(*) DESC
    LIMIT 1
);

-- IN 서브쿼리
SELECT * FROM users
WHERE id IN (
    SELECT DISTINCT user_id FROM posts WHERE status = 'published'
);
```

### CTE (Common Table Expression)

```sql
WITH post_counts AS (
    SELECT user_id, COUNT(*) as cnt
    FROM posts
    GROUP BY user_id
)
SELECT u.username, COALESCE(pc.cnt, 0) as post_count
FROM users u
LEFT JOIN post_counts pc ON u.id = pc.user_id
ORDER BY post_count DESC;
```

### 윈도우 함수

```sql
-- 순위
SELECT
    username,
    post_count,
    RANK() OVER (ORDER BY post_count DESC) as rank
FROM (
    SELECT u.username, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    GROUP BY u.id, u.username
) as user_posts;
```

---

## 데이터 임포트/엑스포트

### CSV 임포트

```bash
# CLI에서
dolt table import -c products products.csv

# 기존 테이블에 추가
dolt table import -u products new_products.csv
```

### SQL에서 LOAD DATA

```sql
LOAD DATA INFILE '/path/to/data.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### 데이터 내보내기

```bash
# CSV로 내보내기
dolt table export products products_backup.csv

# SQL 덤프
dolt dump > backup.sql
```

---

## 실습 과제

### 과제 1: 스키마 설계

전자상거래 데이터베이스 설계:
- customers (고객)
- products (상품)
- orders (주문)
- order_items (주문 항목)
- 적절한 FK와 인덱스 설정

### 과제 2: 복잡한 쿼리 작성

1. 월별 매출 집계
2. 가장 많이 팔린 상품 TOP 10
3. 고객별 구매 금액 순위

### 과제 3: 시점 쿼리 활용

1. 과거 특정 시점의 상품 가격 조회
2. 가격 변동 이력 추적
3. 현재와 과거 데이터 비교 리포트

---

## 다음 단계

- [[04-branching-merging|브랜칭과 머지]]
- [[05-dolthub|DoltHub]]
