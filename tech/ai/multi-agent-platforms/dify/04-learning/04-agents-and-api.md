# 4-4. Agent + API 통합

## 🤖 Agent App 생성

**Studio → Create App → Agent**

- **Function Calling 모드** (GPT-4o, Claude 등 지원 모델): 모델이 도구 직접 호출
- **ReAct 모드**: 명시적 think → action → observation 패턴

### 도구 추가
- 50+ 내장: Google Search, DALL·E, Wolfram, Slack Send Message, ...
- KB Search (자동)
- Custom Plugin
- MCP Server (Claude Code 호환)
- HTTP API (OpenAPI 스펙 import)

## 🔌 API 통합 (외부 앱에서 Dify 호출)

각 앱마다 자동 생성되는 API:

```bash
curl -X POST 'http://localhost/v1/chat-messages' \
  -H 'Authorization: Bearer app-XXXX' \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": {},
    "query": "안녕",
    "response_mode": "streaming",
    "user": "user-123",
    "conversation_id": ""
  }'
```

스트리밍·non-streaming 둘 다 지원.

## 🐍 Python SDK

```python
from dify_client import ChatClient

client = ChatClient(api_key="app-XXXX", base_url="http://localhost/v1")
for event in client.create_chat_message(
    inputs={}, query="안녕", user="u-1", response_mode="streaming"
):
    print(event)
```

## 🔄 외부 시스템 통합 예

### Telegram Bot
```python
@bot.message_handler()
def handle(msg):
    response = dify_client.create_chat_message(
        query=msg.text, user=str(msg.chat.id),
        conversation_id=conv_cache.get(msg.chat.id, "")
    )
    bot.reply_to(msg, response.answer)
    conv_cache[msg.chat.id] = response.conversation_id
```

### Paperclip 직원
Dify를 webhook 어댑터로 등록 → 외부 비기술자는 캔버스 편집, Paperclip이 호출.

## 🔐 보안

- API key는 앱 단위 발급 → granular 통제
- Rate limit 설정
- 로그에 시크릿 마스킹
- Tailnet 외 노출 안 함

## ✅ 체크포인트
- [ ] Agent 앱 생성, 내장 도구 1개 작동
- [ ] API key로 외부 curl 호출 성공
- [ ] conversation_id로 멀티턴 유지
- [ ] DSL export → 다른 환경 import

## 🔗 다음 → [../05-projects.md](../05-projects.md)
