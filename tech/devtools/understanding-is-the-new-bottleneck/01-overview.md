---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — Understanding is the New Bottleneck

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

**Understanding-centered development**는 AI agent가 생성한 결과를 승인하기 위한 review technique만이 아니다. 인간이 system의 concepts, contracts, invariants, trade-offs를 계속 소유해 다음 agent loop의 질문과 설계에 참여하게 하는 개발 방식이다.

| 이해의 목적 | 핵심 질문 | 산출물 |
|---|---|---|
| **Understand to verify** | specification과 일치하는가? bug·security risk가 있는가? | 승인/거절, issue, 수정 요청 |
| **Understand to participate** | 왜 이렇게 구성됐는가? 다음 기능은 어디에 어떻게 붙여야 하는가? | 새 hypothesis, design option, 다음 prompt·plan |

두 번째가 사라지면 인간은 agent output의 최종 승인자일 뿐 system의 공동 설계자가 되지 못한다. Software project는 한 번의 prompt가 아니라 현재 system을 바탕으로 다음 질문을 만드는 연속 loop이기 때문이다.

## Why

AI coding agent는 repository 검색, multi-file edit, test, PR 작성의 throughput을 높인다. 반면 인간의 reading speed와 working memory는 거의 그대로다. 그 결과 다음과 같은 상태가 발생한다.

- test는 green이지만 어느 invariant가 지켜지는지 설명하지 못한다.
- local diff는 그럴듯하지만 cross-file control/data flow를 복원하지 못한다.
- requirement와 rationale이 chat history에만 있고 team artifact로 남지 않는다.
- 다음 기능을 요청할 때 기존 design constraint를 모르므로 prompt의 질이 낮아진다.

### 세 가지 debt

| Debt | 무엇이 뒤처졌는가 | 징후 | 대응 |
|---|---|---|---|
| **Technical debt** | code 구조·품질 | 높은 coupling, 중복, 취약한 test | refactoring, test, architecture 개선 |
| **Cognitive debt** | 사람의 shared understanding | 특정 agent/chat 없이는 change 설명 불가 | explainer, quiz, walkthrough, pairing |
| **Intent debt** | requirement·rationale·decision 기록 | “왜 이렇게 했는가?”에 답할 artifact 없음 | spec, ADR, plan, PR discussion 보존 |

깨끗한 AI-generated code도 팀이 의도와 구조를 모르면 cognitive debt가 높다. 실무 규칙으로는 **AI-generated change마다 최소 한 명의 인간이 무엇과 왜를 설명할 수 있게 한다**가 유용하다.

## Core Features

### 1. Literate diff

일반 diff의 file/line 순서 대신 사람이 이해하기 좋은 순서로 context를 재구성한다.

1. **Background** — 변경 전 component, contract, relevant state
2. **Intuition** — 목표, 핵심 원리, toy example
3. **Code** — dependency와 control/data flow 순서의 walkthrough
4. **Quiz** — causality, invariant, edge case, trade-off 확인

Explainer는 diagram, before/after, concrete data, code snippet을 결합할 수 있지만 raw diff 검토를 대신하지 않는다.

### 2. Quiz as comprehension gate

문서를 읽은 느낌과 실제 설명 능력을 구분한다. “어느 file이 바뀌었나?”보다 다음을 묻는다.

- 입력 X가 들어오면 어떤 state transition을 거쳐 결과 Y가 되는가?
- 반드시 유지되어야 하는 invariant는 무엇인가?
- 실패하는 edge case와 fallback은 무엇인가?
- 선택한 design의 trade-off는 무엇인가?

통과하지 못하면 즉시 merge하기보다 explanation, implementation, test 중 무엇이 불명확한지 되돌아본다. 단, agent가 만든 quiz도 hallucination과 answer-position bias가 있으므로 code·spec·test로 검증한다.

### 3. Interactive micro-world

복잡한 system을 작은 executable explanation으로 만든다. runtime에서 JSON trace를 내보내고 disposable React UI나 local HUD로 다음을 탐색하는 식이다.

- 현재 evaluation rule과 goal
- stack, variable binding, queue, cache state
- 시간축의 state 변화
- solution, failure, infinite loop가 시작되는 지점
- 특정 시점에 연결된 annotation

핵심 product code를 agent에 맡기는 대신, 핵심 code를 인간이 이해하도록 secondary tooling을 위임한다.

### 4. Shared spaces

개인 chat에서 얻은 이해를 team memory로 전환한다.

- technical plan과 rationale을 collaborative document에 기록
- PR에 explainer, diagram, quiz와 근거를 연결
- comment를 code context와 연결
- 신규 팀원이 동일 vocabulary와 mental model을 재구성하도록 보존

### 5. Autonomy slider

| Change 유형 | 권장 autonomy | 필요한 visibility |
|---|---:|---|
| type fix, formatting, mechanical migration | 높음 | test와 concise summary |
| documentation, test 보강 | 중간~높음 | source link, coverage 의도 |
| product behavior, public API | 낮음 | spec, example, human design review |
| security boundary, data model, architecture | 매우 낮음 | threat model/ADR, walkthrough, 강한 gate |

이 접근을 Litt는 **code like a surgeon**이라고 표현한다. 인간은 핵심 창작과 설계를 소유하고 agent에는 context 조사, explainer, debug UI 같은 보조 작업을 위임한다.

## Evidence and Caveats

- 2025년 전문 개발자 연구는 숙련자가 무조건적인 vibe coding보다 planning, supervision, output validation을 사용하며 명세가 분명한 작업을 선호했음을 보고했다.
- agent와 copilot의 controlled study는 effort와 incomplete work 감소 가능성과 함께 agent behavior를 이해하기 어려운 문제를 확인했다.
- METR의 early-2025 RCT에서는 익숙한 대형 repository의 숙련 OSS 개발자가 AI 사용 시 19% 느려졌다. 2026 update는 selection bias 때문에 최신 도구 speedup의 확정적 해석을 경계한다.
- DORA 2025는 AI를 조직 역량의 **amplifier**로 본다. 좋은 practice뿐 아니라 불명확한 process와 취약한 architecture도 증폭될 수 있다.

따라서 결론은 “AI는 항상 빠르다/느리다”가 아니다. **task clarity, repository familiarity, review cost, risk에 따라 autonomy와 comprehension investment를 조절해야 한다.**

## Sources

- [발표 영상](https://www.youtube.com/watch?v=WkBPX-oDMnA)
- [발표 원문](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [Cognitive Debt 논문](https://arxiv.org/abs/2603.22106)
- [Professional Software Developers Don't Vibe, They Control](https://arxiv.org/abs/2512.14012)
- [Code with Me or for Me?](https://arxiv.org/abs/2507.08149)
- [METR 2025 RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [METR 2026 update](https://metr.org/blog/2026-02-24-uplift-update/)
- [DORA 2025](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)
- [Code like a surgeon](https://www.geoffreylitt.com/2025/10/24/code-like-a-surgeon)

