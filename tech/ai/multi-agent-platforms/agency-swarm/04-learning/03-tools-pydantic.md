# 4-3. Pydantic 기반 Type-safe Tools

## 🔧 BaseTool 패턴

```python
# agents/developer/tools/CreateFileTool.py
from agency_swarm.tools import BaseTool
from pydantic import Field
from pathlib import Path

class CreateFileTool(BaseTool):
    """파일 생성. 절대 경로만 허용."""
    
    file_path: str = Field(..., description="절대 경로")
    content: str = Field(..., description="파일 내용")
    
    def run(self):
        path = Path(self.file_path)
        if not path.is_absolute():
            return "ERROR: 절대 경로만 허용"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.content)
        return f"Created: {path}"
```

LLM이 자동으로 도구 스키마를 보고 type-safe하게 호출. 런타임 에러 ↓.

## 🌐 OpenAPI Schema → 자동 도구화

```
agents/developer/schemas/
└── github.openapi.yaml
```

GitHub OpenAPI 스키마를 두면 Agency Swarm이 **자동으로 도구 생성**.

```yaml
# 일부
paths:
  /repos/{owner}/{repo}/pulls/{pull_number}:
    get:
      operationId: getPullRequest
      parameters:
        - name: owner
        - name: repo
        - name: pull_number
```

→ Developer가 `getPullRequest` 도구를 자동 호출 가능.

## 🔐 도구 권한 통제

```python
class ShellTool(BaseTool):
    """제한된 shell 명령 실행."""
    command: str = Field(...)
    
    ALLOWED = {"ls", "cat", "grep", "git status", "git diff"}
    
    def run(self):
        if not any(self.command.startswith(p) for p in self.ALLOWED):
            return "ERROR: not allowed"
        return subprocess.check_output(self.command, shell=True).decode()
```

## ⚙️ Async Tool

```python
class FetchTool(BaseTool):
    url: str
    
    async def run(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.url)
            return r.text[:5000]
```

## ✅ 체크포인트
- [ ] BaseTool subclass 1개 작성 후 동작
- [ ] description으로 LLM이 정확히 호출 가능
- [ ] allowlist로 위험 명령 차단

## 🔗 다음 → [04-multi-llm-litellm.md](04-multi-llm-litellm.md)
