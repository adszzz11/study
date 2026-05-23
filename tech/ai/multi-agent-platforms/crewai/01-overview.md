# Part 1. CrewAI 개요

## 📌 3대 추상화

```
Agent      → 역할(role)·목표(goal)·배경(backstory)을 가진 행위자
   │
   ├─ tools: 사용 가능한 도구
   └─ llm: 어떤 모델 쓸지

Task       → 구체적 작업
   │
   ├─ description: 무엇을
   ├─ expected_output: 어떤 형식으로
   ├─ agent: 누가
   └─ context: 어떤 이전 결과 참조

Crew       → 에이전트 + 작업의 묶음
   │
   ├─ agents: 멤버
   ├─ tasks: 할 일
   ├─ process: 어떤 방식 (sequential/hierarchical)
   └─ memory: 공유 메모리
```

## 🔁 두 가지 Process 타입

### Sequential
- 작업이 정의된 순서대로 실행
- 이전 task의 output이 다음 task의 context로 자동 전달
- 단순하고 예측 가능

### Hierarchical
- **매니저 에이전트가 자동 생성**되어 다른 에이전트에 작업 위임
- LLM이 누구에게 무엇을 시킬지 결정
- 동적이지만 비용·실수↑

## 🆕 CrewAI Flows (2024 추가)

기존 Crew는 "에이전트 자율 결정"이 강함. **Flows**는 그 반대:
- 이벤트 드리븐 + 명시적 분기
- 각 step이 함수로 정의
- 상태 머신처럼 동작
- 프로덕션 컨트롤 가능

```python
from crewai.flow.flow import Flow, listen, start

class ResearchFlow(Flow):
    @start()
    def gather_topic(self):
        return {"topic": "LangGraph"}
    
    @listen(gather_topic)
    def research(self, ctx):
        crew = research_crew()
        return crew.kickoff(inputs=ctx)
    
    @listen(research)
    def review(self, output):
        return review_crew().kickoff(inputs={"draft": output})
```

## ⚖️ 장단점

### ✅ 장점
- **러닝 커브 최저**: 20줄로 시작
- **YAML+decorator 패턴**: 역할·작업을 선언적으로
- **LangChain 독립**: 더 가볍고 빠름
- **100k+ certified developers** — 검색하면 답이 있음
- **CrewAI AMP**: 엔터프라이즈 트레이싱·관제

### ❌ 단점
- **체크포인트 없음** (Flows로 부분 해결)
- **세밀 제어 한계**: hierarchical은 LLM 판단에 위임
- **A2A 통신 통제 약함**
- **장기 실행 시 상태 손실**: 프로덕션엔 Flows 필수
- **프로토타입 → 프로덕션 사이 간극** (LangGraph로 마이그레이션 흔함)

## 🎯 누가 쓰면 좋은가

| 상황 | 적합도 |
|------|--------|
| 빠른 프로토타입 | ⭐⭐⭐⭐⭐ |
| 비즈니스 워크플로우 (리서치→작성→발행) | ⭐⭐⭐⭐⭐ |
| 명확한 역할 분담이 있는 작업 | ⭐⭐⭐⭐⭐ |
| 복잡한 상태 그래프 | ⭐⭐ (LangGraph 추천) |
| 프로덕션 + 체크포인트 필수 | ⭐⭐⭐ (Flows로 보완 가능) |
| 노코드 | ⭐ (Dify 추천) |

## 📊 채택 사례

- Y Combinator 스타트업 다수
- Microsoft, IBM, Oracle 내부 PoC
- AMP Suite 유료 사용자 다수
- 100k+ certified developers community

## 🔗 다음

→ [02-ecosystem.md](02-ecosystem.md) — 다른 프레임워크와 비교
