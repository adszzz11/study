# Container Registry 관리 전략

## Keywords
`Container Registry`, `Image Management`, `Harbor`, `Docker Hub`, `ECR`, `보안`, `정책`, `저장소 관리`

## 핵심 답변
Container Registry는 컨테이너 이미지를 저장, 배포, 관리하는 중앙 저장소입니다. 효과적인 Registry 관리를 위해서는 이미지 태깅 전략, 보안 및 접근 제어, 스토리지 최적화, 고가용성 구성이 필요합니다.

**핵심 관리 전략:**
1. **이미지 태깅 전략**: 시맨틱 버저닝, 환경별 태그, immutable 태그
2. **보안 관리**: 취약점 스캔, 이미지 서명, 접근 제어
3. **스토리지 최적화**: 가비지 컬렉션, 이미지 압축, 스토리지 티어링
4. **고가용성**: 복제, 백업, 재해 복구
5. **거버넌스**: 정책 관리, 감사 로깅, 컴플라이언스

## 상세 설명

### 1. Registry 선택 및 구성

**주요 Registry 옵션:**

| Registry | 장점 | 단점 | 적합한 사용 사례 |
|----------|------|------|------------------|
| Docker Hub | 무료, 공개 이미지 풍부 | Private 저장소 제한, 속도 제한 | 오픈소스, 개발 환경 |
| Harbor | 온프레미스, 기능 풍부, 무료 | 운영 부담 | 엔터프라이즈, 규제 준수 |
| AWS ECR | AWS 통합, 관리형 | AWS 종속 | AWS 인프라 사용 시 |
| GCR/Artifact Registry | GCP 통합, 다중 형식 지원 | GCP 종속 | GCP 인프라 사용 시 |
| Azure ACR | Azure 통합, Geo-replication | Azure 종속 | Azure 인프라 사용 시 |
| GitLab Container Registry | CI/CD 통합 | 상대적으로 기능 제한 | GitLab 사용 시 |

**Harbor 구성 예시:**
```yaml
# docker-compose.yml for Harbor
version: '3.8'

services:
  registry:
    image: goharbor/registry-photon:v2.9.0
    container_name: registry
    restart: always
    volumes:
      - /data/registry:/storage
      - ./config/registry/config.yml:/etc/registry/config.yml:z
    environment:
      - REGISTRY_HTTP_SECRET=secret

  postgresql:
    image: goharbor/harbor-db:v2.9.0
    container_name: harbor-db
    restart: always
    volumes:
      - /data/database:/var/lib/postgresql/data:z
    environment:
      POSTGRES_PASSWORD: root123
      POSTGRES_USER: postgres

  core:
    image: goharbor/harbor-core:v2.9.0
    container_name: harbor-core
    restart: always
    volumes:
      - /data/ca_download/:/etc/core/ca/:z
      - /data/:/data/:z
    environment:
      CORE_SECRET: secret
      JOBSERVICE_SECRET: secret
    depends_on:
      - registry
      - postgresql

  jobservice:
    image: goharbor/harbor-jobservice:v2.9.0
    container_name: harbor-jobservice
    restart: always
    volumes:
      - /data/job_logs:/var/log/jobs:z
    environment:
      CORE_SECRET: secret
      JOBSERVICE_SECRET: secret

  nginx:
    image: goharbor/nginx-photon:v2.9.0
    container_name: nginx
    restart: always
    ports:
      - "80:8080"
      - "443:8443"
    volumes:
      - ./config/nginx:/etc/nginx:z
    depends_on:
      - core
      - registry
```

### 2. 이미지 태깅 전략

**시맨틱 버저닝 + 환경별 태그:**
```bash
# 버전별 태그
registry.example.com/myapp:1.0.0
registry.example.com/myapp:1.0
registry.example.com/myapp:1
registry.example.com/myapp:latest

# 환경별 태그
registry.example.com/myapp:dev
registry.example.com/myapp:staging
registry.example.com/myapp:production

# Git 커밋 기반
registry.example.com/myapp:abc1234
registry.example.com/myapp:main-abc1234

# 빌드 메타데이터
registry.example.com/myapp:1.0.0-20250110-abc1234
```

**태깅 자동화 스크립트:**
```bash
#!/bin/bash
# tag-and-push.sh

set -e

REGISTRY="registry.example.com"
IMAGE_NAME="myapp"
VERSION="$1"
GIT_COMMIT=$(git rev-parse --short HEAD)
BUILD_DATE=$(date +%Y%m%d)

if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  exit 1
fi

# 버전 파싱
MAJOR=$(echo $VERSION | cut -d. -f1)
MINOR=$(echo $VERSION | cut -d. -f2)

# 여러 태그 생성
TAGS=(
  "$VERSION"
  "$MAJOR.$MINOR"
  "$MAJOR"
  "latest"
  "$VERSION-$BUILD_DATE-$GIT_COMMIT"
)

echo "Building image..."
docker build -t ${REGISTRY}/${IMAGE_NAME}:${VERSION} .

echo "Tagging image..."
for TAG in "${TAGS[@]}"; do
  docker tag ${REGISTRY}/${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:${TAG}
done

echo "Pushing images..."
for TAG in "${TAGS[@]}"; do
  docker push ${REGISTRY}/${IMAGE_NAME}:${TAG}
done

echo "Successfully tagged and pushed:"
for TAG in "${TAGS[@]}"; do
  echo "  - ${REGISTRY}/${IMAGE_NAME}:${TAG}"
done
```

### 3. 보안 관리

**Harbor 보안 정책 설정:**
```yaml
# harbor-policy.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: harbor-policy
data:
  # 취약점 스캔 정책
  vulnerability_scan_policy: |
    {
      "rules": [
        {
          "disabled": false,
          "action": "prevent",
          "severity": "critical"
        },
        {
          "disabled": false,
          "action": "warn",
          "severity": "high"
        }
      ]
    }

  # 이미지 보관 정책
  retention_policy: |
    {
      "rules": [
        {
          "disabled": false,
          "priority": 1,
          "action": "retain",
          "template": "latestPushedK",
          "params": {
            "latestPushedK": 10
          },
          "tag_selectors": [
            {
              "kind": "doublestar",
              "decoration": "matches",
              "pattern": "release-**"
            }
          ]
        },
        {
          "disabled": false,
          "priority": 2,
          "action": "retain",
          "template": "nDaysSinceLastPush",
          "params": {
            "nDaysSinceLastPush": 30
          },
          "tag_selectors": [
            {
              "kind": "doublestar",
              "decoration": "matches",
              "pattern": "**"
            }
          ]
        }
      ]
    }
```

**AWS ECR 정책 예시:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPushPull",
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::123456789012:role/EKSNodeRole",
          "arn:aws:iam::123456789012:role/CIRole"
        ]
      },
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:BatchCheckLayerAvailability",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ]
    },
    {
      "Sid": "DenyUnencryptedTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "*",
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

**이미지 서명 및 검증:**
```bash
# Cosign으로 서명
cosign sign --key cosign.key registry.example.com/myapp:1.0.0

# 서명 검증
cosign verify --key cosign.pub registry.example.com/myapp:1.0.0

# Kubernetes에서 서명 검증 적용 (Kyverno)
cat <<EOF | kubectl apply -f -
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signatures
spec:
  validationFailureAction: enforce
  rules:
  - name: verify-signature
    match:
      any:
      - resources:
          kinds:
          - Pod
    verifyImages:
    - imageReferences:
      - "registry.example.com/*"
      attestors:
      - count: 1
        entries:
        - keys:
            publicKeys: |-
              -----BEGIN PUBLIC KEY-----
              MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
              -----END PUBLIC KEY-----
EOF
```

## 예시 코드

### CI/CD 통합

**GitHub Actions:**
```yaml
name: Build and Push to Registry

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]

env:
  REGISTRY: registry.example.com
  IMAGE_NAME: myapp

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v3

    - name: Log in to Harbor
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.HARBOR_USERNAME }}
        password: ${{ secrets.HARBOR_PASSWORD }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=semver,pattern={{major}}
          type=sha,prefix={{branch}}-

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
        cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max

    - name: Scan image with Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Sign image with Cosign
      run: |
        cosign sign --key env://COSIGN_KEY \
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build.outputs.digest }}
      env:
        COSIGN_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
        COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
```

**Jenkins Pipeline:**
```groovy
pipeline {
    agent any

    environment {
        REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
        HARBOR_CREDS = credentials('harbor-credentials')
    }

    stages {
        stage('Build') {
            steps {
                script {
                    def version = sh(returnStdout: true, script: 'git describe --tags --always').trim()
                    def shortCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    def buildDate = sh(returnStdout: true, script: 'date +%Y%m%d').trim()

                    env.VERSION = version
                    env.IMAGE_TAG = "${version}-${buildDate}-${shortCommit}"

                    sh """
                        docker build \
                          --build-arg VERSION=${version} \
                          --build-arg BUILD_DATE=${buildDate} \
                          --build-arg VCS_REF=${shortCommit} \
                          -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                          .
                    """
                }
            }
        }

        stage('Security Scan') {
            parallel {
                stage('Trivy Scan') {
                    steps {
                        sh """
                            trivy image \
                              --severity HIGH,CRITICAL \
                              --exit-code 1 \
                              ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }

                stage('Hadolint') {
                    steps {
                        sh 'hadolint Dockerfile'
                    }
                }
            }
        }

        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry("https://${REGISTRY}", 'harbor-credentials') {
                        // 여러 태그로 푸시
                        def tags = [
                            env.IMAGE_TAG,
                            env.VERSION,
                            env.BRANCH_NAME == 'main' ? 'latest' : env.BRANCH_NAME
                        ]

                        tags.each { tag ->
                            sh "docker tag ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${tag}"
                            sh "docker push ${REGISTRY}/${IMAGE_NAME}:${tag}"
                        }
                    }
                }
            }
        }

        stage('Sign Image') {
            steps {
                withCredentials([file(credentialsId: 'cosign-key', variable: 'COSIGN_KEY')]) {
                    sh """
                        cosign sign \
                          --key \${COSIGN_KEY} \
                          ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
    }
}
```

### 스토리지 최적화

**Harbor 가비지 컬렉션 자동화:**
```bash
#!/bin/bash
# harbor-gc.sh - Harbor 가비지 컬렉션 스크립트

HARBOR_URL="https://registry.example.com"
HARBOR_USER="admin"
HARBOR_PASSWORD="password"

# API로 GC 작업 트리거
curl -X POST "${HARBOR_URL}/api/v2.0/system/gc/schedule" \
  -u "${HARBOR_USER}:${HARBOR_PASSWORD}" \
  -H "Content-Type: application/json" \
  -d '{
    "schedule": {
      "type": "Daily",
      "cron": "0 2 * * *"
    },
    "delete_untagged": true,
    "workers": 3
  }'
```

**AWS ECR Lifecycle Policy:**
```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 10 production images",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["production"],
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 2,
      "description": "Remove untagged images after 7 days",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 3,
      "description": "Remove dev images after 30 days",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["dev", "feature"],
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 30
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
```

### 모니터링 및 알림

**Prometheus Exporter for Harbor:**
```yaml
# harbor-exporter.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: harbor-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: harbor-exporter
  template:
    metadata:
      labels:
        app: harbor-exporter
    spec:
      containers:
      - name: harbor-exporter
        image: c4po/harbor-exporter:latest
        env:
        - name: HARBOR_URI
          value: "https://registry.example.com"
        - name: HARBOR_USERNAME
          valueFrom:
            secretKeyRef:
              name: harbor-credentials
              key: username
        - name: HARBOR_PASSWORD
          valueFrom:
            secretKeyRef:
              name: harbor-credentials
              key: password
        ports:
        - containerPort: 9107
          name: metrics

---
apiVersion: v1
kind: Service
metadata:
  name: harbor-exporter
  labels:
    app: harbor-exporter
spec:
  ports:
  - port: 9107
    targetPort: 9107
    name: metrics
  selector:
    app: harbor-exporter

---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: harbor-exporter
spec:
  selector:
    matchLabels:
      app: harbor-exporter
  endpoints:
  - port: metrics
    interval: 30s
```

**Grafana 대시보드 쿼리:**
```promql
# 총 이미지 수
sum(harbor_project_repo_count)

# 프로젝트별 이미지 크기
sum(harbor_project_quota_usage_byte) by (project)

# 레지스트리 스토리지 사용률
harbor_registry_storage_usage_bytes / harbor_registry_storage_total_bytes * 100

# 취약점이 있는 이미지 수
sum(harbor_artifact_vulnerabilities) by (severity)

# 최근 24시간 Pull 횟수
rate(harbor_artifact_pulled[24h]) * 86400
```

## 실무 적용 팁

### 체크리스트

**보안:**
- [ ] HTTPS/TLS 적용
- [ ] 접근 제어 (RBAC) 설정
- [ ] 취약점 스캔 자동화
- [ ] 이미지 서명 및 검증
- [ ] 감사 로깅 활성화

**성능:**
- [ ] CDN 또는 캐시 계층 구성
- [ ] 지역별 레플리케이션
- [ ] 이미지 압축 최적화
- [ ] 레이어 공유 극대화

**운영:**
- [ ] 백업 및 복구 계획
- [ ] 모니터링 및 알림
- [ ] 가비지 컬렉션 자동화
- [ ] 스토리지 용량 계획

### 비용 최적화

1. **스토리지 티어링**: 오래된 이미지는 저렴한 스토리지로 이동
2. **압축**: 이미지 레이어 최적화
3. **중복 제거**: 동일 레이어 공유
4. **라이프사이클 정책**: 불필요한 이미지 자동 삭제

## 참고 자료
- [Harbor Documentation](https://goharbor.io/docs/)
- [AWS ECR Best Practices](https://docs.aws.amazon.com/AmazonECR/latest/userguide/best-practices.html)
- [Docker Registry Storage Drivers](https://docs.docker.com/registry/storage-drivers/)
- [OCI Distribution Spec](https://github.com/opencontainers/distribution-spec)
