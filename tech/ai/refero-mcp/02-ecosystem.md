---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — Ecosystem

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## Comparison

| 도구 | 강점/출발점 | Refero 대비 적합한 경우 | 주의점 |
|---|---|---|---|
| **Refero MCP** | 검색 가능한 real product screen·flow corpus | pattern discovery부터 필요할 때 | Pro와 OAuth 기반 live access 필요 |
| **Fudge** | 확보한 website의 typography, spacing, DOM/visual detail 관찰 | 특정 reference를 정밀 분석해 구현으로 옮길 때 | 대규모 product-flow discovery가 중심은 아님 |
| **Figma MCP** | 조직 내부 Figma design system·frame | 승인된 자사 디자인을 정확히 구현할 때 | 외부 benchmark discovery의 대체재는 아님 |
| **Mobbin / Pttrns / SaaSFrame** | 사람이 browser에서 inspiration 탐색 | 사람이 직접 browsing·curation할 때 | MCP-native context injection은 약하거나 별도 구성 필요 |
| **`fidgetcoding/refero-design-mcp`** | `styles.refero.design` local cache와 semantic/keyword search | local catalog mirror나 `DESIGN.md` 생성이 필요할 때 | 공식 hosted MCP가 아닌 제3자 project; optional write와 OpenAI key 설정 존재 |

## Complementary Workflow

Refero와 Fudge는 단순한 대체재가 아니다. 다음 순서가 자연스럽다.

```text
Refero: 후보 pattern/flow 발견
  → Fudge: 선택한 page의 DOM·spacing·typography 정밀 관찰
    → 자사 design system: brand token과 accessibility 기준으로 재해석
```

Figma MCP는 마지막 단계의 “승인된 내부 source를 구현에 정확히 반영”하는 역할에 가깝다. 외부 사례는 proof가 아니라 입력 재료다. 한 제품을 그대로 copy하지 않고, 여러 reference에서 목적에 맞는 trait만 합성한다.

## Selection Questions

1. 모르는 pattern을 넓게 찾아야 하는가? → Refero MCP
2. 이미 선택한 URL의 구조를 정확히 읽어야 하는가? → Fudge
3. 내부 component와 frame이 truth인가? → Figma MCP
4. agent보다 designer의 수동 curation이 중심인가? → gallery
5. local index, optional file write가 필요한가? → community MCP를 별도 security review 후 검토

## Sources

- https://refero.design/mcp
- https://design.withfudge.com/share/refero-design-mcp
- https://github.com/fidgetcoding/refero-design-mcp
