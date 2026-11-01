---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 접근법 비교

| 접근 | 강점 | 한계·권장 용도 |
|---|---|---|
| Claude Code native Skills + subagents | Claude 환경과 자연스럽게 결합, procedure 재사용 | skill 품질·권한 검토가 필요 |
| Community `SKILL.md` | token 절약·self-critique 등 빠른 출발 | 작성자 신뢰도·유지보수·보안이 제각각 |
| MCP server | GitHub, DB, browser, SaaS 연결 | tool description도 context를 쓰며 credential 노출 위험 |
| CrewAI / AutoGen / LangGraph류 | 명시적 graph, 관측성, provider-agnostic | 운영·상태관리·비용 제어 부담 증가 |
| 단일 Claude + checklist | 가장 저렴하고 디버깅이 단순 | 독립 조사와 adversarial review 범위가 좁음 |

## 릴의 주장과 구현 방향

| 주장 | 검증 가능한 구현 |
|---|---|
| 여러 Claude가 답하고 한 명이 합침 | 독립 research worker + judge + citation/test gate |
| 자기 답변 공격 | self-critique skill 또는 별도 critic pass |
| token 절약 | `CODEMAP`, file summary cache, concise test/log output |
| business idea 발굴 | evidence-first problem discovery와 willingness-to-pay 검증 |
| AI 티 없는 UI | design-system/reference 조사 + screenshot review |

병렬화는 wall-clock time을 줄일 수 있어도 총 token을 자동으로 줄이지 않는다. 공통 context가 큰 worker 수를 늘리기보다, 입력을 요약·분할하고 한 번의 judge pass에 필요한 evidence만 넘기는 편이 낫다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/03-references|References]]

## Sources

- https://docs.anthropic.com/en/docs/mcp
- https://github.com/camilo-acevedo/claude-skills
- https://github.com/jfkconstruct/claude-skills/blob/main/skills/self-critique/SKILL.md
