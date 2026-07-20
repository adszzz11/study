---
date: 2026-07-20
tags: [tech]
type: tech-tool-study
status: draft
---

# References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Primary Material

| 자료 | 읽을 이유 | 핵심 포인트 |
|---|---|---|
| [발표 영상](https://www.youtube.com/watch?v=WkBPX-oDMnA) | 발표의 framing과 demo 맥락 확인 | code generation보다 understanding이 새 bottleneck이라는 주장 |
| [발표 원문](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html) | 발표 논지를 텍스트로 추적 | verify와 participate의 구분, explainer·quiz·shared space |
| [공개 `/explain-diff` skill](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524) | 실제 artifact 생성 순서 확인 | Background→Intuition→Code→Quiz |
| [Code like a surgeon](https://www.geoffreylitt.com/2025/10/24/code-like-a-surgeon) | autonomy 분배 철학 이해 | 핵심 code/설계와 secondary work의 구분 |
| [AI-generated debugger](https://www.geoffreylitt.com/2024/12/22/making-programming-more-fun-with-an-ai-generated-debugger) | interactive micro-world 사례 | JSON trace를 React UI로 시각화해 infinite loop 탐색 |

## Cognitive and Intent Debt

| 자료 | 핵심 주장 | 적용 시 주의 |
|---|---|---|
| [Storey — Cognitive Debt 논문](https://arxiv.org/abs/2603.22106) | technical·cognitive·intent debt를 구분 | code quality만으로 team understanding을 대리 측정하지 않는다 |
| [Storey — Cognitive Debt 설명](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) | AI-generated change를 적어도 한 인간이 완전히 이해하고 why를 기록할 것을 제안 | “완전히 이해”의 operational definition을 팀이 정해야 한다 |

## Empirical Studies

### Professional Software Developers Don't Vibe, They Control

- URL: https://arxiv.org/abs/2512.14012
- 관찰: 숙련 개발자는 planning, supervision, output validation으로 agent를 통제한다.
- 해석: agent는 복잡한 설계보다 specification이 명확한 task에서 선호된다.
- 적용: autonomy는 model capability 하나가 아니라 task clarity와 reviewability에 맞춘다.

### Code with Me or for Me?

- URL: https://arxiv.org/abs/2507.08149
- 관찰: coding agent는 effort와 incomplete work를 줄일 가능성이 있다.
- 문제: 사용자가 agent behavior를 충분히 이해하기 어려울 수 있다.
- 적용: productivity signal과 comprehension signal을 별도로 측정한다.

### METR Early-2025 RCT와 2026 Update

- [2025 RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/): 익숙한 대형 repository를 다룬 숙련 OSS 개발자가 AI 사용 시 19% 느려졌다는 결과.
- [2026 update](https://metr.org/blog/2026-02-24-uplift-update/): 후속 결과에는 selection bias가 커 최신 도구의 실제 speedup을 확정하기 어렵다고 명시.
- 해석: “AI 사용=항상 speedup” 또는 “항상 slowdown”으로 일반화하지 않는다. task, familiarity, tool generation, review cost를 함께 본다.

### DORA 2025

- URL: https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/
- 관점: AI는 조직 역량의 **amplifier**다.
- 적용: strong engineering practice는 강화되지만 unclear process와 fragile architecture도 증폭될 수 있다.

## Reading Questions

자료를 읽을 때 다음 질문으로 주장과 evidence를 분리한다.

- “understanding”은 recall, explanation, prediction, design participation 중 무엇으로 측정되는가?
- productivity 측정에 review와 correction 시간이 포함되는가?
- 대상 repository와 task는 참가자에게 얼마나 익숙한가?
- agent-generated explanation의 factuality는 어떻게 검증되는가?
- individual comprehension이 team shared understanding으로 전환됐는가?
- artifact가 시간이 지나 code와 drift하지 않게 하는 장치는 무엇인가?

## Sources

- [발표 영상](https://www.youtube.com/watch?v=WkBPX-oDMnA)
- [발표 원문](https://www.geoffreylitt.com/2026/07/02/understanding-is-the-new-bottleneck.html)
- [Storey 논문](https://arxiv.org/abs/2603.22106)
- [Professional Software Developers Don't Vibe, They Control](https://arxiv.org/abs/2512.14012)
- [Code with Me or for Me?](https://arxiv.org/abs/2507.08149)
- [METR 2025 RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [METR 2026 update](https://metr.org/blog/2026-02-24-uplift-update/)
- [DORA 2025](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)

