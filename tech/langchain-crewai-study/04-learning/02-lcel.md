# LCEL - LangChain Expression Language

## 개요

LCEL(LangChain Expression Language)은 LangChain의 핵심 문법으로, `|` (파이프) 연산자를 사용해 컴포넌트를 연결하여 체인을 구성한다.

---

## 1. LCEL 기본 문법

### 파이프 연산자 (|)

```python
# 기본 형태: 컴포넌트1 | 컴포넌트2 | 컴포넌트3
chain = prompt | llm | parser

# 각 컴포넌트의 출력이 다음 컴포넌트의 입력으로 전달됨
```

### 실행 메서드

| 메서드 | 설명 | 반환 |
|--------|------|------|
| `invoke(input)` | 단일 입력 동기 실행 | 결과 |
| `stream(input)` | 단일 입력 스트리밍 | Iterator |
| `batch(inputs)` | 다중 입력 일괄 실행 | 결과 리스트 |
| `ainvoke(input)` | 단일 입력 비동기 실행 | Awaitable |
| `astream(input)` | 비동기 스트리밍 | AsyncIterator |
| `abatch(inputs)` | 다중 입력 비동기 일괄 | Awaitable |

```python
# 단일 실행
result = chain.invoke({"input": "안녕"})

# 배치 실행
results = chain.batch([
    {"input": "안녕"},
    {"input": "반가워"}
])

# 스트리밍
for chunk in chain.stream({"input": "안녕"}):
    print(chunk, end="")
```

---

## 2. Runnable 인터페이스

### 모든 LCEL 컴포넌트는 Runnable

```
Runnable 인터페이스
├── RunnableLambda     # 사용자 정의 함수
├── RunnablePassthrough # 입력 그대로 전달
├── RunnableParallel   # 병렬 실행
├── RunnableBranch     # 조건부 분기
├── RunnableSequence   # 순차 실행 (| 결과)
└── 기타 LangChain 컴포넌트
```

### RunnableLambda - 커스텀 함수

```python
from langchain_core.runnables import RunnableLambda

# 함수를 Runnable로 변환
def custom_parser(text: str) -> dict:
    lines = text.strip().split('\n')
    return {"lines": lines, "count": len(lines)}

parser = RunnableLambda(custom_parser)

# 체인에서 사용
chain = prompt | llm | StrOutputParser() | parser
```

### 데코레이터로 간단하게

```python
from langchain_core.runnables import chain as chain_decorator

@chain_decorator
def format_output(text: str) -> str:
    return f"=== 결과 ===\n{text}\n============"

# 체인에서 사용
full_chain = prompt | llm | StrOutputParser() | format_output
```

---

## 3. RunnablePassthrough

### 입력 그대로 전달

```python
from langchain_core.runnables import RunnablePassthrough

# 입력을 그대로 다음으로 전달
chain = RunnablePassthrough() | llm

# 주로 RunnableParallel과 함께 사용
chain = (
    {"question": RunnablePassthrough(), "context": retriever}
    | prompt
    | llm
)
```

### assign - 값 추가

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough.assign(
    # 기존 입력에 새로운 키-값 추가
    upper_text=lambda x: x["text"].upper()
)

result = chain.invoke({"text": "hello"})
# {"text": "hello", "upper_text": "HELLO"}
```

---

## 4. RunnableParallel - 병렬 실행

### 딕셔너리로 병렬 구성

```python
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 두 개의 프롬프트 병렬 실행
joke_prompt = ChatPromptTemplate.from_template("{topic}에 대한 농담 하나 해줘")
poem_prompt = ChatPromptTemplate.from_template("{topic}에 대한 짧은 시 써줘")

joke_chain = joke_prompt | llm | StrOutputParser()
poem_chain = poem_prompt | llm | StrOutputParser()

# 병렬 실행
parallel_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain
)

# 또는 딕셔너리 문법
parallel_chain = {
    "joke": joke_chain,
    "poem": poem_chain
}

result = parallel_chain.invoke({"topic": "프로그래밍"})
print(result["joke"])
print(result["poem"])
```

### 입력 변환과 병렬 결합

```python
from langchain_core.runnables import RunnablePassthrough

# context 검색과 question 전달을 병렬로
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("LangChain이 뭐야?")
```

---

## 5. RunnableBranch - 조건부 분기

### 조건에 따른 체인 선택

```python
from langchain_core.runnables import RunnableBranch

# 입력 길이에 따라 다른 처리
branch = RunnableBranch(
    # (조건 함수, 실행할 체인)
    (lambda x: len(x["text"]) > 100, long_text_chain),
    (lambda x: len(x["text"]) > 50, medium_text_chain),
    short_text_chain  # 기본값 (조건 없음)
)

result = branch.invoke({"text": "짧은 텍스트"})
```

### 분류 기반 분기

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate

# 분류기
classifier_prompt = ChatPromptTemplate.from_template(
    "다음 질문의 카테고리를 분류해주세요 (기술/일반/요리): {question}"
)
classifier = classifier_prompt | llm | StrOutputParser()

# 카테고리별 전문가 체인
tech_chain = ChatPromptTemplate.from_template(
    "당신은 기술 전문가입니다. {question}"
) | llm | StrOutputParser()

general_chain = ChatPromptTemplate.from_template(
    "당신은 친절한 어시스턴트입니다. {question}"
) | llm | StrOutputParser()

cooking_chain = ChatPromptTemplate.from_template(
    "당신은 요리 전문가입니다. {question}"
) | llm | StrOutputParser()

# 분류 결과에 따른 분기
def route(info):
    category = info["category"].strip().lower()
    question = info["question"]

    if "기술" in category:
        return tech_chain.invoke({"question": question})
    elif "요리" in category:
        return cooking_chain.invoke({"question": question})
    else:
        return general_chain.invoke({"question": question})

# 전체 체인
full_chain = (
    RunnablePassthrough.assign(category=classifier)
    | RunnableLambda(route)
)
```

---

## 6. 체인 조합 패턴

### 패턴 1: 순차 처리

```python
# 단계별 처리
step1 = prompt1 | llm | StrOutputParser()
step2 = prompt2 | llm | StrOutputParser()
step3 = prompt3 | llm | StrOutputParser()

# 체인 연결
chain = (
    {"step1_result": step1}
    | {"step2_result": step2}
    | step3
)
```

### 패턴 2: Map-Reduce

```python
from langchain_core.runnables import RunnableLambda

# Map: 각 항목 처리
def process_item(item):
    return single_item_chain.invoke({"item": item})

# Reduce: 결과 합치기
def combine_results(results):
    return "\n".join(results)

chain = (
    RunnableLambda(lambda x: [process_item(i) for i in x["items"]])
    | RunnableLambda(combine_results)
)
```

### 패턴 3: 폴백 (Fallback)

```python
from langchain_openai import ChatOpenAI

# 메인 모델
main_llm = ChatOpenAI(model="gpt-4o")

# 백업 모델
fallback_llm = ChatOpenAI(model="gpt-4o-mini")

# 폴백 설정
llm_with_fallback = main_llm.with_fallbacks([fallback_llm])

chain = prompt | llm_with_fallback | StrOutputParser()
```

### 패턴 4: 재시도

```python
from langchain_core.runnables import RunnableRetry

# 재시도 설정
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

---

## 7. 고급 기능

### bind - 파라미터 바인딩

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

# 특정 파라미터 고정
llm_with_temp = llm.bind(temperature=0)

# 도구 바인딩
llm_with_tools = llm.bind_tools([my_tool])

# 함수 호출 강제
llm_force_function = llm.bind(
    function_call={"name": "get_weather"}
)
```

### configurable - 런타임 설정

```python
from langchain_core.runnables import ConfigurableField

llm = ChatOpenAI(model="gpt-4o-mini").configurable_fields(
    model=ConfigurableField(
        id="model",
        name="Model Name",
        description="사용할 모델"
    ),
    temperature=ConfigurableField(
        id="temperature",
        name="Temperature",
        description="창의성 수준"
    )
)

chain = prompt | llm | StrOutputParser()

# 런타임에 설정 변경
result = chain.invoke(
    {"input": "안녕"},
    config={"configurable": {"model": "gpt-4o", "temperature": 0.9}}
)
```

### 이벤트 스트리밍

```python
# 상세 이벤트 스트리밍
async for event in chain.astream_events({"input": "안녕"}, version="v2"):
    print(f"Event: {event['event']}")
    if event['event'] == 'on_chat_model_stream':
        print(event['data']['chunk'].content, end="")
```

---

## 8. 디버깅

### 체인 시각화

```python
# 체인 구조 출력
chain.get_graph().print_ascii()

# 입력/출력 스키마 확인
print(chain.input_schema.schema())
print(chain.output_schema.schema())
```

### 중간 결과 확인

```python
from langchain_core.runnables import RunnableLambda

def debug_print(x):
    print(f"Debug: {x}")
    return x

chain = (
    prompt
    | RunnableLambda(debug_print)  # 디버깅 포인트
    | llm
    | RunnableLambda(debug_print)  # 디버깅 포인트
    | StrOutputParser()
)
```

### LangSmith 추적

```python
import os

# 환경 변수 설정
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# 이후 모든 체인 실행이 자동으로 추적됨
```

---

## 9. 실습 예제

### 예제 1: 다단계 분석 파이프라인

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini")

# 1단계: 핵심 키워드 추출
keyword_prompt = ChatPromptTemplate.from_template(
    "다음 텍스트에서 핵심 키워드 5개를 추출하세요:\n\n{text}"
)

# 2단계: 요약
summary_prompt = ChatPromptTemplate.from_template(
    "다음 텍스트를 3문장으로 요약하세요:\n\n{text}"
)

# 3단계: 최종 리포트
report_prompt = ChatPromptTemplate.from_template(
    """다음 정보를 바탕으로 분석 리포트를 작성하세요:

원문:
{text}

키워드:
{keywords}

요약:
{summary}
"""
)

# 파이프라인 구성
analysis_chain = (
    RunnablePassthrough.assign(
        keywords=keyword_prompt | llm | StrOutputParser(),
        summary=summary_prompt | llm | StrOutputParser()
    )
    | report_prompt
    | llm
    | StrOutputParser()
)

text = """
인공지능 기술이 빠르게 발전하면서 다양한 산업에 큰 변화를 가져오고 있다.
특히 자연어 처리 분야에서는 GPT, Claude 등의 대규모 언어 모델이 등장하여
텍스트 생성, 번역, 요약 등의 작업에서 인간에 근접한 성능을 보여주고 있다.
이러한 기술은 고객 서비스, 콘텐츠 제작, 교육 등 다양한 분야에 적용되고 있다.
"""

result = analysis_chain.invoke({"text": text})
print(result)
```

### 예제 2: 다국어 처리 파이프라인

```python
from langchain_core.runnables import RunnableParallel

llm = ChatOpenAI(model="gpt-4o-mini")

# 각 언어 번역 체인
def make_translator(target_lang):
    prompt = ChatPromptTemplate.from_template(
        f"다음을 {target_lang}로 번역하세요:\n\n{{text}}"
    )
    return prompt | llm | StrOutputParser()

# 병렬 번역
multi_translate = RunnableParallel(
    english=make_translator("영어"),
    japanese=make_translator("일본어"),
    chinese=make_translator("중국어"),
    spanish=make_translator("스페인어")
)

result = multi_translate.invoke({"text": "오늘 날씨가 정말 좋습니다."})
print(f"English: {result['english']}")
print(f"Japanese: {result['japanese']}")
print(f"Chinese: {result['chinese']}")
print(f"Spanish: {result['spanish']}")
```

### 예제 3: 동적 프롬프트 선택

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda

llm = ChatOpenAI(model="gpt-4o-mini")

# 톤별 프롬프트
formal_prompt = ChatPromptTemplate.from_template(
    "정중하고 격식있는 어조로 답변하세요: {question}"
)
casual_prompt = ChatPromptTemplate.from_template(
    "친근하고 편안한 어조로 답변하세요: {question}"
)
professional_prompt = ChatPromptTemplate.from_template(
    "전문적이고 기술적인 어조로 답변하세요: {question}"
)

# 톤에 따른 분기
tone_branch = RunnableBranch(
    (lambda x: x.get("tone") == "formal", formal_prompt),
    (lambda x: x.get("tone") == "professional", professional_prompt),
    casual_prompt  # 기본값
)

chain = tone_branch | llm | StrOutputParser()

# 사용
print(chain.invoke({"question": "AI란 무엇인가요?", "tone": "formal"}))
print(chain.invoke({"question": "AI란 무엇인가요?", "tone": "casual"}))
```

---

## 10. 성능 최적화

### 배치 처리

```python
# 개별 호출 (느림)
results = []
for item in items:
    results.append(chain.invoke(item))

# 배치 호출 (빠름)
results = chain.batch(items, config={"max_concurrency": 5})
```

### 비동기 처리

```python
import asyncio

async def process_all(items):
    tasks = [chain.ainvoke(item) for item in items]
    return await asyncio.gather(*tasks)

results = asyncio.run(process_all(items))
```

### 캐싱

```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# 메모리 캐시 설정
set_llm_cache(InMemoryCache())

# 동일 입력에 대해 캐시된 결과 반환
```

---

## 핵심 요약

```
┌─────────────────────────────────────────────────┐
│ LCEL 핵심 요약                                   │
├─────────────────────────────────────────────────┤
│ 파이프: a | b | c (순차 실행)                    │
│ 병렬: {"key1": chain1, "key2": chain2}          │
│ 분기: RunnableBranch((조건, 체인), 기본값)       │
│ 커스텀: RunnableLambda(함수)                     │
│ 전달: RunnablePassthrough()                      │
│ 추가: RunnablePassthrough.assign(key=값)         │
│ 실행: invoke, stream, batch, ainvoke            │
└─────────────────────────────────────────────────┘
```

## 다음 단계

- [[03-rag|RAG 파이프라인]] - LCEL로 RAG 구축
- [[04-crewai-basics|CrewAI 기초]] - 에이전트 협업
