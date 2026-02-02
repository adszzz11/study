# Prefect Cheat Sheet

## 설치 및 시작

```bash
# 설치
pip install prefect

# 서버 시작
prefect server start

# 버전 확인
prefect version
```

## 기본 데코레이터

```python
from prefect import flow, task

@task(retries=3, retry_delay_seconds=10)
def my_task():
    pass

@flow(name="My Flow", log_prints=True)
def my_flow():
    my_task()
```

## CLI 명령어

| 명령어 | 설명 |
|--------|------|
| `prefect server start` | 로컬 서버 시작 |
| `prefect deploy` | Flow 배포 |
| `prefect work-pool create NAME --type TYPE` | Work Pool 생성 |
| `prefect worker start --pool NAME` | Worker 시작 |
| `prefect config set KEY=VALUE` | 설정 변경 |
| `prefect cloud login` | Cloud 로그인 |

## Task 옵션

```python
@task(
    retries=3,                    # 재시도 횟수
    retry_delay_seconds=10,       # 재시도 대기
    cache_key_fn=task_input_hash, # 캐싱
    cache_expiration=timedelta(hours=1),
    timeout_seconds=300           # 타임아웃
)
```

## Flow 옵션

```python
@flow(
    name="My Flow",
    description="설명",
    log_prints=True,              # print 로깅
    timeout_seconds=3600,         # 타임아웃
    retries=1
)
```

## 병렬 실행

```python
# map 사용
results = my_task.map([1, 2, 3, 4, 5])

# 결과 가져오기
values = [r.result() for r in results]
```

## 스케줄 설정

```python
# serve로 스케줄
my_flow.serve(
    name="my-deployment",
    cron="0 9 * * *"  # 매일 오전 9시
)
```

## Cron 표현식

| 표현식 | 의미 |
|--------|------|
| `* * * * *` | 매분 |
| `0 * * * *` | 매시간 |
| `0 9 * * *` | 매일 오전 9시 |
| `0 9 * * 1` | 매주 월요일 오전 9시 |
| `0 0 1 * *` | 매월 1일 자정 |

## 상태 확인

```python
result = my_flow(return_state=True)

if result.is_completed():
    print("성공")
elif result.is_failed():
    print("실패")
```

## 환경 변수

```bash
# API URL 설정
export PREFECT_API_URL="http://localhost:4200/api"

# Cloud API 키
export PREFECT_API_KEY="pnu_xxx"
```

## Block 사용

```python
from prefect.blocks.system import Secret

# 저장
Secret(value="my-secret").save("my-key")

# 로드
secret = Secret.load("my-key").get()
```

## 유용한 링크

- 공식 문서: https://docs.prefect.io/
- GitHub: https://github.com/PrefectHQ/prefect
- Slack: https://prefect.io/slack
