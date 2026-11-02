---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템: Cheatsheet

[[tech/ai/ai-agent-automation-systems/README|README]] · [[tech/ai/ai-agent-automation-systems/01-overview|Overview]]

## 빠른 구분

| 질문 | 선택 |
|---|---|
| 단계와 규칙이 이미 정해졌는가? | deterministic workflow |
| 다음 행동을 해석·판단해야 하는가? | Agent |
| LLM에 외부 tool/data를 표준으로 붙여야 하는가? | MCP |
| 반복 instruction과 tool 조합을 재사용하는가? | Skill |

## Agent contract

```text
Role: 무엇을 판단하는가
Context: 어떤 source와 rule을 보는가
Output: 어떤 schema로 반환하는가
Allowed tools: 무엇을 읽거나 실행할 수 있는가
Forbidden actions: 무엇을 절대 하지 않는가
Done: 언제 완료인가
```

## 운영 체크리스트

- [ ] read-only tool부터 연결했다.
- [ ] publish, email, payment, delete에 human approval을 뒀다.
- [ ] input/output, tool call, cost, failure, approval을 기록한다.
- [ ] retry와 idempotency를 workflow에 넣었다.
- [ ] source URL과 사실성 검토를 결과물에 남긴다.
- [ ] style guide·decision log·brief를 분리해 retrieval한다.
- [ ] 자동 게시 전에 draft 단계와 eval set을 검증한다.

## 위험 신호

- “그냥 전체 권한을 주자”라는 요구
- 출처 없는 요약을 바로 고객·대중에게 발송
- 실패를 prompt만으로 고치려는 시도
- workflow로 충분한 일을 multi-agent로 확장

## Sources

- https://docs.anthropic.com/en/docs/mcp
- https://n8n.io/ai-agents/
- https://platform.openai.com/docs/assistants/migration
