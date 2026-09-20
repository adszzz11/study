---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — Cheatsheet

> [[05-projects|이전: Projects]] · [[README|목차]]

## Core Model

```text
Styles (visual direction)
  → Screens (single pattern)
    → Flows (multi-step journey)
      → reference lock
        → implementation + visual QA
```

## Access

| 항목 | 값/원칙 |
|---|---|
| Endpoint | `https://api.refero.design/mcp` |
| Authentication | 최초 연결 시 browser OAuth |
| Access mode | official MCP는 read-only |
| Live corpus | Refero paid plan 필요 |
| Tool names | 공개 docs가 아니라 실제 client discovery를 기준으로 확인 |

```bash
codex plugin marketplace add referodesign/refero_skill
codex plugin add refero@refero
```

## Brief Template

```yaml
screen: 
user: 
platform: 
primary_goal: 
brand_constraints: 
research_layers: [styles, screens, flows]
```

## Reference Lock

```md
- References: 2–3
- Keep: hierarchy / density / CTA / recovery traits
- Exclude: copied branding / irrelevant visual novelty
- Tokens: semantic roles, not raw values
- States: happy path + loading + empty + error + completion
```

## QA Checklist

- [ ] desktop와 mobile screenshot을 비교했다.
- [ ] typography, density, spacing, color role, imagery를 확인했다.
- [ ] empty, loading, error, completion state를 확인했다.
- [ ] keyboard, focus, contrast, semantic label을 별도 검사했다.
- [ ] 자사 brand token과 component에 맞게 재해석했다.

## Avoid

- 단일 product UI를 그대로 copy하기
- corpus count를 coverage/quality의 보증으로 읽기
- documentation의 tool name을 automation에 hard-code하기
- read-only research MCP에 write 권한을 기대하기
- screenshot QA를 accessibility 검증으로 오해하기

## Sources

- https://refero.design/mcp
- https://github.com/referodesign/refero_skill
- https://github.com/referodesign/refero_skill/blob/master/.mcp.json
