# 4-3. Tools, Memory, RAG

## 🛠️ 내장 도구

```bash
uv pip install 'crewai[tools]'
```

```python
from crewai_tools import (
    SerperDevTool,         # Google 검색
    WebsiteSearchTool,
    FileReadTool, FileWriterTool,
    DirectoryReadTool,
    GithubSearchTool,
    YoutubeChannelSearchTool,
    PDFSearchTool,
    EXASearchTool,
    BraveSearchTool,
    MCPServerAdapter,      # MCP 서버 통합
)

researcher = Agent(
    role="...",
    tools=[SerperDevTool(), WebsiteSearchTool()],
)
```

## 🔌 커스텀 도구

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class FetchPRInput(BaseModel):
    pr_number: int = Field(..., description="PR 번호")

class FetchPRTool(BaseTool):
    name: str = "fetch_pr"
    description: str = "GitHub PR 정보를 가져옴"
    args_schema: type[BaseModel] = FetchPRInput

    def _run(self, pr_number: int) -> str:
        # 실제 호출
        return github_api.get_pr(pr_number)

agent = Agent(..., tools=[FetchPRTool()])
```

## 🧠 메모리 시스템

CrewAI 메모리는 4계층:

| 종류 | 용도 |
|------|------|
| **Short-term** | 현재 실행 컨텍스트 |
| **Long-term** | 작업 간 영속 (DB) |
| **Entity** | 사람·장소·개념 추출 |
| **Contextual** | RAG 스타일 검색 |

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"},
    },
)
```

데이터 저장 위치: `~/.crewai/storage/` (SQLite + Chroma).

## 📚 RAG 패턴

### 방법 1: PDFSearchTool / WebsiteSearchTool
```python
from crewai_tools import PDFSearchTool

tool = PDFSearchTool(pdf="docs/spec.pdf")
agent = Agent(..., tools=[tool])
# 에이전트가 "spec에서 X 찾아" → 자동으로 RAG
```

### 방법 2: 커스텀 벡터DB
```python
import chromadb
from crewai.tools import BaseTool

class VaultSearchTool(BaseTool):
    name = "search_vault"
    
    def _run(self, query: str) -> str:
        results = chromadb.PersistentClient(path="./vault_db")\
            .get_collection("notes").query(query_texts=[query])
        return "\n".join(results["documents"][0])
```

### 방법 3: Mem0 / Letta 외부 연결
```python
from mem0 import MemoryClient

class Mem0Tool(BaseTool):
    name = "recall_user"
    def _run(self, query: str) -> str:
        return MemoryClient().search(query, user_id="sm")
```

## 🔌 MCP 통합 (2025+)

```python
from crewai_tools import MCPServerAdapter

mcp_tools = MCPServerAdapter(server_url="http://localhost:3001")
agent = Agent(..., tools=mcp_tools)
```

→ Claude Code / Cursor의 MCP 서버를 그대로 재사용 가능

## ✅ 체크포인트
- [ ] 내장 도구 1개 적용 (예: SerperDevTool)
- [ ] 커스텀 도구 1개 작성
- [ ] memory=True로 두 번째 kickoff 시 이전 컨텍스트 활용 확인
- [ ] RAG 도구로 PDF·노트 질의응답

## 🔗 다음 → [04-flows-production.md](04-flows-production.md)
