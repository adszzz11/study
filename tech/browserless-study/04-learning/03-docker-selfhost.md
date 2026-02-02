# Docker Self-hosted 실행

## 개요

Browserless를 Docker로 Self-hosted하면 무료로 강력한 헤드리스 브라우저 환경을 운영할 수 있습니다. 이 문서에서는 설치부터 프로덕션 배포까지 다룹니다.

## 기본 실행

### Quick Start

```bash
# 최신 Chromium 이미지 실행
docker run -p 3000:3000 ghcr.io/browserless/chromium

# 백그라운드 실행
docker run -d -p 3000:3000 --name browserless ghcr.io/browserless/chromium

# 실행 확인
curl http://localhost:3000
```

### 이미지 종류

| 이미지 | 설명 |
|--------|------|
| `ghcr.io/browserless/chromium` | 최신 Chromium (권장) |
| `ghcr.io/browserless/chrome` | Chrome 브라우저 |
| `browserless/chrome` | Docker Hub (v1 레거시) |

## 환경 변수 설정

### 주요 환경 변수

```bash
docker run -d \
  -p 3000:3000 \
  -e "CONCURRENT=10" \
  -e "QUEUED=50" \
  -e "TIMEOUT=60000" \
  -e "TOKEN=my-secret-token" \
  ghcr.io/browserless/chromium
```

### 환경 변수 설명

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `CONCURRENT` | 10 | 동시 실행 브라우저 수 |
| `QUEUED` | 10 | 대기열 최대 크기 |
| `TIMEOUT` | 30000 | 기본 타임아웃 (ms) |
| `TOKEN` | - | API 인증 토큰 |
| `MAX_PAYLOAD_SIZE` | 5mb | 최대 요청 크기 |
| `WORKSPACE_DIR` | /tmp | 작업 디렉토리 |

### 성능 관련 설정

```bash
docker run -d \
  -p 3000:3000 \
  -e "CONCURRENT=5" \
  -e "QUEUED=20" \
  -e "TIMEOUT=60000" \
  -e "PREBOOT_CHROME=true" \
  -e "KEEP_ALIVE=true" \
  ghcr.io/browserless/chromium
```

| 변수 | 설명 |
|------|------|
| `PREBOOT_CHROME` | 브라우저 미리 시작 |
| `KEEP_ALIVE` | 연결 유지 |
| `DEMO_MODE` | 데모 UI 활성화 |
| `DEBUG` | 디버그 로그 활성화 |

## Docker Compose 설정

### 기본 구성

```yaml
# docker-compose.yml
version: '3.8'

services:
  browserless:
    image: ghcr.io/browserless/chromium
    container_name: browserless
    ports:
      - "3000:3000"
    environment:
      - CONCURRENT=10
      - QUEUED=50
      - TIMEOUT=60000
      - TOKEN=my-secret-token
    restart: unless-stopped
    shm_size: 2gb
```

### 프로덕션 구성

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  browserless:
    image: ghcr.io/browserless/chromium
    container_name: browserless
    ports:
      - "3000:3000"
    environment:
      - CONCURRENT=20
      - QUEUED=100
      - TIMEOUT=60000
      - TOKEN=${BROWSERLESS_TOKEN}
      - PREBOOT_CHROME=true
      - KEEP_ALIVE=true
      - MAX_PAYLOAD_SIZE=10mb
      - WORKSPACE_DIR=/workspace
    volumes:
      - browserless-workspace:/workspace
      - browserless-downloads:/downloads
    restart: always
    shm_size: 4gb
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  browserless-workspace:
  browserless-downloads:
```

### 역방향 프록시 (Nginx)

```yaml
# docker-compose.with-nginx.yml
version: '3.8'

services:
  browserless:
    image: ghcr.io/browserless/chromium
    environment:
      - CONCURRENT=10
      - TOKEN=my-secret-token
    shm_size: 2gb
    networks:
      - browserless-net

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - browserless
    networks:
      - browserless-net

networks:
  browserless-net:
```

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream browserless {
        server browserless:3000;
    }

    server {
        listen 80;
        server_name browserless.example.com;

        location / {
            proxy_pass http://browserless;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 3600s;
        }
    }
}
```

## 리소스 최적화

### 메모리 설정

```bash
# shm_size 설정 (Chrome은 공유 메모리 사용)
docker run -d \
  --shm-size=2gb \
  -p 3000:3000 \
  ghcr.io/browserless/chromium

# 또는 /dev/shm 마운트
docker run -d \
  -v /dev/shm:/dev/shm \
  -p 3000:3000 \
  ghcr.io/browserless/chromium
```

### CPU 제한

```bash
docker run -d \
  --cpus="2" \
  --memory="4g" \
  -p 3000:3000 \
  ghcr.io/browserless/chromium
```

### 동시 실행 계산

```
권장 CONCURRENT 값 = (사용 가능 메모리 GB) / 0.5

예시:
- 4GB RAM → CONCURRENT=8
- 8GB RAM → CONCURRENT=16
- 16GB RAM → CONCURRENT=32
```

## 보안 설정

### API 토큰 인증

```bash
# 토큰 설정
docker run -d \
  -e "TOKEN=my-secure-token-12345" \
  -p 3000:3000 \
  ghcr.io/browserless/chromium
```

```javascript
// 클라이언트에서 토큰 사용
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:3000?token=my-secure-token-12345'
});
```

### 네트워크 격리

```yaml
# docker-compose.yml
services:
  browserless:
    image: ghcr.io/browserless/chromium
    networks:
      - internal
    # 외부 포트 노출 안함

  app:
    build: .
    networks:
      - internal
    ports:
      - "8080:8080"

networks:
  internal:
    driver: bridge
```

### Sandbox 모드

```bash
# Sandbox 비활성화 (권장하지 않음, 필요 시에만)
docker run -d \
  --cap-add=SYS_ADMIN \
  -p 3000:3000 \
  ghcr.io/browserless/chromium
```

## 모니터링

### 헬스체크

```bash
# 헬스체크 엔드포인트
curl http://localhost:3000/
curl http://localhost:3000/pressure  # 부하 상태

# Docker 헬스체크
docker inspect --format='{{.State.Health.Status}}' browserless
```

### 로깅

```bash
# 로그 확인
docker logs browserless

# 실시간 로그
docker logs -f browserless

# 디버그 모드
docker run -d \
  -e "DEBUG=browserless*" \
  -p 3000:3000 \
  ghcr.io/browserless/chromium
```

### Prometheus 메트릭

```bash
# 메트릭 엔드포인트
curl http://localhost:3000/metrics
```

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'browserless'
    static_configs:
      - targets: ['browserless:3000']
```

## 스케일링

### 수평 확장

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  browserless:
    image: ghcr.io/browserless/chromium
    environment:
      - CONCURRENT=10
    shm_size: 2gb
    deploy:
      replicas: 3

  nginx:
    image: nginx:alpine
    ports:
      - "3000:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - browserless
```

```nginx
# nginx-lb.conf
upstream browserless_cluster {
    least_conn;
    server browserless:3000;
}

server {
    listen 80;

    location / {
        proxy_pass http://browserless_cluster;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Kubernetes 배포

```yaml
# browserless-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: browserless
spec:
  replicas: 3
  selector:
    matchLabels:
      app: browserless
  template:
    metadata:
      labels:
        app: browserless
    spec:
      containers:
      - name: browserless
        image: ghcr.io/browserless/chromium
        ports:
        - containerPort: 3000
        env:
        - name: CONCURRENT
          value: "10"
        - name: TOKEN
          valueFrom:
            secretKeyRef:
              name: browserless-secret
              key: token
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: dshm
          mountPath: /dev/shm
      volumes:
      - name: dshm
        emptyDir:
          medium: Memory
          sizeLimit: 2Gi
---
apiVersion: v1
kind: Service
metadata:
  name: browserless
spec:
  selector:
    app: browserless
  ports:
  - port: 3000
    targetPort: 3000
```

## 문제 해결

### 일반적인 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 브라우저 크래시 | 메모리 부족 | shm_size 증가 |
| 연결 거부 | 동시 접속 초과 | CONCURRENT 증가 |
| 타임아웃 | 네트워크/페이지 느림 | TIMEOUT 증가 |
| 권한 오류 | Sandbox 문제 | --cap-add=SYS_ADMIN |

### 디버깅 명령어

```bash
# 컨테이너 상태 확인
docker stats browserless

# 컨테이너 내부 접속
docker exec -it browserless /bin/sh

# 프로세스 확인
docker exec browserless ps aux

# 메모리 확인
docker exec browserless cat /proc/meminfo
```

## 다음 단계

- [[04-antibot|안티봇 우회]] - BrowserQL로 봇 탐지 우회
- [[05-sessions|Persistent Sessions]] - 세션 유지 방법
