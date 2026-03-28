# Dolt 설치 및 기본 사용

## 설치 방법

### Linux / macOS (권장)

```bash
# 공식 설치 스크립트
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | sudo bash
```

### macOS (Homebrew)

```bash
brew install dolt
```

### Windows

```powershell
# Chocolatey
choco install dolt

# 또는 MSI 설치 파일 다운로드
# https://github.com/dolthub/dolt/releases
```

### Docker

```bash
# 이미지 풀
docker pull dolthub/dolt:latest

# 실행
docker run -it dolthub/dolt:latest
```

### 설치 확인

```bash
dolt version
# dolt version x.x.x
```

---

## 초기 설정

### 사용자 설정 (필수)

```bash
# 전역 설정
dolt config --global --add user.email "your-email@example.com"
dolt config --global --add user.name "Your Name"

# 설정 확인
dolt config --list
```

### 에디터 설정 (선택)

```bash
# 커밋 메시지 에디터
dolt config --global --add core.editor "vim"
# 또는 "code --wait", "nano" 등
```

---

## 첫 번째 데이터베이스 만들기

### 1. 디렉토리 생성 및 초기화

```bash
# 작업 디렉토리 생성
mkdir my-first-dolt
cd my-first-dolt

# Dolt 저장소 초기화
dolt init
```

초기화 후 디렉토리 구조:

```
my-first-dolt/
└── .dolt/
    ├── config.json
    ├── noms/
    └── ...
```

### 2. SQL 쉘 시작

```bash
dolt sql
```

```sql
-- 프롬프트
my_first_dolt>
```

### 3. 테이블 생성

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2),
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. 데이터 삽입

```sql
INSERT INTO products (name, price, category) VALUES
    ('노트북', 1500000, '전자제품'),
    ('마우스', 35000, '전자제품'),
    ('책상', 250000, '가구'),
    ('의자', 180000, '가구');

-- 확인
SELECT * FROM products;
```

### 5. 변경사항 확인 및 커밋

```bash
# SQL 쉘 종료
exit;

# 상태 확인
dolt status
# Changes not staged for commit:
#   new table:        products

# 스테이징
dolt add products
# 또는
dolt add .

# 커밋
dolt commit -m "products 테이블 생성 및 초기 데이터 추가"

# 로그 확인
dolt log
```

---

## 기본 명령어

### 저장소 관리

```bash
# 초기화
dolt init

# 상태 확인
dolt status

# 변경사항 스테이징
dolt add <table>
dolt add .          # 모든 테이블

# 커밋
dolt commit -m "메시지"

# 로그 확인
dolt log
dolt log --oneline
```

### SQL 작업

```bash
# SQL 쉘 시작
dolt sql

# 단일 쿼리 실행
dolt sql -q "SELECT * FROM products"

# SQL 파일 실행
dolt sql < script.sql
```

### 차이점 확인

```bash
# 스테이징되지 않은 변경사항
dolt diff

# 특정 테이블
dolt diff products

# 커밋 간 비교
dolt diff HEAD~1 HEAD
```

---

## SQL 서버 모드

### 서버 시작

```bash
# 기본 포트 (3306)
dolt sql-server

# 포트 지정
dolt sql-server -P 3307

# 백그라운드 실행
dolt sql-server &
```

### MySQL 클라이언트로 접속

```bash
mysql -h 127.0.0.1 -P 3306 -u root

# 또는 비밀번호 설정 시
mysql -h 127.0.0.1 -P 3306 -u root -p
```

### 서버 설정 파일

```yaml
# .dolt/config.yaml
log_level: info
listener:
  host: 0.0.0.0
  port: 3306
  max_connections: 100
user:
  name: root
  password: ""
```

---

## 데이터 가져오기

### CSV 파일

```bash
# 기본 임포트
dolt table import -c products products.csv

# 옵션 지정
dolt table import -c \
    --pk id \
    products \
    products.csv
```

### JSON 파일

```bash
dolt table import -c products products.json
```

### SQL 덤프

```bash
dolt sql < dump.sql
```

---

## 데이터 내보내기

### CSV 내보내기

```bash
dolt table export products products.csv
```

### SQL 덤프

```bash
dolt dump > backup.sql
```

---

## 디렉토리 구조 이해

```
my-dolt-db/
├── .dolt/                 # Dolt 메타데이터
│   ├── config.json        # 로컬 설정
│   ├── noms/              # 데이터 저장소
│   │   ├── chunks/        # 실제 데이터
│   │   └── manifest       # 청크 인덱스
│   └── repo_state.json    # 현재 상태
└── (작업 디렉토리는 비어있음)
```

---

## 문제 해결

### 권한 오류

```bash
# Linux/macOS 설치 시 권한 오류
sudo chown -R $(whoami) /usr/local/bin/dolt
```

### 포트 충돌

```bash
# 다른 포트 사용
dolt sql-server -P 3307

# 또는 기존 MySQL 중지
sudo systemctl stop mysql
```

### 설정 초기화

```bash
# 로컬 설정 삭제
rm -rf .dolt

# 전역 설정 위치
# Linux/macOS: ~/.dolt
# Windows: %USERPROFILE%\.dolt
```

---

## 실습 과제

### 과제 1: 첫 번째 저장소 만들기

1. `practice-dolt` 디렉토리 생성
2. Dolt 초기화
3. `users` 테이블 생성 (id, name, email, age)
4. 5명의 사용자 데이터 추가
5. 커밋

### 과제 2: 데이터 수정 및 이력 확인

1. 사용자 한 명의 이메일 수정
2. diff로 변경사항 확인
3. 커밋
4. log로 커밋 이력 확인

### 과제 3: 데이터 가져오기

1. CSV 파일 생성 (orders.csv)
2. orders 테이블로 임포트
3. 데이터 확인 및 커밋

---

## 다음 단계

- [[02-git-for-data|Git 명령어와 데이터 버전 관리]]
- [[03-sql-operations|SQL 작업]]
