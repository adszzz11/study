# Container 보안 Best Practice

## Keywords
`Container Security`, `Image Scanning`, `Rootless`, `Security Context`, `Network Policy`, `Secrets Management`, `CVE`

## 핵심 답변
Container 보안은 이미지 빌드부터 런타임까지 전체 생명주기에 걸친 다층 방어(Defense in Depth) 전략이 필요합니다. 주요 보안 원칙은 최소 권한 원칙(Least Privilege), 불변 인프라(Immutable Infrastructure), 공격 표면 최소화(Attack Surface Reduction)입니다.

**핵심 보안 영역:**
1. **이미지 보안**: 신뢰할 수 있는 베이스 이미지, 취약점 스캔, 서명 검증
2. **런타임 보안**: Rootless 컨테이너, Capability 제한, Seccomp/AppArmor 프로파일
3. **네트워크 보안**: Network Policy, Service Mesh, TLS 통신
4. **시크릿 관리**: 환경변수 대신 Secrets Manager 사용
5. **접근 제어**: RBAC, Pod Security Standards

## 상세 설명

### 1. 이미지 보안

**신뢰할 수 있는 베이스 이미지 사용:**
```dockerfile
# ❌ 나쁜 예: latest 태그, 출처 불명
FROM ubuntu:latest

# ✅ 좋은 예: 특정 버전, 공식 이미지
FROM ubuntu:22.04

# ✅ 더 좋은 예: 최소 이미지
FROM alpine:3.19

# ✅ 최고의 예: Distroless (Google)
FROM gcr.io/distroless/static-debian11:nonroot
```

**취약점 스캔 통합:**
```bash
# Trivy로 이미지 스캔
trivy image myapp:latest

# 심각도별 필터링
trivy image --severity HIGH,CRITICAL myapp:latest

# CI/CD 파이프라인 통합
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# Grype 사용
grype myapp:latest

# Snyk 사용
snyk container test myapp:latest
```

**이미지 서명 및 검증:**
```bash
# Docker Content Trust 활성화
export DOCKER_CONTENT_TRUST=1

# 서명된 이미지 푸시
docker trust sign myapp:1.0.0

# Cosign으로 서명 (Sigstore)
cosign sign --key cosign.key myapp:latest

# 서명 검증
cosign verify --key cosign.pub myapp:latest
```

### 2. Dockerfile 보안 Best Practice

```dockerfile
# 보안이 강화된 Dockerfile
FROM node:18-alpine AS builder

# 보안 업데이트 적용
RUN apk update && apk upgrade && \
    apk add --no-cache dumb-init

# 비root 사용자 생성
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# 의존성 복사 및 설치
COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# 애플리케이션 코드 복사
COPY --chown=nodejs:nodejs . .

# 프로덕션 이미지
FROM node:18-alpine

# dumb-init으로 PID 1 문제 해결
RUN apk add --no-cache dumb-init

# 비root 사용자
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# 빌드 결과물만 복사
COPY --from=builder --chown=nodejs:nodejs /app .

# 불필요한 파일 제거
RUN rm -rf .git .env* *.md

# 비root 사용자로 전환
USER nodejs

# 읽기 전용 루트 파일시스템 대비
VOLUME ["/tmp", "/app/logs"]

EXPOSE 3000

# dumb-init으로 실행
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1
```

### 3. 런타임 보안 설정

**Kubernetes Security Context:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    # Pod 레벨 보안 컨텍스트
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault

  containers:
  - name: app
    image: myapp:latest
    securityContext:
      # Container 레벨 보안 컨텍스트
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1001
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE  # 80 포트 바인딩만 허용

    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: cache
      mountPath: /app/cache

    resources:
      limits:
        memory: "512Mi"
        cpu: "500m"
      requests:
        memory: "256Mi"
        cpu: "250m"

  volumes:
  - name: tmp
    emptyDir: {}
  - name: cache
    emptyDir: {}
```

**Docker 실행 시 보안 옵션:**
```bash
# 보안이 강화된 컨테이너 실행
docker run -d \
  --name secure-app \
  --read-only \                      # 읽기 전용 루트 FS
  --tmpfs /tmp \                     # 임시 파일용 tmpfs
  --tmpfs /run \
  --cap-drop=ALL \                   # 모든 capability 제거
  --cap-add=NET_BIND_SERVICE \       # 필요한 것만 추가
  --security-opt=no-new-privileges \ # 권한 상승 방지
  --security-opt=seccomp=seccomp.json \  # Seccomp 프로파일
  --user 1001:1001 \                 # 비root 사용자
  --memory=512m \                    # 메모리 제한
  --cpus=0.5 \                       # CPU 제한
  --pids-limit=100 \                 # 프로세스 수 제한
  --network=app-network \            # 전용 네트워크
  -p 8080:8080 \
  myapp:latest
```

### 4. 네트워크 보안

**Kubernetes Network Policy:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp

  policyTypes:
  - Ingress
  - Egress

  ingress:
  # Ingress Controller에서만 수신
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080

  egress:
  # 데이터베이스로만 송신
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432

  # DNS 쿼리 허용
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

**Service Mesh (Istio) mTLS:**
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # 모든 통신에 mTLS 강제

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: app-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: myapp
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/frontend/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/*"]
```

## 예시 코드

### Seccomp 프로파일

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_AARCH64"
  ],
  "syscalls": [
    {
      "names": [
        "accept4",
        "access",
        "arch_prctl",
        "bind",
        "brk",
        "close",
        "connect",
        "epoll_create1",
        "epoll_ctl",
        "epoll_wait",
        "exit_group",
        "fcntl",
        "fstat",
        "futex",
        "getpid",
        "getsockname",
        "listen",
        "mmap",
        "mprotect",
        "openat",
        "read",
        "rt_sigaction",
        "rt_sigprocmask",
        "setsockopt",
        "socket",
        "write"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### Secrets 관리

**❌ 나쁜 예: 환경변수로 전달**
```dockerfile
ENV DATABASE_PASSWORD=supersecret
```

**✅ 좋은 예: Docker Secrets**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: myapp:latest
    secrets:
      - db_password
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**✅ Kubernetes Secrets:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DATABASE_URL: postgresql://user:pass@db:5432/mydb

---
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: myapp:latest
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DATABASE_URL
    # 또는 파일로 마운트
    volumeMounts:
    - name: secrets
      mountPath: "/etc/secrets"
      readOnly: true

  volumes:
  - name: secrets
    secret:
      secretName: app-secrets
```

**✅ 최고의 예: External Secrets Operator**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore

  target:
    name: app-secrets
    creationPolicy: Owner

  data:
  - secretKey: DATABASE_URL
    remoteRef:
      key: prod/database/url
```

### Pod Security Standards

```yaml
# Restricted 정책 적용
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# OPA Gatekeeper 정책
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-security-labels
spec:
  match:
    kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
  parameters:
    labels:
    - key: "app"
    - key: "version"
    - key: "security-scan"
```

### 이미지 스캔 자동화

**GitHub Actions:**
```yaml
name: Container Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Build image
      run: docker build -t myapp:${{ github.sha }} .

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: myapp:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Fail on high vulnerabilities
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: myapp:${{ github.sha }}
        exit-code: '1'
        severity: 'CRITICAL,HIGH'
```

**Jenkins Pipeline:**
```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }

        stage('Security Scan') {
            parallel {
                stage('Trivy Scan') {
                    steps {
                        sh '''
                            trivy image \
                              --severity HIGH,CRITICAL \
                              --exit-code 1 \
                              --no-progress \
                              myapp:${BUILD_NUMBER}
                        '''
                    }
                }

                stage('Dockerfile Lint') {
                    steps {
                        sh 'hadolint Dockerfile'
                    }
                }

                stage('Secret Detection') {
                    steps {
                        sh 'gitleaks detect --source . --verbose'
                    }
                }
            }
        }

        stage('Sign Image') {
            steps {
                withCredentials([file(credentialsId: 'cosign-key', variable: 'COSIGN_KEY')]) {
                    sh '''
                        cosign sign \
                          --key ${COSIGN_KEY} \
                          myapp:${BUILD_NUMBER}
                    '''
                }
            }
        }
    }
}
```

## 실무 적용 팁

### 보안 체크리스트

**빌드 시점:**
- [ ] 신뢰할 수 있는 베이스 이미지 사용
- [ ] 최신 보안 패치 적용
- [ ] 취약점 스캔 통과
- [ ] 불필요한 패키지 제거
- [ ] 비root 사용자로 실행
- [ ] .dockerignore 파일 작성
- [ ] 시크릿 파일 제외
- [ ] 이미지 서명

**배포 시점:**
- [ ] Security Context 설정
- [ ] Resource Limits 설정
- [ ] Network Policy 적용
- [ ] RBAC 구성
- [ ] Secrets Manager 사용
- [ ] Read-only 루트 FS
- [ ] Pod Security Standards 적용

**런타임:**
- [ ] 로깅 및 모니터링
- [ ] 런타임 보안 스캐닝
- [ ] 이상 행위 탐지
- [ ] 정기적인 패치 및 업데이트

### 도구 추천

1. **이미지 스캔**: Trivy, Grype, Snyk, Clair
2. **Dockerfile 린트**: Hadolint
3. **시크릿 탐지**: Gitleaks, TruffleHog
4. **런타임 보안**: Falco, Sysdig
5. **정책 관리**: OPA, Kyverno
6. **Secrets 관리**: HashiCorp Vault, AWS Secrets Manager

## 참고 자료
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Container Security](https://owasp.org/www-project-docker-top-10/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [NIST Container Security Guide](https://www.nist.gov/publications/application-container-security-guide)
