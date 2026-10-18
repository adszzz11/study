---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Responsively — Cheatsheet

[[tech/devtools/responsively/README|학습 진입점]]

## 빠른 점검 순서

```text
local URL 열기
→ suite 선택 (375 / 768 / 1440부터)
→ header·form·modal 한 번 조작
→ long text·error state 추가
→ portrait/landscape 확인
→ screenshot 캡처
→ 재현 breakpoint를 CI test로 승격
```

## 자주 쓰는 기능

| 필요 | 기능 |
|---|---|
| 여러 폭을 동시에 보기 | Multi-viewport preview |
| 같은 입력을 반복하지 않기 | Mirrored interaction |
| 표준 폭 조합 재사용 | Preview Suite / custom device |
| layout 차이 추적 | Unified Inspector, ruler·guide |
| PR 증적 남기기 | viewport/full-page screenshot |
| 방향 차이 확인 | device rotation |
| design과 겹쳐 보기 | mockup overlay |
| agent 시각 검증 | localhost MCP endpoint |

## breakpoint 기본 집합

| 폭 | 확인 목적 |
|---:|---|
| 320px | 작은 mobile의 wrapping·CTA |
| 375px | 일반 mobile layout |
| 768px | tablet 전환점 |
| 1024px | desktop 전환점 |
| 1440px | 넓은 desktop의 container·여백 |

실제 breakpoint 값은 제품의 CSS와 design token을 우선한다.

## MCP task template

```text
{local URL}에서 {375, 768, 1440} viewport를 활성화한다.
{state}를 재현하고 screenshot을 촬영한다.
horizontal overflow, hidden CTA, clipped modal, text truncation을 보고한다.
```

## 기억할 한계

- Chromium preview 통과는 iOS Safari·Android 실기기 통과를 뜻하지 않는다.
- visual preview는 CI regression test를 대체하지 않는다.
- MCP 연결 전 localhost 접근 범위와 최신 tool schema를 확인한다.

## Sources

- [Responsively App](https://responsively.app/)
- [Responsively App GitHub repository](https://github.com/responsively-org/responsively-app)
- [Chrome Device Mode limitations](https://developer.chrome.google.cn/docs/devtools/device-mode?hl=en)
