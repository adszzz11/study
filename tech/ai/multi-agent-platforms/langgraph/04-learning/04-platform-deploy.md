# 4-4. LangGraph Platform 배포

## 🚀 옵션 비교

| 옵션 | 적합 |
|------|------|
| **FastAPI 래핑** | 가벼움, 직접 통제 |
| **LangGraph Platform Cloud** | 매니지드, HITL UI, Cron, OAuth |
| **LangGraph Platform Self-hosted** | 회사 인프라, 데이터 격리 |
| **Paperclip 직원으로** | 다른 에이전트와 통합 운영 |

## 🐳 FastAPI 패턴

```python
# main.py
from fastapi import FastAPI
from app import compiled_graph

app = FastAPI()

@app.post("/run")
async def run(payload: dict):
    config = {"configurable": {"thread_id": payload["session_id"]}}
    result = compiled_graph.invoke(payload["input"], config=config)
    return result

@app.post("/resume")
async def resume(payload: dict):
    from langgraph.types import Command
    config = {"configurable": {"thread_id": payload["session_id"]}}
    result = compiled_graph.invoke(
        Command(resume=payload["value"]), config=config
    )
    return result
```

```dockerfile
FROM python:3.12-slim
RUN pip install langgraph langchain-anthropic langgraph-checkpoint-postgres fastapi uvicorn
COPY . /app
WORKDIR /app
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## ☁️ LangGraph Platform

### 1. langgraph.json
```json
{
  "dependencies": ["."],
  "graphs": {
    "my-graph": "./app.py:compiled_graph"
  },
  "env": ".env"
}
```

### 2. CLI
```bash
pip install langgraph-cli

# 로컬 dev
langgraph dev

# Cloud 배포
langgraph deploy
```

### 3. 기능
- 자동 OpenAPI
- thread/state 관리 UI
- Cron 스케줄러
- HITL 승인 UI
- LangSmith 자동 연동

## 🔌 Studio (데스크탑 IDE)

```bash
# https://github.com/langchain-ai/langgraph-studio 에서 다운로드
```

- 그래프 시각화
- 실행 디버그
- state 편집
- 시간여행 UI

## 🛡️ 프로덕션 체크리스트
- [ ] PostgresSaver + 백업 정책
- [ ] thread_id 격리 (멀티 유저)
- [ ] recursion_limit, max_iter 명시
- [ ] LangSmith 키 + sampling rate
- [ ] interrupt timeout (방치된 thread 정리)
- [ ] OpenTelemetry export
- [ ] 시크릿 env로
- [ ] 로드 테스트 (k6, locust)

## 🔗 본 vault 내
- 다음 → [../05-projects.md](../05-projects.md)
