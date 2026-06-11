---
date: 2026-06-08
tags:
  - tech
  - ai
  - mcp
  - model-context-protocol
status: learning
type: tech-tool-study
---

# Model Context Protocol (MCP)

> **한 줄 정의**: Model Context Protocol(MCP)은 LLM/agent host가 외부 data source, tool, prompt, workflow를 표준 JSON-RPC 기반 client-server 방식으로 발견하고 호출하게 해주는 open protocol이다.

## 개요

MCP는 AI application이 외부 system과 통합되는 방식을 표준화한다. 기존에는 Claude, Cursor, VS Code, OpenAI Responses API, LangChain 같은 host마다 Slack, DB, GitHub, 내부 API connector를 따로 붙여야 했지만, MCP는 이 문제를 `AI app -> MCP client -> MCP server -> external system` 구조로 분리한다.

핵심은 **tool/resource/prompt discovery**, **capability negotiation**, **local stdio + remote Streamable HTTP transport**, **OAuth 기반 remote MCP**, **human-in-the-loop 보안 모델**이다.

---

## Quick Start

```bash
# 1. MCP server scaffold 또는 예제 server 준비
# 예: TypeScript/Python SDK 기반 local stdio server

# 2. MCP Inspector로 local server 연결
npx @modelcontextprotocol/inspector

# 3. tools/list, tools/call, resources/list 흐름 확인
# Inspector UI에서 server command와 arguments를 입력
```

---

## 학습 경로

### 1단계: 프로토콜의 문제의식 이해

- [ ] [[01-overview|개요]] 읽기 - MCP가 해결하는 `N x M` integration 문제
- [ ] Host, Client, Server, Tool, Resource, Prompt 용어 정리
- [ ] `stdio`와 `Streamable HTTP` transport 차이 이해

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]] 파악 - Function Calling, OpenAPI, A2A, LangChain tools와 비교
- [ ] MCP가 integration layer인지, agent framework인지 구분
- [ ] [[study/tech/ai/litellm]]와의 역할 차이 정리

### 3단계: 공식 문서와 스펙 확인

- [ ] [[03-references|참고자료]]에서 MCP Specification, Architecture, Transports, Authorization 확인
- [ ] `2025-11-25` protocol version의 주요 변경점 확인
- [ ] Security Best Practices 읽기

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - local `stdio` MCP server와 Inspector 실습
- [ ] [[04-learning/02-deep-dive|심화]] - resource, prompt, remote MCP, OAuth, elicitation 설계

### 5단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]] - Obsidian vault, internal API, RAG 검색, 업무 workflow를 MCP server로 감싸기
- [ ] [[cheatsheet|치트시트]] - JSON-RPC method, feature, 설계 체크리스트 빠른 참조

---

## 파일 구조

```text
model-context-protocol-mcp/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | What/Why, 아키텍처, 핵심 특징 |
| 생태계 | [[02-ecosystem]] | 관련 기술 비교, 함께 쓰는 방식 |
| 참고자료 | [[03-references]] | 공식 문서, 발표, SDK, 가이드 |
| 시작하기 | [[04-learning/01-getting-started]] | local stdio server와 Inspector 실습 |
| 심화 | [[04-learning/02-deep-dive]] | remote MCP, OAuth, elicitation, tasks |
| 프로젝트 | [[05-projects]] | 실전 적용 아이디어와 best practices |
| 치트시트 | [[cheatsheet]] | method, transport, 설계 체크리스트 |

---

## 관련 노트

- [[study/tech/ai/litellm]] - LLM provider routing/gateway 계층
- [[study/tech/ai/llm-wiki-study]] - MCP로 vault/wiki 작업을 노출할 수 있는 지식 관리 패턴
- [[study/tech/ai/agent-orchestration/cli-agents]] - agent CLI와 tool integration 맥락
- [[study/tech/ai/multi-agent-platforms]] - multi-agent platform 생태계

---

**생성일**: 2026-06-08  
**상태**: 학습 중
