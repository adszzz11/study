# 4-4. CrewAI Flows로 프로덕션 가기

## 🚀 왜 Flows가 필요한가

기본 Crew의 한계:
- 상태 영속화 ✗
- 명시적 분기/루프 ✗
- 외부 이벤트 트리거 ✗
- 부분 재실행 ✗

Flows가 이 모두 해결.

## 🌊 Flow 기본 구조

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel

class State(BaseModel):
    topic: str = ""
    draft: str = ""
    approved: bool = False

class ContentFlow(Flow[State]):
    @start()
    def gather(self):
        self.state.topic = input("주제? ")
    
    @listen(gather)
    def research(self):
        crew = research_crew()
        result = crew.kickoff(inputs={"topic": self.state.topic})
        self.state.draft = str(result)
    
    @router(research)
    def review(self):
        # 분기 결정
        if len(self.state.draft) < 500:
            return "redo"
        return "publish"
    
    @listen("redo")
    def redo(self):
        # 다시 research 호출
        self.research()
    
    @listen("publish")
    def publish(self):
        Path("output.md").write_text(self.state.draft)
        print("발행 완료")

ContentFlow().kickoff()
```

## 🔑 상태 영속화

```python
flow = ContentFlow()
flow.kickoff()

# 상태 저장
state_json = flow.state.model_dump_json()
Path("flow.state.json").write_text(state_json)

# 재개
flow = ContentFlow()
flow.state = State.model_validate_json(Path("flow.state.json").read_text())
flow.kickoff_from_state()
```

## ⏸️ HITL (Human-in-the-loop)

```python
@listen(research)
def approval_gate(self):
    print(f"초안:\n{self.state.draft}")
    answer = input("승인? (y/n): ")
    self.state.approved = (answer == "y")
```

또는 외부 알림(텔레그램):
```python
@listen(research)
async def approval_gate(self):
    await telegram.send(f"초안 검토: {self.state.draft}\n/approve")
    self.state.approved = await wait_for_approval(timeout=3600)
```

## 🌐 API로 노출

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/run")
async def run(topic: str):
    flow = ContentFlow()
    flow.state.topic = topic
    flow.kickoff()
    return {"draft": flow.state.draft}
```

## 📊 Observability (AMP)

```python
import crewai
crewai.amp_init(api_key=os.getenv("CREWAI_AMP_KEY"))
```

자동으로:
- 모든 LLM 호출 trace
- Token usage 집계
- 실패 알림
- 대시보드

## 🐳 Docker 배포

```dockerfile
FROM python:3.12-slim
RUN pip install crewai 'crewai[tools]' fastapi uvicorn
COPY . /app
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## ✅ 프로덕션 체크리스트
- [ ] Flow + State 모델 사용
- [ ] 상태 영속화 (DB나 파일)
- [ ] HITL 게이트 (위험 작업)
- [ ] max_rpm·max_iter로 비용 통제
- [ ] AMP 또는 LangSmith 트레이싱
- [ ] Sentry 같은 오류 추적
- [ ] 헬스체크 엔드포인트
- [ ] 시크릿은 env로

## 🔗 다음 → [../05-projects.md](../05-projects.md)
