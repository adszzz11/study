---
date: 2026-01-24
tags:
  - tech
  - claude
  - mcp
  - integration
parent: "[[README]]"
---

# Claude Code - MCP (Model Context Protocol)

> ⬅️ [[06-hooks|이전: Hooks]] | [[README|목차]] | ➡️ [[08-subagents|다음: Subagents]]

---

## 1. MCP란?

> 외부 도구, 데이터베이스, API를 Claude Code에 연결하는 개방형 프로토콜

### 핵심 특징

- 100+ 외부 서비스 연동
- 표준화된 통신 프로토콜
- 동적 도구 로딩
- 보안 연결

---

## 2. MCP 서버 유형

### Transport 방식

| 타입 | 설명 | 권장 |
|------|------|------|
| HTTP | HTTP 기반 서버 | ✅ 권장 |
| Stdio | 표준 입출력 기반 | 로컬 도구 |
| SSE | Server-Sent Events | ❌ Deprecated |

### 범위 (Scope)

| 범위 | 설정 파일 | 공유 |
|------|----------|------|
| Local | `.claude/settings.local.json` | 로컬만 |
| Project | `.mcp.json` | 팀 공유 |
| User | `~/.claude/settings.json` | 전역 |

---

## 3. MCP 서버 추가

### CLI로 추가

```bash
# HTTP 서버
claude mcp add github --transport http https://api.github.com/mcp/

# Stdio 서버
claude mcp add postgres --transport stdio -- npx -y @bytebase/dbhub --dsn "postgresql://..."

# 환경 변수와 함께
claude mcp add slack --transport http https://slack.mcp.server \
  --env SLACK_TOKEN=xoxb-xxx
```

### 설정 파일로 추가

**.mcp.json (프로젝트 공유):**

```json
{
  "mcpServers": {
    "github": {
      "transport": "http",
      "url": "https://api.github.com/mcp/"
    },
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "postgresql://..."]
    }
  }
}
```

---

## 4. 주요 MCP 서버

### 개발 도구

| 서버 | 기능 |
|------|------|
| GitHub | PR, Issue, 코드 검색 |
| GitLab | GitLab 연동 |
| Sentry | 에러 모니터링 |
| Linear | 이슈 트래킹 |

### 데이터베이스

| 서버 | 기능 |
|------|------|
| PostgreSQL | SQL 쿼리, 스키마 |
| MySQL | MySQL 연동 |
| MongoDB | NoSQL 쿼리 |
| Redis | 캐시 조회 |

### 생산성

| 서버 | 기능 |
|------|------|
| Slack | 메시지, 채널 |
| Notion | 페이지, 데이터베이스 |
| Google Drive | 문서 접근 |
| Figma | 디자인 파일 |

---

## 5. MCP 서버 관리

### 목록 확인

```bash
claude mcp list
```

### 서버 제거

```bash
claude mcp remove github
```

### 서버 상태 확인

```bash
claude mcp status
```

---

## 6. Tool Search (v2.1.0+)

### 개념

MCP 도구가 많을 때 컨텍스트 효율화

### 효과

- 컨텍스트 사용량 46.9% 감소
- 51K → 8.5K 토큰 절약
- 필요한 도구만 동적 로딩

### 자동 활성화 조건

MCP 도구가 컨텍스트의 10% 초과 시 자동 활성화

---

## 7. MCP Resources

### 리소스 참조 문법

```
@서버명:프로토콜://경로
```

### 예시

```
> @github:repo://anthropics/claude-code 분석해줘
> @postgres:table://users 스키마 보여줘
> @notion:page://meeting-notes 요약해줘
```

---

## 8. 실전 예시

### GitHub 연동

```bash
# GitHub MCP 추가
claude mcp add github --transport http https://api.github.com/mcp/ \
  --env GITHUB_TOKEN=$GITHUB_TOKEN
```

**사용:**

```
> 최근 PR 목록 보여줘
> #123 이슈에 댓글 달아줘
> main 브랜치 최근 커밋 확인
```

### PostgreSQL 연동

```bash
claude mcp add mydb --transport stdio -- \
  npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"
```

**사용:**

```
> users 테이블 스키마 보여줘
> 최근 가입한 사용자 10명 조회
> 월별 매출 통계 쿼리 작성해줘
```

### Slack 연동

```bash
claude mcp add slack --transport http https://slack.mcp.server \
  --env SLACK_TOKEN=$SLACK_TOKEN
```

**사용:**

```
> #general 채널 최근 메시지 요약
> @john에게 DM 보내줘
```

---

## 9. 보안 설정

### 조직 관리 설정

```json
{
  "mcpServers": {
    "allowed": ["github", "postgres"],
    "denied": ["*"]
  }
}
```

### 권한 제어

```json
{
  "mcpServers": {
    "github": {
      "permissions": {
        "read": true,
        "write": false
      }
    }
  }
}
```

---

## 10. 커스텀 MCP 서버

### 기본 구조 (Python)

```python
from mcp import Server, Tool

server = Server("my-server")

@server.tool("search_docs")
async def search_docs(query: str) -> str:
    """문서 검색"""
    results = await do_search(query)
    return results

if __name__ == "__main__":
    server.run()
```

### 등록

```bash
claude mcp add my-server --transport stdio -- python my_server.py
```

---

## 11. 트러블슈팅

| 문제 | 원인 | 해결 |
|------|------|------|
| 연결 실패 | 네트워크/인증 | 토큰 확인, URL 확인 |
| 도구 없음 | 서버 미시작 | `claude mcp status` |
| 타임아웃 | 느린 서버 | 타임아웃 설정 증가 |
| 권한 오류 | 토큰 권한 부족 | 토큰 스코프 확인 |

---

## 12. Best Practices

### DO ✅

- 필요한 서버만 연결
- 환경 변수로 토큰 관리
- Project scope로 팀 공유
- Tool Search 활용

### DON'T ❌

- 토큰 하드코딩
- 불필요한 서버 연결
- 과도한 권한 부여
- 프로덕션 DB 직접 연결

---

## 다음 단계

> [!tip] 다음으로
> MCP를 이해했다면 [[08-subagents|Subagents]]에서 멀티 에이전트를 배워보세요.

---

## References

- [MCP 공식 문서](https://docs.anthropic.com/claude/docs/mcp)
- [MCP 서버 목록](https://github.com/modelcontextprotocol/servers)
- [MCP 프로토콜 스펙](https://spec.modelcontextprotocol.io/)
