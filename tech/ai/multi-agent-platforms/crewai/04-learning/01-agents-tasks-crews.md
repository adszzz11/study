# 4-1. Agents, Tasks, Crews — 3대 추상화

## 🎭 Agent 정의

```python
from crewai import Agent
from langchain_community.tools import DuckDuckGoSearchRun

researcher = Agent(
    role="시니어 리서치 분석가",
    goal="AI 트렌드를 정확하고 깊이 있게 조사",
    backstory="""당신은 10년차 AI 분석가. 
    1차 자료를 우선시하고, 출처를 명확히 표기한다.""",
    tools=[DuckDuckGoSearchRun()],
    llm=ChatAnthropic(model="claude-opus-4-7"),
    verbose=True,
    allow_delegation=False,    # 다른 에이전트에 위임 허용?
    max_iter=15,               # 최대 반복
    memory=True,
)
```

### 좋은 backstory 작성 팁
- 직무 경력 명시 (10년차 등)
- 작업 스타일 (정확/창의/꼼꼼)
- 출력 선호 (한국어/마크다운/번호 매김)
- 금기사항 (출처 없는 추정 금지)

## 📋 Task 정의

```python
from crewai import Task

t1 = Task(
    description="""LangGraph의 최신 동향을 조사하라.
    - 2026년 5월까지 릴리즈 노트
    - 주요 enterprise 채택 사례
    - 경쟁 프레임워크 대비 강점""",
    expected_output="""bullet 5-7개의 한국어 요약.
    각 항목 끝에 [출처](url) 형식 링크.""",
    agent=researcher,
    context=[],   # 이전 task 결과 참조 시
    output_file="research.md",   # 자동 저장
)
```

### context로 task 연결
```python
t2 = Task(
    description="t1 결과를 1페이지 칼럼 형태로 작성",
    agent=writer,
    context=[t1],   # t1의 output이 자동으로 prompt에 주입
)
```

## 👥 Crew 정의

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[t1, t2, t3],
    process=Process.sequential,
    memory=True,                # 크루 전체 공유 메모리
    cache=True,                 # tool 결과 캐싱
    max_rpm=30,                 # 분당 요청 한도
    verbose=2,                  # 0/1/2
    output_log_file="crew.log",
)

result = crew.kickoff(inputs={"topic": "LangGraph"})
```

`inputs`는 task description의 `{topic}` 같은 변수에 주입됨.

## ✅ 체크포인트
- [ ] 3개 agent 정의, role/goal/backstory 다 다름
- [ ] tasks가 순서대로 흐름
- [ ] context로 이전 task 참조 시 결과 활용됨
- [ ] `kickoff()` 결과가 expected_output 형식과 일치

## ⚠️ 흔한 실수
| 증상 | 원인 |
|------|------|
| Agent가 같은 일 반복 | goal이 추상적. 더 구체적으로 |
| 출력 형식 들쭉날쭉 | expected_output에 예시 포함 |
| 비용 폭주 | max_iter, max_rpm 명시, 작은 모델 우선 |
| context로 안 넘어옴 | task.context는 list, []로 명시 |
| 한국어 깨짐 | backstory에 "한국어로 답변" 명시 |

## 🔗 다음 → [02-processes.md](02-processes.md)
