# Dolt 치트시트

## 설치 및 설정

```bash
# 설치 (Linux/macOS)
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | sudo bash

# macOS (Homebrew)
brew install dolt

# 버전 확인
dolt version

# 사용자 설정
dolt config --global --add user.email "email@example.com"
dolt config --global --add user.name "Your Name"
```

---

## 저장소 작업

```bash
# 초기화
dolt init

# 클론
dolt clone <remote-url>
dolt clone dolthub/museum-collections

# 상태 확인
dolt status
```

---

## 버전 관리

### 기본 명령어

```bash
# 스테이징
dolt add <table>
dolt add .

# 커밋
dolt commit -m "메시지"
dolt commit -am "스테이징 + 커밋"

# 로그
dolt log
dolt log --oneline
dolt log -n 5

# 차이점
dolt diff
dolt diff <table>
dolt diff HEAD~1 HEAD
```

### 리셋

```bash
# 스테이징 취소
dolt reset <table>
dolt reset

# 변경 폐기 (주의!)
dolt reset --hard
dolt reset --hard HEAD~2
```

---

## 브랜치

```bash
# 목록
dolt branch
dolt branch -a

# 생성
dolt branch <name>
dolt checkout -b <name>

# 이동
dolt checkout <branch>

# 삭제
dolt branch -d <name>
dolt branch -D <name>  # 강제

# 머지
dolt checkout main
dolt merge <branch>
```

---

## 원격 저장소

```bash
# 원격 추가
dolt remote add origin <url>

# 원격 목록
dolt remote -v

# 푸시
dolt push origin main
dolt push -u origin main

# 풀
dolt pull origin main

# 페치
dolt fetch origin
```

---

## SQL 작업

### SQL 실행

```bash
# 대화형 쉘
dolt sql

# 단일 쿼리
dolt sql -q "SELECT * FROM users"

# 파일 실행
dolt sql < script.sql
```

### SQL 서버

```bash
# 서버 시작
dolt sql-server
dolt sql-server -P 3307

# MySQL 클라이언트 접속
mysql -h 127.0.0.1 -P 3306 -u root
```

### 데이터 임포트/익스포트

```bash
# 임포트
dolt table import -c <table> <file.csv>
dolt table import -u <table> <file.csv>  # 업데이트

# 익스포트
dolt table export <table> <file.csv>
dolt dump > backup.sql
```

---

## 자주 쓰는 SQL

### 스키마

```sql
-- 테이블 생성
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- 테이블 수정
ALTER TABLE users ADD COLUMN age INT;
ALTER TABLE users DROP COLUMN age;

-- 테이블 목록
SHOW TABLES;
DESCRIBE users;
```

### CRUD

```sql
-- 삽입
INSERT INTO users (name, email) VALUES ('홍길동', 'hong@example.com');

-- 조회
SELECT * FROM users WHERE id = 1;

-- 수정
UPDATE users SET name = '김철수' WHERE id = 1;

-- 삭제
DELETE FROM users WHERE id = 1;
```

### 인덱스

```sql
-- 생성
CREATE INDEX idx_users_email ON users(email);

-- 확인
SHOW INDEX FROM users;

-- 삭제
DROP INDEX idx_users_email ON users;
```

---

## Dolt 시스템 테이블

```sql
-- 커밋 로그
SELECT * FROM dolt_log;

-- 브랜치 목록
SELECT * FROM dolt_branches;

-- 현재 상태
SELECT * FROM dolt_status;

-- 테이블 변경 이력
SELECT * FROM dolt_history_<table>;

-- 행별 마지막 수정자
SELECT * FROM dolt_blame_<table>;

-- 충돌 확인
SELECT * FROM dolt_conflicts;
SELECT * FROM dolt_conflicts_<table>;
```

---

## Dolt SQL 함수

```sql
-- 버전 관리
CALL dolt_add('users');
CALL dolt_commit('-m', '메시지');
CALL dolt_checkout('branch-name');
CALL dolt_checkout('-b', 'new-branch');
CALL dolt_branch('new-branch');
CALL dolt_merge('branch-name');

-- 현재 브랜치
SELECT active_branch();

-- 커밋 해시
SELECT dolt_hashof('HEAD');
```

---

## 시점 쿼리 (Time Travel)

```sql
-- 특정 커밋 시점
SELECT * FROM users AS OF 'abc123';

-- 상대 참조
SELECT * FROM users AS OF 'HEAD~3';

-- 브랜치 시점
SELECT * FROM users AS OF 'feature/old';

-- 타임스탬프
SELECT * FROM users AS OF '2024-01-01';

-- diff 조회
SELECT * FROM dolt_diff('HEAD~1', 'HEAD', 'users');
```

---

## 충돌 해결

```bash
# 머지 시 충돌 발생 시
dolt merge feature
# CONFLICT...

# 상태 확인
dolt status

# 충돌 내용 확인 (SQL)
SELECT * FROM dolt_conflicts_<table>;

# 해결 후 커밋
dolt add .
dolt commit -m "충돌 해결"

# 또는 머지 취소
dolt merge --abort
```

```sql
-- SQL에서 충돌 해결
CALL dolt_conflicts_resolve('--ours', 'users');   -- 현재 브랜치 값
CALL dolt_conflicts_resolve('--theirs', 'users'); -- 머지 브랜치 값
```

---

## DoltHub

```bash
# 로그인
dolt login

# 클론 (DoltHub)
dolt clone dolthub/<repo>
dolt clone <username>/<repo>

# 원격 추가 (DoltHub)
dolt remote add origin <username>/<repo>
```

---

## 자주 쓰는 패턴

### 새 기능 작업

```bash
dolt checkout -b feature/new-data
# 작업...
dolt add .
dolt commit -m "새 기능 추가"
dolt checkout main
dolt merge feature/new-data
dolt branch -d feature/new-data
```

### 데이터 백업

```bash
dolt tag "backup-$(date +%Y%m%d)"
dolt push origin --tags
```

### 특정 테이블 복구

```bash
dolt checkout HEAD~1 -- users
dolt add users
dolt commit -m "users 테이블 이전 버전으로 복구"
```

### 현재와 과거 비교

```sql
SELECT
    curr.id,
    curr.price as current_price,
    old.price as old_price
FROM products AS curr
JOIN products AS OF 'HEAD~5' AS old ON curr.id = old.id
WHERE curr.price != old.price;
```

---

## 유용한 옵션

```bash
# 로그 포맷
dolt log --oneline --graph

# diff 포맷
dolt diff --sql          # SQL 형식
dolt diff --stat         # 통계만

# SQL 결과 포맷
dolt sql -q "..." -r csv   # CSV
dolt sql -q "..." -r json  # JSON
dolt sql -q "..." -r table # 테이블 (기본)
```

---

## 문제 해결

```bash
# 로컬 변경 모두 폐기
dolt reset --hard

# 설정 확인
dolt config --list

# 저장소 정보
dolt status
dolt log --oneline -5

# SQL 서버 포트 충돌
dolt sql-server -P 3307
```

---

## 참고 링크

- 공식 문서: https://docs.dolthub.com
- CLI 레퍼런스: https://docs.dolthub.com/cli-reference/cli
- GitHub: https://github.com/dolthub/dolt
- Discord: https://discord.gg/gqr7K4VNKe
