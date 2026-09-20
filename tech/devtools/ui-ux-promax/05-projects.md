---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — Projects

[[tech/devtools/ui-ux-promax/README|학습 진입점]]

## 1. B2B SaaS dashboard

- **목표:** role-based information density와 chart/table/filter/error state를 하나의 Design System으로 고정한다.
- **입력:** user role, 핵심 KPI, desktop/mobile usage, existing brand token, Next.js.
- **완료 조건:** `MASTER.md`, chart 선택 이유, keyboard-accessible filter, loading/empty/error state를 갖춘다.

## 2. Fintech onboarding / checkout

- **목표:** trust-oriented palette와 짧은 form flow를 만든다.
- **입력:** regulation copy, validation timing, one-handed mobile use, React Native 또는 Flutter.
- **완료 조건:** error recovery, visible focus, contrast, confirmation state가 acceptance test에 포함된다.

## 3. E-commerce mobile UI

- **목표:** product detail, cart, checkout surface별 pattern을 생성한다.
- **방법:** 공유 color/type token은 master에 두고, surface별 conversion action만 override한다.
- **완료 조건:** 상품 정보·가격·배송·재고의 hierarchy와 cart state가 작은 화면에서 유지된다.

## 4. Legacy redesign

- **목표:** 기존 token을 보존하면서 accessibility와 responsive layout을 우선 개선한다.
- **주의:** 결과가 기존 brand를 대체하도록 하지 말고, 현재 token을 명시적 constraint로 넣는다.
- **완료 조건:** before/after keyboard path, contrast audit, breakpoint별 reflow를 기록한다.

## 5. Design-system bootstrap

shadcn/ui + Tailwind 프로젝트에서 UI UX Pro Max로 `MASTER.md`를 만들고, Storybook으로 rendered component를 검증한다. session마다 새 style을 발명하는 대신 master 변경을 review해 visual drift를 줄인다.

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/search.py
