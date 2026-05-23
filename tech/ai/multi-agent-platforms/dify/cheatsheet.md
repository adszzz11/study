# Dify Cheat Sheet

## 🚀 설치
```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
# http://localhost
```

## 🐳 Docker
```bash
docker compose ps
docker compose logs -f api
docker compose logs worker
docker compose restart
docker compose pull && docker compose up -d   # 업데이트
docker compose down -v                         # ⚠️ 데이터 삭제
```

## 🔑 환경변수 (.env 핵심)
```bash
NGINX_PORT=80
INIT_PASSWORD=admin-pw
ALLOW_REGISTRATION=false
SECRET_KEY=$(openssl rand -hex 32)
DB_PASSWORD=...
REDIS_PASSWORD=...
VECTOR_STORE=weaviate          # 또는 milvus, qdrant, pgvector
```

## 🌐 API 호출
```bash
# Chat
curl -X POST 'http://localhost/v1/chat-messages' \
  -H 'Authorization: Bearer app-KEY' \
  -d '{"inputs":{},"query":"안녕","user":"u-1","response_mode":"blocking"}'

# Workflow
curl -X POST 'http://localhost/v1/workflows/run' \
  -H 'Authorization: Bearer app-KEY' \
  -d '{"inputs":{"text":"..."}, "user":"u-1"}'

# Completion
curl -X POST 'http://localhost/v1/completion-messages' ...
```

## 🐍 Python SDK
```bash
pip install dify-client
```
```python
from dify_client import ChatClient, CompletionClient
c = ChatClient(api_key="app-KEY", base_url="http://localhost/v1")
```

## 📚 KB API
```bash
# 문서 업로드
curl -X POST 'http://localhost/v1/datasets/{dataset_id}/document/create-by-file' \
  -H 'Authorization: Bearer dataset-KEY' \
  -F 'data={"indexing_technique":"high_quality"}' \
  -F 'file=@my.pdf'
```

## 💾 백업
```bash
# Postgres
docker compose exec db pg_dump -U postgres dify > backup.sql

# Weaviate (별도 procedure)
docker compose exec weaviate sh -c "..."
```

## 🔗 빠른 링크
- 공식: https://github.com/langgenius/dify
- Docs: https://docs.dify.ai
- 본 study: `study/tech/ai/multi-agent-platforms/dify/`
