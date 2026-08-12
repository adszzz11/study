---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 포지션

Diagram Design은 renderer 위의 **agent-directed editorial layer**다. Mermaid·D2가 문법과 deterministic rendering을 제공하고, draw.io·Figma가 직접 편집 환경을 제공한다면, Diagram Design은 audience·brand·density를 해석해 새로운 HTML/SVG composition을 만드는 데 집중한다.

## 비교

| 도구 | 핵심 모델 | 재현성 | Brand/editorial 제어 | 적합한 상황 |
|---|---|---:|---:|---|
| Diagram Design | LLM Agent Skill + reference + template | 낮음~중간 | 높음, opinionated | 발표·문서용 맞춤형 editorial diagram |
| Mermaid | text DSL + renderer | 높음 | theme 범위 내 중간 | Markdown 문서, version-controlled diagram |
| D2 | declarative DSL + layout engine | 높음 | 중간~높음 | text-first architecture diagram과 자동 layout |
| draw.io | GUI canvas + XML model | 수동 편집 기준 높음 | 높음 | 세밀한 enterprise diagram, handoff |
| Figma | collaborative visual editor | 수동 편집 기준 높음 | 매우 높음 | pixel-level design, design system 협업 |
| 직접 SVG/HTML | code-native graphics | 구현에 따라 높음 | 매우 높음 | 완전한 제어와 유지보수 비용을 감수할 때 |

## Mermaid와 함께 쓰기

둘은 대체재라기보다 서로 다른 단계를 맡을 수 있다.

```text
Mermaid source
  ├─ 그대로 render → 변경 추적·재현성이 중요한 문서
  └─ semantic import → Diagram Design redraw → 발표·외부 공유용 결과
```

Diagram Design의 import는 Mermaid를 pixel-level로 변환하지 않는다. node, edge, group, cycle, hub 같은 의미 구조를 intermediate representation으로 추출한 뒤 새 layout을 만든다. 따라서 source fidelity보다 communication quality가 우선이다.

## draw.io와 함께 쓰기

draw.io는 사람이 coordinate와 style을 직접 관리하기 좋다. Diagram Design은 기존 draw.io에서 semantic content를 가져와 audience와 output size에 맞게 재편하는 데 유리하다.

- 원본 coordinate·palette 보존이 중요하면 draw.io를 유지한다.
- executive slide를 위해 복잡도를 줄여야 하면 redraw를 고려한다.
- 결과를 다시 draw.io에서 완전하게 round-trip해야 한다면 Diagram Design을 피한다.

## Figma와의 경계

Diagram Design은 초안과 일관된 방향 설정을 빠르게 만들지만, 자유로운 visual system이나 pixel-perfect collaboration에서는 Figma가 더 적합하다. 실무에서는 agent가 semantic composition을 만들고 designer가 최종 brand review를 수행하는 조합이 현실적이다.

## 선택 질문

| 질문 | Yes라면 |
|---|---|
| source와 결과가 항상 같아야 하는가? | Mermaid 또는 D2 |
| 원본 coordinate를 보존해야 하는가? | draw.io |
| pixel-level 공동 편집이 핵심인가? | Figma |
| audience별로 내용과 hierarchy를 다시 편집해야 하는가? | Diagram Design |
| build step 없는 독립 HTML/SVG가 필요한가? | Diagram Design 또는 직접 SVG/HTML |

## Sources

- [Diagram Design README](https://github.com/cathrynlavery/diagram-design/blob/main/README.md)
- [Mermaid](https://mermaid.js.org/)
- [D2](https://d2lang.com/)
- [draw.io](https://www.drawio.com/)
- [Figma](https://www.figma.com/)

