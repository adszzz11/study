# LiteLLM 실전 프로젝트

## 학습 목표

- 실제 프로젝트에 LiteLLM 적용하기
- Best Practices 익히기
- 프로덕션 배포 준비하기

---

## 프로젝트 1: AI 챗봇 API 서버

FastAPI와 LiteLLM을 결합한 챗봇 API 서버입니다.

### 프로젝트 구조

```
chatbot-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   └── chat.py
│   └── services/
│       └── llm.py
├── config.yaml
├── docker-compose.yaml
├── requirements.txt
└── .env
```

### requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
litellm==1.27.0
python-dotenv==1.0.0
pydantic==2.5.0
```

### app/services/llm.py

```python
from litellm import completion, acompletion
from typing import List, Dict, AsyncGenerator
import os

class LLMService:
    def __init__(self):
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-4o")

    async def chat(
        self,
        messages: List[Dict],
        model: str = None,
        stream: bool = False
    ):
        model = model or self.default_model

        if stream:
            return await self._stream_chat(messages, model)
        else:
            response = await acompletion(
                model=model,
                messages=messages
            )
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

    async def _stream_chat(
        self,
        messages: List[Dict],
        model: str
    ) -> AsyncGenerator:
        response = await acompletion(
            model=model,
            messages=messages,
            stream=True
        )

        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

llm_service = LLMService()
```

### app/routes/chat.py

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.llm import llm_service

router = APIRouter()

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: Optional[str] = None
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    content: str
    model: str
    usage: Dict[str, int]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if request.stream:
        return StreamingResponse(
            llm_service.chat(
                messages=request.messages,
                model=request.model,
                stream=True
            ),
            media_type="text/event-stream"
        )

    try:
        result = await llm_service.chat(
            messages=request.messages,
            model=request.model
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        async for chunk in llm_service._stream_chat(
            messages=request.messages,
            model=request.model or "gpt-4o"
        ):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

### app/main.py

```python
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import chat

load_dotenv()

app = FastAPI(title="AI Chatbot API")

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### 실행

```bash
# 환경 변수 설정
export OPENAI_API_KEY=sk-xxx

# 서버 실행
uvicorn app.main:app --reload --port 8000

# 테스트
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "안녕하세요!"}]
  }'
```

---

## 프로젝트 2: 멀티 프로바이더 API 게이트웨이

팀별로 다른 모델과 예산을 할당하는 API 게이트웨이입니다.

### config.yaml

```yaml
model_list:
  # 프리미엄 모델 (고비용)
  - model_name: premium
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: premium
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  # 표준 모델 (중간)
  - model_name: standard
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

  # 경제적 모델 (저비용)
  - model_name: economy
    litellm_params:
      model: groq/llama-3.2-90b-text-preview
      api_key: os.environ/GROQ_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL

litellm_settings:
  max_budget: 10000.0
  budget_duration: 1mo
  fallbacks:
    - premium: [standard]
    - standard: [economy]

router_settings:
  routing_strategy: least-busy
  num_retries: 3
  cooldown_time: 30
```

### docker-compose.yaml

```yaml
version: "3.9"
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    ports:
      - "4000:4000"
    volumes:
      - ./config.yaml:/app/config.yaml
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/litellm
    command: --config /app/config.yaml
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: litellm
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### 팀별 키 생성 스크립트

```python
# setup_teams.py
import requests
import os

PROXY_URL = "http://localhost:4000"
MASTER_KEY = os.environ["LITELLM_MASTER_KEY"]

teams = [
    {
        "name": "frontend",
        "budget": 500,
        "models": ["standard", "economy"],
        "rpm_limit": 50
    },
    {
        "name": "backend",
        "budget": 1000,
        "models": ["premium", "standard", "economy"],
        "rpm_limit": 100
    },
    {
        "name": "data",
        "budget": 2000,
        "models": ["premium", "standard"],
        "rpm_limit": 200
    }
]

def create_team_key(team):
    response = requests.post(
        f"{PROXY_URL}/key/generate",
        headers={"Authorization": f"Bearer {MASTER_KEY}"},
        json={
            "max_budget": team["budget"],
            "budget_duration": "1mo",
            "models": team["models"],
            "rpm_limit": team["rpm_limit"],
            "metadata": {"team": team["name"]}
        }
    )
    return response.json()

for team in teams:
    result = create_team_key(team)
    print(f"{team['name']}: {result['key']}")
```

---

## 프로젝트 3: 로컬 개발 + 클라우드 프로덕션

개발 환경에서는 로컬 LLM, 프로덕션에서는 클라우드 LLM을 사용합니다.

### config.dev.yaml

```yaml
# 개발 환경 - 로컬 Ollama 사용
model_list:
  - model_name: chat
    litellm_params:
      model: ollama/llama3.2
      api_base: http://localhost:11434

  - model_name: code
    litellm_params:
      model: ollama/codellama
      api_base: http://localhost:11434

general_settings:
  master_key: dev-key-1234

litellm_settings:
  set_verbose: true
```

### config.prod.yaml

```yaml
# 프로덕션 환경 - 클라우드 LLM 사용
model_list:
  - model_name: chat
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: chat
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: code
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL

litellm_settings:
  max_budget: 5000.0
  budget_duration: 1mo
  fallbacks:
    - chat: [code]

router_settings:
  routing_strategy: least-busy
```

### 환경별 실행 스크립트

```bash
#!/bin/bash
# run.sh

ENV=${1:-dev}

if [ "$ENV" == "dev" ]; then
    echo "Starting in development mode..."
    # Ollama 실행 확인
    ollama list || ollama run llama3.2
    litellm --config config.dev.yaml --port 4000

elif [ "$ENV" == "prod" ]; then
    echo "Starting in production mode..."
    litellm --config config.prod.yaml --port 4000

else
    echo "Usage: ./run.sh [dev|prod]"
fi
```

---

## Best Practices

### 1. 보안

```yaml
# 민감 정보는 환경 변수로
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY  # 하드코딩 X

# 가상 키 사용
# 직접 프로바이더 키 노출하지 않기
```

### 2. 에러 처리

```python
from litellm.exceptions import (
    AuthenticationError,
    RateLimitError,
    APIConnectionError
)

async def safe_chat(messages):
    try:
        response = await acompletion(
            model="gpt-4o",
            messages=messages,
            timeout=30
        )
        return response
    except AuthenticationError:
        # 키 문제 → 로깅, 알림
        logger.error("API key invalid")
        raise
    except RateLimitError:
        # 한도 초과 → 재시도 또는 폴백
        logger.warning("Rate limited, retrying...")
        await asyncio.sleep(1)
        return await safe_chat(messages)
    except APIConnectionError:
        # 연결 문제 → 폴백 모델
        logger.warning("Connection error, using fallback")
        return await acompletion(
            model="claude-3-5-sonnet-20241022",
            messages=messages
        )
```

### 3. 로깅

```yaml
litellm_settings:
  success_callback: ["langfuse"]  # 성공 로깅
  failure_callback: ["langfuse"]  # 실패 로깅

  # 또는 커스텀 로깅
  set_verbose: true
  json_logs: true
```

### 4. 캐싱

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: redis
    host: localhost
    port: 6379
    ttl: 3600  # 1시간
```

### 5. 타임아웃 설정

```yaml
litellm_settings:
  request_timeout: 60  # 전역 타임아웃

model_list:
  - model_name: fast-model
    litellm_params:
      model: groq/llama-3.2-90b-text-preview
      timeout: 10  # 모델별 타임아웃
```

### 6. 헬스체크

```python
import requests

def check_litellm_health():
    try:
        response = requests.get("http://localhost:4000/health", timeout=5)
        return response.status_code == 200
    except:
        return False
```

---

## 프로덕션 체크리스트

### 배포 전

- [ ] 환경 변수로 민감 정보 관리
- [ ] 데이터베이스 설정 (PostgreSQL)
- [ ] 레이트 리미팅 설정
- [ ] 예산 제한 설정
- [ ] 폴백 모델 구성
- [ ] 헬스체크 엔드포인트 설정
- [ ] 로깅/모니터링 설정

### 배포 후

- [ ] 헬스체크 모니터링
- [ ] 비용 대시보드 확인
- [ ] 알림 설정 테스트
- [ ] 로드 테스트

---

## 정리

| 프로젝트 | 핵심 학습 |
|---------|----------|
| 챗봇 API | FastAPI + LiteLLM 연동 |
| API 게이트웨이 | 팀별 예산 관리, 가상 키 |
| 멀티 환경 | 개발/프로덕션 설정 분리 |

### 다음 단계

- [[cheatsheet|치트시트]] - 빠른 참조
- [[03-references|참고 자료]] - 추가 학습 자료
