---
date: 2026-02-02
tags:
  - tech
  - modal
  - web
  - api
  - tutorial
parent: "[[../README]]"
---

# Modal - 웹 엔드포인트 만들기

> [[03-gpu|이전: GPU 사용]] | [[../README|목차]] | [[05-volumes|다음: 볼륨]]

---

## 1. 웹 엔드포인트 기본

### @modal.web_endpoint()

가장 간단한 웹 엔드포인트:

```python
import modal

app = modal.App("web-example")

@app.function()
@modal.web_endpoint()
def hello():
    return {"message": "Hello, World!"}
```

배포:
```bash
modal deploy app.py
```

결과:
```
https://your-workspace--web-example-hello.modal.run
```

### HTTP 메서드 지정

```python
@app.function()
@modal.web_endpoint(method="GET")
def get_data():
    return {"data": "값"}

@app.function()
@modal.web_endpoint(method="POST")
def post_data(item: dict):
    return {"received": item}
```

---

## 2. FastAPI 통합

### @modal.asgi_app()

전체 FastAPI 앱을 Modal에 배포:

```python
import modal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = modal.App("fastapi-example")

# FastAPI 앱 정의
web_app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@web_app.get("/")
def root():
    return {"message": "Welcome to Modal FastAPI!"}

@web_app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@web_app.post("/items")
def create_item(item: Item):
    return {"created": item.dict()}

# Modal에 FastAPI 앱 연결
@app.function()
@modal.asgi_app()
def fastapi_app():
    return web_app
```

### 로컬 개발

```bash
# 핫 리로드 모드로 로컬 실행
modal serve app.py
```

브라우저에서 `http://localhost:8000` 접속

---

## 3. GPU + 웹 엔드포인트

### ML 모델 API

```python
import modal
from fastapi import FastAPI
from pydantic import BaseModel

app = modal.App("ml-api")

image = modal.Image.debian_slim().pip_install(
    "torch", "transformers", "fastapi"
)

web_app = FastAPI()

class TextRequest(BaseModel):
    text: str
    max_length: int = 100

class TextResponse(BaseModel):
    generated: str

# GPU를 사용하는 모델 함수
@app.function(gpu="T4", image=image)
def generate(prompt: str, max_length: int) -> str:
    from transformers import pipeline

    generator = pipeline("text-generation", model="gpt2", device=0)
    result = generator(prompt, max_length=max_length)
    return result[0]["generated_text"]

# 웹 엔드포인트 (CPU)
@app.function(image=image)
@modal.asgi_app()
def api():
    @web_app.post("/generate", response_model=TextResponse)
    def generate_endpoint(request: TextRequest):
        # GPU 함수 호출
        result = generate.remote(request.text, request.max_length)
        return TextResponse(generated=result)

    return web_app
```

---

## 4. 간단한 웹 엔드포인트

### JSON 응답

```python
@app.function()
@modal.web_endpoint()
def api_endpoint(name: str = "World"):
    return {
        "greeting": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat()
    }
```

호출:
```bash
curl "https://your-url.modal.run?name=Modal"
```

### 쿼리 파라미터

```python
@app.function()
@modal.web_endpoint(method="GET")
def search(query: str, limit: int = 10):
    # query와 limit은 URL 쿼리 파라미터로 받음
    results = perform_search(query, limit)
    return {"results": results}
```

### POST 요청 처리

```python
from pydantic import BaseModel

class RequestBody(BaseModel):
    text: str
    option: bool = False

@app.function()
@modal.web_endpoint(method="POST")
def process(body: RequestBody):
    return {"processed": body.text, "option": body.option}
```

호출:
```bash
curl -X POST "https://your-url.modal.run" \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "option": true}'
```

---

## 5. 이미지 반환

### 이미지 생성 API

```python
import modal
from fastapi import Response

app = modal.App("image-api")

image = modal.Image.debian_slim().pip_install("pillow")

@app.function(image=image)
@modal.web_endpoint()
def generate_image(width: int = 100, height: int = 100, color: str = "red"):
    from PIL import Image
    import io

    # 이미지 생성
    img = Image.new("RGB", (width, height), color)

    # 바이트로 변환
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="image/png"
    )
```

---

## 6. 인증 추가

### API 키 인증

```python
import modal
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = modal.App("auth-api")

web_app = FastAPI()
security = HTTPBearer()

API_KEY = "your-secret-key"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

@web_app.get("/protected")
def protected_route(token: str = Depends(verify_token)):
    return {"message": "인증됨!", "data": "비밀 데이터"}

@app.function()
@modal.asgi_app()
def api():
    return web_app
```

호출:
```bash
curl -H "Authorization: Bearer your-secret-key" \
  "https://your-url.modal.run/protected"
```

### Modal Secret 활용

```python
import os
import modal

app = modal.App("secure-api")

@app.function(secrets=[modal.Secret.from_name("api-keys")])
@modal.web_endpoint()
def secure_endpoint(api_key: str):
    valid_key = os.environ["API_KEY"]
    if api_key != valid_key:
        return {"error": "Invalid key"}, 401
    return {"message": "Success"}
```

---

## 7. 배포와 관리

### 배포 명령어

```bash
# 배포
modal deploy app.py

# 배포된 앱 확인
modal app list

# 앱 중지
modal app stop <app-name>
```

### URL 구조

```
https://{workspace}--{app-name}-{function-name}.modal.run

예시:
https://myworkspace--ml-api-generate.modal.run
```

### 커스텀 도메인

Modal 대시보드에서 커스텀 도메인 설정 가능

---

## 8. 실전 예제: 간단한 API 서버

```python
import modal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = modal.App("todo-api")

web_app = FastAPI(title="Todo API", version="1.0")

# 메모리 저장소 (간단한 예시)
todos = {}

class Todo(BaseModel):
    title: str
    completed: bool = False

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: str

@web_app.get("/")
def root():
    return {"message": "Todo API", "docs": "/docs"}

@web_app.get("/todos")
def list_todos():
    return list(todos.values())

@web_app.post("/todos", response_model=TodoResponse)
def create_todo(todo: Todo):
    todo_id = len(todos) + 1
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "completed": todo.completed,
        "created_at": datetime.now().isoformat()
    }
    todos[todo_id] = new_todo
    return new_todo

@web_app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@web_app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"message": "Deleted"}

@app.function()
@modal.asgi_app()
def api():
    return web_app
```

---

## 9. 체크리스트

### 학습 확인

- [ ] @modal.web_endpoint() 사용 가능
- [ ] @modal.asgi_app()으로 FastAPI 배포 가능
- [ ] GPU와 웹 엔드포인트 연결 가능
- [ ] 다양한 HTTP 메서드 처리 가능
- [ ] 인증 구현 방법 이해
- [ ] 배포 및 관리 명령어 숙지

---

## 다음 단계

> [!tip] 다음으로
> 웹 엔드포인트를 만들 수 있게 되었다면 [[05-volumes|볼륨과 영구 저장소]]를 배워보세요.

---

## References

- [Modal Web Endpoints](https://modal.com/docs/guide/webhooks)
- [Modal ASGI Apps](https://modal.com/docs/guide/webhooks#asgi)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
