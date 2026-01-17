# GitOps 구성의 핵심 원칙은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- GitOps
- Declarative
- Git as Source of Truth
- Pull-based Deployment
- ArgoCD
- FluxCD
- 인프라 코드화

## GitOps 4가지 핵심 원칙

### 1. Declarative (선언적)
-

### 2. Versioned and Immutable (버전 관리 및 불변성)
-

### 3. Pulled Automatically (자동 동기화)
-

### 4. Continuously Reconciled (지속적 조정)
-

## GitOps 도구 비교

### ArgoCD
-

### FluxCD
-

## GitOps 리포지토리 구조

-

## 환경별 관리 전략

-

## 시크릿 관리

-

## 설정 예시

### ArgoCD Application
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: main
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Kustomization 구조
```bash
# 디렉토리 구조
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

### Sealed Secrets
```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: production
spec:
  encryptedData:
    password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
```

## 참고 자료

-
