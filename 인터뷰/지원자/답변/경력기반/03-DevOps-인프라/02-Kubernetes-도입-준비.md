# Kubernetes 도입을 위한 초석을 다졌다고 했는데, 구체적으로 어떤 준비를 했나요?

## 답변

Kubernetes 도입은 단순히 오케스트레이션 도구를 설치하는 것이 아니라 전체 인프라 아키텍처와 조직 문화의 전환을 의미하기 때문에, 신중하게 단계적으로 준비했습니다.

기존 모놀리식 애플리케이션을 바로 K8s로 이전하는 것은 위험도가 높았기 때문에, 우선 신규 개발하는 마이크로서비스부터 컨테이너화하고, 팀원들이 Docker와 K8s 개념을 익히도록 스터디와 PoC(Proof of Concept)를 진행했습니다. 또한 개발/스테이징 환경에 K3s 클러스터를 구축하여 실제 운영 전에 충분히 실험할 수 있는 환경을 마련했습니다.

## 핵심 키워드

- Kubernetes
- 컨테이너화
- 마이크로서비스
- IaC (Infrastructure as Code)
- 조직 역량 강화

## 준비 작업 내역

### 1. 기술적 준비

#### 1.1 컨테이너화 (Dockerization)
- **기존 애플리케이션 분석**: 의존성, 설정 파일, 외부 연동 포인트 파악
- **Multi-stage Docker 빌드 작성**: 빌드 이미지와 런타임 이미지 분리로 이미지 크기 최적화
- **베이스 이미지 표준화**: 사내 표준 베이스 이미지(JDK 17 + Alpine) 작성 및 배포
- **환경변수 기반 설정**: 12-Factor App 원칙에 따라 하드코딩된 설정을 환경변수로 전환

```dockerfile
# 예시: Multi-stage Dockerfile
FROM gradle:8.5-jdk17-alpine AS builder
WORKDIR /app
COPY build.gradle settings.gradle ./
COPY src ./src
RUN gradle build --no-daemon -x test

FROM eclipse-temurin:17-jre-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-XX:+UseG1GC", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
```

#### 1.2 로컬 K8s 클러스터 구축 (PoC)
- **K3s 클러스터 설치**: 가볍고 빠른 K3s를 개발 환경에 설치하여 학습 환경 제공
- **Helm Chart 작성**: 주요 서비스의 Helm Chart 템플릿 작성 및 버전 관리
- **Ingress Controller 설정**: Traefik을 이용한 HTTP 라우팅 구성
- **Persistent Volume 전략 수립**: StatefulSet이 필요한 서비스(DB, Redis) 식별 및 스토리지 클래스 정의

```yaml
# 예시: Helm values.yaml
replicaCount: 3

image:
  repository: harbor.internal.com/trading-api
  tag: "1.2.3"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: traefik
  hosts:
    - host: trading-api.dev.internal.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 5
```

#### 1.3 CI/CD 파이프라인 확장
- **이미지 빌드 자동화**: GitHub Actions에 Docker 빌드 및 Harbor 푸시 단계 추가
- **이미지 스캐닝**: Trivy를 통한 보안 취약점 스캔 자동화
- **GitOps 준비**: ArgoCD 설치 및 Git 기반 배포 흐름 설계

```yaml
# GitHub Actions - Docker 빌드 예시
name: Build and Push Docker Image

on:
  push:
    branches: [main, develop]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Harbor
        uses: docker/login-action@v3
        with:
          registry: harbor.internal.com
          username: ${{ secrets.HARBOR_USERNAME }}
          password: ${{ secrets.HARBOR_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: harbor.internal.com/trading-api
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

#### 1.4 서비스 메시 검토
- **Istio vs Linkerd 비교**: 금융 시스템의 복잡한 네트워크 정책과 mTLS 요구사항 분석
- **사이드카 패턴 PoC**: Envoy 프록시를 이용한 트래픽 제어 및 서킷 브레이커 테스트

### 2. 조직/문화적 준비

#### 2.1 기술 교육 및 스터디
- **Kubernetes 기초 교육**: CKAD(Certified Kubernetes Application Developer) 교재 기반 사내 스터디 진행 (8주 과정)
- **핸즈온 워크샵**: 주 1회 실습 세션으로 Pod, Deployment, Service, Ingress 직접 작성
- **장애 시뮬레이션 훈련**: Chaos Engineering 도구(Chaos Mesh)를 사용한 장애 대응 훈련

#### 2.2 운영 프로세스 정립
- **On-call 체계 재정비**: K8s 장애 시 1차 대응 가이드 작성 (Pod Restart, Log 확인 등)
- **Runbook 작성**: 주요 장애 상황별 대응 절차 문서화 (OOMKilled, CrashLoopBackOff 등)
- **포스트모텀 문화 도입**: 장애 발생 시 비난 없는 회고 문화 정착

#### 2.3 보안 및 컴플라이언스
- **금융권 보안 요구사항 매핑**: K8s 환경에서 개인정보보호법, 전자금융거래법 준수 방안 수립
- **네트워크 정책 설계**: Namespace 간 트래픽 격리, Egress 제어
- **RBAC 정책 수립**: 팀별 권한 분리 (개발팀은 dev namespace만, 운영팀은 전체)

```yaml
# 예시: NetworkPolicy - namespace 간 트래픽 제어
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-from-other-namespaces
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
      - podSelector: {}  # 같은 namespace 내 pod만 허용
```

### 3. 인프라 준비

#### 3.1 클러스터 아키텍처 설계
- **멀티 클러스터 전략**: 개발/스테이징/프로덕션 클러스터 분리 (보안 및 리소스 격리)
- **노드 그룹 설계**: 일반 워크로드 / DB StatefulSet / 배치 Job 전용 노드 그룹 분리
- **고가용성 구성**: Control Plane 3대, etcd 3대 구성으로 단일 장애점 제거

#### 3.2 모니터링 및 로깅 인프라
- **Prometheus + Grafana**: K8s 클러스터 메트릭 수집 및 시각화
- **Loki**: 컨테이너 로그 중앙화 (ELK 대비 리소스 효율적)
- **Kube-state-metrics**: K8s 오브젝트 상태 메트릭 수집
- **Alert Manager**: PagerDuty 연동으로 장애 알림 자동화

#### 3.3 스토리지 및 네트워크
- **Persistent Volume 프로비저닝**: Rook-Ceph 클러스터 구축으로 동적 PV 제공
- **Ingress Controller 이중화**: Traefik 2대 이상 구성으로 고가용성 확보
- **Service Mesh 준비**: Istio 설치 및 mTLS 기본 활성화

#### 3.4 백업 및 재해복구
- **Velero 설치**: K8s 리소스 및 PV 백업 자동화 (일 1회)
- **Disaster Recovery 시나리오 테스트**: 전체 클러스터 복구 절차 검증

## 실제 적용 사례

### 1. 신규 마이크로서비스 우선 적용
- **알림 서비스 (Notification Service)**: 기존 시스템과 결합도가 낮아 첫 K8s 배포 대상으로 선정
- **성과**: 배포 시간 30분 → 5분으로 단축, 무중단 배포 구현 (Rolling Update)

### 2. 배치 작업 K8s Job 전환
- **월말 정산 배치**: Cron 기반 스크립트를 K8s CronJob으로 전환
- **성과**: 실패 시 자동 재시도(restartPolicy), 로그 중앙화로 디버깅 시간 50% 단축

### 3. 개발 환경 빠른 구축
- **Namespace 기반 격리**: 개발자별 독립 namespace 제공으로 충돌 방지
- **성과**: 신규 개발자 온보딩 시 환경 구축 시간 2일 → 2시간으로 단축

## 남은 과제

### 1. 레거시 모놀리스 전환
- **과제**: 10년 이상 운영된 모놀리식 거래 시스템을 어떻게 분해하고 컨테이너화할 것인가
- **계획**: Strangler Fig 패턴으로 점진적 마이그레이션 (신규 기능은 마이크로서비스로, 기존 기능은 유지)

### 2. 프로덕션 클러스터 고도화
- **현재 상태**: 스테이징까지만 K8s 적용, 프로덕션은 여전히 VM 기반
- **계획**: 트래픽이 적은 서비스부터 순차적으로 프로덕션 K8s 이전 (Blue-Green 배포)

### 3. 멀티 클라우드/하이브리드 전략
- **과제**: 금융권 규제로 인한 온프레미스 유지 + 클라우드 버스팅 전략 필요
- **계획**: K8s Federation 또는 클러스터 메시 도입 검토

### 4. GitOps 완전 정착
- **현재 상태**: ArgoCD 설치했으나 일부 수동 배포 병행
- **계획**: 모든 배포를 Git PR 기반으로 전환, 배포 이력 추적성 확보

### 5. 비용 최적화
- **과제**: K8s 클러스터 운영으로 인한 오버헤드 (유휴 리소스) 최소화
- **계획**: Cluster Autoscaler, VPA(Vertical Pod Autoscaler) 도입으로 리소스 최적화

## 참고 자료

- [Kubernetes Official Documentation](https://kubernetes.io/docs/home/)
- [CNCF Cloud Native Interactive Landscape](https://landscape.cncf.io/)
- [Kubernetes Patterns by Bilgin Ibryam & Roland Huß](https://www.oreilly.com/library/view/kubernetes-patterns/9781492050278/)
- [Strangler Fig Pattern - Martin Fowler](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [금융권 클라우드 이용 가이드 - 금융보안원](https://www.fsec.or.kr/)
