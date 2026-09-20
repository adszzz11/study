---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — Overview

[[tech/devtools/ui-ux-promax/README|학습 진입점]] · 다음: [[tech/devtools/ui-ux-promax/02-ecosystem|Ecosystem]]

## What

UI UX Pro Max는 AI agent를 위한 design-intelligence retrieval layer다. 로컬 CSV knowledge base에서 product type, UI style, color, typography, landing pattern, UX guideline, stack별 지침을 찾아 구조화된 Design System을 생성한다. 핵심 경로에는 별도 design-generation API가 필수가 아니다.

## Why

AI는 component code를 잘 생성해도 제품 맥락에 맞는 정보 hierarchy와 visual tone을 매번 동일하게 선택하기 어렵다. 이 도구는 구현 전에 근거 있는 선택지를 제공하고 anti-pattern과 accessibility check를 함께 반환한다. 따라서 “예쁜 화면 하나”보다 **재현 가능한 제품 결정**을 만드는 데 맞는다.

## 특징

| 특징 | 의미 |
|---|---|
| Local-first | Python 3 script와 CSV data를 project skill path에서 실행 |
| Hybrid retrieval | BM25 ranking과 regex search를 함께 사용 |
| Stack-aware | Next.js, Vue, SwiftUI, Flutter 등 22개 stack 지침 제공 |
| Persistent decisions | `--persist`로 `MASTER.md`에 기준을 저장 |
| QA guardrails | contrast, focus, reduced motion, feedback state 등을 확인 |

```text
Prompt
  → intent / product / surface extraction
  → CSV domain retrieval (BM25 + regex)
  → rule ranking · conflict / anti-pattern filtering
  → Design System (pattern + tokens + type + UX checks)
  → stack-specific component code / persisted MASTER.md
```

## 결과를 읽는 법

- **pattern**: 화면 목적에 맞는 layout·interaction 구조다.
- **colors / typography**: 브랜드를 대체하는 정답이 아니라 color role과 readable type scale의 출발점이다.
- **anti-patterns**: 과도한 gradient, 낮은 contrast, 모호한 affordance처럼 피할 결정을 검토한다.
- **accessibility**: keyboard focus, motion, state feedback을 구현 acceptance criteria로 옮긴다.

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/CLAUDE.md
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/core.py
