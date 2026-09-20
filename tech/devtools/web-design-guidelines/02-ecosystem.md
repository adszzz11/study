---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem and Comparison

| 체계/도구 | 강점 | 적합한 상황 | 유의점 |
|---|---|---|---|
| W3C WCAG 2.2 | 국제 표준, 테스트 가능한 Success Criteria | 접근성 기준·공공·금융·enterprise | checklist 통과만으로 좋은 UX가 되지는 않음 |
| GOV.UK Design System | content-first, 명확한 form·a11y 사례 | 서비스 UI, form-heavy 제품 | GOV.UK 브랜드 규칙을 그대로 이식하지 않음 |
| Material Design 3 | token/component 중심, Android·web 친화 | 빠른 system 구축, Google/Android 성격 | 고유한 정보 구조와 브랜드를 희생하지 않음 |
| Apple HIG | 명확성, 일관성, platform 친화성 | Apple ecosystem, native-like UX | iOS 관례가 웹 표준을 대체하지 않음 |
| Tailwind CSS | token화와 구현 속도, 낮은 추상화 | bespoke UI 빠른 구현 | utility 누적으로 semantic·component API가 흐려질 수 있음 |
| Bootstrap | scaffold와 기본 component | admin, 내부 도구, 초기 MVP | 기본 외형 의존은 차별성·성능 비용으로 이어질 수 있음 |
| Storybook + axe/Lighthouse | component 문서화와 회귀 감지 | Design System 운영 | 자동 검사는 manual usability test를 대체하지 않음 |

## 선택 기준

1. **기준선**은 WCAG와 HTML 표준으로 둔다.
2. **재사용 체계**는 제품의 content model과 team workflow에 맞춰 정한다.
3. **구현 도구**는 semantics를 보존하고 실제 performance budget을 충족하는지로 평가한다.
4. **검증 체계**는 lint/axe/Lighthouse와 keyboard·Screen Reader·사용자 task test를 조합한다.

Material 3 Expressive처럼 표현성을 높이는 흐름도 핵심 task의 명료성, 접근성, 사용자 연구 검증을 전제로 한다.

## Sources

- https://design.google/library/expressive-material-design-google-research
- https://design-system.service.gov.uk/styles/layout/
- https://developer.apple.com/design/human-interface-guidelines/
- https://www.w3.org/TR/WCAG22/
