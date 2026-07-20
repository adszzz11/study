---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 이해를 돕는 접근 비교

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## Positioning

Litt의 접근은 code review, documentation, observability 중 하나를 대체하는 단일 product가 아니다. agent가 만든 change에서 context를 재구성하고 인간의 mental model을 확인한 뒤 team artifact로 보존하는 **comprehension layer**다.

## 비교

| 접근/도구 | 주목적 | 강점 | 한계 | 권장 위치 |
|---|---|---|---|---|
| **Litt `/explain-diff`** | comprehension·participation | Background→Intuition→Code→Quiz로 mental model 형성 | 설명 hallucination, quiz 품질 편차, 별도 자동화 필요 | PR 작성 직후, human review 이전 |
| **Raw diff / GitHub PR review** | 정확한 line-level change 검토 | source of truth에 가깝고 comment·approval workflow가 성숙 | file 순서라 execution flow와 intent 복원이 어려움 | explainer 후 반드시 수행하는 최종 검토 |
| **Agent summary / chat** | 빠른 변경 요약과 Q&A | 저비용, follow-up 질문이 쉬움 | session에 갇히고 근거 누락·과신 가능 | initial orientation, explainer 초안 |
| **ADR / technical plan** | architectural intent와 rationale 보존 | intent debt 감소, 장기 decision history | runtime behavior나 실제 diff와 drift 가능 | 구현 전·중, high-risk decision |
| **Static diagram / code map** | component와 dependency 시각화 | onboarding과 전체 구조 파악에 유리 | 시간에 따른 state와 edge case 표현이 약함 | Background, architecture review |
| **Test suite / CI** | executable behavior 검증 | regression gate, 반복 가능, objective signal | 왜 설계했는지와 인간 이해를 보장하지 않음 | 구현 중·merge gate |
| **Debugger / tracing / observability** | runtime state와 causality 조사 | 실제 execution evidence, production 문제 분석 | setup 비용, 정보량 과다, intent 설명 부족 | 의심 경로와 failure 조사 |
| **Interactive micro-world** | executable explanation·탐색 | state transition과 edge case를 직접 조작 | 일회성 UI 비용, model이 잘못 표현할 위험 | 복잡한 algorithm·protocol·state machine |
| **Pair/mob programming** | shared real-time understanding | 질문·설계 맥락·tacit knowledge 공유 | 시간 동기화와 인력 비용 | 핵심 architecture, 고위험 change |
| **Code ownership / mandatory reviewer** | 책임과 domain review 보장 | 최소 한 명의 human owner를 명확히 함 | 승인만 형식화되면 comprehension 보장 실패 | team governance |

## 상호 보완 관계

```text
ADR / Spec ── intent의 기준
      │
      ▼
Agent change ──► Explainer ──► Quiz ──► Raw diff review ──► CI / Merge
                    │             │              │
                    └──── 근거: code · tests · runtime trace ────┘
                                      │
                                      ▼
                           Shared plan / PR / onboarding
```

핵심 원칙은 **설명 artifact와 verification evidence를 분리하면서 연결하는 것**이다.

- Explainer는 이해 순서를 최적화한다.
- Raw diff는 실제 변경을 확인한다.
- Test/trace는 behavior evidence를 제공한다.
- ADR/spec은 intent의 기준을 제공한다.
- Quiz는 reviewer의 mental model을 sampling한다.

## 선택 가이드

| 상황 | 최소 조합 | 추가할 것 |
|---|---|---|
| 작은 mechanical change | agent summary + diff + CI | 위험이 발견되면 explainer |
| multi-file feature | spec + explainer + quiz + diff + CI | diagram, walkthrough |
| state machine / interpreter | explainer + runtime trace | interactive micro-world |
| public API / data model | spec/ADR + low autonomy + human design review | migration simulation, consumer examples |
| security boundary | threat model + expert review + tests | trace, adversarial cases; quiz만으로 gate 금지 |
| onboarding | curated explainer + diagram + guided task | quiz와 pair session |

## 도입 판단 기준

다음 값이 클수록 comprehension artifact에 더 투자한다.

```text
Comprehension investment
  ∝ change complexity
  × blast radius
  × decision lifetime
  × repository unfamiliarity
  × cost of misunderstanding
```

반대로 predictable하고 reversible한 mechanical task에는 짧은 summary와 test로 충분할 수 있다. 모든 PR에 긴 설명과 quiz를 강제하면 cognitive debt를 줄이기보다 ceremony debt를 만든다.

## Sources

- [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524)
- [Understanding is the new bottleneck](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [AI-generated debugger 사례](https://www.geoffreylitt.com/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger)
- [Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
- [DORA 2025](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)

