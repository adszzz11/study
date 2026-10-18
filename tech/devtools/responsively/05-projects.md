---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively — Projects

[[tech/devtools/responsively/README|학습 진입점]]

## 1. Design-system QA

Storybook 또는 component route를 열고 navigation, card grid, dialog의 target device suite screenshot set을 만든다.

- 각 component에 default, long text, error, disabled state를 준비한다.
- suite별 screenshot을 비교하고 발견한 issue에 viewport 폭을 기록한다.
- 반복되는 결함은 component contract 또는 visual regression test로 옮긴다.

## 2. Checkout / 가입 flow 검증

Mirrored text input으로 login, coupon, address 입력을 여러 viewport에서 한 번에 확인한다.

| 확인할 것 | 예시 |
|---|---|
| 입력 오류 | 이메일 형식 오류, 쿠폰 만료, 주소 누락 |
| 화면 크기 | 320px에서 CTA·error가 함께 보이는지 |
| 상태 전이 | loading, success, server error 때 layout shift |
| 최종 검증 | mobile keyboard와 real-device 차이 |

Mobile keyboard와 실제 browser chrome은 preview만으로 확정하지 않고 실기기 테스트로 보완한다.

## 3. PR visual review

변경 화면을 target suite에서 캡처해 PR에 첨부한다. reviewer는 "어떤 viewport와 state를 봤는가"를 알 수 있고, 발견한 breakpoint는 Playwright visual regression test로 승격할 수 있다.

```text
PR checklist
- [ ] 375 / 768 / 1440 screenshot 첨부
- [ ] long text 및 error state 확인
- [ ] 발견한 issue의 재현 폭 기록
- [ ] CI test로 옮길 후보 표시
```

## 4. AI-assisted frontend loop

Agent가 코드 변경 후 Responsively MCP로 local URL을 열고 screenshot·DOM text를 검사하게 한다. overflow, hidden CTA, clipped modal처럼 명시 가능한 조건을 task에 적고, agent의 screenshot 결과는 사람이 검토한다. credentials나 민감한 production data는 local visual verification에 넣지 않는다.

## Sources

- [Responsively App guide](https://responsively.app/blog/responsively-app-guide)
- [Responsively App GitHub repository](https://github.com/responsively-org/responsively-app)
- [Playwright emulation](https://playwright.dev/docs/next/emulation)
- [BrowserStack Responsive Testing](https://www.browserstack.com/docs/testing-toolkit/responsive-testing)
