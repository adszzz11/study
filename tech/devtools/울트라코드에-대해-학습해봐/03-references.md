---
date: 2026-06-19
tags:
  - tech
  - devtools
  - ai
  - coding-agent
  - references
type: tech-tool-study
parent: "[[README]]"
---

# 울트라코드 - 참고자료

> [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 문서

| 자료 | URL | 메모 |
|------|-----|------|
| OpenAI Codex docs | https://developers.openai.com/codex/ | OpenAI의 software development용 coding agent 문서. 코드 작성, 이해, 리뷰, 디버깅, 반복 작업 자동화 흐름을 확인 |
| Claude Code overview | https://code.claude.com/docs/en/overview | codebase 읽기, 파일 수정, command 실행, terminal/IDE/desktop/browser 동작을 설명 |
| GitHub Copilot cloud agent docs | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent | GitHub-native cloud agent, sandbox, policies, MCP, issue/PR workflow |
| OpenCode docs | https://opencode.ai/docs/ | terminal, desktop app, IDE extension으로 제공되는 open-source AI coding agent |
| Aider docs | https://aider.chat/docs/usage.html | terminal 기반 AI pair programming, git diff/commit/undo workflow |
| Devin Desktop docs | https://docs.devin.ai/desktop/getting-started | AI IDE, local agent harness, MCP, memories, context awareness, workflow 자동화 |

---

## 연구 자료

| 자료 | URL | 학습 포인트 |
|------|-----|-------------|
| AIDev paper, 2026 | https://arxiv.org/abs/2602.09185 | Codex, Devin, GitHub Copilot, Cursor, Claude Code가 만든 agent-authored PR dataset 분석 |
| Claude Code architecture analysis, 2026 | https://arxiv.org/abs/2604.14228 | permission, compaction, MCP/plugins/skills/hooks, subagent, session storage 관점 분석 |

---

## 읽는 순서

1. OpenAI Codex docs 또는 Claude Code overview로 agentic coding의 기본 workflow 확인
2. GitHub Copilot cloud agent docs로 issue/PR 중심 cloud workflow 이해
3. OpenCode/Aider docs로 local terminal 기반 접근법 비교
4. Devin Desktop docs로 AI IDE + local/cloud agent 형태 확인
5. AIDev paper로 agent-authored PR이 실제 생태계에서 어떻게 나타나는지 확인
6. Claude Code architecture analysis로 permission/context/tool 확장 구조 학습

---

## 검토 질문

- 이 도구는 파일을 실제로 수정하는가, 아니면 제안만 하는가?
- command 실행 권한은 어떻게 제한되는가?
- repo context는 어떤 방식으로 주입되는가?
- `AGENTS.md`, `CLAUDE.md`, rules, memory에 해당하는 장치가 있는가?
- test/lint/typecheck 실행을 agent loop 안에 넣을 수 있는가?
- GitHub issue/PR, Jira, Slack, internal docs와 연결할 수 있는가?

---

## 관련 노트

- [[study/tech/ai/codex/03-references]] - Codex 참고자료
- [[study/tech/ai/model-context-protocol-mcp/03-references]] - MCP 참고자료
- [[study/tech/ai/claude/07-mcp]] - Claude Code와 MCP
