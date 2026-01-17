# Blue-Green vs Canary vs Rolling 배포 중 선택 기준은?

## 답변

[여기에 답변 작성]

## 핵심 키워드

- Blue-Green Deployment
- Canary Deployment
- Rolling Deployment
- 트래픽 분산
- 리스크 관리
- 리소스 효율성

## Blue-Green 배포

### 특징
-

### 장점
-

### 단점
-

### 적합한 상황
-

## Canary 배포

### 특징
-

### 장점
-

### 단점
-

### 적합한 상황
-

## Rolling 배포

### 특징
-

### 장점
-

### 단점
-

### 적합한 상황
-

## 선택 기준

-

## 설정 예시

### Kubernetes Rolling Update
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
```

### Kubernetes Blue-Green (Service Switch)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: green  # blue에서 green으로 전환
```

## 참고 자료

-
