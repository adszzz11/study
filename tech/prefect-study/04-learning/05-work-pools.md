# Work Pools와 인프라 관리

## 📌 핵심 개념

Work Pool은 Flow가 실행될 인프라를 정의합니다:

| 타입 | 설명 |
|------|------|
| **Process** | 로컬 프로세스 |
| **Docker** | 컨테이너 실행 |
| **Kubernetes** | K8s Job으로 실행 |

---

## 💻 설정 예제: Docker Work Pool

### 1. Work Pool 생성

```bash
# Work Pool 생성
prefect work-pool create my-docker-pool --type docker

# Worker 시작 (Flow 실행을 대기)
prefect worker start --pool my-docker-pool
```

### 2. Flow 배포

```python
from prefect import flow

@flow
def containerized_flow():
    return "Running in Docker!"

if __name__ == "__main__":
    containerized_flow.deploy(
        name="docker-deployment",
        work_pool_name="my-docker-pool",
        image="my-registry/my-image:latest"
    )
```

### 3. prefect.yaml로 인프라 설정

```yaml
# prefect.yaml
deployments:
  - name: k8s-etl
    entrypoint: flows/etl.py:etl_pipeline
    work_pool:
      name: kubernetes-pool
      job_variables:
        image: "{{ build-image.image }}"
        cpu_request: "500m"
        memory_request: "1Gi"

build:
  - prefect_docker.deployments.steps.build_docker_image:
      id: build-image
      dockerfile: Dockerfile
      image_name: my-flow
      tag: latest
```

---

## ✅ 체크포인트

- [ ] Work Pool의 역할을 설명할 수 있는가?
- [ ] Docker/Kubernetes Work Pool을 설정할 수 있는가?
- [ ] Worker의 역할을 이해하는가?

---

## ⚠️ 흔한 실수

| 실수 | 해결책 |
|------|--------|
| Worker 시작 안 함 | Deployment가 실행되지 않음 |
| Work Pool 타입 불일치 | Worker 타입과 일치해야 함 |

---

## 🔗 더 알아보기

- [Work pools](https://docs.prefect.io/v3/deploy/infrastructure-concepts/work-pools)
