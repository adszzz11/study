# 4-3. Streaming 응답

## 🌊 기본 스트리밍

```python
stream = client.run(
    agent=triage,
    messages=[{"role":"user","content":"..."}],
    stream=True,
)

for chunk in stream:
    if "content" in chunk and chunk["content"]:
        print(chunk["content"], end="", flush=True)
    if "delim" in chunk and chunk["delim"] == "start":
        print(f"\n[{chunk['sender']}]: ", end="")
```

## 🎭 이벤트 종류

- `delim: "start"` / `"end"` — 발화 시작/끝
- `content` — 텍스트 청크
- `tool_call` — 도구 호출 시작
- `sender` — 현재 발화 에이전트 이름
- `response` — 최종 결과 객체

## 🔌 핸드오프 시 스트리밍

```python
[Triage]: 결제 문의로 보입니다. Sales에게 연결합니다.
[Sales]: 안녕하세요, 어떤 결제 문제 있으신가요?
```

스트림에서 sender가 바뀜 → 핸드오프 발생.

## 🌐 FastAPI Server-Sent Events
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat(msg: str):
    def gen():
        stream = client.run(triage, [{"role":"user","content":msg}], stream=True)
        for chunk in stream:
            yield f"data: {json.dumps(chunk)}\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```

## ⚠️ 함정
- chunk 형식이 OpenAI native와 약간 다름 → docs 참고
- 핸드오프 시점에 빈 줄 처리 주의
- 에러 발생 시 stream 닫히는 패턴 핸들링

## 🔗 다음 → [04-migrate-to-agents-sdk.md](04-migrate-to-agents-sdk.md)
