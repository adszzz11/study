# CrewAI 고급 - Flow, Tools, Memory

## 개요

CrewAI의 고급 기능인 Flow(워크플로우), Tools(도구), Memory(메모리)를 학습한다.

---

## 1. Tools (도구)

### 도구란?

도구는 에이전트가 외부 리소스와 상호작용할 수 있게 해주는 기능이다.

### 내장 도구 (crewai-tools)

```bash
pip install crewai-tools
```

```python
from crewai_tools import (
    SerperDevTool,      # Google 검색
    WebsiteSearchTool,  # 웹사이트 검색
    FileReadTool,       # 파일 읽기
    DirectoryReadTool,  # 디렉토리 탐색
    PDFSearchTool,      # PDF 검색
    YoutubeVideoSearchTool,  # YouTube 검색
    GithubSearchTool,   # GitHub 검색
    CodeInterpreterTool # 코드 실행
)
```

### 주요 내장 도구

| 도구 | 설명 | 환경 변수 |
|------|------|-----------|
| `SerperDevTool` | Google 검색 | SERPER_API_KEY |
| `WebsiteSearchTool` | 웹사이트 RAG | - |
| `FileReadTool` | 파일 읽기 | - |
| `DirectoryReadTool` | 디렉토리 목록 | - |
| `PDFSearchTool` | PDF 내용 검색 | - |
| `ScrapeWebsiteTool` | 웹 스크래핑 | - |
| `BrowserbaseLoadTool` | 브라우저 자동화 | BROWSERBASE_API_KEY |

### 도구 사용 예제

```python
from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool

# 도구 생성
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()

# 에이전트에 도구 할당
researcher = Agent(
    role="리서처",
    goal="최신 정보를 조사한다",
    backstory="당신은 검색 전문가입니다.",
    tools=[search_tool, web_rag_tool],
    verbose=True
)
```

### 특정 웹사이트 RAG

```python
from crewai_tools import WebsiteSearchTool

# 특정 URL만 검색
docs_search = WebsiteSearchTool(
    website="https://python.langchain.com/docs"
)

agent = Agent(
    role="문서 전문가",
    goal="LangChain 문서에서 정보를 찾는다",
    backstory="문서 검색 전문가",
    tools=[docs_search]
)
```

### 커스텀 도구 만들기

```python
from crewai.tools import BaseTool
from pydantic import Field
from typing import Type

class MyCustomTool(BaseTool):
    name: str = "내 커스텀 도구"
    description: str = "이 도구는 특정 작업을 수행합니다."

    def _run(self, argument: str) -> str:
        # 도구 로직
        return f"처리 결과: {argument}"

# 사용
custom_tool = MyCustomTool()
agent = Agent(
    role="작업자",
    goal="작업 수행",
    backstory="작업 전문가",
    tools=[custom_tool]
)
```

### 데코레이터로 도구 만들기

```python
from crewai.tools import tool

@tool("계산기")
def calculator(expression: str) -> str:
    """
    수학 표현식을 계산합니다.

    Args:
        expression: 계산할 수식 (예: "2 + 2")

    Returns:
        계산 결과
    """
    try:
        result = eval(expression)
        return f"결과: {result}"
    except Exception as e:
        return f"계산 오류: {e}"

# 사용
agent = Agent(
    role="수학자",
    goal="수학 문제 해결",
    backstory="수학 전문가",
    tools=[calculator]
)
```

### 도구 인자 정의 (Pydantic)

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class SearchInput(BaseModel):
    """검색 도구 입력"""
    query: str = Field(..., description="검색 쿼리")
    max_results: int = Field(default=5, description="최대 결과 수")

class AdvancedSearchTool(BaseTool):
    name: str = "고급 검색"
    description: str = "고급 검색을 수행합니다."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        # 검색 로직
        return f"'{query}' 검색 결과 {max_results}개"
```

---

## 2. Memory (메모리)

### 메모리란?

메모리는 에이전트가 이전 상호작용을 기억하고 학습할 수 있게 해주는 기능이다.

### 메모리 유형

```
┌─────────────────────────────────────────────────┐
│                CrewAI 메모리 시스템              │
├─────────────────────────────────────────────────┤
│                                                 │
│  단기 메모리 (Short-term)                       │
│  └─ 현재 실행 중 대화/작업 기억                 │
│                                                 │
│  장기 메모리 (Long-term)                        │
│  └─ 여러 실행에 걸쳐 지식 유지                  │
│                                                 │
│  엔티티 메모리 (Entity)                         │
│  └─ 특정 엔티티(사람, 장소 등) 정보 추적        │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 메모리 활성화

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    memory=True,  # 메모리 활성화
    verbose=True
)
```

### 메모리 설정 커스터마이징

```python
from crewai import Crew
from crewai.memory import ShortTermMemory, LongTermMemory, EntityMemory
from crewai.memory.storage import RAGStorage

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    memory=True,
    # 메모리 설정 (선택적)
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    }
)
```

### 메모리 사용 사례

```python
# 첫 번째 실행
result1 = crew.kickoff(inputs={"topic": "Python"})

# 두 번째 실행 - 이전 실행의 지식을 활용
result2 = crew.kickoff(inputs={"topic": "Python 고급"})
# 첫 번째 실행에서 학습한 내용이 두 번째에 영향
```

---

## 3. Flow (플로우)

### Flow란?

Flow는 복잡한 워크플로우를 구성하기 위한 상태 기반 시스템이다.

### 기본 Flow

```python
from crewai.flow.flow import Flow, listen, start

class SimpleFlow(Flow):
    @start()
    def first_step(self):
        print("첫 번째 단계 시작")
        return "첫 번째 결과"

    @listen(first_step)
    def second_step(self, result):
        print(f"두 번째 단계 - 입력: {result}")
        return f"처리됨: {result}"

# 실행
flow = SimpleFlow()
result = flow.kickoff()
print(result)
```

### Flow 데코레이터

| 데코레이터 | 설명 |
|------------|------|
| `@start()` | 시작 메서드 표시 |
| `@listen(method)` | 특정 메서드 완료 후 실행 |
| `@router(method)` | 조건부 라우팅 |

### 상태 관리

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ResearchState(BaseModel):
    topic: str = ""
    research_results: str = ""
    draft: str = ""
    final_output: str = ""

class ResearchFlow(Flow[ResearchState]):
    @start()
    def get_topic(self):
        self.state.topic = "AI 에이전트"
        return self.state.topic

    @listen(get_topic)
    def research(self, topic):
        # 연구 수행
        self.state.research_results = f"{topic}에 대한 조사 결과..."
        return self.state.research_results

    @listen(research)
    def write_draft(self, research):
        # 초안 작성
        self.state.draft = f"초안: {research}"
        return self.state.draft

    @listen(write_draft)
    def finalize(self, draft):
        self.state.final_output = f"최종: {draft}"
        return self.state.final_output

# 실행
flow = ResearchFlow()
result = flow.kickoff()
print(flow.state.final_output)
```

### 조건부 라우팅

```python
from crewai.flow.flow import Flow, listen, start, router

class ConditionalFlow(Flow):
    @start()
    def analyze_input(self):
        # 입력 분석
        return {"type": "technical", "content": "Python 질문"}

    @router(analyze_input)
    def route_by_type(self, result):
        if result["type"] == "technical":
            return "handle_technical"
        else:
            return "handle_general"

    @listen("handle_technical")
    def handle_technical(self, result):
        return f"기술 질문 처리: {result['content']}"

    @listen("handle_general")
    def handle_general(self, result):
        return f"일반 질문 처리: {result['content']}"
```

### Flow + Crew 통합

```python
from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Task, Crew

class ContentFlow(Flow):
    @start()
    def research_phase(self):
        # 연구 크루
        researcher = Agent(
            role="연구원",
            goal="주제 조사",
            backstory="경험 많은 연구원"
        )

        research_task = Task(
            description=f"{self.inputs['topic']}에 대해 조사하세요",
            expected_output="조사 리포트",
            agent=researcher
        )

        crew = Crew(
            agents=[researcher],
            tasks=[research_task]
        )

        return crew.kickoff()

    @listen(research_phase)
    def writing_phase(self, research_result):
        # 작성 크루
        writer = Agent(
            role="작성자",
            goal="콘텐츠 작성",
            backstory="콘텐츠 전문가"
        )

        writing_task = Task(
            description=f"다음 조사 결과를 바탕으로 글 작성:\n{research_result}",
            expected_output="블로그 포스트",
            agent=writer
        )

        crew = Crew(
            agents=[writer],
            tasks=[writing_task]
        )

        return crew.kickoff()

# 실행
flow = ContentFlow()
result = flow.kickoff(inputs={"topic": "AI 에이전트"})
```

---

## 4. 고급 에이전트 패턴

### 위임 (Delegation)

```python
from crewai import Agent, Task, Crew

# 매니저 에이전트
manager = Agent(
    role="프로젝트 매니저",
    goal="팀을 관리하고 작업을 조율한다",
    backstory="경험 많은 프로젝트 매니저",
    allow_delegation=True  # 위임 허용
)

# 전문가 에이전트들
researcher = Agent(
    role="연구원",
    goal="조사 수행",
    backstory="조사 전문가"
)

writer = Agent(
    role="작성자",
    goal="글 작성",
    backstory="콘텐츠 전문가"
)

# 매니저가 작업 조율
management_task = Task(
    description="""
    다음 프로젝트를 관리하세요:
    1. AI 트렌드 조사
    2. 조사 결과를 바탕으로 리포트 작성

    필요시 팀원에게 작업을 위임하세요.
    """,
    expected_output="완성된 리포트",
    agent=manager
)

crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[management_task],
    verbose=True
)
```

### 계층적 프로세스

```python
from crewai import Crew, Process, LLM

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_llm=LLM(model="gpt-4o"),
    # 또는 매니저 에이전트 직접 지정
    # manager_agent=manager
)

result = crew.kickoff()
```

### 비동기 태스크 실행

```python
from crewai import Task

# 비동기 실행 태스크
async_task1 = Task(
    description="첫 번째 병렬 작업",
    expected_output="결과 1",
    agent=agent1,
    async_execution=True  # 비동기 실행
)

async_task2 = Task(
    description="두 번째 병렬 작업",
    expected_output="결과 2",
    agent=agent2,
    async_execution=True
)

# 결과 합치는 태스크 (동기)
combine_task = Task(
    description="두 결과를 합쳐서 최종 리포트 작성",
    expected_output="최종 리포트",
    agent=agent3,
    context=[async_task1, async_task2]  # 비동기 태스크들 완료 대기
)
```

---

## 5. 콜백과 이벤트

### 태스크 콜백

```python
from crewai import Task

def task_callback(output):
    print(f"태스크 완료!")
    print(f"결과: {output.raw}")
    # 로깅, 알림 등 추가 작업

task = Task(
    description="작업 수행",
    expected_output="결과",
    agent=agent,
    callback=task_callback
)
```

### 스텝 콜백

```python
from crewai import Crew

def step_callback(step_output):
    print(f"스텝 완료: {step_output}")

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    step_callback=step_callback
)
```

---

## 6. 에러 처리

### 재시도 설정

```python
from crewai import Agent

agent = Agent(
    role="연구원",
    goal="조사 수행",
    backstory="연구 전문가",
    max_iter=15,  # 최대 반복 횟수
    max_rpm=10,   # 분당 최대 요청
    verbose=True
)
```

### 예외 처리

```python
from crewai import Crew

try:
    result = crew.kickoff(inputs={"topic": "AI"})
except Exception as e:
    print(f"크루 실행 중 오류: {e}")
    # 폴백 로직
```

---

## 7. 실전 예제: 리서치 봇

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from typing import List

# 상태 정의
class ResearchState(BaseModel):
    topic: str = ""
    search_queries: List[str] = []
    raw_data: str = ""
    analysis: str = ""
    report: str = ""

class ResearchBot(Flow[ResearchState]):
    def __init__(self):
        super().__init__()
        self.search_tool = SerperDevTool()
        self.web_tool = WebsiteSearchTool()

    @start()
    def plan_research(self):
        """검색 쿼리 계획"""
        planner = Agent(
            role="연구 기획자",
            goal="효과적인 검색 전략 수립",
            backstory="연구 방법론 전문가"
        )

        plan_task = Task(
            description=f"""
            '{self.state.topic}'에 대한 연구를 위해
            3-5개의 검색 쿼리를 생성하세요.
            다양한 관점을 포함해야 합니다.
            """,
            expected_output="검색 쿼리 목록 (줄바꿈으로 구분)",
            agent=planner
        )

        crew = Crew(agents=[planner], tasks=[plan_task])
        result = crew.kickoff()
        self.state.search_queries = result.raw.strip().split('\n')
        return self.state.search_queries

    @listen(plan_research)
    def gather_data(self, queries):
        """데이터 수집"""
        gatherer = Agent(
            role="데이터 수집가",
            goal="관련 정보 수집",
            backstory="정보 수집 전문가",
            tools=[self.search_tool, self.web_tool]
        )

        gather_task = Task(
            description=f"""
            다음 쿼리들로 정보를 수집하세요:
            {queries}

            각 쿼리에 대해 주요 정보를 요약하세요.
            """,
            expected_output="수집된 정보 요약",
            agent=gatherer
        )

        crew = Crew(agents=[gatherer], tasks=[gather_task])
        result = crew.kickoff()
        self.state.raw_data = result.raw
        return self.state.raw_data

    @listen(gather_data)
    def analyze_data(self, raw_data):
        """데이터 분석"""
        analyst = Agent(
            role="데이터 분석가",
            goal="데이터에서 인사이트 도출",
            backstory="분석 전문가"
        )

        analyze_task = Task(
            description=f"""
            다음 데이터를 분석하세요:
            {raw_data}

            주요 트렌드, 패턴, 인사이트를 도출하세요.
            """,
            expected_output="분석 결과",
            agent=analyst
        )

        crew = Crew(agents=[analyst], tasks=[analyze_task])
        result = crew.kickoff()
        self.state.analysis = result.raw
        return self.state.analysis

    @listen(analyze_data)
    def write_report(self, analysis):
        """리포트 작성"""
        writer = Agent(
            role="리포트 작성자",
            goal="명확한 리포트 작성",
            backstory="문서 작성 전문가"
        )

        write_task = Task(
            description=f"""
            다음 분석 결과를 바탕으로 리포트를 작성하세요:
            {analysis}

            구조:
            1. 요약
            2. 주요 발견
            3. 상세 분석
            4. 결론 및 제언
            """,
            expected_output="마크다운 형식의 리포트",
            agent=writer,
            output_file="output/research_report.md"
        )

        crew = Crew(agents=[writer], tasks=[write_task])
        result = crew.kickoff()
        self.state.report = result.raw
        return self.state.report

# 실행
bot = ResearchBot()
bot.state.topic = "2024 AI 에이전트 트렌드"
result = bot.kickoff()
print(bot.state.report)
```

---

## 핵심 요약

```
┌─────────────────────────────────────────────────┐
│ CrewAI 고급 기능 핵심                            │
├─────────────────────────────────────────────────┤
│ Tools:                                          │
│ - 내장: SerperDevTool, WebsiteSearchTool 등     │
│ - 커스텀: BaseTool 상속 또는 @tool 데코레이터   │
├─────────────────────────────────────────────────┤
│ Memory:                                         │
│ - 단기: 현재 실행 내 기억                        │
│ - 장기: 여러 실행에 걸친 학습                    │
│ - 활성화: Crew(memory=True)                     │
├─────────────────────────────────────────────────┤
│ Flow:                                           │
│ - @start(): 시작점                              │
│ - @listen(method): 이전 단계 완료 후 실행       │
│ - @router(method): 조건부 분기                  │
│ - 상태: Flow[StateModel]로 상태 관리            │
└─────────────────────────────────────────────────┘
```

## 다음 단계

- [[06-integration|LangChain + CrewAI 통합]] - 두 프레임워크 결합
- [[../05-projects|실전 프로젝트]] - 실제 애플리케이션 구축
