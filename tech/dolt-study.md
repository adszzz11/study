# Dolt 심층 스터디 가이드

> **한 줄 정의**: Git처럼 버전 관리가 되는 SQL 데이터베이스 - 테이블을 branch, commit, merge, push, pull 할 수 있음

---

## Part 1: 개요

### 1.1 정의 및 핵심 개념

**3줄 요약**:
1. MySQL 호환 SQL 데이터베이스에 Git의 버전 관리 기능을 결합
2. 데이터의 모든 변경 이력을 추적하고, 언제든 이전 상태로 돌아갈 수 있음
3. 데이터 협업, 감사 로그, 롤백이 필요한 프로젝트에 최적

**핵심 키워드**: `#버전관리` `#SQL` `#Git` `#데이터협업` `#MySQL호환`

**Git과 Dolt 비교**:

| Git | Dolt |
|-----|------|
| 파일 버전 관리 | 테이블 버전 관리 |
| `git init` | `dolt init` |
| `git add` | `dolt add` |
| `git commit` | `dolt commit` |
| `git branch` | `dolt branch` |
| `git merge` | `dolt merge` |
| `git push` | `dolt push` |
| GitHub | DoltHub |

### 1.2 Quick Start (30초 체험)

```bash
# 1. 설치 (macOS)
brew install dolt

# Linux
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | sudo bash

# 2. 데이터베이스 생성
mkdir my_database && cd my_database
dolt init

# 3. 테이블 생성
dolt sql -q "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))"

# 4. 데이터 추가
dolt sql -q "INSERT INTO users VALUES (1, '홍길동', 'hong@example.com')"

# 5. 변경사항 커밋
dolt add .
dolt commit -m "사용자 테이블 생성"

# 6. 히스토리 확인
dolt log
```

**SQL 서버로 실행**:
```bash
# MySQL 호환 서버 시작
dolt sql-server

# 다른 터미널에서 MySQL 클라이언트로 연결
mysql -h 127.0.0.1 -u root -P 3306 my_database
```

### 1.3 왜 Dolt인가?

**장점**:
- **완전한 이력 추적**: 모든 데이터 변경의 who, what, when
- **쉬운 롤백**: 실수해도 이전 상태로 복원
- **브랜치로 실험**: 프로덕션 영향 없이 데이터 변경 테스트
- **협업**: DoltHub로 데이터 공유 및 PR
- **MySQL 호환**: 기존 도구/ORM 그대로 사용
- **감사 로그 내장**: 규정 준수(Compliance) 요구사항 충족

**단점**:
- 일반 MySQL보다 약간 느림 (버전 관리 오버헤드)
- 스토리지 사용량 증가 (히스토리 저장)
- 복잡한 머지 충돌 해결 필요할 수 있음

**주요 사용 사례**:
- ML 데이터셋 버전 관리
- 설정/구성 데이터 관리
- 감사 로그가 필요한 시스템
- 데이터 협업 프로젝트
- 스테이징/프로덕션 데이터 분리
- AI 에이전트 상태 관리

---

## Part 2: 생태계 파악

### 2.1 관련 기술/용어 맵

```
┌─────────────────────────────────────────────────────────────┐
│                    Dolt 생태계                               │
├─────────────────────────────────────────────────────────────┤
│  [Core]                                                      │
│  ├── dolt: CLI 및 데이터베이스 엔진                          │
│  ├── dolt sql: 대화형 SQL 쉘                                 │
│  └── dolt sql-server: MySQL 호환 서버                        │
│                                                              │
│  [버전 관리 명령어]                                           │
│  ├── init, add, commit, status                              │
│  ├── branch, checkout, merge                                │
│  ├── log, diff, blame                                       │
│  └── push, pull, clone, fetch                               │
│                                                              │
│  [SQL 확장]                                                  │
│  ├── dolt_log: 커밋 히스토리 테이블                           │
│  ├── dolt_diff_*: 변경사항 조회                               │
│  ├── dolt_commit(): SQL에서 커밋                             │
│  └── dolt_merge(): SQL에서 머지                              │
│                                                              │
│  [관련 제품]                                                  │
│  ├── DoltHub: 데이터 GitHub (호스팅, 협업)                    │
│  ├── Doltgres: PostgreSQL 버전 (Beta)                       │
│  └── Dolt Workbench: GUI 클라이언트                          │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 함께 자주 쓰이는 기술 스택

| 영역 | 기술 | 용도 |
|------|------|------|
| **ORM** | SQLAlchemy, Django ORM | Python 앱 연동 |
| **클라이언트** | MySQL Workbench, DBeaver | GUI 접근 |
| **ML** | DVC, MLflow | ML 파이프라인 |
| **ETL** | dbt, Airflow | 데이터 변환 |
| **복제** | MySQL Binlog | 기존 DB 동기화 |

### 2.3 경쟁/대안 기술 비교

| 기준 | Dolt | Git-LFS | DVC | LakeFS |
|------|------|---------|-----|--------|
| **대상** | 테이블 데이터 | 대용량 파일 | ML 데이터 | 데이터 레이크 |
| **SQL 지원** | 네이티브 | 없음 | 없음 | 없음 |
| **머지** | SQL 기반 | 파일 대체 | 파일 대체 | S3 기반 |
| **쿼리** | 풀 SQL | 불가 | 불가 | Spark/Presto |
| **저장소** | 로컬/DoltHub | Git 서버 | S3/GCS | S3 |

**선택 가이드**:
- **Dolt**: 구조화된 테이블 데이터, SQL 쿼리 필요
- **DVC**: ML 파이프라인, 대용량 파일
- **LakeFS**: 데이터 레이크, Spark 환경
- **Git-LFS**: 단순 파일 버전 관리

### 2.4 최신 트렌드 및 동향 (2025)

- **Doltgres Beta 출시**: PostgreSQL 호환 버전
- **AI 에이전트 통합**: 버전 관리로 에이전트 상태 안전 관리
- **Dolt Workbench**: GUI에서 diff, commit 지원
- **MySQL Replication**: 기존 MySQL → Dolt 실시간 복제
- **성능 개선**: 지속적인 쿼리 최적화

---

## Part 3: 레퍼런스

### 3.1 공식 문서 및 필수 링크

| 리소스 | URL | 설명 |
|--------|-----|------|
| 🟢 공식 문서 | [docs.dolthub.com](https://docs.dolthub.com/) | 메인 문서 |
| 🟢 GitHub | [github.com/dolthub/dolt](https://github.com/dolthub/dolt) | 소스 코드 |
| 🟢 DoltHub | [dolthub.com](https://www.dolthub.com/) | 데이터 호스팅 |
| 🟡 Dolt Workbench | [github.com/dolthub/dolt-workbench](https://github.com/dolthub/dolt-workbench) | GUI 클라이언트 |

### 3.2 추천 학습 자료

**🟢 입문**:
- [Dolt for Beginners](https://www.dolthub.com/blog/2025-01-23-dolt-basics/) - 기초 가이드
- [Git for Data](https://docs.dolthub.com/introduction/getting-started/git-for-data) - 개념 이해

**🟡 중급**:
- [Version Control in SQL](https://docs.dolthub.com/sql-reference/version-control) - SQL 버전 관리
- [Dolt Workbench Tutorial](https://www.dolthub.com/blog/2025-03-24-dolt-basics-workbench/) - GUI 사용

**🔴 고급**:
- [MySQL Replication](https://docs.dolthub.com/sql-reference/replication) - 복제 설정
- [Performance Tuning](https://docs.dolthub.com/sql-reference/benchmarks) - 성능 최적화

### 3.3 커뮤니티 및 질문할 곳

- **GitHub Issues**: [dolthub/dolt/issues](https://github.com/dolthub/dolt/issues)
- **Discord**: DoltHub 공식 커뮤니티
- **Twitter/X**: @DoltHub

---

## Part 4: 상세 학습 로드맵

### 4.1 CLI 기본 명령어

📌 **핵심 개념**

Dolt CLI는 Git CLI와 거의 동일합니다. Git을 알면 Dolt도 안다고 볼 수 있습니다.

💻 **코드 예제: 기본 워크플로우**

```bash
# 1. 데이터베이스 초기화
mkdir inventory && cd inventory
dolt init

# 2. 테이블 생성
dolt sql -q "
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2),
    stock INT DEFAULT 0
);
"

# 3. 데이터 삽입
dolt sql -q "
INSERT INTO products (name, price, stock) VALUES
    ('노트북', 1200000, 50),
    ('키보드', 80000, 200),
    ('마우스', 35000, 300);
"

# 4. 상태 확인
dolt status
# Changes not staged for commit:
#   modified:   products

# 5. 스테이징
dolt add products
# 또는 모든 변경사항
dolt add .

# 6. 커밋
dolt commit -m "상품 테이블 및 초기 데이터 추가"

# 7. 로그 확인
dolt log
# commit abc123...
# Author: Your Name <email@example.com>
# Date:   2025-01-15 10:30:00

# 8. 변경사항 보기 (diff)
dolt sql -q "UPDATE products SET price = 1100000 WHERE name = '노트북'"
dolt diff
# diff --dolt a/products b/products
# --- a/products
# +++ b/products
# | id | name   | price   | stock |
# | 1  | 노트북 | 1200000 | 50    | -> | 1100000 |
```

**브랜치 작업**:
```bash
# 1. 브랜치 생성
dolt branch feature/new-products

# 2. 브랜치 전환
dolt checkout feature/new-products

# 3. 변경 및 커밋
dolt sql -q "INSERT INTO products VALUES (4, '모니터', 500000, 30)"
dolt add .
dolt commit -m "모니터 상품 추가"

# 4. main으로 돌아가기
dolt checkout main

# 5. 머지
dolt merge feature/new-products

# 6. 브랜치 삭제
dolt branch -d feature/new-products
```

✅ **체크포인트**
- [ ] `dolt init`으로 데이터베이스를 생성할 수 있는가?
- [ ] add → commit 워크플로우를 이해하는가?
- [ ] 브랜치를 생성하고 머지할 수 있는가?

⚠️ **흔한 실수**
- `dolt add` 없이 커밋하면 변경사항 누락
- 브랜치명에 `/` 사용 가능 (Git과 동일)

🔗 **더 알아보기**: [CLI Reference](https://docs.dolthub.com/cli-reference/cli)

---

### 4.2 SQL 서버 모드

📌 **핵심 개념**

`dolt sql-server`는 MySQL 호환 서버를 시작합니다. 모든 MySQL 클라이언트와 ORM으로 연결 가능합니다.

💻 **코드 예제: 서버 운영**

```bash
# 1. 서버 시작
dolt sql-server --host 0.0.0.0 --port 3306

# 또는 백그라운드 실행
nohup dolt sql-server > dolt.log 2>&1 &

# 2. 설정 파일 사용
cat > config.yaml << EOF
listener:
  host: 0.0.0.0
  port: 3306
  max_connections: 100
behavior:
  read_only: false
  autocommit: true
user:
  name: root
  password: "secret"
EOF

dolt sql-server --config config.yaml
```

**Python 연결**:
```python
import mysql.connector
from sqlalchemy import create_engine

# mysql-connector 사용
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="inventory"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM products")
for row in cursor.fetchall():
    print(row)

# SQLAlchemy 사용
engine = create_engine("mysql+pymysql://root@localhost:3306/inventory")
with engine.connect() as conn:
    result = conn.execute("SELECT * FROM products")
    for row in result:
        print(row)
```

**Django 설정**:
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'inventory',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

✅ **체크포인트**
- [ ] `dolt sql-server`로 서버를 시작할 수 있는가?
- [ ] MySQL 클라이언트로 연결할 수 있는가?
- [ ] Python/ORM에서 Dolt에 연결할 수 있는가?

⚠️ **흔한 실수**
- 비밀번호 없이 시작하면 보안 취약
- 포트 충돌 시 다른 포트 사용

🔗 **더 알아보기**: [SQL Server](https://docs.dolthub.com/introduction/getting-started/database)

---

### 4.3 SQL로 버전 관리

📌 **핵심 개념**

Dolt의 버전 관리 기능은 SQL 함수와 시스템 테이블로도 사용할 수 있습니다. CLI 없이 SQL만으로 모든 작업이 가능합니다.

💻 **코드 예제: SQL 버전 관리**

```sql
-- 1. 현재 브랜치 확인
SELECT active_branch();
-- main

-- 2. 커밋 히스토리 조회
SELECT * FROM dolt_log LIMIT 5;

-- 3. 변경사항 확인
SELECT * FROM dolt_status;

-- 4. diff 조회 (두 커밋 간 차이)
SELECT * FROM dolt_diff_products
WHERE from_commit = 'abc123' AND to_commit = 'def456';

-- 5. SQL에서 커밋
CALL dolt_add('products');
CALL dolt_commit('-m', '가격 업데이트');

-- 6. 브랜치 생성 및 전환
CALL dolt_branch('feature/sale');
CALL dolt_checkout('feature/sale');

-- 7. 머지
CALL dolt_checkout('main');
CALL dolt_merge('feature/sale');

-- 8. 특정 시점의 데이터 조회 (Time Travel)
SELECT * FROM products AS OF 'abc123';  -- 커밋 해시

SELECT * FROM products AS OF '2025-01-01';  -- 날짜

-- 9. blame (누가 수정했는지)
SELECT * FROM dolt_blame_products;

-- 10. 롤백 (reset)
CALL dolt_reset('--hard', 'abc123');
```

**시스템 테이블**:
```sql
-- 커밋 로그
SELECT * FROM dolt_log;

-- 브랜치 목록
SELECT * FROM dolt_branches;

-- 원격 저장소
SELECT * FROM dolt_remotes;

-- 태그
SELECT * FROM dolt_tags;

-- 변경된 테이블
SELECT * FROM dolt_status;

-- 충돌 (머지 시)
SELECT * FROM dolt_conflicts;
```

✅ **체크포인트**
- [ ] `dolt_commit()` 프로시저로 SQL에서 커밋할 수 있는가?
- [ ] `AS OF`로 과거 데이터를 조회할 수 있는가?
- [ ] 시스템 테이블에서 히스토리를 확인할 수 있는가?

⚠️ **흔한 실수**
- `AS OF` 뒤에 커밋 해시 또는 날짜 문자열 사용
- `dolt_diff_*` 테이블은 테이블별로 생성됨

🔗 **더 알아보기**: [Version Control SQL](https://docs.dolthub.com/sql-reference/version-control)

---

### 4.4 DoltHub 연동

📌 **핵심 개념**

DoltHub는 Dolt 데이터베이스를 위한 GitHub입니다. 원격 저장소, 협업, 데이터 공유가 가능합니다.

💻 **코드 예제: DoltHub 사용**

```bash
# 1. 로그인
dolt login

# 2. 원격 저장소 추가
dolt remote add origin https://doltremoteapi.dolthub.com/your-org/inventory

# 3. 푸시
dolt push origin main

# 4. 클론
dolt clone your-org/inventory

# 5. 풀
dolt pull origin main

# 6. 페치
dolt fetch origin

# 7. 데이터 탐색 (웹)
# https://www.dolthub.com/repositories/your-org/inventory
```

**Pull Request 워크플로우**:
```bash
# 1. 포크 (DoltHub 웹에서)

# 2. 클론
dolt clone your-username/forked-inventory

# 3. 브랜치 생성 및 작업
dolt checkout -b fix/update-prices
dolt sql -q "UPDATE products SET price = price * 0.9"
dolt add .
dolt commit -m "10% 할인 적용"

# 4. 푸시
dolt push origin fix/update-prices

# 5. PR 생성 (DoltHub 웹에서)
```

**공개 데이터셋 사용**:
```bash
# 1. 공개 데이터 탐색
# https://www.dolthub.com/discover

# 2. 클론
dolt clone dolthub/us-housing-prices

# 3. 쿼리
cd us-housing-prices
dolt sql -q "SELECT city, AVG(price) FROM listings GROUP BY city LIMIT 10"
```

✅ **체크포인트**
- [ ] DoltHub에 데이터베이스를 푸시할 수 있는가?
- [ ] 원격 저장소에서 클론할 수 있는가?
- [ ] 공개 데이터셋을 활용할 수 있는가?

⚠️ **흔한 실수**
- 민감한 데이터는 Private 저장소 사용
- 대용량 푸시는 시간이 걸림

🔗 **더 알아보기**: [DoltHub](https://www.dolthub.com/)

---

### 4.5 MySQL Replication

📌 **핵심 개념**

기존 MySQL을 Dolt replica로 설정하면, MySQL의 모든 변경이 자동으로 Dolt 커밋이 됩니다.

💻 **코드 예제: Replication 설정**

```bash
# 1. MySQL (Source) 설정
# my.cnf에 추가:
# [mysqld]
# server-id=1
# log-bin=mysql-bin
# binlog_format=ROW

# 2. MySQL에서 복제 사용자 생성
mysql -u root -p
> CREATE USER 'replication_user'@'%' IDENTIFIED BY 'password';
> GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'%';
> FLUSH PRIVILEGES;

# 3. Dolt (Replica) 설정
cd dolt_database
dolt sql-server --config replica.yaml
```

**replica.yaml**:
```yaml
listener:
  host: 0.0.0.0
  port: 3307

replication:
  source:
    host: mysql-server
    port: 3306
    user: replication_user
    password: password
  database: production_db
  commit_on_write: true  # 모든 쓰기가 커밋됨
```

**복제 상태 확인**:
```sql
-- Dolt에서
SHOW REPLICA STATUS;

-- 커밋 로그 확인 (MySQL 변경마다 커밋)
SELECT * FROM dolt_log ORDER BY date DESC LIMIT 10;
```

✅ **체크포인트**
- [ ] MySQL binlog 복제 개념을 이해하는가?
- [ ] Dolt를 replica로 설정할 수 있는가?

⚠️ **흔한 실수**
- MySQL의 binlog_format은 ROW여야 함
- 대용량 초기 복제는 시간 소요

🔗 **더 알아보기**: [Replication](https://docs.dolthub.com/sql-reference/replication)

---

### 4.6 AI 에이전트와 Dolt

📌 **핵심 개념**

AI 에이전트가 데이터베이스를 수정할 때, Dolt의 버전 관리는 안전망 역할을 합니다.

💻 **코드 예제: 에이전트 상태 관리**

```python
import mysql.connector
from datetime import datetime

class DoltAgentState:
    """AI 에이전트의 상태를 Dolt로 관리"""

    def __init__(self, host="localhost", port=3306, database="agent_state"):
        self.conn = mysql.connector.connect(
            host=host, port=port, user="root", database=database
        )
        self.cursor = self.conn.cursor()

    def save_state(self, agent_id: str, state: dict, message: str):
        """상태 저장 및 커밋"""
        # 상태 업데이트
        self.cursor.execute("""
            INSERT INTO agent_states (agent_id, state_json, updated_at)
            VALUES (%s, %s, NOW())
            ON DUPLICATE KEY UPDATE state_json = %s, updated_at = NOW()
        """, (agent_id, str(state), str(state)))

        # 커밋
        self.cursor.execute("CALL dolt_add('agent_states')")
        self.cursor.execute("CALL dolt_commit('-m', %s)", (message,))
        self.conn.commit()

    def rollback_state(self, agent_id: str, commit_hash: str):
        """이전 상태로 롤백"""
        # 특정 커밋 시점의 상태 조회
        self.cursor.execute(f"""
            SELECT state_json FROM agent_states
            AS OF '{commit_hash}'
            WHERE agent_id = %s
        """, (agent_id,))

        old_state = self.cursor.fetchone()
        if old_state:
            # 해당 상태로 복원
            self.save_state(agent_id, old_state[0], f"Rollback to {commit_hash}")

    def get_history(self, agent_id: str, limit: int = 10):
        """상태 변경 히스토리"""
        self.cursor.execute("""
            SELECT l.commit_hash, l.message, l.date
            FROM dolt_log l
            WHERE l.message LIKE %s
            ORDER BY l.date DESC
            LIMIT %s
        """, (f"%{agent_id}%", limit))

        return self.cursor.fetchall()

# 사용 예시
state_manager = DoltAgentState(database="my_agents")

# 에이전트 상태 저장
state_manager.save_state(
    agent_id="agent_001",
    state={"task": "research", "progress": 50, "context": {...}},
    message="Research 50% complete"
)

# 문제 발생 시 롤백
state_manager.rollback_state("agent_001", "abc123")

# 히스토리 확인
history = state_manager.get_history("agent_001")
for commit in history:
    print(f"{commit[2]}: {commit[1]}")
```

**브랜치로 에이전트 실험**:
```python
def run_agent_experiment(agent_id: str, experiment_name: str):
    """브랜치에서 에이전트 실험"""
    conn = get_connection()
    cursor = conn.cursor()

    # 실험 브랜치 생성
    cursor.execute(f"CALL dolt_branch('{experiment_name}')")
    cursor.execute(f"CALL dolt_checkout('{experiment_name}')")

    try:
        # 에이전트 실행
        result = run_agent(agent_id)

        # 성공 시 main에 머지
        cursor.execute("CALL dolt_checkout('main')")
        cursor.execute(f"CALL dolt_merge('{experiment_name}')")
        cursor.execute(f"CALL dolt_branch('-d', '{experiment_name}')")

        return result

    except Exception as e:
        # 실패 시 브랜치 폐기
        cursor.execute("CALL dolt_checkout('main')")
        cursor.execute(f"CALL dolt_branch('-D', '{experiment_name}')")
        raise
```

✅ **체크포인트**
- [ ] 에이전트 상태를 Dolt로 관리할 수 있는가?
- [ ] `AS OF`로 과거 상태를 조회할 수 있는가?
- [ ] 브랜치로 실험적 실행을 할 수 있는가?

⚠️ **흔한 실수**
- 커밋이 너무 자주 되면 스토리지 증가
- 적절한 커밋 단위 결정 필요

🔗 **더 알아보기**: [Agentic Systems](https://www.dolthub.com/blog/2025-10-31-agentic-systems-need-version-control/)

---

## Part 5: 실전 프로젝트

### 5.1 미니 프로젝트 아이디어

| 난이도 | 프로젝트 | 학습 포인트 |
|--------|---------|------------|
| 🟢 | 설정 데이터 관리 시스템 | 기본 버전 관리 |
| 🟢 | 팀 스프레드시트 대체 | 협업, DoltHub |
| 🟡 | ML 데이터셋 버전 관리 | 브랜치, 태그 |
| 🟡 | 감사 로그 시스템 | 이력 추적, blame |
| 🔴 | 멀티 환경 동기화 | Replication, 머지 |

### 5.2 단계별 구현 가이드: 설정 관리 시스템

**목표**: 애플리케이션 설정을 버전 관리하고 환경별로 분리

```python
# config_manager.py
import mysql.connector
from typing import Dict, Any, Optional
import json

class ConfigManager:
    def __init__(self, host="localhost", port=3306):
        self.conn = mysql.connector.connect(
            host=host, port=port, user="root", database="app_config"
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self._init_schema()

    def _init_schema(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                `key` VARCHAR(100) PRIMARY KEY,
                value JSON NOT NULL,
                description VARCHAR(500),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def set(self, key: str, value: Any, description: str = "") -> None:
        """설정값 저장"""
        self.cursor.execute("""
            INSERT INTO config (`key`, value, description, updated_at)
            VALUES (%s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
                value = VALUES(value),
                description = VALUES(description),
                updated_at = NOW()
        """, (key, json.dumps(value), description))
        self.conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        """설정값 조회"""
        self.cursor.execute("SELECT value FROM config WHERE `key` = %s", (key,))
        row = self.cursor.fetchone()
        return json.loads(row['value']) if row else default

    def commit(self, message: str) -> str:
        """변경사항 커밋"""
        self.cursor.execute("CALL dolt_add('config')")
        self.cursor.execute("CALL dolt_commit('-m', %s)", (message,))
        self.conn.commit()

        # 커밋 해시 반환
        self.cursor.execute("SELECT commit_hash FROM dolt_log LIMIT 1")
        return self.cursor.fetchone()['commit_hash']

    def get_at(self, key: str, commit_hash: str) -> Any:
        """특정 시점의 설정값"""
        self.cursor.execute(f"""
            SELECT value FROM config AS OF '{commit_hash}' WHERE `key` = %s
        """, (key,))
        row = self.cursor.fetchone()
        return json.loads(row['value']) if row else None

    def history(self, key: str, limit: int = 10) -> list:
        """설정 변경 이력"""
        self.cursor.execute(f"""
            SELECT d.from_value, d.to_value, l.message, l.date, l.commit_hash
            FROM dolt_diff_config d
            JOIN dolt_log l ON d.to_commit = l.commit_hash
            WHERE d.`key` = %s
            ORDER BY l.date DESC
            LIMIT %s
        """, (key, limit))
        return self.cursor.fetchall()

    def switch_branch(self, branch: str) -> None:
        """환경(브랜치) 전환"""
        try:
            self.cursor.execute(f"CALL dolt_checkout('{branch}')")
        except:
            # 브랜치가 없으면 생성
            self.cursor.execute(f"CALL dolt_branch('{branch}')")
            self.cursor.execute(f"CALL dolt_checkout('{branch}')")
        self.conn.commit()


# 사용 예시
if __name__ == "__main__":
    config = ConfigManager()

    # 기본 설정
    config.set("database.pool_size", 10, "DB 연결 풀 크기")
    config.set("api.timeout", 30, "API 타임아웃 (초)")
    config.set("features.dark_mode", True, "다크 모드 활성화")
    config.commit("초기 설정 추가")

    # 개발 환경 설정
    config.switch_branch("development")
    config.set("api.timeout", 60, "개발 환경은 타임아웃 길게")
    config.set("debug", True, "디버그 모드")
    config.commit("개발 환경 설정")

    # 프로덕션 환경 설정
    config.switch_branch("production")
    config.set("database.pool_size", 50)
    config.set("api.timeout", 10)
    config.commit("프로덕션 최적화")

    # 설정 조회
    config.switch_branch("production")
    print(f"Production pool size: {config.get('database.pool_size')}")

    config.switch_branch("development")
    print(f"Development debug: {config.get('debug')}")

    # 히스토리
    for h in config.history("api.timeout"):
        print(f"{h['date']}: {h['from_value']} -> {h['to_value']}")
```

### 5.3 Best Practices

**프로젝트 구조**:
```
dolt-project/
├── databases/
│   ├── app_config/     # 설정 DB
│   └── user_data/      # 사용자 데이터 DB
├── scripts/
│   ├── init.sql        # 스키마 초기화
│   └── seed.sql        # 초기 데이터
├── config/
│   └── dolt-server.yaml
└── docker-compose.yml
```

**운영 권장사항**:

1. **커밋 전략**: 의미 있는 단위로 커밋 (트랜잭션 단위)
2. **브랜치 전략**: 환경별 브랜치 (dev, staging, prod)
3. **백업**: DoltHub에 정기 푸시
4. **모니터링**: 커밋 빈도, 스토리지 사용량 추적
5. **정리**: 오래된 브랜치 삭제, gc 실행

```bash
# 가비지 컬렉션
dolt gc

# 오래된 브랜치 정리
dolt branch -d old-feature-branch

# 스토리지 확인
du -sh .dolt/
```

---

## 요약

Dolt는 데이터에 Git의 힘을 더합니다:

- **핵심 가치**: 모든 데이터 변경을 추적하고 되돌릴 수 있음
- **사용법**: Git CLI와 동일 + SQL로도 가능
- **호환성**: MySQL 100% 호환, 기존 도구 사용 가능
- **협업**: DoltHub로 데이터 공유 및 PR

다음 단계:
1. `dolt init`으로 첫 데이터베이스 생성
2. 기존 프로젝트의 설정 데이터를 Dolt로 관리
3. DoltHub에 공개 데이터셋 탐색
