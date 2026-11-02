---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템: Ecosystem

[[tech/ai/ai-agent-automation-systems/README|README]] · [[tech/ai/ai-agent-automation-systems/03-references|References]]

| 선택지 | 잘 맞는 일 | 장점 | 주의점 |
|---|---|---|---|
| Claude Code + Skills/MCP | code·file·local 개발 자동화 | 작업 맥락과 terminal workflow에 강함 | permission과 MCP 공급망 검증 필요 |
| OpenAI Responses API | 제품에 Agent 내장 | web search, tools, MCP 등 API 확장 | orchestration·검증·비용 제어를 직접 설계 |
| n8n | 업무 자동화·팀 운영 | trigger, retry, approval, log, integration 관리 | 단순 작업까지 Agent화하지 말 것 |
| Zapier / Make | SaaS 중심의 빠른 자동화 | 낮은 진입장벽 | 복잡한 state·custom logic에 제약 |
| LangGraph / 자체 code | 장기 실행·정교한 runtime | state와 제어 흐름의 자유도 | 운영·관측·보안 책임 증가 |
| Higgsfield 등 생성 도구 | 영상·이미지 asset 제작 | 콘텐츠 생산 속도 향상 | IP, likeness, 광고 표기, QA 필요 |

## 선택 기준

1. 우선 workflow로 고정할 수 있는지를 확인한다.
2. 판단이 필요한 노드에만 Agent를 넣는다.
3. tool은 read-only부터 연결하고 write scope를 별도로 승인한다.
4. 제품 내 기능이면 API, 팀의 반복 운영이면 workflow platform, 개발 업무면 coding agent를 우선 검토한다.

## 역할 경계

- **MCP**: LLM application과 data source/tool을 연결하는 protocol이다. Agent framework 자체는 아니다.
- **Skill**: 반복 업무의 instructions와 tool 사용법을 패키징한 재사용 단위다.
- **Agent**: 목표를 바탕으로 다음 행동을 판단한다.
- **Workflow**: 미리 결정된 순서대로 안정적으로 실행한다.

## Sources

- https://docs.anthropic.com/en/docs/claude-code/cli-usage
- https://platform.openai.com/docs/assistants/migration
- https://n8n.io/ai-agents/
- https://docs.n8n.io/advanced-ai/ai-agents/

