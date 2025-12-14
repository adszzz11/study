# ZonAgent 개발 환경 설정 가이드

> Phase A 시작을 위한 상세 설정 가이드

---

## 📋 사전 요구사항

### 필수 소프트웨어

| 항목 | 버전 | 설치 확인 명령어 | 설치 방법 (macOS) |
|------|------|------------------|-------------------|
| Python | 3.11+ | `python3 --version` | `brew install python@3.11` |
| Java | 17+ | `java -version` | `brew install openjdk@17` |
| PostgreSQL | 14+ | `psql --version` | `brew install postgresql@14` |
| MongoDB | 6+ | `mongod --version` | `brew install mongodb-community@6.0` |
| Node.js | 18+ | `node --version` | `brew install node` |
| Git | 2.x | `git --version` | 기본 설치됨 |

### 개발 도구 (권장)

- **IDE**: IntelliJ IDEA (Ultimate) 또는 VS Code
- **API 테스트**: Postman 또는 HTTPie
- **DB 클라이언트**: DBeaver, TablePlus, MongoDB Compass

---

## 🚀 Step-by-Step 설정

### Step 1: 레포지토리 클론

```bash
git clone https://github.com/sm-assign-zonagent/sm-zonagent-assignment.git
cd sm-zonagent-assignment
```

### Step 2: 데이터베이스 설정

#### PostgreSQL 설정

```bash
# PostgreSQL 시작
brew services start postgresql@14

# 데이터베이스 생성
createdb zonagent

# 접속 확인
psql zonagent

# psql 프롬프트에서
\l                    # 데이터베이스 목록 확인
\q                    # 종료
```

**연결 정보**:
- Host: `localhost`
- Port: `5432`
- Database: `zonagent`
- Username: `postgres` (또는 현재 사용자)
- Password: 기본적으로 없음 (설정 필요시 변경)

#### MongoDB 설정

```bash
# MongoDB 시작
brew services start mongodb-community@6.0

# 접속 확인
mongosh

# MongoDB 셸에서
use zonagent          # 데이터베이스 생성 (사용 시 자동 생성)
show dbs              # 데이터베이스 목록
exit                  # 종료
```

**연결 정보**:
- Host: `localhost`
- Port: `27017`
- Database: `zonagent`
- Auth: 기본적으로 없음

### Step 3: Python Agent 프로젝트 생성

```bash
# 프로젝트 루트에서
mkdir python-agent
cd python-agent

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 기본 패키지 설치
pip install --upgrade pip
```

#### requirements.txt 생성

```bash
cat > requirements.txt << 'EOF'
# LLM & AI
anthropic==0.39.0

# Web Scraping
playwright==1.48.0
beautifulsoup4==4.12.3
lxml==5.1.0

# HTTP Client
httpx==0.27.0
requests==2.31.0

# Data Validation & Models
pydantic==2.9.2
pydantic-settings==2.6.1

# CLI & Utilities
click==8.1.7
python-dotenv==1.0.1
loguru==0.7.2

# Date & Time
python-dateutil==2.9.0

# Testing (optional)
pytest==8.3.4
pytest-asyncio==0.24.0
EOF

pip install -r requirements.txt
```

#### Playwright 브라우저 설치

```bash
playwright install chromium
```

#### 디렉토리 구조 생성

```bash
mkdir -p agent/{scrapers,models}
touch agent/__init__.py
touch agent/main.py
touch agent/orchestrator.py
touch agent/rule_generator.py
touch agent/data_extractor.py
touch agent/validator.py
touch agent/api_client.py
touch agent/scrapers/__init__.py
touch agent/scrapers/base.py
touch agent/scrapers/cherokee.py
touch agent/models/__init__.py
touch agent/models/dto.py
touch config.py

# .env 파일 생성
cat > .env << 'EOF'
# Claude API
CLAUDE_API_KEY=sk-ant-api03-...  # 여기에 실제 키 입력

# Kotlin API
KOTLIN_API_BASE_URL=http://localhost:8080

# Logging
LOG_LEVEL=INFO
EOF
```

**최종 구조**:
```
python-agent/
├── venv/                 # 가상환경 (git ignore)
├── agent/
│   ├── __init__.py
│   ├── main.py
│   ├── orchestrator.py
│   ├── rule_generator.py
│   ├── data_extractor.py
│   ├── validator.py
│   ├── api_client.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── cherokee.py
│   └── models/
│       ├── __init__.py
│       └── dto.py
├── config.py
├── requirements.txt
├── .env                  # git ignore
└── README.md
```

### Step 4: Spring Boot Kotlin 프로젝트 생성

#### 방법 1: Spring Initializr (웹)

1. https://start.spring.io/ 접속
2. 다음 설정 선택:
   - **Project**: Gradle - Kotlin
   - **Language**: Kotlin
   - **Spring Boot**: 3.2.x (최신 stable)
   - **Project Metadata**:
     - Group: `com.zonagent`
     - Artifact: `zonagent-backend`
     - Name: `zonagent-backend`
     - Package name: `com.zonagent`
     - Packaging: Jar
     - Java: 17
   - **Dependencies**:
     - Spring Web
     - Spring Data JPA
     - PostgreSQL Driver
     - Spring Data MongoDB
     - Validation
     - Spring Boot DevTools
     - Lombok (optional)

3. Generate → 다운로드 → 압축 해제
4. 프로젝트 루트에 `kotlin-backend` 폴더로 이동

```bash
cd sm-zonagent-assignment
mv ~/Downloads/zonagent-backend kotlin-backend
```

#### 방법 2: IntelliJ IDEA

1. New Project → Spring Initializr
2. 위와 동일한 설정
3. 프로젝트 위치: `sm-zonagent-assignment/kotlin-backend`

#### 디렉토리 구조 생성

```bash
cd kotlin-backend/src/main/kotlin/com/zonagent

mkdir -p controller
mkdir -p service
mkdir -p domain
mkdir -p repository
mkdir -p dto/request
mkdir -p dto/response
mkdir -p config
mkdir -p exception
```

**최종 구조**:
```
kotlin-backend/
├── src/main/
│   ├── kotlin/com/zonagent/
│   │   ├── ZonagentApplication.kt
│   │   ├── controller/
│   │   │   ├── ScraperController.kt
│   │   │   ├── MeetingController.kt
│   │   │   └── FileController.kt
│   │   ├── service/
│   │   │   ├── ScraperService.kt
│   │   │   ├── MeetingService.kt
│   │   │   ├── SchedulerService.kt
│   │   │   └── ProcessExecutor.kt
│   │   ├── domain/
│   │   │   ├── Meeting.kt
│   │   │   ├── Document.kt
│   │   │   ├── ExtractedData.kt
│   │   │   └── ScraperConfig.kt
│   │   ├── repository/
│   │   │   ├── MeetingRepository.kt
│   │   │   └── DocumentRepository.kt
│   │   ├── dto/
│   │   │   ├── request/
│   │   │   └── response/
│   │   ├── config/
│   │   │   ├── DatabaseConfig.kt
│   │   │   └── PythonConfig.kt
│   │   └── exception/
│   │       └── GlobalExceptionHandler.kt
│   └── resources/
│       ├── application.yml
│       └── application-local.yml
└── build.gradle.kts
```

#### application.yml 설정

```bash
cd kotlin-backend/src/main/resources

cat > application.yml << 'EOF'
spring:
  application:
    name: zonagent-backend

  # PostgreSQL
  datasource:
    url: jdbc:postgresql://localhost:5432/zonagent
    username: postgres
    password: # 필요시 설정
    driver-class-name: org.postgresql.Driver

  jpa:
    hibernate:
      ddl-auto: update  # 개발: update, 프로덕션: validate
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.PostgreSQLDialect

  # MongoDB
  data:
    mongodb:
      uri: mongodb://localhost:27017/zonagent
      auto-index-creation: true

server:
  port: 8080

# Python Agent 설정
python:
  agent:
    path: ../python-agent
    venv: ../python-agent/venv
    interpreter: ../python-agent/venv/bin/python

# 파일 저장 경로
file:
  storage:
    base-path: ./data/files

logging:
  level:
    com.zonagent: DEBUG
    org.springframework.web: DEBUG
EOF
```

#### build.gradle.kts 의존성 추가

`kotlin-backend/build.gradle.kts` 파일 열어서 확인:

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-data-mongodb")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.postgresql:postgresql")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("org.jetbrains.kotlin:kotlin-reflect")

    developmentOnly("org.springframework.boot:spring-boot-devtools")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
}
```

### Step 5: Claude API 키 발급

1. https://console.anthropic.com/ 접속
2. 로그인 또는 회원가입
3. API Keys → Create Key
4. 생성된 키를 복사
5. `python-agent/.env` 파일의 `CLAUDE_API_KEY`에 입력

**사용 모델**: `claude-3-5-sonnet-20241022`

**Rate Limits 확인**:
- Tier 1: 50 requests/min, 40,000 tokens/min
- 필요시 업그레이드

### Step 6: 파일 저장 경로 생성

```bash
cd sm-zonagent-assignment
mkdir -p data/files/{pdfs,markdowns,rules,extracted}
```

### Step 7: .gitignore 설정

프로젝트 루트에 `.gitignore` 파일이 있는지 확인하고 없으면 생성합니다.

---

## ✅ 설정 확인

### Python Agent 확인

```bash
cd python-agent
source venv/bin/activate

# Python 버전 확인
python --version  # 3.11 이상

# 패키지 설치 확인
pip list | grep anthropic
pip list | grep playwright

# .env 파일 확인
cat .env  # CLAUDE_API_KEY 설정 확인
```

### Kotlin Backend 확인

```bash
cd kotlin-backend

# Gradle 빌드
./gradlew build

# 애플리케이션 실행
./gradlew bootRun

# 다른 터미널에서 health check
curl http://localhost:8080/actuator/health
# 또는
http :8080/actuator/health  # HTTPie 사용시
```

### 데이터베이스 연결 확인

**PostgreSQL**:
```bash
psql zonagent -c "SELECT version();"
```

**MongoDB**:
```bash
mongosh zonagent --eval "db.version()"
```

---

## 🧪 첫 번째 테스트

### 1. Python에서 Claude API 테스트

```python
# test_claude.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude! This is a test."}
    ]
)

print(message.content[0].text)
```

```bash
cd python-agent
python test_claude.py
# 출력: Hello! I'm Claude...
```

### 2. Kotlin에서 간단한 API 테스트

**HealthController.kt** 생성:
```kotlin
package com.zonagent.controller

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class HealthController {

    @GetMapping("/health")
    fun health(): Map<String, String> {
        return mapOf(
            "status" to "UP",
            "service" to "zonagent-backend"
        )
    }
}
```

```bash
# 애플리케이션 실행 후
curl http://localhost:8080/health
# {"status":"UP","service":"zonagent-backend"}
```

---

## 📚 다음 단계

설정이 완료되면:

1. **`PROGRESS.md` 읽기** - Phase A 작업 항목 확인
2. **`요구사항-명세.md` 3.2절** - API 명세 확인
3. **`요구사항-명세.md` 3.5절** - DB 스키마 확인
4. **Phase A-1 시작**: Scraper Control API 구현

---

## 🆘 트러블슈팅

### PostgreSQL 연결 실패

**증상**: `Connection refused` 또는 `database "zonagent" does not exist`

**해결**:
```bash
# PostgreSQL 실행 확인
brew services list | grep postgresql

# 재시작
brew services restart postgresql@14

# 데이터베이스 재생성
dropdb zonagent  # 주의: 기존 데이터 삭제
createdb zonagent
```

### MongoDB 연결 실패

**증상**: `MongoTimeoutError`

**해결**:
```bash
# MongoDB 실행 확인
brew services list | grep mongodb

# 재시작
brew services restart mongodb-community@6.0

# 로그 확인
tail -f /opt/homebrew/var/log/mongodb/mongo.log
```

### Python 가상환경 활성화 안됨

**증상**: `pip install` 시 권한 오류 또는 전역 설치됨

**해결**:
```bash
# 가상환경 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# 프롬프트 확인: (venv) 표시되어야 함
```

### Claude API 키 오류

**증상**: `AuthenticationError` 또는 `401 Unauthorized`

**해결**:
1. API 키 재확인: https://console.anthropic.com/
2. `.env` 파일 형식 확인 (공백, 따옴표 없이)
3. 환경변수 로드 확인:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(os.getenv("CLAUDE_API_KEY"))  # 키가 출력되는지 확인
   ```

### Playwright 브라우저 실행 오류

**증상**: `Executable doesn't exist`

**해결**:
```bash
# 브라우저 재설치
playwright install chromium

# 시스템 의존성 설치 (Linux)
playwright install-deps
```

---

## 📞 참고 문서

- [Spring Boot 공식 문서](https://spring.io/projects/spring-boot)
- [Kotlin 공식 문서](https://kotlinlang.org/docs/home.html)
- [Claude API 문서](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Playwright Python 문서](https://playwright.dev/python/docs/intro)
- [PostgreSQL 문서](https://www.postgresql.org/docs/)
- [MongoDB 문서](https://www.mongodb.com/docs/)

---

**작성일**: 2025-12-15
**작성자**: Claude Code
**대상**: Phase A 개발자
