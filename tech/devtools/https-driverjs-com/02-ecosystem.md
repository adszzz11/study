---
date: 2026-09-07
tags: [tech]
type: tech-tool-study
status: draft
---

# Driver.js Ecosystem과 비교

> [[01-overview|이전: Overview]] · [[README|목차]] · [[03-references|다음: References]]

## 포지션

Driver.js는 product-adoption platform이 아니라 client-side UI library다. code와 release cycle 안에서 tour를 직접 관리하고 작은 bundle과 제어력을 얻는 대신, audience targeting·analytics·content publishing은 application이 책임진다.

## Library 비교

| 선택지 | 강점 | 주의점 | 잘 맞는 상황 |
|---|---|---|---|
| **Driver.js** | 약 5 KB gzip, zero dependency, MIT, tour/highlight/hints, framework-independent | persistence·analytics·orchestration을 직접 구현 | 작은 footprint와 custom behavior가 중요한 application |
| **Shepherd.js** | keyboard navigation, focus trapping, ARIA, framework integration을 전면에 둠 | Driver.js보다 tour framework의 구조가 더 큼 | accessibility 지원과 정교한 step lifecycle을 우선할 때 |
| **Intro.js** | tours와 hints, 단순한 API, 성숙한 생태계 | AGPL이며 commercial use에는 공식 commercial license 검토 필요 | 기존 Intro.js 생태계 또는 상용 지원/라이선스 구매를 선택할 때 |
| **React Joyride** | React component/state model에 자연스럽게 통합 | React 전용이며 다른 stack에는 부적합 | React application에서 declarative integration을 원할 때 |
| **직접 구현** | DOM, design system, a11y를 완전히 통제 | positioning, collision, scroll, cleanup 비용이 큼 | 아주 단순하거나 특수한 UX이고 외부 library를 둘 수 없을 때 |

> Bundle size와 API는 release에 따라 변한다. 표의 수치는 Driver.js 1.8.0 공식 자료 기준이며, 최종 선택 전 각 package의 최신 문서와 license를 다시 확인한다.

## Product-adoption SaaS와 비교

| 역량 | Driver.js | 일반적인 SaaS platform |
|---|---|---|
| UI rendering | 제공 | 제공 |
| Code-level customization | 높음 | platform 범위 안에서 제공 |
| Segmentation | 직접 구현 | 주로 제공 |
| A/B test | 직접 구현 | 주로 제공 |
| Funnel analytics | hook으로 연동 | 주로 내장 |
| Non-developer editor/CMS | 없음 | 주로 제공 |
| Remote content publish | 없음 | 주로 제공 |
| Data/control ownership | application이 소유 | vendor architecture에 의존 |
| 운영 비용 | 개발팀 시간 | 구독료와 vendor governance |

## 선택 질문

1. **누가 content를 바꾸는가?** 개발자만 release와 함께 수정한다면 Driver.js가 단순하다. 운영팀이 수시로 바꿔야 한다면 SaaS가 유리하다.
2. **무엇을 측정해야 하는가?** step view/click 정도면 hook으로 충분할 수 있다. cohort funnel과 experiment가 핵심이면 analytics platform이 낫다.
3. **몇 개의 surface를 연결하는가?** 한 SPA 안의 짧은 tour는 쉽다. 여러 domain/page라면 resume state와 routing protocol이 필요하다.
4. **license 조건은 무엇인가?** Driver.js는 MIT다. 대안의 open-source/commercial 조건은 법무·조직 정책과 함께 검토한다.
5. **접근성 검증 역량이 있는가?** library의 기능 표만 믿지 말고 실제 keyboard, focus, screen reader behavior를 test한다.

## Rule of Thumb

- **Driver.js**: engineering-owned, code-defined onboarding.
- **Shepherd.js**: accessibility와 tour composition을 더 전면에 둔 library 선택.
- **Intro.js**: 기존 생태계 적합성과 license 조건을 수용할 수 있을 때.
- **React Joyride**: React component tree와 declarative state가 우선일 때.
- **SaaS**: growth/product team의 독립 운영, targeting, experiment, analytics가 우선일 때.

## Sources

- https://driverjs.com/
- https://driverjs.com/docs/hints
- https://www.shepherdjs.dev/
- https://introjs.com/
- https://docs.react-joyride.com/
- https://github.com/gilbarbara/react-joyride

