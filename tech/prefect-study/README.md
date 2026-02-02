# Prefect 심층 스터디

> **한 줄 정의**: Python 함수를 프로덕션급 데이터 파이프라인으로 변환하는 워크플로우 오케스트레이션 프레임워크

## 3줄 요약

1. Python 함수에 데코레이터만 붙이면 자동으로 상태 추적, 실패 처리, 모니터링이 되는 데이터 파이프라인 구축
2. DSL이나 복잡한 설정 파일 없이 순수 Python으로 워크플로우 정의
3. 로컬, 클라우드, 하이브리드 어디서든 실행 가능한 유연한 배포

## 핵심 키워드

`#워크플로우오케스트레이션` `#데이터파이프라인` `#Python` `#ETL` `#MLOps`

---

## Quick Start (30초 체험)

```bash
# 1. 설치 (Python 3.10+ 필요)
pip install prefect

# 2. 서버 시작 (선택)
prefect server start
```

```python
from prefect import flow, task

@task
def say_hello(name: str) -> str:
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

@flow(name="My First Flow")
def hello_flow(name: str = "World"):
    result = say_hello(name)
    return result

# 실행
if __name__ == "__main__":
    hello_flow("Prefect")
```

```bash
# 3. 실행
python hello_prefect.py

# 4. UI 확인
# 브라우저에서 http://localhost:4200 접속
```

---

## 목차

| 파일 | 내용 |
|------|------|
| [01-overview.md](./01-overview.md) | 핵심 개념, 장단점, 주요 사용 사례 |
| [02-ecosystem.md](./02-ecosystem.md) | 관련 기술, 경쟁 비교, 최신 동향 |
| [03-references.md](./03-references.md) | 공식 문서, 학습 자료, 커뮤니티 |
| [04-learning/](./04-learning/) | 상세 학습 로드맵 (주제별) |
| [05-projects.md](./05-projects.md) | 실전 프로젝트 및 Best Practices |
| [cheatsheet.md](./cheatsheet.md) | 자주 쓰는 명령어/코드 빠른 참조 |

### 04-learning/ 상세

| 파일 | 주제 |
|------|------|
| [01-flow-task.md](./04-learning/01-flow-task.md) | Flow와 Task 기초 |
| [02-deployment.md](./04-learning/02-deployment.md) | Deployment와 스케줄링 |
| [03-state-management.md](./04-learning/03-state-management.md) | 상태 관리와 에러 처리 |
| [04-concurrency.md](./04-learning/04-concurrency.md) | 병렬 실행과 동시성 |
| [05-work-pools.md](./04-learning/05-work-pools.md) | Work Pools와 인프라 관리 |
| [06-cloud-vs-selfhosted.md](./04-learning/06-cloud-vs-selfhosted.md) | Prefect Cloud vs Self-hosted |

---

## 학습 플랜

### Day 1: 기초 (2-3시간)
- [ ] Quick Start 따라하기
- [ ] [01-overview.md](./01-overview.md) 읽기
- [ ] 간단한 Flow/Task 작성

### Day 2: 실행 환경 (2-3시간)
- [ ] [04-learning/01-flow-task.md](./04-learning/01-flow-task.md)
- [ ] [04-learning/02-deployment.md](./04-learning/02-deployment.md)
- [ ] 로컬 서버에서 스케줄 설정

### Day 3: 고급 기능 (3-4시간)
- [ ] [04-learning/03-state-management.md](./04-learning/03-state-management.md)
- [ ] [04-learning/04-concurrency.md](./04-learning/04-concurrency.md)
- [ ] 에러 처리 및 병렬 처리 실습

### Day 4: 프로덕션 (3-4시간)
- [ ] [04-learning/05-work-pools.md](./04-learning/05-work-pools.md)
- [ ] [04-learning/06-cloud-vs-selfhosted.md](./04-learning/06-cloud-vs-selfhosted.md)
- [ ] Docker 기반 배포 실습

### Day 5: 프로젝트 (4시간+)
- [ ] [05-projects.md](./05-projects.md) 미니 프로젝트 구현
- [ ] 실제 ETL 파이프라인 구축
