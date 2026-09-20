---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code

> **한 줄 정의**: Multimodal LLM이 UI 이미지에서 text·layout·component·style·asset을 추론하고, 실행 가능한 frontend code를 생성한 뒤 rendering feedback으로 반복 보정하는 기술이다.

## Overview

이 노트에서 **image to code**는 일반 OCR이 아니라 screenshot·wireframe·Figma frame 같은 UI 이미지를 HTML/CSS/React 등으로 재구현하는 **Screenshot-to-Code / Design-to-Code** 영역을 뜻한다.

```text
Image(s)
  → visual/OCR analysis
  → layout·component·asset representation
  → framework-aware code generation
  → sandbox build & browser render
  → screenshot/DOM/interaction comparison
  → targeted patch
  → QA & human review
```

핵심 목표는 원본 source code를 그대로 복원하는 것이 아니다. 같은 화면을 Flexbox, Grid, SVG 등 여러 방식으로 구현할 수 있고, 정적 이미지에는 behavior·responsive rule·semantics·backend contract가 없기 때문이다. 실무 목표는 **시각적으로 충실하면서 유지보수 가능한 재구현**이다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why와 핵심 architecture 이해
- [ ] [[02-ecosystem|Ecosystem]] — tool·research approach·수동 구현 비교
- [ ] [[03-references|References]] — 논문, repository, 표준 원문 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — 한 화면을 baseline으로 재구현
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — IR, visual diff, localized repair, 다차원 QA 설계
- [ ] [[05-projects|Projects]] — 난이도별 실전 프로젝트 수행
- [ ] [[cheatsheet|Cheatsheet]] — prompt, metric, checklist 빠른 참조

## When To Use

- 디자인→개발 handoff 시간을 줄일 때
- screenshot·wireframe으로 빠른 prototype을 만들 때
- 권한이 있는 기존 UI를 migration 또는 recreation할 때
- 기존 design system 기반 component scaffold가 필요할 때
- visual regression test용 fixture·mock을 만들 때
- 디자이너와 개발자가 conversational iteration을 수행할 때

## When Not To Use

- 타사 UI·logo·font·image를 복제할 권한이 확인되지 않았을 때
- screenshot만으로 production behavior, API, authentication까지 정확히 복원해야 할 때
- pixel similarity만 통과하면 accessibility·semantics·maintainability도 보장된다고 가정할 때
- 원본 design file, component library, source code가 있는데도 이를 버리고 image만 사용할 때
- 결제·의료·보안처럼 interaction 오류의 영향이 큰 화면을 human review 없이 배포할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/ai-ecosystem/01-overview|AI Ecosystem]]
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]]

## Sources

- Design2Code, NAACL 2025: https://aclanthology.org/2025.naacl-long.199/
- screenshot-to-code repository: https://github.com/abi/screenshot-to-code
- Widget2Code: https://github.com/Djanghao/widget2code
- DesignBench: https://arxiv.org/abs/2506.06251
- 1D-Bench: https://arxiv.org/abs/2602.18548
- VisRefiner: https://arxiv.org/abs/2602.05998
- UI2App: https://arxiv.org/abs/2607.06306
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Google Stitch 소개: https://developers.googleblog.com/stitch-a-new-way-to-design-uis/
- Figma Make 안내: https://help.figma.com/hc/en-us/articles/31304485164695-Create-a-Figma-Make-file

