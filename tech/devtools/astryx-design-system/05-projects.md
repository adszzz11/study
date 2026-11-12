---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — Projects

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/03-references|References]]

## 적용 아이디어

| 프로젝트 | Astryx 적용 | 검증 포인트 |
|---|---|---|
| Internal admin console | Table, filter, form, side panel, role-aware action을 공통 theme으로 조합 | keyboard flow, destructive action 권한, 여러 team의 visual consistency |
| AI-assisted SaaS backoffice | agent가 CLI docs/template을 읽고 CRUD 초안을 생성 | generated UI의 domain rule과 a11y review |
| Multi-brand B2B platform | 하나의 component layer 위에 customer/region theme package 적용 | brand별 token diff, `extends` 유지, upgrade compatibility |
| SSR product dashboard | Next.js/Remix에서 built theme CSS/JS를 deploy | first-paint flash, hydration mismatch, dark-mode 초기화 |
| DS integration package | 조직 고유 component, theme, docs를 package로 배포 | public API, semver, consumer migration |

## Mini project: multi-brand dashboard

1. Neutral 또는 적절한 first-party theme을 base로 선택한다.
2. Brand A/B가 공유하는 layout·behavior는 core component composition으로 유지한다.
3. accent, typography, radius만 각 theme에서 `extends`한다.
4. SSR app에서 `theme build` artifact를 연결하고 light/dark first paint를 capture한다.
5. agent에는 template 생성 전 `component`와 `docs tokens`를 실행하도록 project instruction을 둔다.
6. `doctor`와 custom theme rebuild를 CI/release checklist에 넣는다.

이 실습은 source fork 없이도 product 차이를 흡수할 수 있는지 검증한다. component markup 자체가 장기적으로 달라질 때만 `swizzle`의 유지보수 비용을 계산한다.

## Sources

- https://astryx.atmeta.com/blog/introducing-astryx
- https://astryx.atmeta.com/docs/theme
