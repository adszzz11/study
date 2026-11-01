---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# References — 공식 문서와 공개 소스

| 구분 | 출처 | 활용 |
|---|---|---|
| 원본 | [Instagram 릴](https://www.instagram.com/reel/DfLLn3DDG9C/) | 주제 식별용 공개 캡션 |
| 공식 | [Claude Code getting started](https://docs.anthropic.com/en/docs/claude-code/getting-started) | 설치·인증·기본 실행 |
| 공식 | [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code/cli-usage) | CLI 동작 확인 |
| 공식 | [MCP documentation](https://docs.anthropic.com/en/docs/mcp) | 외부 도구 연결과 경계 |
| 공식 | [LLM Gateway](https://docs.anthropic.com/en/docs/claude-code/llm-gateway) | usage tracking·budget·audit logging |
| 공식 | [Corporate proxy](https://docs.anthropic.com/en/docs/claude-code/corporate-proxy) | network/security 고려 |
| community | [camilo-acevedo/claude-skills](https://github.com/camilo-acevedo/claude-skills) | token-saving skill 예시 |
| community | [self-critique skill](https://github.com/jfkconstruct/claude-skills/blob/main/skills/self-critique/SKILL.md) | 비평 절차 예시 |
| community | [idea-hunt-skill](https://github.com/ANVEAI/idea-hunt-skill) | evidence-first idea discovery |

외부 repository는 추천 목록이 아니라 검토 대상이다. 설치 전 commit/release를 pin하고 `SKILL.md`, 실행 script, network/file access, dependency를 읽은 뒤 sandbox에서 시험한다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/04-learning/01-getting-started|시작하기]]

## Sources

- https://docs.anthropic.com/en/docs/claude-code/cli-usage
- https://docs.anthropic.com/en/docs/claude-code/corporate-proxy
