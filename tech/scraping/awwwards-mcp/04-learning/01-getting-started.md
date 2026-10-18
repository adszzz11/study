---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started

## 1. 사전 조건

- Node `22.13+`
- MCP를 지원하는 host (예: Codex)
- 대상 공개 페이지의 이용 정책과 저작권을 준수할 작업 목적

## 2. MCP 등록

```sh
node --version
codex mcp add awwwards -- npx -y awwwards-mcp
```

`npx -y`는 새 release를 가져올 수 있다. team workflow나 재현성 있는 실습에서는 검증한 version을 pinning하고 release note를 기록한다.

## 3. 첫 조사 workflow

1. `search_sites`에 목표를 넣어 3개 안팎의 후보를 찾는다. 예: `dark editorial fintech`.
2. 각 screenshot을 사람이 확인한다. ranking만으로 적합성을 확정하지 않는다.
3. `get_site_details`와 `get_site_elements`로 palette, typography, layout, hero/CTA/footer cue를 메모한다.
4. `create_design_brief`에 선택한 reference slug와 제품 목표를 전달한다.
5. brief에는 재현할 원칙과 **재현하지 않을** asset, copy, brand identifier를 함께 쓴다.

## 4. 좋은 brief의 최소 형태

```text
Goal: B2B fintech landing page
Reference cues: deep neutral background, editorial grid, restrained serif accent
Implement: section rhythm, contrast hierarchy, CTA placement
Do not copy: logo, imagery, copy, proprietary illustrations, exact composition
Validation: compare hero/section band map against local staging URL
```

## Sources

- https://github.com/INSANE0777/Awwwards-mcp
- https://www.npmjs.com/package/awwwards-mcp
