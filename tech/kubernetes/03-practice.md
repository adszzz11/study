---
date: 2025-01-18
tags:
  - tech
  - practice
  - kubernetes
  - kubectl
parent: "[[README]]"
---

# Kubernetes - 실무 적용

> ⬅️ [[02-core|이전: 아키텍처]] | [[README|목차]] | ➡️ [[04-advanced|다음: 심화]]

---

## 1. Quick Start

### 로컬 환경 설치

```bash
# minikube 설치 (macOS)
brew install minikube

# 클러스터 시작
minikube start

# kubectl 설치 확인
kubectl version --client

# 클러스터 상태 확인
kubectl cluster-info
```

### Hello World

```bash
# nginx 배포
kubectl create deployment nginx --image=nginx:1.25

# 서비스 노출
kubectl expose deployment nginx --port=80 --type=NodePort

# 상태 확인
kubectl get pods,svc

# 접속 URL 확인 (minikube)
minikube service nginx --url
```

---

## 2. kubectl 필수 명령어

### 기본 명령어

```bash
# 리소스 조회
kubectl get pods                    # Pod 목록
kubectl get pods -o wide            # 상세 정보 (Node, IP)
kubectl get all                     # 모든 리소스
kubectl get pods -n kube-system     # 특정 네임스페이스

# 리소스 상세 정보
kubectl describe pod <pod-name>
kubectl describe deployment <name>

# 로그 확인
kubectl logs <pod-name>
kubectl logs -f <pod-name>          # 실시간 로그
kubectl logs <pod-name> -c <container>  # 특정 컨테이너

# Pod 접속
kubectl exec -it <pod-name> -- /bin/bash
kubectl exec -it <pod-name> -- sh   # bash 없는 경우
```

### CRUD 명령어

```bash
# 생성
kubectl apply -f deployment.yaml
kubectl create deployment nginx --image=nginx

# 수정
kubectl edit deployment nginx
kubectl set image deployment/nginx nginx=nginx:1.26

# 삭제
kubectl delete pod <pod-name>
kubectl delete -f deployment.yaml
kubectl delete deployment nginx

# 스케일링
kubectl scale deployment nginx --replicas=5
```

### 디버깅 명령어

```bash
# 이벤트 확인
kubectl get events --sort-by='.lastTimestamp'

# 리소스 사용량
kubectl top pods
kubectl top nodes

# Pod 상태 원인 파악
kubectl describe pod <pod-name> | grep -A 10 Events
```

---

## 3. YAML 매니페스트

### Deployment 예시

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service 예시

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
---
# 외부 노출용 (LoadBalancer)
apiVersion: v1
kind: Service
metadata:
  name: myapp-external
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### ConfigMap & Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=  # base64 encoded
```

### 환경변수로 주입

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:1.0.0
    envFrom:
    - configMapRef:
        name: myapp-config
    - secretRef:
        name: myapp-secret
```

---

## 4. 배포 전략

### Rolling Update (기본)

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 최대 추가 Pod 수
      maxUnavailable: 0  # 최대 불가용 Pod 수
```

```bash
# 이미지 업데이트 (롤링)
kubectl set image deployment/myapp myapp=myapp:2.0.0

# 롤아웃 상태 확인
kubectl rollout status deployment/myapp

# 롤백
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2
```

### Blue/Green & Canary

```bash
# Blue/Green: Service selector 변경
kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'

# Canary: replicas 비율 조정 (90% old, 10% new)
# 또는 Istio, Argo Rollouts 사용
```

---

## 5. Best Practices

### DO ✅

```yaml
# 1. 리소스 제한 설정
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"

# 2. Probe 설정
livenessProbe:
  httpGet:
    path: /health
    port: 8080
readinessProbe:
  httpGet:
    path: /ready
    port: 8080

# 3. 레이블 활용
metadata:
  labels:
    app: myapp
    version: v1
    env: production
```

### DON'T ❌

- ❌ `latest` 태그 사용 → 명시적 버전 태그 사용
- ❌ root로 컨테이너 실행 → securityContext 설정
- ❌ 리소스 제한 없이 배포 → requests/limits 필수
- ❌ ConfigMap/Secret 직접 값 입력 → 환경변수 주입

---

## 6. 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| **ImagePullBackOff** | 이미지 없거나 권한 없음 | 이미지 이름/태그 확인, imagePullSecrets |
| **CrashLoopBackOff** | 컨테이너 시작 직후 종료 | `kubectl logs` 로그 확인 |
| **Pending** | 스케줄링 실패 | 리소스 부족, Node selector 확인 |
| **OOMKilled** | 메모리 초과 | memory limit 증가 |
| **Readiness 실패** | 앱 준비 안 됨 | Probe 경로/포트 확인 |

### 디버깅 흐름

```bash
# 1. Pod 상태 확인
kubectl get pods

# 2. 이벤트 확인
kubectl describe pod <pod-name>

# 3. 로그 확인
kubectl logs <pod-name>

# 4. 컨테이너 접속
kubectl exec -it <pod-name> -- sh
```

---

## 7. 체크리스트

### 배포 전 확인

- [ ] 이미지 태그 명시 (latest 금지)
- [ ] resources requests/limits 설정
- [ ] liveness/readiness Probe 설정
- [ ] ConfigMap/Secret 분리

### 배포 후 확인

- [ ] `kubectl get pods` 상태 Running 확인
- [ ] `kubectl logs` 에러 없음
- [ ] Service 연결 테스트
- [ ] 모니터링 지표 확인

---

## 📖 다음 단계

> [!tip] 다음으로
> 실무 적용에 성공했다면 [[04-advanced|심화 학습]]에서 HA, 모니터링을 배워보세요.

---

## References

- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
