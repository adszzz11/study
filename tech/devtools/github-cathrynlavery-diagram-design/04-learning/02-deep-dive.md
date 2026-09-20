---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Agent Skill architecture

```text
User request
   ↓
Skill metadata → SKILL.md
   ↓
intent·audience 분석 → diagram type 선택
   ↓
선택한 type-*.md와 필요한 utility만 로드
   ↓
semantic model + design tokens + layout rules
   ↓
HTML + inline SVG
   ↓ optional
SVG extraction / Playwright PNG rasterization
```

Progressive disclosure의 장점은 context cost를 줄이고 현재 type의 규칙에 attention을 집중하는 것이다. 반대로 `SKILL.md`의 routing이 잘못되면 적절하지 않은 reference를 읽게 되므로 **type selection 자체가 품질의 첫 decision gate**다.

## 2. Semantic model과 layout 분리

Diagram Design의 중요한 경계는 “무엇이 존재하는가”와 “어디에 그릴 것인가”의 분리다.

| 층 | 예시 | 검수 질문 |
|---|---|---|
| Semantic | nodes, edges, groups, cycles, hubs, fields | 핵심 entity와 relation이 보존됐는가? |
| Editorial | audience, emphasis, simplification | 무엇을 생략하고 강조했는가? |
| Visual | coordinate, gap, connector, typography | hierarchy가 시각적으로 명확한가? |
| Delivery | HTML, SVG, PNG, preset | target 환경에서 읽히는가? |

이 분리 때문에 같은 semantic input도 audience와 detail dial에 따라 다른 결과가 될 수 있다.

## 3. Import pipeline

```text
Mermaid / draw.io
    ↓ bounded parser
Intermediate Representation
(nodes, edges, groups, cycles, hubs, fields)
    ↓
Format × Size × Detail × Audience
    ↓
type 선택 + semantic simplification
    ↓
4px-grid 신규 layout
    ↓
HTML/SVG/PNG + fidelity ledger
```

Import는 원본의 pixel, coordinate, palette를 보존하는 converter가 아니다. 원본에서 의미를 추출한 뒤 다시 그리므로, 검수는 시각적 동일성이 아니라 semantic fidelity를 기준으로 해야 한다.

### Output dial

| Dial | 대표 값 | 결정하는 것 |
|---|---|---|
| `format` | `html`, `svg`, `png`, `html+png` | 전달·후처리 방식 |
| `size` | `doc-inline`, `doc-wide`, `slide-16x9`, `social-og`, print preset | canvas와 label scale |
| `detail` | `faithful`, `balanced`, `simplified` | 보존할 semantic detail |
| `audience` | `engineer`, `mixed`, `executive` | terminology와 hierarchy |

### Fidelity ledger

redraw 후 다음을 짧게 기록하면 검토가 쉬워진다.

```text
preserved: services, external PSP, retry path
merged: three internal validation steps → Validation
omitted: field-level payload details
changed: left-to-right sequence → grouped architecture
reason: executive audience, slide-16x9, simplified
```

## 4. Design token contract

website의 raw style을 그대로 복사하지 않고 semantic role로 mapping한다.

```css
:root {
  --paper: ...;
  --paper-2: ...;
  --ink: ...;
  --muted: ...;
  --accent: ...;
  --link: ...;
}
```

- `ink`와 `paper`는 작은 label에서 충분한 contrast를 가져야 한다.
- `accent`는 brand color라는 이유만으로 넓게 칠하지 않는다.
- font를 가져오지 못할 경우 layout shift를 줄일 fallback stack이 필요하다.
- managed update가 수정된 `style-guide.md`를 덮을 수 있으므로 persistent custom skin은 editable clone/fork로 관리한다.

## 5. Accessibility contract

각 SVG는 독립적인 accessible object여야 한다.

```html
<svg role="img" aria-labelledby="payment-title payment-desc">
  <title id="payment-title">Payment request flow</title>
  <desc id="payment-desc">API Gateway에서 PSP까지의 요청과 retry 경로</desc>
  <!-- diagram content -->
</svg>
```

여러 diagram을 한 페이지에 둘 때 ID를 재사용하면 `aria-labelledby`가 잘못 연결될 수 있다. color만으로 상태를 구분하지 말고 label, line style, shape 같은 중복 cue를 둔다.

## 6. Non-determinism 관리

- source prompt, input diagram, agent/model, commit SHA를 함께 기록한다.
- 중요한 결과는 HTML/SVG artifact를 version control에 넣는다.
- regeneration을 update 방식으로 간주하고 visual/semantic review를 수행한다.
- CI가 필요하면 generated artifact의 존재·HTML validity·accessibility attribute를 검사하되 pixel identity를 기본 계약으로 삼지 않는다.

## Sources

- [README — Architecture](https://github.com/cathrynlavery/diagram-design/blob/main/README.md#architecture)
- [SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md)
- [Style guide](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/style-guide.md)
- [Onboarding spec](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/onboarding.md)

