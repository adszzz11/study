---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md

> **한 줄 정의**: `awesome-design-md`는 실제 웹사이트의 시각 언어를 AI coding agent가 읽을 수 있는 `DESIGN.md`로 분석·정리한 오픈소스 reference collection이다.

## Overview

- 이 노트에서 **awsome design**은 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)를 뜻한다.
- 이름이 비슷한 [gztchan/awesome-design](https://github.com/gztchan/awesome-design)은 일반 UI/UX 링크 모음이며 이 학습 노트의 대상이 아니다.
- `DESIGN.md`는 design tokens와 Markdown rationale을 결합해 색상·typography·spacing 같은 exact value뿐 아니라 사용 의도와 guardrail도 전달한다.
- collection은 약 73개의 brand-inspired analysis와 각 reference의 `DESIGN.md`, `preview.html`, `preview-dark.html`을 제공한다.
- 공식 Google `DESIGN.md` specification과 CLI는 collection을 작성·검증·변환할 때 함께 사용할 수 있지만, 현재 format은 `alpha`이므로 version pinning과 migration 검토가 필요하다.

```text
Public website/CSS 관찰
        ↓
YAML design tokens + Markdown rationale
        ↓
DESIGN.md ── lint / diff / export
        ↓
AI coding agent
        ↓
React·CSS·Tailwind·native UI 구현
        ↓
preview / Storybook / visual·a11y test
```

## Learning Path

- [ ] [[01-overview|1. Overview]] — What/Why, 문서 구조와 핵심 특징
- [ ] [[02-ecosystem|2. Ecosystem]] — Google spec, DTCG, Figma, Storybook과 비교
- [ ] [[03-references|3. References]] — 공식 자료와 reference collection 탐색
- [ ] [[04-learning/01-getting-started|4. Getting Started]] — reference 선택, 자체 `DESIGN.md` 작성, CLI 검증
- [ ] [[04-learning/02-deep-dive|5. Deep Dive]] — token architecture, CI, security, accessibility
- [ ] [[05-projects|6. Projects]] — 실전 적용 과제
- [ ] [[cheatsheet|7. Cheatsheet]] — format과 명령 빠른 참조

## When To Use

- AI coding agent에게 매 prompt마다 반복하지 않을 persistent visual context가 필요할 때
- 기존 웹사이트에서 빠르게 visual direction을 선택한 뒤 자체 product 규칙으로 변형할 때
- design tokens와 “왜 이렇게 쓰는가”라는 design rationale을 하나의 version-controlled 문서에서 관리할 때
- React, CSS, Tailwind, native UI 등 여러 구현 대상에 공통 design contract를 제공할 때
- token 변경을 Git diff, review, lint, export pipeline으로 관리하고 싶을 때

## When Not To Use

- 완성된 UI component code나 즉시 적용되는 theme package가 필요할 때
- user research, information architecture, interaction design 결정을 대신할 도구를 찾을 때
- 특정 브랜드를 그대로 복제하거나 상표·proprietary font·사진의 사용 권한까지 얻었다고 가정할 때
- keyboard navigation, focus management, semantics, reduced motion을 contrast lint 하나로 검증하려 할 때
- `alpha` schema 변경을 감당할 version pinning·migration 전략이 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/codex/README|Codex tool-study]] — `DESIGN.md`를 구현 context로 소비하는 coding agent
- [[tech/devtools/ripgrep/README|ripgrep tool-study]] — 외부 reference와 repository 규칙을 검토할 때 유용한 검색 도구

## Sources

- https://github.com/VoltAgent/awesome-design-md
- https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/vercel/DESIGN.md
- https://github.com/google-labs-code/design.md
- https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/
- https://www.w3.org/community/design-tokens/
- https://github.com/gztchan/awesome-design

