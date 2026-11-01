---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — Claude Code Skills와 Multi-Agent

## What

`SKILL.md`는 특정 일을 언제, 어떤 입력으로, 어떤 순서와 완료 기준으로 수행할지를 담는 on-demand procedure다. Claude Code의 subagent와 MCP를 함께 쓰면 procedure가 외부 도구·repository·CI까지 연결된 실행 흐름이 된다.

```text
task + success criteria
→ coordinator (scope / budget)
→ research · implementation · design workers
→ critic / judge
→ evidence, deterministic tests, human approval
```

## Why

단일 agent는 탐색 편향과 누락, 과도한 확신을 만들기 쉽다. 반대로 무분별한 병렬화는 context, token, merge 충돌을 키운다. 따라서 worker의 산출물을 “그럴듯한 답”이 아니라 citation, test 결과, scope 준수 여부로 평가해야 한다.

## 핵심 특징

| 요소 | 역할 | 실무 원칙 |
|---|---|---|
| Skills | 반복 절차 재사용 | 단일 목적·명확한 입력/출력으로 좁힌다 |
| Parallel specialists | 독립 탐색 가속 | 공유 상태가 없을 때만 병렬화한다 |
| Critic / judge | draft를 공격하고 통합 | 생성자와 검토자를 분리한다 |
| MCP | GitHub·DB·browser 등 연결 | least privilege와 credential 격리가 우선이다 |
| Git/CI | 검증 가능한 종료 조건 | 설명보다 test와 diff를 신뢰한다 |

`draft → critique → refine`은 self-critique의 기본 패턴이다. 다만 judge도 hallucination할 수 있으므로, 최종 gate는 근거 URL, 재현 가능한 test, regression 확인, 사람의 승인으로 둔다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/04-learning/02-deep-dive|Deep Dive]]

## Sources

- https://docs.anthropic.com/en/docs/claude-code/getting-started
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables

## 추가 조사: 역할 분리와 Subagent Orchestration

릴스의 “여러 Claude에게 맡긴다”는 말은 agent 수 자체가 아니라 **독립 workstream을 분리하고 결과 계약(contract)을 고정**하는 것으로 해석해야 한다. Anthropic의 최신 prompting guidance도 병렬 실행·격리된 context·독립 작업일 때만 subagent를 쓰고, 단순 작업·순차 작업·단일 파일 편집에는 직접 수행을 권한다.

| 작업 특성 | 적합한 실행 방식 | 완료 증거(Evidence) |
|---|---|---|
| 서로 독립인 경쟁사·문서 조사 | 병렬 researcher | URL, 발췌 근거, 반증, confidence |
| 같은 코드 경로를 바꾸는 구현 | 단일 implementer 또는 순차 handoff | diff, test, review |
| 서로 다른 관점의 위험 검토 | 병렬 critic | 재현 절차, severity, 영향 범위 |
| 한 파일의 작은 수정 | coordinator가 직접 수행 | focused test 또는 manual check |

```text
coordinator: acceptance criteria와 파일 소유권을 고정
researcher A/B: 서로 다른 source set에서 독립 조사
critic: 누락·모순·반증만 찾기
judge: claim이 아니라 evidence/test를 기준으로 accept | revise | reject
```

- worker에는 role 이름만 주지 말고 `input / output / budget / done / do-not`을 명시한다.
- 병렬 worker가 같은 파일을 수정하면 review·merge 비용이 이득을 상쇄하므로, 조사 결과는 별도 artifact로 모은 뒤 한 agent가 통합한다.
- “세 agent가 같은 결론”은 정확성 증거가 아니다. source 독립성, 인용 품질, 재현 가능한 test를 별도 gate로 둔다.

**실습 과제:** 동일한 공개 API의 제한 사항을 2명의 researcher가 각기 공식 문서와 issue tracker에서 조사하게 하고, critic이 상충 주장만 표로 정리한다. judge가 인용 URL을 열어 확인한 뒤에만 결론을 기록한다.

출처: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
