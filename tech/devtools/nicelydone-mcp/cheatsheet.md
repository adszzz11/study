---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Nicelydone MCP Cheatsheet

## Mental model

```text
Reference retrieval ≠ UI copying
metadata search → comparison → design brief → original implementation → QA
```

## Query formula

```text
[product context]의 [page / flow / component]에서
[interaction]과 [state] 사례를 N개 찾고,
[comparison criteria] 기준으로 관찰과 해석을 분리해 표로 요약해줘.
원본 copy·branding·asset은 인용하거나 재현하지 마.
```

## Prompt examples

```text
B2B analytics SaaS의 data table + multi-filter + empty state 사례를 8개 찾아줘.
information density, clear-all, recovery CTA, keyboard path를 비교해줘.
```

```text
team invite onboarding flow 5개를 비교해줘.
progress indicator, skip policy, email verification, resume path를 표로 만들고
우리 제품의 SSO 제약을 고려한 brief 초안을 제안해줘.
```

```text
선택한 reference들의 pattern을 그대로 복제하지 말고,
우리 design system의 Button, Dialog, DataTable 규칙에 맞는 original React 구현 계획을 작성해줘.
empty/loading/error/permission state와 focus management를 포함해줘.
```

## Before code

- [ ] account 페이지에서 실제 MCP config를 복사했다.
- [ ] 조사 질문에 context, object, interaction, state가 있다.
- [ ] 관찰한 사실과 팀의 해석을 분리했다.
- [ ] 채택할 구조 / 피할 요소 / 제품 제약을 brief로 썼다.

## Before merge

- [ ] responsive state와 overflow를 확인했다.
- [ ] empty, loading, error, permission state를 검토했다.
- [ ] keyboard navigation, visible focus, contrast, status announcement를 확인했다.
- [ ] reference의 copy, logo, asset, 고유 composition을 복제하지 않았다.
- [ ] 가격, quota, endpoint, client support처럼 변하는 정보는 공식 페이지에서 재확인했다.

## Fast facts

| 항목 | 내용 |
| --- | --- |
| Integration | remote MCP server + SaaS UI reference database + AI client integration |
| Retrieval unit | screen, user flow, UI component, app |
| Best use | 실제 product pattern에 근거한 design research |
| Avoid | visual cloning 또는 내부 design system을 우회하는 결정 |
| Config | 로그인한 [MCP 페이지](https://nicelydone.club/mcp)의 client별 값을 사용 |

## Sources

- [Nicelydone MCP](https://nicelydone.club/mcp)
- [Nicelydone UI library](https://nicelydone.club/)
- [Nicelydone Pricing](https://nicelydone.club/pricing)
