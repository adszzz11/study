# CrewAI 기초 - Agent, Task, Crew

## 개요

CrewAI는 역할 기반의 다중 AI 에이전트가 협업하여 복잡한 작업을 수행하는 프레임워크이다. 마치 실제 팀처럼 각 에이전트가 전문 역할을 맡아 협력한다.

---

## 1. 환경 설정

### 설치

```bash
# 기본 설치
pip install crewai crewai-tools

# 또는 uv 사용 (권장)
uv pip install crewai crewai-tools
```

### 환경 변수

```bash
# .env 파일
OPENAI_API_KEY=sk-your-key

# 선택적
SERPER_API_KEY=your-serper-key    # 검색 도구 사용 시
OPENAI_MODEL_NAME=gpt-4o-mini     # 기본 모델 지정
```

### 프로젝트 생성 (권장)

```bash
# CrewAI CLI로 프로젝트 생성
crewai create crew my-project

# 생성되는 구조
my-project/
├── src/my_project/
│   ├── config/
│   │   ├── agents.yaml    # 에이전트 정의
│   │   └── tasks.yaml     # 태스크 정의
│   ├── tools/             # 커스텀 도구
│   │   └── custom_tool.py
│   ├── crew.py            # 크루 구성
│   └── main.py            # 진입점
├── pyproject.toml
└── README.md
```

---

## 2. Agent (에이전트)

### 에이전트란?

에이전트는 특정 역할(role), 목표(goal), 배경(backstory)을 가진 AI 개체이다.

### 기본 에이전트 생성

```python
from crewai import Agent

# 연구원 에이전트
researcher = Agent(
    role="시장 조사 연구원",
    goal="주어진 주제에 대해 철저하고 정확한 조사를 수행한다",
    backstory="""
    당신은 10년 경력의 시장 조사 전문가입니다.
    데이터 분석과 트렌드 파악에 뛰어난 능력을 가지고 있습니다.
    항상 신뢰할 수 있는 출처에서 정보를 수집합니다.
    """,
    verbose=True,  # 상세 로그
    allow_delegation=True  # 다른 에이전트에게 위임 허용
)
```

### 에이전트 주요 파라미터

| 파라미터 | 설명 | 필수 |
|----------|------|------|
| `role` | 에이전트의 역할/직책 | O |
| `goal` | 에이전트의 목표 | O |
| `backstory` | 배경 설명, 페르소나 | O |
| `llm` | 사용할 LLM 모델 | X |
| `tools` | 사용 가능한 도구 리스트 | X |
| `verbose` | 상세 로그 출력 | X |
| `allow_delegation` | 작업 위임 허용 | X |
| `max_iter` | 최대 반복 횟수 | X |
| `max_rpm` | 분당 최대 요청 수 | X |
| `memory` | 메모리 활성화 | X |

### 다양한 에이전트 예시

```python
# 작성자 에이전트
writer = Agent(
    role="콘텐츠 작성자",
    goal="명확하고 매력적인 콘텐츠를 작성한다",
    backstory="""
    당신은 경험 많은 콘텐츠 작성자입니다.
    복잡한 주제를 쉽게 설명하는 능력이 있습니다.
    독자의 관심을 끄는 글을 씁니다.
    """,
    verbose=True
)

# 편집자 에이전트
editor = Agent(
    role="편집자",
    goal="콘텐츠의 품질과 정확성을 보장한다",
    backstory="""
    당신은 꼼꼼한 편집자입니다.
    문법, 스타일, 논리적 흐름을 검토합니다.
    항상 독자 관점에서 콘텐츠를 평가합니다.
    """,
    verbose=True
)

# 분석가 에이전트
analyst = Agent(
    role="데이터 분석가",
    goal="데이터에서 의미 있는 인사이트를 도출한다",
    backstory="""
    당신은 숙련된 데이터 분석가입니다.
    숫자 뒤에 숨은 이야기를 찾아냅니다.
    복잡한 데이터를 시각화하고 설명합니다.
    """,
    verbose=True
)
```

### LLM 설정

```python
from crewai import Agent, LLM

# OpenAI 모델 지정
agent = Agent(
    role="연구원",
    goal="조사 수행",
    backstory="경험 많은 연구원",
    llm=LLM(model="gpt-4o", temperature=0.7)
)

# 다른 모델 사용
from langchain_anthropic import ChatAnthropic

claude_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
agent = Agent(
    role="연구원",
    goal="조사 수행",
    backstory="경험 많은 연구원",
    llm=claude_llm
)
```

---

## 3. Task (태스크)

### 태스크란?

태스크는 에이전트가 수행해야 할 구체적인 작업이다.

### 기본 태스크 생성

```python
from crewai import Task

# 조사 태스크
research_task = Task(
    description="""
    2024년 AI 트렌드에 대해 조사하세요.
    주요 기술 발전, 산업별 적용 사례, 향후 전망을 포함해야 합니다.
    최소 5개의 주요 트렌드를 식별하세요.
    """,
    expected_output="AI 트렌드 조사 보고서 (마크다운 형식)",
    agent=researcher
)
```

### 태스크 주요 파라미터

| 파라미터 | 설명 | 필수 |
|----------|------|------|
| `description` | 작업 설명 | O |
| `expected_output` | 기대 출력 형식 | O |
| `agent` | 담당 에이전트 | X |
| `tools` | 사용할 도구 | X |
| `context` | 이전 태스크 결과 참조 | X |
| `output_file` | 결과 저장 파일 | X |
| `output_json` | JSON 출력 스키마 | X |
| `output_pydantic` | Pydantic 출력 모델 | X |
| `async_execution` | 비동기 실행 | X |

### 태스크 의존성 (Context)

```python
# 첫 번째 태스크: 조사
research_task = Task(
    description="AI 트렌드 조사",
    expected_output="조사 결과 리포트",
    agent=researcher
)

# 두 번째 태스크: 작성 (조사 결과 참조)
writing_task = Task(
    description="""
    조사 결과를 바탕으로 블로그 포스트를 작성하세요.
    일반 독자가 이해하기 쉽게 작성해야 합니다.
    """,
    expected_output="블로그 포스트 (1500단어 이상)",
    agent=writer,
    context=[research_task]  # research_task 결과 참조
)

# 세 번째 태스크: 편집 (작성 결과 참조)
editing_task = Task(
    description="블로그 포스트를 검토하고 개선하세요.",
    expected_output="편집된 최종 블로그 포스트",
    agent=editor,
    context=[writing_task]
)
```

### 구조화된 출력

```python
from pydantic import BaseModel
from typing import List

class TrendReport(BaseModel):
    title: str
    trends: List[str]
    summary: str
    recommendations: List[str]

research_task = Task(
    description="AI 트렌드 조사",
    expected_output="구조화된 트렌드 리포트",
    agent=researcher,
    output_pydantic=TrendReport  # Pydantic 모델로 출력
)
```

### 파일 출력

```python
writing_task = Task(
    description="블로그 포스트 작성",
    expected_output="마크다운 형식의 블로그 포스트",
    agent=writer,
    output_file="output/blog_post.md"  # 파일로 저장
)
```

---

## 4. Crew (크루)

### 크루란?

크루는 에이전트와 태스크를 조합한 팀이다.

### 기본 크루 생성

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,  # 순차 실행
    verbose=True
)

# 크루 실행
result = crew.kickoff()
print(result)
```

### 크루 주요 파라미터

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `agents` | 에이전트 리스트 | - |
| `tasks` | 태스크 리스트 | - |
| `process` | 실행 방식 | sequential |
| `verbose` | 상세 로그 | False |
| `manager_llm` | 매니저 LLM (hierarchical용) | - |
| `memory` | 메모리 활성화 | False |
| `embedder` | 임베딩 설정 | OpenAI |
| `full_output` | 전체 출력 반환 | False |

### Process 타입

```python
from crewai import Process

# 순차 실행: 태스크를 순서대로 실행
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential
)

# 계층적 실행: 매니저가 작업 분배
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.hierarchical,
    manager_llm=LLM(model="gpt-4o")  # 매니저 LLM 필수
)
```

### 입력값 전달

```python
# 태스크에 변수 포함
research_task = Task(
    description="다음 주제에 대해 조사하세요: {topic}",
    expected_output="조사 리포트",
    agent=researcher
)

crew = Crew(
    agents=[researcher],
    tasks=[research_task]
)

# kickoff 시 입력값 전달
result = crew.kickoff(inputs={"topic": "LangChain vs CrewAI"})
```

---

## 5. 전체 예제

### 콘텐츠 제작 크루

```python
from crewai import Agent, Task, Crew, Process

# 1. 에이전트 정의
researcher = Agent(
    role="리서처",
    goal="주어진 주제에 대해 깊이 있는 조사를 수행한다",
    backstory="당신은 10년 경력의 리서치 전문가입니다.",
    verbose=True
)

writer = Agent(
    role="작성자",
    goal="조사 내용을 바탕으로 매력적인 글을 작성한다",
    backstory="당신은 경험 많은 콘텐츠 작성자입니다.",
    verbose=True
)

editor = Agent(
    role="편집자",
    goal="글의 품질을 검토하고 개선한다",
    backstory="당신은 꼼꼼한 편집자입니다.",
    verbose=True
)

# 2. 태스크 정의
research_task = Task(
    description="""
    {topic}에 대해 종합적으로 조사하세요.
    - 핵심 개념 정리
    - 주요 기능과 특징
    - 장단점 분석
    - 실제 사용 사례
    """,
    expected_output="상세한 조사 리포트",
    agent=researcher
)

writing_task = Task(
    description="""
    조사 결과를 바탕으로 블로그 포스트를 작성하세요.
    - 초보자도 이해하기 쉽게
    - 실용적인 예제 포함
    - 1500단어 이상
    """,
    expected_output="마크다운 형식의 블로그 포스트",
    agent=writer,
    context=[research_task]
)

editing_task = Task(
    description="""
    블로그 포스트를 검토하고 개선하세요.
    - 문법 및 맞춤법 확인
    - 논리적 흐름 검토
    - 가독성 개선
    """,
    expected_output="편집된 최종 블로그 포스트",
    agent=editor,
    context=[writing_task],
    output_file="output/final_post.md"
)

# 3. 크루 구성
content_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential,
    verbose=True
)

# 4. 실행
result = content_crew.kickoff(inputs={"topic": "LangChain과 CrewAI"})
print(result)
```

---

## 6. YAML 기반 설정 (권장)

### agents.yaml

```yaml
researcher:
  role: "시장 조사 연구원"
  goal: "주어진 주제에 대해 철저한 조사를 수행한다"
  backstory: |
    당신은 10년 경력의 시장 조사 전문가입니다.
    데이터 분석과 트렌드 파악에 뛰어난 능력을 가지고 있습니다.

writer:
  role: "콘텐츠 작성자"
  goal: "조사 결과를 매력적인 콘텐츠로 변환한다"
  backstory: |
    당신은 경험 많은 콘텐츠 작성자입니다.
    복잡한 주제를 쉽게 설명하는 능력이 있습니다.

editor:
  role: "편집자"
  goal: "콘텐츠의 품질과 정확성을 보장한다"
  backstory: |
    당신은 꼼꼼한 편집자입니다.
    독자 관점에서 콘텐츠를 평가합니다.
```

### tasks.yaml

```yaml
research_task:
  description: |
    {topic}에 대해 조사하세요.
    핵심 개념, 주요 기능, 장단점을 포함해야 합니다.
  expected_output: "상세한 조사 리포트"
  agent: researcher

writing_task:
  description: |
    조사 결과를 바탕으로 블로그 포스트를 작성하세요.
    초보자도 이해하기 쉽게 작성해야 합니다.
  expected_output: "블로그 포스트"
  agent: writer

editing_task:
  description: |
    블로그 포스트를 검토하고 개선하세요.
  expected_output: "편집된 최종 블로그 포스트"
  agent: editor
  output_file: "output/final_post.md"
```

### crew.py

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ContentCrew:
    """콘텐츠 제작 크루"""

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'], verbose=True)

    @agent
    def writer(self) -> Agent:
        return Agent(config=self.agents_config['writer'], verbose=True)

    @agent
    def editor(self) -> Agent:
        return Agent(config=self.agents_config['editor'], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config['writing_task'])

    @task
    def editing_task(self) -> Task:
        return Task(config=self.tasks_config['editing_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

### main.py

```python
from content_crew.crew import ContentCrew

def run():
    crew = ContentCrew()
    result = crew.crew().kickoff(inputs={"topic": "AI 에이전트"})
    print(result)

if __name__ == "__main__":
    run()
```

---

## 7. 일반적인 실수

### 실수 1: 모호한 역할 정의

```python
# 나쁜 예
agent = Agent(
    role="도우미",
    goal="도움을 준다",
    backstory="당신은 AI입니다."
)

# 좋은 예
agent = Agent(
    role="기술 문서 작성자",
    goal="복잡한 기술 개념을 초보자도 이해하기 쉬운 문서로 작성한다",
    backstory="""
    당신은 5년 경력의 기술 문서 작성 전문가입니다.
    개발자와 비개발자 모두를 위한 문서를 작성해왔습니다.
    복잡한 개념을 단계별로 설명하는 것이 특기입니다.
    """
)
```

### 실수 2: 태스크 설명 부족

```python
# 나쁜 예
task = Task(
    description="글 써줘",
    expected_output="글",
    agent=writer
)

# 좋은 예
task = Task(
    description="""
    {topic}에 대한 블로그 포스트를 작성하세요.

    요구사항:
    - 대상 독자: 프로그래밍 초보자
    - 길이: 1500-2000 단어
    - 구조: 서론, 본론(3-4개 섹션), 결론
    - 코드 예제 포함
    - 마크다운 형식
    """,
    expected_output="마크다운 형식의 블로그 포스트 (1500단어 이상)",
    agent=writer
)
```

### 실수 3: Context 미설정

```python
# 나쁜 예: 이전 작업 결과 참조 안 함
writing_task = Task(
    description="조사 결과를 바탕으로 글 작성",
    expected_output="블로그 포스트",
    agent=writer
    # context 없음 - 조사 결과 접근 불가
)

# 좋은 예
writing_task = Task(
    description="조사 결과를 바탕으로 글 작성",
    expected_output="블로그 포스트",
    agent=writer,
    context=[research_task]  # 이전 태스크 결과 참조
)
```

---

## 핵심 요약

```
┌─────────────────────────────────────────────────┐
│ CrewAI 기초 핵심                                 │
├─────────────────────────────────────────────────┤
│ Agent: role + goal + backstory                  │
│ Task: description + expected_output + agent     │
│ Crew: agents + tasks + process                  │
├─────────────────────────────────────────────────┤
│ 실행: crew.kickoff(inputs={"key": "value"})     │
│ 의존성: context=[previous_task]                  │
│ 프로세스: sequential (순차), hierarchical (계층)│
└─────────────────────────────────────────────────┘
```

## 다음 단계

- [[05-crewai-advanced|CrewAI 고급]] - Flow, Tools, Memory
- [[06-integration|통합 활용]] - LangChain + CrewAI
