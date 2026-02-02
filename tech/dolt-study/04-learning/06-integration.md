# 프로그래밍 언어 통합

## 통합 방법 개요

Dolt와 애플리케이션 통합 방법:

| 방법 | 설명 | 적합한 경우 |
|------|------|------------|
| **MySQL 드라이버** | 기존 MySQL 커넥터 사용 | 기존 코드 마이그레이션 |
| **doltpy** | Python 전용 라이브러리 | Python 애플리케이션, 데이터 분석 |
| **go-dolt** | Go 네이티브 | Go 애플리케이션 |
| **CLI 호출** | subprocess로 dolt 명령 실행 | 간단한 스크립트 |

---

## Python 통합

### MySQL 커넥터 사용

#### 설치

```bash
pip install mysql-connector-python
# 또는
pip install pymysql
```

#### 연결 및 쿼리

```python
import mysql.connector

# Dolt SQL 서버에 연결
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="my_dolt_db"
)

cursor = conn.cursor()

# 쿼리 실행
cursor.execute("SELECT * FROM products")
for row in cursor.fetchall():
    print(row)

# 데이터 삽입
cursor.execute(
    "INSERT INTO products (name, price) VALUES (%s, %s)",
    ("새 상품", 10000)
)
conn.commit()

cursor.close()
conn.close()
```

### doltpy 라이브러리

#### 설치

```bash
pip install doltpy
```

#### 기본 사용법

```python
from doltpy.core import Dolt

# 기존 저장소 열기
dolt = Dolt("/path/to/dolt-repo")

# 또는 클론
dolt = Dolt.clone("dolthub/museum-collections")

# 또는 초기화
dolt = Dolt.init("/path/to/new-repo")
```

#### SQL 실행

```python
from doltpy.core import Dolt

dolt = Dolt("/path/to/repo")

# SELECT 쿼리
result = dolt.sql("SELECT * FROM products", result_format="csv")
print(result)

# DataFrame으로 변환
import pandas as pd
df = pd.read_csv(result)

# 데이터 수정
dolt.sql("INSERT INTO products (name, price) VALUES ('새 상품', 10000)")
```

#### 버전 관리 작업

```python
from doltpy.core import Dolt

dolt = Dolt("/path/to/repo")

# 상태 확인
status = dolt.status()
print(status)

# 스테이징 및 커밋
dolt.add("products")
dolt.commit("제품 데이터 업데이트")

# 로그 확인
logs = dolt.log()
for log in logs:
    print(f"{log.commit}: {log.message}")

# 브랜치 작업
dolt.branch("feature/new-data")
dolt.checkout("feature/new-data")

# 머지
dolt.checkout("main")
dolt.merge("feature/new-data")
```

#### DataFrame 활용

```python
import pandas as pd
from doltpy.core import Dolt
from doltpy.core.write import import_df

dolt = Dolt("/path/to/repo")

# DataFrame을 테이블로 저장
df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["A", "B", "C"],
    "value": [100, 200, 300]
})

import_df(
    dolt,
    table_name="my_table",
    df=df,
    primary_keys=["id"],
    import_mode="create"  # create, update, replace
)

# 커밋
dolt.add("my_table")
dolt.commit("DataFrame에서 테이블 생성")
```

---

## Go 통합

### MySQL 드라이버 사용

```go
package main

import (
    "database/sql"
    "fmt"
    "log"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // Dolt SQL 서버에 연결
    db, err := sql.Open("mysql", "root:@tcp(127.0.0.1:3306)/my_dolt_db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // 쿼리 실행
    rows, err := db.Query("SELECT id, name, price FROM products")
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    for rows.Next() {
        var id int
        var name string
        var price float64
        rows.Scan(&id, &name, &price)
        fmt.Printf("ID: %d, Name: %s, Price: %.2f\n", id, name, price)
    }
}
```

### go-dolt (Dolt 내장)

```go
package main

import (
    "context"
    "fmt"

    "github.com/dolthub/dolt/go/libraries/doltcore/doltdb"
    "github.com/dolthub/dolt/go/libraries/doltcore/env"
    "github.com/dolthub/dolt/go/libraries/utils/filesys"
)

func main() {
    ctx := context.Background()
    fs := filesys.LocalFS

    // 저장소 열기
    dEnv := env.Load(ctx, env.GetCurrentUserHomeDir, fs, "/path/to/repo", "0.0.0")

    // 작업 수행...
}
```

---

## JavaScript/Node.js 통합

### mysql2 패키지

```bash
npm install mysql2
```

```javascript
const mysql = require('mysql2/promise');

async function main() {
    // 연결
    const connection = await mysql.createConnection({
        host: '127.0.0.1',
        port: 3306,
        user: 'root',
        database: 'my_dolt_db'
    });

    // 쿼리 실행
    const [rows] = await connection.execute('SELECT * FROM products');
    console.log(rows);

    // 데이터 삽입
    await connection.execute(
        'INSERT INTO products (name, price) VALUES (?, ?)',
        ['새 상품', 10000]
    );

    // Dolt 커밋
    await connection.execute("CALL dolt_commit('-am', '새 상품 추가')");

    await connection.end();
}

main();
```

### TypeScript 타입

```typescript
interface Product {
    id: number;
    name: string;
    price: number;
}

const [rows] = await connection.execute<Product[]>(
    'SELECT * FROM products'
);
```

---

## Java 통합

### JDBC 연결

```java
import java.sql.*;

public class DoltExample {
    public static void main(String[] args) {
        String url = "jdbc:mysql://127.0.0.1:3306/my_dolt_db";
        String user = "root";
        String password = "";

        try (Connection conn = DriverManager.getConnection(url, user, password)) {
            // 쿼리 실행
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM products");

            while (rs.next()) {
                System.out.printf("ID: %d, Name: %s, Price: %.2f%n",
                    rs.getInt("id"),
                    rs.getString("name"),
                    rs.getDouble("price"));
            }

            // 데이터 삽입
            PreparedStatement pstmt = conn.prepareStatement(
                "INSERT INTO products (name, price) VALUES (?, ?)"
            );
            pstmt.setString(1, "새 상품");
            pstmt.setDouble(2, 10000);
            pstmt.executeUpdate();

            // Dolt 커밋
            stmt.execute("CALL dolt_commit('-am', '새 상품 추가')");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

---

## CLI 호출 방식

### Python subprocess

```python
import subprocess
import json

def dolt_sql(query, repo_path):
    """Dolt SQL 쿼리 실행"""
    result = subprocess.run(
        ["dolt", "sql", "-q", query, "-r", "json"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def dolt_commit(message, repo_path):
    """변경사항 커밋"""
    subprocess.run(["dolt", "add", "."], cwd=repo_path)
    subprocess.run(["dolt", "commit", "-m", message], cwd=repo_path)

# 사용 예
repo = "/path/to/repo"
data = dolt_sql("SELECT * FROM products", repo)
print(data)

dolt_sql("INSERT INTO products (name, price) VALUES ('새 상품', 10000)", repo)
dolt_commit("새 상품 추가", repo)
```

### Bash 스크립트

```bash
#!/bin/bash

REPO_PATH="/path/to/dolt-repo"
cd "$REPO_PATH"

# 쿼리 실행
dolt sql -q "SELECT * FROM products" -r csv > products.csv

# 데이터 업데이트
dolt sql -q "UPDATE products SET price = price * 1.1 WHERE category = 'electronics'"

# 커밋
dolt add .
dolt commit -m "전자제품 가격 10% 인상"

# 원격 푸시
dolt push origin main
```

---

## ORM 통합

### SQLAlchemy (Python)

```python
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 엔진 생성 (MySQL 방언 사용)
engine = create_engine('mysql+pymysql://root:@127.0.0.1:3306/my_dolt_db')

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# 조회
products = session.query(Product).all()
for p in products:
    print(f"{p.name}: {p.price}")

# 추가
new_product = Product(name="새 상품", price=10000)
session.add(new_product)
session.commit()

# Dolt 커밋 (raw SQL)
session.execute("CALL dolt_commit('-am', 'ORM으로 상품 추가')")
```

### GORM (Go)

```go
package main

import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

type Product struct {
    ID    uint    `gorm:"primaryKey"`
    Name  string  `gorm:"size:100"`
    Price float64
}

func main() {
    dsn := "root:@tcp(127.0.0.1:3306)/my_dolt_db?parseTime=true"
    db, _ := gorm.Open(mysql.Open(dsn), &gorm.Config{})

    // 조회
    var products []Product
    db.Find(&products)

    // 추가
    db.Create(&Product{Name: "새 상품", Price: 10000})

    // Dolt 커밋
    db.Exec("CALL dolt_commit('-am', 'GORM으로 상품 추가')")
}
```

---

## 데이터 파이프라인 예제

### ETL 파이프라인 (Python)

```python
import pandas as pd
from doltpy.core import Dolt
from doltpy.core.write import import_df

def extract():
    """외부 소스에서 데이터 추출"""
    return pd.read_csv("https://example.com/data.csv")

def transform(df):
    """데이터 변환"""
    df['processed_at'] = pd.Timestamp.now()
    df = df.dropna()
    return df

def load(df, dolt_repo):
    """Dolt에 로드"""
    import_df(
        dolt_repo,
        table_name="processed_data",
        df=df,
        primary_keys=["id"],
        import_mode="update"
    )
    dolt_repo.add("processed_data")
    dolt_repo.commit(f"ETL 실행: {pd.Timestamp.now()}")

def main():
    dolt = Dolt("/path/to/repo")

    # ETL 실행
    raw_data = extract()
    processed_data = transform(raw_data)
    load(processed_data, dolt)

    # 원격 푸시
    dolt.push("origin", "main")

if __name__ == "__main__":
    main()
```

### Airflow DAG 예제

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from doltpy.core import Dolt

def sync_data():
    dolt = Dolt("/opt/dolt/my-db")

    # 원격에서 최신 데이터 가져오기
    dolt.pull("origin", "main")

    # 데이터 처리...

    # 변경사항 푸시
    dolt.add(".")
    dolt.commit("자동 동기화")
    dolt.push("origin", "main")

dag = DAG(
    'dolt_sync',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly'
)

sync_task = PythonOperator(
    task_id='sync_dolt_data',
    python_callable=sync_data,
    dag=dag
)
```

---

## 테스트 환경 구성

### pytest fixture

```python
import pytest
from doltpy.core import Dolt
import tempfile
import shutil

@pytest.fixture
def dolt_repo():
    """테스트용 임시 Dolt 저장소"""
    temp_dir = tempfile.mkdtemp()
    dolt = Dolt.init(temp_dir)

    # 테스트 스키마 설정
    dolt.sql("""
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name VARCHAR(100)
        )
    """)
    dolt.add(".")
    dolt.commit("초기 스키마")

    yield dolt

    # 정리
    shutil.rmtree(temp_dir)

def test_insert_user(dolt_repo):
    dolt_repo.sql("INSERT INTO users VALUES (1, 'Test User')")
    result = dolt_repo.sql("SELECT * FROM users", result_format="json")
    assert len(result['rows']) == 1
```

---

## 실습 과제

### 과제 1: Python 연동

1. doltpy 설치
2. 로컬 저장소 생성
3. DataFrame 데이터 저장
4. 버전 관리 작업 수행

### 과제 2: REST API 서버

1. Flask/FastAPI로 API 서버 구축
2. Dolt를 백엔드 DB로 사용
3. CRUD 엔드포인트 구현
4. 버전 이력 조회 API 추가

### 과제 3: 데이터 파이프라인

1. 외부 데이터 소스에서 데이터 수집
2. 데이터 변환 및 정제
3. Dolt에 저장 및 커밋
4. 스케줄링 설정

---

## 다음 단계

- [[../05-projects|실전 프로젝트]]
- [[../cheatsheet|치트시트]]
