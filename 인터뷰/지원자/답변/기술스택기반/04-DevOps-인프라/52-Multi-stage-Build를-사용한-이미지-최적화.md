# Multi-stage Build를 사용한 이미지 최적화

## Keywords
`Docker`, `Multi-stage Build`, `이미지 최적화`, `레이어 캐싱`, `빌드 크기 축소`, `보안`

## 핵심 답변
Multi-stage Build는 Docker 17.05부터 도입된 기능으로, 하나의 Dockerfile에서 여러 FROM 구문을 사용하여 빌드 단계를 분리하는 방법입니다. 빌드 환경과 실행 환경을 분리함으로써 최종 이미지 크기를 크게 줄이고, 불필요한 빌드 도구와 중간 산출물을 제거할 수 있습니다.

**주요 이점:**
1. **이미지 크기 감소**: 빌드 도구와 의존성을 최종 이미지에서 제외
2. **보안 강화**: 소스 코드와 빌드 도구가 프로덕션 이미지에 포함되지 않음
3. **빌드 속도 향상**: 레이어 캐싱을 효과적으로 활용
4. **관리 편의성**: 하나의 Dockerfile로 전체 빌드 프로세스 관리

## 상세 설명

### Multi-stage Build 개념

**기존 방식의 문제점:**
```dockerfile
# 빌드와 실행이 혼재된 단일 스테이지
FROM node:18
WORKDIR /app

# 빌드 도구 설치
COPY package*.json ./
RUN npm install  # devDependencies 포함

# 소스 코드 복사 및 빌드
COPY . .
RUN npm run build

# 실행
CMD ["node", "dist/main.js"]

# 문제점:
# - node_modules에 devDependencies 포함 (불필요)
# - 소스 코드 전체 포함 (보안 위험)
# - 빌드 도구들이 최종 이미지에 남음
# - 이미지 크기: ~1.2GB
```

**Multi-stage Build 적용:**
```dockerfile
# Stage 1: 빌드 환경
FROM node:18 AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: 실행 환경
FROM node:18-alpine
WORKDIR /app

# 빌드된 결과물만 복사
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production

USER node
CMD ["node", "dist/main.js"]

# 결과:
# - devDependencies 제외
# - 소스 코드 제외
# - 경량 alpine 이미지 사용
# - 이미지 크기: ~150MB (약 87% 감소)
```

### 언어별 최적화 전략

**1. Node.js 애플리케이션:**
```dockerfile
# 빌드 스테이지
FROM node:18 AS builder
WORKDIR /app

# 의존성 설치 (레이어 캐싱 활용)
COPY package*.json ./
RUN npm ci

# TypeScript 빌드
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

# 프로덕션 의존성만 설치
RUN npm ci --only=production

# 실행 스테이지
FROM node:18-alpine
WORKDIR /app

# 필요한 파일만 복사
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# 보안 설정
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000
CMD ["node", "dist/main.js"]
```

**2. Java/Spring Boot 애플리케이션:**
```dockerfile
# 빌드 스테이지
FROM gradle:8.5-jdk17 AS builder
WORKDIR /app

# Gradle 캐시 활용
COPY build.gradle settings.gradle ./
COPY gradle ./gradle
RUN gradle dependencies --no-daemon

# 소스 빌드
COPY src ./src
RUN gradle bootJar --no-daemon

# 실행 스테이지
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# JAR 파일만 복사
COPY --from=builder /app/build/libs/*.jar app.jar

# 보안 설정
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**3. Go 애플리케이션 (가장 극적인 최적화):**
```dockerfile
# 빌드 스테이지
FROM golang:1.21 AS builder
WORKDIR /app

# 모듈 다운로드 (캐시 활용)
COPY go.mod go.sum ./
RUN go mod download

# 정적 바이너리 빌드
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# 실행 스테이지 (scratch 사용 가능)
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

# 바이너리만 복사
COPY --from=builder /app/main .

# 또는 완전한 최소화
# FROM scratch
# COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
# COPY --from=builder /app/main .

EXPOSE 8080
CMD ["./main"]

# 이미지 크기: ~10MB (golang:1.21은 ~900MB)
```

**4. Python 애플리케이션:**
```dockerfile
# 빌드 스테이지
FROM python:3.11 AS builder
WORKDIR /app

# 가상환경 생성
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 실행 스테이지
FROM python:3.11-slim
WORKDIR /app

# 가상환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 애플리케이션 코드 복사
COPY . .

# 보안 설정
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "main.py"]
```

## 예시 코드

### 고급 최적화 기법

**1. 빌드 캐시 최적화:**
```dockerfile
# 의존성 캐시 최적화
FROM node:18 AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# 빌드 캐시 활용
FROM node:18 AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# 프로덕션 의존성
FROM node:18 AS prod-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# 최종 이미지
FROM node:18-alpine
WORKDIR /app
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/main.js"]
```

**2. 테스트 스테이지 추가:**
```dockerfile
# 베이스 이미지
FROM node:18 AS base
WORKDIR /app
COPY package*.json ./

# 의존성 설치
FROM base AS deps
RUN npm ci

# 테스트 스테이지
FROM deps AS test
COPY . .
RUN npm run lint
RUN npm run test

# 빌드 스테이지
FROM deps AS builder
COPY . .
RUN npm run build

# 프로덕션 이미지
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --only=production
CMD ["node", "dist/main.js"]
```

**3. 개발/프로덕션 분리:**
```dockerfile
# 공통 베이스
FROM node:18 AS base
WORKDIR /app
COPY package*.json ./

# 개발 환경
FROM base AS development
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# 프로덕션 빌드
FROM base AS builder
RUN npm ci
COPY . .
RUN npm run build

# 프로덕션 환경
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production && npm cache clean --force
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Docker Compose와 통합

```yaml
# docker-compose.yml
version: '3.8'

services:
  app-dev:
    build:
      context: .
      target: development  # development 스테이지 사용
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: development

  app-prod:
    build:
      context: .
      target: production  # production 스테이지 사용
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
    restart: unless-stopped

  app-test:
    build:
      context: .
      target: test  # test 스테이지 사용
    command: npm run test:watch
```

### 빌드 인자 활용

```dockerfile
# 버전 관리
ARG NODE_VERSION=18
FROM node:${NODE_VERSION} AS builder

# 빌드 타입 설정
ARG BUILD_ENV=production
ENV NODE_ENV=${BUILD_ENV}

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build:${BUILD_ENV}

# 최종 이미지
FROM node:${NODE_VERSION}-alpine
ARG APP_VERSION=latest
LABEL version=${APP_VERSION}

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production

CMD ["node", "dist/main.js"]
```

```bash
# 빌드 시 인자 전달
docker build \
  --build-arg NODE_VERSION=18 \
  --build-arg BUILD_ENV=production \
  --build-arg APP_VERSION=1.2.3 \
  -t myapp:1.2.3 \
  .
```

## 실무 적용 팁

### 최적화 체크리스트

1. **베이스 이미지 선택**
   - Alpine 이미지 사용 (크기 최소화)
   - Distroless 이미지 고려 (보안 강화)
   - 특정 버전 태그 사용 (재현성)

2. **레이어 캐싱**
   - 변경 빈도가 낮은 파일 먼저 COPY
   - 의존성 설치를 소스 코드 복사보다 먼저
   - .dockerignore 파일 작성

3. **불필요한 파일 제거**
   ```dockerfile
   # .dockerignore
   node_modules
   npm-debug.log
   .git
   .gitignore
   README.md
   .env
   .vscode
   coverage
   .DS_Store
   ```

4. **보안 설정**
   - 비root 사용자로 실행
   - 불필요한 패키지 제거
   - 최신 보안 패치 적용

### 이미지 크기 비교

```bash
# 빌드 전후 크기 확인
docker images myapp

# 레이어별 크기 분석
docker history myapp:latest

# dive 도구로 상세 분석
dive myapp:latest
```

### 모니터링 및 측정

```bash
# 빌드 시간 측정
time docker build -t myapp:latest .

# 빌드 캐시 활용 확인
docker build --progress=plain -t myapp:latest .

# 특정 스테이지만 빌드
docker build --target builder -t myapp:builder .
```

## 참고 자료
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Layer Caching](https://docs.docker.com/build/cache/)
- [Dive - Docker Image Analysis](https://github.com/wagoodman/dive)
