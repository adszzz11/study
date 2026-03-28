# LangChain 기초 - Chain, LLM, Prompt

## 개요

LangChain의 핵심 개념인 LLM, Prompt, Chain을 학습한다.

---

## 1. 환경 설정

### 설치

```bash
# 기본 패키지
pip install langchain langchain-openai langchain-core

# 환경 변수 설정
export OPENAI_API_KEY="sk-..."
```

### 기본 프로젝트 구조

```
my-langchain-app/
├── .env                 # API 키
├── requirements.txt     # 의존성
├── main.py             # 메인 코드
└── prompts/            # 프롬프트 템플릿
```

### .env 파일

```bash
OPENAI_API_KEY=sk-your-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
```

---

## 2. LLM (Large Language Model)

### ChatOpenAI 기본 사용

```python
from langchain_openai import ChatOpenAI

# LLM 초기화
llm = ChatOpenAI(
    model="gpt-4o-mini",    # 모델 선택
    temperature=0.7,         # 창의성 (0-1)
    max_tokens=1000,         # 최대 토큰
)

# 직접 호출
response = llm.invoke("안녕하세요!")
print(response.content)
```

### 주요 모델 옵션

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `model` | 사용할 모델 | gpt-4o-mini |
| `temperature` | 출력 다양성 (0=결정적, 1=창의적) | 0.7 |
| `max_tokens` | 최대 출력 토큰 | None |
| `timeout` | API 타임아웃 (초) | None |
| `max_retries` | 재시도 횟수 | 2 |

### 다양한 LLM 제공자

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")

# Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Ollama (로컬)
from langchain_community.llms import Ollama
llm = Ollama(model="llama3")

# Google
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")
```

---

## 3. Prompt Template

### 기본 프롬프트 템플릿

```python
from langchain_core.prompts import PromptTemplate

# 단순 템플릿
template = PromptTemplate.from_template(
    "다음 단어를 {language}로 번역해주세요: {word}"
)

# 프롬프트 생성
prompt = template.format(language="영어", word="안녕하세요")
print(prompt)
# 출력: 다음 단어를 영어로 번역해주세요: 안녕하세요
```

### ChatPromptTemplate (대화형)

```python
from langchain_core.prompts import ChatPromptTemplate

# 시스템 + 사용자 메시지
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 번역가입니다. {language}로 번역해주세요."),
    ("user", "{text}")
])

# 메시지 생성
messages = prompt.format_messages(language="영어", text="오늘 날씨가 좋네요")
print(messages)
```

### 다양한 메시지 타입

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 요리 전문가입니다."),
    ("human", "파스타 만드는 법 알려주세요"),       # 사용자
    ("ai", "네, 파스타 레시피를 알려드릴게요..."),   # AI 응답 예시
    ("human", "{question}")                          # 변수
])
```

### MessagesPlaceholder (동적 메시지)

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 어시스턴트입니다."),
    MessagesPlaceholder(variable_name="history"),  # 대화 기록 삽입
    ("human", "{input}")
])
```

---

## 4. Chain (체인)

### LCEL 기본 체인

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 컴포넌트 정의
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 어시스턴트입니다."),
    ("human", "{input}")
])
output_parser = StrOutputParser()

# LCEL로 체인 구성 (| 연산자)
chain = prompt | llm | output_parser

# 실행
result = chain.invoke({"input": "Python이 뭐야?"})
print(result)
```

### 체인 구성 이해

```
prompt | llm | output_parser
   ↓      ↓        ↓
  입력   처리     출력
  변환   (LLM)    파싱

┌─────────────────────────────────────────────────┐
│  {"input": "질문"}                              │
│         ↓                                       │
│  ┌─────────┐                                    │
│  │ Prompt  │ → 메시지 리스트 생성               │
│  └────┬────┘                                    │
│       ↓                                         │
│  ┌─────────┐                                    │
│  │   LLM   │ → AI 응답 생성                     │
│  └────┬────┘                                    │
│       ↓                                         │
│  ┌─────────┐                                    │
│  │ Parser  │ → 문자열 추출                      │
│  └────┬────┘                                    │
│       ↓                                         │
│  "응답 텍스트"                                  │
└─────────────────────────────────────────────────┘
```

### 여러 체인 연결

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 첫 번째 체인: 주제 생성
topic_prompt = ChatPromptTemplate.from_template(
    "다음 분야의 흥미로운 주제를 하나 제안해주세요: {field}"
)
topic_chain = topic_prompt | llm | StrOutputParser()

# 두 번째 체인: 설명 생성
explain_prompt = ChatPromptTemplate.from_template(
    "다음 주제에 대해 초등학생도 이해할 수 있게 설명해주세요: {topic}"
)
explain_chain = explain_prompt | llm | StrOutputParser()

# 체인 연결
full_chain = (
    {"topic": topic_chain}  # 첫 번째 체인 결과를 topic으로
    | explain_chain          # 두 번째 체인에 전달
)

result = full_chain.invoke({"field": "우주"})
print(result)
```

---

## 5. Output Parser

### 기본 파서

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
# AIMessage → 문자열로 변환
```

### JSON 파서

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# 출력 스키마 정의
class Recipe(BaseModel):
    name: str = Field(description="요리 이름")
    ingredients: list[str] = Field(description="재료 목록")
    steps: list[str] = Field(description="조리 순서")

# 파서 생성
parser = JsonOutputParser(pydantic_object=Recipe)

# 프롬프트에 포맷 지시 추가
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 요리 전문가입니다."),
    ("human", "{dish} 레시피를 JSON으로 알려주세요.\n{format_instructions}")
])

chain = prompt | llm | parser

result = chain.invoke({
    "dish": "김치찌개",
    "format_instructions": parser.get_format_instructions()
})
print(result)  # Recipe 객체 또는 딕셔너리
```

### 구조화된 출력 (with_structured_output)

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class MovieReview(BaseModel):
    title: str = Field(description="영화 제목")
    rating: int = Field(description="평점 1-10")
    summary: str = Field(description="한줄 요약")

llm = ChatOpenAI(model="gpt-4o-mini")
structured_llm = llm.with_structured_output(MovieReview)

result = structured_llm.invoke("인셉션 영화에 대해 리뷰해주세요")
print(result.title)   # "인셉션"
print(result.rating)  # 9
print(result.summary) # "꿈 속의 꿈을 다룬 SF 걸작"
```

---

## 6. 실습 예제

### 예제 1: 간단한 번역기

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 전문 번역가입니다. {source_lang}를 {target_lang}로 번역합니다."),
    ("human", "{text}")
])

translator = prompt | llm | StrOutputParser()

result = translator.invoke({
    "source_lang": "한국어",
    "target_lang": "영어",
    "text": "오늘 점심은 김치찌개를 먹었습니다."
})
print(result)
```

### 예제 2: 요약기

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_template("""
다음 텍스트를 {length}문장으로 요약해주세요:

텍스트:
{text}

요약:
""")

summarizer = prompt | llm | StrOutputParser()

long_text = """
인공지능(AI)은 인간의 학습능력, 추론능력, 지각능력을 인공적으로 구현한
컴퓨터 프로그램 또는 이를 포함한 컴퓨터 시스템이다. 최근 딥러닝의 발전으로
AI는 이미지 인식, 자연어 처리, 게임 등 다양한 분야에서 인간 수준의 성능을
보여주고 있다. 특히 GPT와 같은 대규모 언어 모델의 등장으로 AI는 텍스트 생성,
번역, 요약 등의 작업에서 놀라운 성과를 거두고 있다.
"""

result = summarizer.invoke({"text": long_text, "length": 2})
print(result)
```

### 예제 3: 감정 분석기

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class SentimentResult(BaseModel):
    sentiment: str = Field(description="긍정/부정/중립")
    confidence: float = Field(description="확신도 0-1")
    reason: str = Field(description="판단 근거")

llm = ChatOpenAI(model="gpt-4o-mini")
parser = JsonOutputParser(pydantic_object=SentimentResult)

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 감정 분석 전문가입니다."),
    ("human", "다음 리뷰의 감정을 분석해주세요:\n\n{review}\n\n{format_instructions}")
])

analyzer = prompt | llm | parser

result = analyzer.invoke({
    "review": "이 제품 정말 최고예요! 배송도 빠르고 품질도 좋아요.",
    "format_instructions": parser.get_format_instructions()
})

print(f"감정: {result['sentiment']}")
print(f"확신도: {result['confidence']}")
print(f"근거: {result['reason']}")
```

---

## 7. 스트리밍

### 기본 스트리밍

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
prompt = ChatPromptTemplate.from_template("{input}")
chain = prompt | llm

# 스트리밍 출력
for chunk in chain.stream({"input": "Python의 장점 5가지 알려줘"}):
    print(chunk.content, end="", flush=True)
```

### 비동기 스트리밍

```python
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

async def stream_response():
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_template("{input}")
    chain = prompt | llm

    async for chunk in chain.astream({"input": "AI의 미래는?"}):
        print(chunk.content, end="", flush=True)

asyncio.run(stream_response())
```

---

## 8. 일반적인 실수와 해결

### 실수 1: API 키 노출

```python
# 나쁜 예
llm = ChatOpenAI(api_key="sk-xxx...")  # 하드코딩 금지!

# 좋은 예
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI()  # 환경 변수에서 자동 로드
```

### 실수 2: 프롬프트 변수 불일치

```python
# 나쁜 예
prompt = ChatPromptTemplate.from_template("번역: {text}")
chain.invoke({"input": "안녕"})  # KeyError: 'text'

# 좋은 예
chain.invoke({"text": "안녕"})  # 변수명 일치
```

### 실수 3: 레거시 문법 사용

```python
# 레거시 (사용 자제)
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# LCEL (권장)
chain = prompt | llm
```

---

## 핵심 요약

```
┌─────────────────────────────────────────────────┐
│ LangChain 기초 핵심                              │
├─────────────────────────────────────────────────┤
│ LLM: ChatOpenAI(model="gpt-4o-mini")            │
│ Prompt: ChatPromptTemplate.from_messages()      │
│ Chain: prompt | llm | parser (LCEL)             │
│ Parser: StrOutputParser, JsonOutputParser       │
│ 실행: chain.invoke({"key": "value"})            │
│ 스트림: chain.stream(), chain.astream()         │
└─────────────────────────────────────────────────┘
```

## 다음 단계

- [[02-lcel|LCEL 심화]] - 더 복잡한 체인 구성
- [[03-rag|RAG]] - 문서 기반 QA 시스템
