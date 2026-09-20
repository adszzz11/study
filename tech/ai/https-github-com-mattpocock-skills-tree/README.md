---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills

> **한 줄 정의**: `writing-great-skills`는 stochastic AI agent가 같은 output이 아니라 같은 process와 품질 기준을 따르도록 Agent Skill을 설계·편집·진단하는 Matt Pocock의 user-invoked meta-skill이다.

## Overview

Agent Skill은 반복 절차, domain knowledge, scripts, references, assets를 `SKILL.md` 중심으로 패키징해 필요할 때만 context에 적재한다. `writing-great-skills`의 목적은 Skill 문서를 길게 만드는 것이 아니라, probabilistic한 실행에서 **process predictability**를 높이는 것이다.

```text
좋은 Skill
= reliable routing
+ explicit steps
+ checkable completion criteria
+ progressive disclosure
+ repeated evaluation and pruning
```

핵심 질문은 “매번 같은 문장이 나오는가?”가 아니라 “매번 필요한 탐색·분기·검증·완료 판정을 거치는가?”다. 공개 `SWE-Skills-Bench` 결과처럼 Skill의 존재만으로 성능이 개선되지는 않으며, scope·selection·version compatibility·evaluation이 품질을 좌우한다.

| 설계 면 | 핵심 원칙 |
|---|---|
| Discovery | `description`을 routing interface로 작성한다. |
| Execution | step마다 agent가 판정 가능한 completion criterion을 둔다. |
| Context | 모든 branch에 필요한 내용만 inline하고 나머지는 조건부 공개한다. |
| Language | 검증된 leading word를 behavioral anchor로 쓴다. |
| Maintenance | duplication, sediment, sprawl, no-op, negation을 제거한다. |
| Portability | core specification과 client-specific field를 구분해 validation한다. |

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, architecture, 핵심 failure mode
- [ ] [[02-ecosystem|Ecosystem]] — Agent Skill과 대안, invocation 방식 비교
- [ ] [[03-references|References]] — primary source와 specification 읽기
- [ ] [[04-learning/01-getting-started|Getting started]] — 작은 Skill 초안과 criterion 작성
- [ ] [[04-learning/02-deep-dive|Deep dive]] — routing, disclosure, pruning, eval 심화
- [ ] [[05-projects|Projects]] — Skill linter와 evaluation harness 만들기
- [ ] [[cheatsheet|Cheatsheet]] — 빠른 작성·리뷰 체크리스트

## When To Use

- 여러 세션에서 반복되는 multi-step workflow를 재사용할 때
- agent가 절차 일부를 건너뛰거나 너무 빨리 완료하는 문제를 고칠 때
- 긴 system prompt를 on-demand context로 분리할 때
- 여러 Skill 사이의 false positive/false negative trigger를 개선할 때
- 기존 `SKILL.md`의 stale rule, duplication, no-op을 audit할 때
- 동일 task를 반복 실행해 process consistency를 평가할 때

## When Not To Use

- 한 번만 수행할 단순 질문이나 짧은 변환 작업
- agent의 판단이 필요 없는 deterministic script로 충분한 작업
- 모든 대화에 항상 적용해야 하는 repository policy나 safety rule
- output equality가 반드시 필요한 계산·검증 로직: code와 tests로 구현한다.
- 사용 중인 client가 지원하는 field와 validation 규칙을 확인하지 않은 cross-agent 배포

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol]] — Skill resource와 tool context의 경계
- [[tech/ai/lazy-codex/README|Lazy Codex]] — verified completion과 agent evaluation
- [[tech/ai/agent-garden|Agent Garden]] — agent capability를 모듈로 관리하는 관점

## Sources

- [Matt Pocock, writing-great-skills `SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- [Matt Pocock, Writing Great Skills](https://www.aihero.dev/skills-writing-great-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic, Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic, Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)

