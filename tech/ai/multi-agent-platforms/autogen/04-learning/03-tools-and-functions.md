# 4-3. Tools & Function Calling

## 🔧 v0.4 Tool 등록
```python
from autogen_core.tools import FunctionTool

def get_weather(city: str) -> str:
    """도시의 현재 날씨"""
    return f"{city}: 맑음 22°C"

weather = FunctionTool(get_weather, description="도시 날씨 조회")
agent = AssistantAgent("assistant", model_client=model, tools=[weather])
```

## 🔌 LangChain Tool 호환
```python
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.tools import DuckDuckGoSearchRun

ddg = LangChainToolAdapter(DuckDuckGoSearchRun())
agent = AssistantAgent(..., tools=[ddg])
```

## 🐳 Code Execution (v0.2/AG2)
```python
from autogen.coding import DockerCommandLineCodeExecutor

executor = DockerCommandLineCodeExecutor(
    image="python:3.12-slim",
    timeout=60,
    work_dir="./work",
)
user = UserProxyAgent("user", code_execution_config={"executor": executor})
```

**중요**: production에서 `use_docker=True` 강제. 안 그러면 호스트에 임의 코드 실행됨.

## 🔐 권한 통제
```python
def safe_shell(cmd: str) -> str:
    ALLOWED = ["ls", "cat", "grep"]
    if cmd.split()[0] not in ALLOWED:
        return "ERROR: not allowed"
    return subprocess.check_output(cmd, shell=True).decode()
```

도구 자체에서 allowlist 적용. LLM 판단에 의존 ✗.

## ✅ 체크포인트
- [ ] FunctionTool 호출 성공
- [ ] LangChain tool 호환
- [ ] Docker code execution 격리 확인
- [ ] tool 권한 allowlist 적용

## 🔗 다음 → [04-studio.md](04-studio.md)
