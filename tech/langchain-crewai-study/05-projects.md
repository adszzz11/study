# 실전 프로젝트 및 Best Practices

## 프로젝트 아이디어

### 초급 프로젝트

| 프로젝트 | 설명 | 핵심 기술 |
|----------|------|-----------|
| 문서 QA 봇 | PDF/웹 문서 기반 질문 답변 | LangChain RAG |
| 번역 앱 | 다국어 번역 + 톤 조절 | LCEL, Prompt |
| 감정 분석기 | 리뷰/텍스트 감정 분류 | Output Parser |
| 요약 봇 | 긴 문서 자동 요약 | Chain, Prompt |

### 중급 프로젝트

| 프로젝트 | 설명 | 핵심 기술 |
|----------|------|-----------|
| 콘텐츠 생성 크루 | 조사→작성→편집 파이프라인 | CrewAI, Flow |
| 코드 리뷰어 | 코드 분석 + 개선 제안 | Agent, Tools |
| 뉴스 큐레이터 | 뉴스 수집→분석→요약 | RAG + CrewAI |
| 학습 도우미 | 문서 기반 튜터 봇 | RAG, Memory |

### 고급 프로젝트

| 프로젝트 | 설명 | 핵심 기술 |
|----------|------|-----------|
| 리서치 에이전트 | 자율적 조사 + 리포트 생성 | 통합, Flow |
| 고객 지원 시스템 | 분류→응답→에스컬레이션 | 계층적 크루 |
| 데이터 분석 파이프라인 | 수집→분석→시각화 | 통합, Tools |
| 자동화 워크플로우 | 복잡한 비즈니스 프로세스 | Flow, Memory |

---

## 프로젝트 1: 문서 QA 봇 (초급)

### 요구사항

- PDF 파일 업로드 및 인덱싱
- 자연어 질문에 대한 답변
- 출처 표시

### 구현

```python
"""
문서 QA 봇
- PDF 문서 기반 질문 답변 시스템
"""

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class DocumentQABot:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.persist_dir = persist_dir
        self.vectorstore = None
        self.chain = None

    def load_document(self, file_path: str) -> int:
        """PDF 문서 로드 및 인덱싱"""
        # 로드
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # 분할
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(documents)

        # 벡터 저장소 생성
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )

        # 체인 설정
        self._setup_chain()

        return len(chunks)

    def _setup_chain(self):
        """QA 체인 설정"""
        retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4, "fetch_k": 10}
        )

        prompt = ChatPromptTemplate.from_template("""
        당신은 문서 전문가입니다. 주어진 컨텍스트를 바탕으로 질문에 답변하세요.
        컨텍스트에 답이 없으면 "문서에서 해당 정보를 찾을 수 없습니다"라고 답하세요.

        컨텍스트:
        {context}

        질문: {question}

        답변:
        """)

        def format_docs(docs):
            return "\n\n---\n\n".join(
                f"[페이지 {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
                for doc in docs
            )

        self.chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> str:
        """질문에 답변"""
        if not self.chain:
            return "먼저 문서를 로드해주세요."
        return self.chain.invoke(question)

    def load_existing(self):
        """기존 벡터 저장소 로드"""
        if os.path.exists(self.persist_dir):
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
            self._setup_chain()
            return True
        return False


# 사용 예제
if __name__ == "__main__":
    bot = DocumentQABot()

    # 문서 로드
    chunks = bot.load_document("my_document.pdf")
    print(f"인덱싱 완료: {chunks}개 청크")

    # 질문
    while True:
        question = input("\n질문 (종료: q): ")
        if question.lower() == 'q':
            break
        answer = bot.ask(question)
        print(f"\n답변: {answer}")
```

---

## 프로젝트 2: 콘텐츠 생성 크루 (중급)

### 요구사항

- 주제 조사
- 초안 작성
- 편집 및 최종 검토
- 마크다운 출력

### 구현

```python
"""
콘텐츠 생성 크루
- 조사 → 작성 → 편집 워크플로우
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from pydantic import BaseModel
from typing import List

class BlogPost(BaseModel):
    title: str
    introduction: str
    sections: List[str]
    conclusion: str

class ContentCreationCrew:
    def __init__(self):
        self.search_tool = SerperDevTool()
        self._setup_agents()
        self._setup_tasks()

    def _setup_agents(self):
        """에이전트 설정"""
        self.researcher = Agent(
            role="콘텐츠 리서처",
            goal="주제에 대해 깊이 있고 정확한 정보를 수집한다",
            backstory="""
            당신은 10년 경력의 리서처입니다.
            다양한 소스에서 신뢰할 수 있는 정보를 찾아냅니다.
            복잡한 주제도 이해하기 쉽게 정리합니다.
            """,
            tools=[self.search_tool],
            verbose=True
        )

        self.writer = Agent(
            role="콘텐츠 작성자",
            goal="매력적이고 유익한 블로그 포스트를 작성한다",
            backstory="""
            당신은 경험 많은 블로그 작가입니다.
            독자의 관심을 끌고 가치를 전달하는 글을 씁니다.
            SEO를 고려한 구조화된 콘텐츠를 만듭니다.
            """,
            verbose=True
        )

        self.editor = Agent(
            role="편집자",
            goal="콘텐츠의 품질을 높이고 오류를 수정한다",
            backstory="""
            당신은 꼼꼼한 편집자입니다.
            문법, 스타일, 논리적 흐름을 완벽하게 검토합니다.
            독자 경험을 최우선으로 생각합니다.
            """,
            verbose=True
        )

    def _setup_tasks(self):
        """태스크 설정"""
        self.research_task = Task(
            description="""
            {topic}에 대해 종합적으로 조사하세요.

            조사 항목:
            1. 핵심 개념 및 정의
            2. 최신 트렌드와 발전
            3. 실제 사용 사례
            4. 장단점 분석
            5. 전문가 의견 또는 통계

            최소 5개 이상의 핵심 포인트를 포함하세요.
            """,
            expected_output="상세한 조사 리포트 (마크다운 형식)",
            agent=self.researcher
        )

        self.writing_task = Task(
            description="""
            조사 결과를 바탕으로 블로그 포스트를 작성하세요.

            요구사항:
            - 대상 독자: {audience}
            - 톤: {tone}
            - 길이: 1500-2000 단어
            - 구조: 제목, 서론, 본론(3-5 섹션), 결론
            - 각 섹션에 소제목 포함
            - 실용적인 예시 포함
            """,
            expected_output="마크다운 형식의 블로그 포스트",
            agent=self.writer,
            context=[self.research_task]
        )

        self.editing_task = Task(
            description="""
            블로그 포스트를 검토하고 개선하세요.

            검토 항목:
            1. 맞춤법 및 문법
            2. 문장 가독성
            3. 논리적 흐름
            4. 정보 정확성
            5. SEO 최적화 (키워드, 메타 설명)

            수정된 최종 버전을 출력하세요.
            """,
            expected_output="편집된 최종 블로그 포스트 (마크다운)",
            agent=self.editor,
            context=[self.writing_task],
            output_file="output/blog_post.md"
        )

    def create(self, topic: str, audience: str = "일반 독자",
               tone: str = "친근하고 전문적인") -> str:
        """콘텐츠 생성 실행"""
        crew = Crew(
            agents=[self.researcher, self.writer, self.editor],
            tasks=[self.research_task, self.writing_task, self.editing_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff(inputs={
            "topic": topic,
            "audience": audience,
            "tone": tone
        })

        return result.raw


# 사용 예제
if __name__ == "__main__":
    crew = ContentCreationCrew()

    result = crew.create(
        topic="2024년 AI 에이전트 트렌드",
        audience="개발자 및 기술 관심자",
        tone="전문적이면서 접근하기 쉬운"
    )

    print(result)
```

---

## 프로젝트 3: 리서치 에이전트 (고급)

### 요구사항

- 자율적인 조사 계획 수립
- 다중 소스 데이터 수집
- 분석 및 인사이트 도출
- 종합 리포트 생성

### 구현

```python
"""
리서치 에이전트 시스템
- LangChain RAG + CrewAI 통합
"""

from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start
from crewai.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from typing import List, Dict, Any
import json

# 상태 정의
class ResearchState(BaseModel):
    query: str = ""
    search_queries: List[str] = []
    sources: List[str] = []
    raw_data: Dict[str, str] = {}
    analysis: str = ""
    insights: List[str] = []
    report: str = ""

class ResearchAgent(Flow[ResearchState]):
    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = None

    @start()
    def plan_research(self):
        """조사 계획 수립"""
        planner = Agent(
            role="연구 기획자",
            goal="효과적인 연구 계획을 수립한다",
            backstory="""
            당신은 체계적인 연구 방법론 전문가입니다.
            복잡한 주제를 세부 질문으로 분해합니다.
            """,
            verbose=True
        )

        plan_task = Task(
            description=f"""
            다음 주제에 대한 연구 계획을 수립하세요: {self.state.query}

            출력 형식 (JSON):
            {{
                "search_queries": ["검색 쿼리 1", "검색 쿼리 2", ...],
                "sources": ["웹사이트 URL 1", "웹사이트 URL 2", ...]
            }}

            5-7개의 검색 쿼리와 3-5개의 관련 웹사이트를 포함하세요.
            """,
            expected_output="JSON 형식의 연구 계획",
            agent=planner
        )

        crew = Crew(agents=[planner], tasks=[plan_task])
        result = crew.kickoff()

        # 결과 파싱
        try:
            plan = json.loads(result.raw)
            self.state.search_queries = plan.get("search_queries", [])
            self.state.sources = plan.get("sources", [])
        except:
            self.state.search_queries = [self.state.query]

        return self.state.search_queries

    @listen(plan_research)
    def gather_data(self, queries):
        """데이터 수집 및 인덱싱"""
        all_docs = []

        # 웹 소스에서 데이터 수집
        for url in self.state.sources[:3]:  # 최대 3개 소스
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                all_docs.extend(docs)
                self.state.raw_data[url] = docs[0].page_content[:1000]
            except Exception as e:
                print(f"소스 로드 실패: {url} - {e}")

        if all_docs:
            # 분할 및 인덱싱
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = splitter.split_documents(all_docs)

            self.vectorstore = Chroma.from_documents(
                chunks, self.embeddings
            )

        return f"수집된 소스: {len(self.state.raw_data)}"

    @listen(gather_data)
    def analyze_data(self, gather_result):
        """데이터 분석"""
        # RAG 도구 생성
        @tool("데이터 검색")
        def search_data(query: str) -> str:
            """수집된 데이터에서 정보를 검색합니다."""
            if self.vectorstore:
                docs = self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ).invoke(query)
                return "\n\n".join(doc.page_content for doc in docs)
            return "데이터가 없습니다."

        analyst = Agent(
            role="데이터 분석가",
            goal="데이터에서 의미 있는 패턴과 인사이트를 찾는다",
            backstory="경험 많은 데이터 분석 전문가",
            tools=[search_data],
            verbose=True
        )

        analysis_task = Task(
            description=f"""
            '{self.state.query}'에 대해 수집된 데이터를 분석하세요.

            분석 항목:
            1. 주요 트렌드
            2. 핵심 발견
            3. 패턴 및 상관관계
            4. 한계점 또는 갭

            데이터 검색 도구를 활용하여 근거를 찾으세요.
            """,
            expected_output="상세한 분석 결과",
            agent=analyst
        )

        crew = Crew(agents=[analyst], tasks=[analysis_task])
        result = crew.kickoff()
        self.state.analysis = result.raw

        return self.state.analysis

    @listen(analyze_data)
    def generate_insights(self, analysis):
        """인사이트 도출"""
        strategist = Agent(
            role="전략 컨설턴트",
            goal="분석 결과를 실행 가능한 인사이트로 전환한다",
            backstory="전략적 사고와 문제 해결 전문가",
            verbose=True
        )

        insight_task = Task(
            description=f"""
            다음 분석 결과에서 핵심 인사이트를 도출하세요:

            {analysis}

            5-7개의 실행 가능한 인사이트를 제공하세요.
            각 인사이트는 구체적이고 명확해야 합니다.
            """,
            expected_output="번호가 매겨진 인사이트 목록",
            agent=strategist
        )

        crew = Crew(agents=[strategist], tasks=[insight_task])
        result = crew.kickoff()
        self.state.insights = result.raw.split('\n')

        return self.state.insights

    @listen(generate_insights)
    def create_report(self, insights):
        """최종 리포트 생성"""
        writer = Agent(
            role="리포트 작성자",
            goal="종합적이고 전문적인 리포트를 작성한다",
            backstory="기술 문서 작성 전문가",
            verbose=True
        )

        report_task = Task(
            description=f"""
            다음 정보를 바탕으로 종합 연구 리포트를 작성하세요:

            주제: {self.state.query}

            분석 결과:
            {self.state.analysis}

            인사이트:
            {insights}

            리포트 구조:
            1. 요약 (Executive Summary)
            2. 서론 및 배경
            3. 연구 방법론
            4. 주요 발견
            5. 분석 및 논의
            6. 결론 및 제언
            7. 참고 자료

            마크다운 형식으로 작성하세요.
            """,
            expected_output="마크다운 형식의 종합 리포트",
            agent=writer,
            output_file="output/research_report.md"
        )

        crew = Crew(agents=[writer], tasks=[report_task])
        result = crew.kickoff()
        self.state.report = result.raw

        return self.state.report


# 사용 예제
if __name__ == "__main__":
    agent = ResearchAgent()
    agent.state.query = "2024년 AI 에이전트 프레임워크 비교: LangChain vs CrewAI"

    result = agent.kickoff()
    print(result)
```

---

## Best Practices

### 1. 프롬프트 설계

```python
# 나쁜 예
prompt = "글 써줘"

# 좋은 예
prompt = """
당신은 {role}입니다.

목표: {goal}

요구사항:
- {requirement_1}
- {requirement_2}

출력 형식:
{output_format}

제약사항:
- {constraint}
"""
```

### 2. 에러 처리

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def safe_llm_call(chain, input_data):
    try:
        return chain.invoke(input_data)
    except Exception as e:
        print(f"LLM 호출 실패: {e}")
        raise
```

### 3. 비용 관리

```python
# 토큰 사용량 추적
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke({"input": "안녕"})
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Total Cost: ${cb.total_cost}")
```

### 4. 테스트

```python
import pytest
from unittest.mock import Mock, patch

def test_qa_bot():
    """QA 봇 테스트"""
    bot = DocumentQABot()

    # 모의 응답 설정
    with patch.object(bot, 'chain') as mock_chain:
        mock_chain.invoke.return_value = "테스트 답변"

        answer = bot.ask("테스트 질문")

        assert answer == "테스트 답변"
        mock_chain.invoke.assert_called_once()
```

### 5. 환경 분리

```python
import os
from dotenv import load_dotenv

# 환경별 설정 로드
env = os.getenv("ENVIRONMENT", "development")
load_dotenv(f".env.{env}")

# 설정
CONFIG = {
    "development": {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "verbose": True
    },
    "production": {
        "model": "gpt-4o",
        "temperature": 0.3,
        "verbose": False
    }
}

config = CONFIG[env]
```

### 6. 로깅

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_request(request):
    logger.info(f"처리 시작: {request}")
    try:
        result = chain.invoke(request)
        logger.info(f"처리 완료")
        return result
    except Exception as e:
        logger.error(f"처리 실패: {e}")
        raise
```

---

## 배포 고려사항

### Docker 구성

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
```

### 환경 변수 관리

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGCHAIN_TRACING_V2=true
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
    volumes:
      - ./output:/app/output
```

### 성능 최적화

- 배치 처리 활용
- 캐싱 구현
- 비동기 처리
- 적절한 청크 크기 설정
- 모델 선택 최적화 (gpt-4o-mini vs gpt-4o)

---

## 다음 단계

- [[cheatsheet|치트시트]] - 빠른 참조
- 공식 문서 지속 확인 - 버전 업데이트 대응
