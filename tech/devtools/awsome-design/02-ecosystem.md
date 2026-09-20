---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — Ecosystem 비교

> [[01-overview|이전: Overview]] · [[README|목차로 돌아가기]] · [[03-references|다음: References]]

## 포지션

`awesome-design-md`는 design tool, token standard, component library가 아니라 **visual direction을 탐색하기 위한 reference collection**이다. 실무에서는 공식 `DESIGN.md` spec으로 자체 contract를 작성하고, DTCG나 Tailwind로 export한 뒤, Storybook·visual regression·accessibility test로 구현을 검증하는 흐름에 들어간다.

## 비교표

| 도구/방식 | 핵심 역할 | 실행 가능한 UI code | Design rationale | Agent 친화성 | 적합한 상황 |
|---|---|---:|---:|---:|---|
| **awesome-design-md** | 실제 사이트에서 추출한 `DESIGN.md` reference collection | 아니오 | 높음 | 매우 높음 | 빠르게 visual direction을 선택하고 자체 규칙으로 변형 |
| **Google DESIGN.md spec** | `DESIGN.md` schema, linter, diff, exporter의 표준 기반 | 아니오 | 높음 | 매우 높음 | 조직 자체 design contract 작성·검증 |
| **W3C DTCG tokens** | design token의 vendor-neutral interchange | 아니오 | 낮음 | 중간 | Figma·web·iOS·Android 사이 token source of truth |
| **Figma Variables/Libraries** | 시각 설계, component와 variable 공동 편집 | 일부 code handoff | 중간 | 중간 | designer 중심의 visual authoring과 협업 |
| **Tailwind theme/config** | web 구현에 쓰는 utility와 token mapping | 예 | 낮음 | 높음 | design decision이 끝난 뒤 빠르게 UI 구현 |
| **Storybook** | component catalog, documentation, interaction/visual test | 예 | 중간 | 중간 | 구현된 component 상태와 variant 검증 |
| **Screenshot/prompt only** | 화면 이미지나 자연어로 style 전달 | 아니오 | 낮음 | 중간 | 일회성 prototype, 짧은 visual exploration |

## 서로 대체하지 않는 계층

```text
awesome-design-md reference
          ↓ 선택·비판·변형
project DESIGN.md contract
          ↓ export
DTCG tokens / Tailwind theme
          ↓ implementation
React / CSS / native components
          ↓ verification
Storybook / visual regression / a11y tests
```

| 계층 | 질문 |
|---|---|
| Reference | 어떤 visual direction에서 출발할 것인가? |
| Contract | 우리 제품에서 어떤 규칙과 예외를 지킬 것인가? |
| Interchange | token을 여러 platform과 tool 사이에 어떻게 전달할 것인가? |
| Implementation | 실제 component와 화면을 어떻게 만들 것인가? |
| Verification | 의도대로 보이고 작동하며 접근 가능한가? |

## 선택 가이드

### awesome-design-md가 유리한 경우

- blank canvas보다 구체적인 reference에서 시작해야 한다.
- coding agent에게 일관된 시각 언어와 rationale을 빠르게 제공하고 싶다.
- 여러 브랜드의 spacing, type, elevation, component 규칙을 비교하고 싶다.

### Google DESIGN.md spec을 직접 써야 하는 경우

- 팀의 normative token과 design rationale을 version control해야 한다.
- `lint`, `diff`, `export`를 CI에 넣어 schema와 reference 오류를 잡아야 한다.
- reference를 그대로 쓰지 않고 product 고유의 규칙으로 바꿔야 한다.

### DTCG를 우선할 경우

- 여러 design tool과 web/iOS/Android 사이의 token interchange가 핵심이다.
- narrative보다 vendor-neutral structured data가 source of truth여야 한다.

### Figma/Storybook이 필요한 경우

- designer가 시각적으로 authoring하고 component를 공동 편집해야 한다.
- 구현된 component의 state, interaction, responsive behavior를 실행 환경에서 검증해야 한다.

## Trade-off

| 판단 기준 | 얻는 것 | 지불하는 비용 |
|---|---|---|
| Markdown contract | review와 agent portability | 시각 편집 경험과 즉시 실행성 부족 |
| Inspired reference | 빠른 방향 탐색 | 정확성·공식성·brand/IP 검토 필요 |
| Alpha CLI/spec | lint·diff·export 자동화 | breaking change와 migration 위험 |
| Rich rationale | 일관된 design judgment | 문서 최신성 유지 비용 |

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://github.com/google-labs-code/design.md
- https://www.w3.org/community/design-tokens/
- https://www.figma.com/variables/
- https://storybook.js.org/
- https://tailwindcss.com/docs/theme

