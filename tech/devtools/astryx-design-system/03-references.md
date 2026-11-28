---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — References

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/cheatsheet|Cheatsheet]]

## 공식 source

| 용도 | URL |
|---|---|
| repository 및 source | https://github.com/meta/astryx |
| 공개 배경 | https://astryx.atmeta.com/blog/introducing-astryx |
| theme 문서 | https://astryx.atmeta.com/docs/theme |
| core package/version | https://www.npmjs.com/package/@astryxdesign/core |
| CLI package/version | https://www.npmjs.com/package/@astryxdesign/cli |
| CLI README | https://github.com/meta/astryx/blob/main/packages/cli/README.md |
| release·engineering updates | https://astryx.atmeta.com/blog |

## 주변 기술과 비교 source

- StyleX at scale: https://engineering.fb.com/2025/11/11/web/stylex-a-styling-library-for-css-at-scale/
- shadcn/ui: https://ui.shadcn.com/docs/official
- MUI: https://mui.com/material-ui/getting-started/
- Radix Primitives: https://www.radix-ui.com/primitives/docs/overview/introduction

## 검증 체크

- version, React peer dependency, breaking change는 npm과 repository release/CHANGELOG를 함께 확인한다.
- CLI option 및 JSON output은 설치된 버전에서 `--help`와 command 실행으로 확인한다.
- theme runtime injection과 `theme build` artifact의 SSR 차이는 theme 문서 및 실제 framework build로 검증한다.

## Sources

- https://github.com/meta/astryx
- https://github.com/meta/astryx/blob/main/packages/cli/README.md
