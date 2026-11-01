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

## 추가 조사: Self-Critique와 Judge를 분리하는 이유

`draft → critique → refine`은 유용한 **self-correction** 패턴이지만, 같은 agent가 쓴 답을 같은 관점으로 재검토하면 blind spot이 남는다. 따라서 릴스의 “자기 답변 공격”은 아래처럼 비판의 입력과 판정 기준을 분리해야 실무에서 의미가 있다.

| 단계 | 질문 | 산출물 |
|---|---|---|
| Draft | 무엇을 주장·변경하는가? | claim, patch, 가정 |
| Critique | 이 결론을 틀리게 할 반례는? | missing evidence, contradiction, regression risk |
| Verify | 사실·동작이 재현되는가? | source check, test/log, screenshot |
| Judge | acceptance criteria를 만족하는가? | accept / revise / reject와 이유 |

```text
Critic prompt:
"결론을 다시 쓰지 말고, (1) 검증되지 않은 claim,
 (2) 반례, (3) 실패할 test, (4) scope/권한 위반만 기록하라."
```

- critic의 품질은 부정적인 문장 수가 아니라, **결론을 바꿀 수 있는 반례**와 재현 절차로 평가한다.
- judge는 다수결이 아니라 acceptance criteria의 gate다. CI/test가 없으면 “검증 불충분”으로 남기며, 그럴듯한 합의로 대체하지 않는다.
- 최신 guidance는 긴 연구에서 competing hypothesis, confidence, progress note를 유지하고 주기적으로 접근법을 self-critique하도록 권한다.

## 추가 조사: Token 절약은 Context Engineering이다

token 절약은 worker 수를 기계적으로 줄이는 문제가 아니라, 각 호출에 **판단에 필요한 최소 context**를 전달하고 재사용 가능한 상태를 파일로 남기는 문제다.

| 낭비 원인 | 대안 | 측정값 |
|---|---|---|
| 모든 worker에 전체 repo 주입 | `CODEMAP.md` + 관련 경로 + API contract | input token, 재탐색 횟수 |
| 긴 성공 log 전달 | 실패 구간·명령·exit code만 전달 | output token, 디버그 시간 |
| context 소진 직전의 즉흥 요약 | `progress.md`, 구조화된 test 목록 | handoff 후 재작업 수 |
| “병렬화=저비용” 가정 | direct 실행 baseline과 비교 | 총 token, wall-clock, 성공률 |

```text
handoff.md
- Goal / acceptance criteria:
- Files changed and why:
- Commands run + result:
- Evidence URLs:
- Open risks / next smallest step:
```

- 장기 작업에서는 첫 context window에 test·setup·상태 파일을 마련하고, 이후 window에서는 그 artifact를 읽어 재개하는 방식이 안정적이다.
- `--max-turns` 같은 실행 상한과 gateway의 budget/rate limit은 runaway loop 방지에는 유효하지만 품질 지표를 대신하지 않는다.

출처: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables · https://docs.anthropic.com/en/docs/claude-code/cli-usage · https://docs.anthropic.com/en/docs/claude-code/llm-gateway
