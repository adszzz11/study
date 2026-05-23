# 4-2. Process — Sequential vs Hierarchical

## 🔁 Sequential — 가장 흔함

```python
crew = Crew(
    agents=[r, w, e],
    tasks=[t1, t2, t3],
    process=Process.sequential,
)
```

- 명시한 task 순서대로 실행
- 각 task의 output이 다음 task의 context로 흐름
- 예측 가능, 디버깅 쉬움

**적합**:
- 단계가 명확 (조사 → 작성 → 검토)
- 비용/품질 통제 우선

## 👔 Hierarchical — 매니저가 분배

```python
crew = Crew(
    agents=[w, e],    # 일반 직원만
    tasks=[t1, t2],
    process=Process.hierarchical,
    manager_llm=ChatAnthropic(model="claude-opus-4-7"),
    # 또는 manager_agent=specific_agent
)
```

- CrewAI가 **자동으로 매니저 에이전트 생성**
- 매니저가 LLM으로 누구에게 무엇을 시킬지 판단
- 동적 위임, 결과 검증, 재할당

**적합**:
- 작업이 동적 (어떤 직원이 처리할지 미정)
- 검증·재시도 로직 자동화

**주의**:
- LLM 호출 추가 → 비용·지연 증가
- LLM 판단 실수 가능 (잘못된 직원 할당)

## 🎯 매니저 커스터마이즈

```python
manager = Agent(
    role="프로젝트 매니저",
    goal="작업을 적합한 직원에게 할당하고 품질을 검토",
    backstory="20년차 PM. 위임 정확함.",
    allow_delegation=True,
)

crew = Crew(
    agents=[w, e],
    tasks=[t1, t2],
    process=Process.hierarchical,
    manager_agent=manager,
)
```

## 🔀 둘을 섞기 — Flows로

기본 Crew는 한 process만. **CrewAI Flows**로 단계마다 다른 process 사용:

```python
class HybridFlow(Flow):
    @start()
    def discover(self):
        crew = Crew(..., process=Process.hierarchical)  # 매니저가 탐색
        return crew.kickoff()
    
    @listen(discover)
    def execute(self, plan):
        crew = Crew(..., process=Process.sequential)    # 명확한 실행
        return crew.kickoff(inputs={"plan": plan})
```

## ✅ 결정 가이드

| 상황 | 추천 |
|------|------|
| 처음 만들기 | Sequential |
| 단계 명확 | Sequential |
| 작업 종류가 사전에 안 정해짐 | Hierarchical |
| 결과 검토·재시도 자동화 필요 | Hierarchical |
| 프로덕션 + 비용 통제 | Sequential 또는 Flows |

## 🔗 다음 → [03-tools-and-memory.md](03-tools-and-memory.md)
