---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Understanding is the New Bottleneck

> **한 줄 정의**: AI agent가 만든 code를 인간이 검증하는 데 그치지 않고 다음 설계에 능동적으로 참여할 수 있도록 explanation·quiz·interactive micro-world·shared workspace로 mental model을 유지하는 개발 방법론이다.

## Overview

AI coding agent는 code generation, test 실행, PR 생성을 빠르게 하지만 인간과 팀의 이해 속도를 같은 비율로 높여 주지는 않는다. Geoffrey Litt의 AI Engineer World's Fair 2026 발표는 이 간극을 **understanding bottleneck**으로 정의한다.

핵심은 단순히 “이 변경이 안전한가?”를 확인하는 **understand to verify**를 넘어, “다음에는 무엇을 만들고 어떤 방향으로 설계할 것인가?”에 답할 수 있는 **understand to participate**를 유지하는 것이다.

```text
Spec·Intent + Repository + Diff + Tests + Runtime trace
                         │
                         ▼
                  Context reconstruction
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
     Literate explainer  Quiz     Interactive micro-world
            │            │            │
            └────────────┼────────────┘
                         ▼
              Human mental-model check
                         │
                         ▼
          Shared plan / PR discussion / next loop
```

이 study는 단일 tool 사용법보다 위 pipeline을 실제 팀 workflow에 적용하는 법을 다룬다. 시작은 [[01-overview|개요]], 빠른 적용은 [[04-learning/01-getting-started|Getting Started]], 운영 설계는 [[04-learning/02-deep-dive|Deep Dive]]에서 확인한다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, cognitive debt, 핵심 특징 이해
- [ ] [[02-ecosystem|Ecosystem]] — diff review, documentation, debugger 등 대안 비교
- [ ] [[03-references|References]] — 발표·연구·사례의 주장과 한계 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — 작은 PR에 explainer와 quiz 적용
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — causality·invariant 중심 gate와 autonomy 설계
- [ ] [[05-projects|Projects]] — 팀에 단계적으로 도입하는 실전 과제
- [ ] [[cheatsheet|Cheatsheet]] — review 직전 checklist 빠른 참조

## When To Use

- AI agent가 여러 file과 subsystem을 가로지르는 change를 생성했을 때
- build와 test는 통과하지만 reviewer가 변경의 causality와 blast radius를 설명하기 어려울 때
- public API, data model, security boundary, architecture처럼 다음 설계에 장기 영향을 주는 결정을 검토할 때
- 반복되는 onboarding 질문을 shared mental model과 vocabulary로 남기고 싶을 때
- runtime trace가 복잡해 terminal log만으로 state transition을 이해하기 어려울 때

## When Not To Use

- typo, formatting, 명백한 one-line mechanical change처럼 설명 비용이 변경 위험보다 큰 경우
- explainer나 quiz를 raw diff, test, specification 검토의 대체물로 쓰려는 경우
- secret·PII·proprietary code를 안전한 통제 없이 외부 model 또는 shared artifact에 노출해야 하는 경우
- 긴 문서를 생성하는 행위 자체를 이해의 증거로 취급하는 경우
- incident 대응 중 즉시 rollback이 우선인 순간—복구 후 retrospective에서 mental model을 보완한다

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/codex]] — coding agent와 human review workflow
- [[tech/ai/agent-orchestration]] — agent autonomy와 orchestration 설계
- [[tech/devtools/git]] — diff, commit, PR 단위의 변경 추적

## Sources

- [발표 영상 — Understanding is the new bottleneck](https://www.youtube.com/watch?v=WkBPX-oDMnA)
- [Geoffrey Litt — 발표 원문](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
- [Margaret-Anne Storey — Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
- [Storey — Cognitive Debt 논문](https://arxiv.org/abs/2603.22106)
- [DORA 2025 State of AI-assisted Software Development](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)

