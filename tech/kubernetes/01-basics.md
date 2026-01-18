---
date: 2025-01-18
tags:
  - tech
  - basics
  - kubernetes
parent: "[[README]]"
---

# Kubernetes - 기초

> ⬅️ [[README|목차로 돌아가기]] | ➡️ [[02-core|다음: 아키텍처]]

---

## 1. What - 개념 정의

> **한 줄 정의**: 컨테이너화된 워크로드와 서비스를 관리하기 위한 이식 가능하고 확장 가능한 오픈소스 플랫폼

### 핵심 개념

- **Container Orchestration**: 여러 컨테이너의 배포, 확장, 네트워킹을 자동 관리
- **Declarative Configuration**: 원하는 상태를 선언하면 K8s가 현재 상태를 맞춤
- **Self-healing**: 컨테이너 실패 시 자동 재시작, 교체
- **Auto-scaling**: 부하에 따라 자동으로 Pod 수 조절

### 주요 용어

| 용어 | 설명 |
|------|------|
| **Cluster** | Control Plane + Worker Node들의 집합 |
| **Node** | 컨테이너가 실행되는 물리/가상 머신 |
| **Pod** | K8s 최소 배포 단위, 1개 이상의 컨테이너 그룹 |
| **Service** | Pod 집합에 대한 네트워크 접근점 |
| **Deployment** | Pod 배포와 스케일링을 관리하는 리소스 |
| **Namespace** | 클러스터 내 가상 분리 단위 |
| **kubectl** | K8s 클러스터를 제어하는 CLI 도구 |

---

## 2. Why - 등장 배경

### 해결하려는 문제

- **컨테이너 수동 관리의 한계**: 수백, 수천 개 컨테이너를 사람이 관리 불가
- **서비스 디스커버리**: 동적으로 생성/삭제되는 컨테이너 간 통신
- **로드 밸런싱**: 트래픽을 여러 컨테이너에 분산
- **롤링 업데이트**: 무중단 배포

### Docker만 사용 시 한계

| 문제 | Docker만 | Kubernetes |
|------|----------|------------|
| 멀티 호스트 관리 | 수동 | 자동 |
| 장애 복구 | 수동 재시작 | 자동 Self-healing |
| 스케일링 | 수동 | 자동 (HPA) |
| 서비스 디스커버리 | 직접 구현 | 내장 (Service, DNS) |
| 로드 밸런싱 | 별도 구성 | 내장 |
| 롤링 배포 | 직접 구현 | 내장 (Deployment) |

---

## 3. 핵심 리소스

### Pod

> K8s의 **최소 배포 단위**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.25
    ports:
    - containerPort: 80
```

**특징**:
- 1개 이상의 컨테이너를 포함
- 같은 Pod 내 컨테이너는 네트워크/스토리지 공유
- Pod는 휘발성 (언제든 재생성될 수 있음)

### Service

> Pod 집합에 대한 **안정적인 네트워크 엔드포인트**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

**Service 타입**:

| 타입 | 설명 |
|------|------|
| **ClusterIP** | 클러스터 내부에서만 접근 (기본값) |
| **NodePort** | 노드 포트로 외부 노출 |
| **LoadBalancer** | 클라우드 LB 연동 |
| **ExternalName** | 외부 DNS 이름 매핑 |

### Deployment

> Pod의 **선언적 업데이트** 관리

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
```

**기능**:
- 원하는 Pod 수 유지 (replicas)
- 롤링 업데이트
- 롤백

---

## 4. 장단점

### 장점

- ✅ **자동화**: 배포, 스케일링, 복구 자동화
- ✅ **이식성**: 온프레미스, 클라우드 어디서나 동일하게 동작
- ✅ **확장성**: 수천 노드까지 확장 가능
- ✅ **생태계**: Helm, Istio 등 풍부한 에코시스템

### 단점

- ❌ **복잡성**: 러닝커브가 높음
- ❌ **오버헤드**: 소규모 프로젝트에는 과함
- ❌ **운영 부담**: 클러스터 자체 운영 필요 (관리형 K8s 권장)

---

## 📖 다음 단계

> [!tip] 다음으로
> 기초 개념을 이해했다면 [[02-core|아키텍처]]에서 Control Plane과 Worker Node를 학습하세요.

---

## References

- [Kubernetes 공식 문서](https://kubernetes.io/docs/concepts/)
- [Kubernetes Architecture Explained](https://devopscube.com/kubernetes-architecture-explained/)
