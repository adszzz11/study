---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — Cheatsheet

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/03-references|References]]

## Install

```bash
npm install @astryxdesign/core @astryxdesign/theme-neutral @stylexjs/stylex
npm install -D @astryxdesign/cli
npx @astryxdesign/cli init
```

## CLI workflow

| 목적 | Command | 운영 메모 |
|---|---|---|
| component 목록 | `component --list` | 설치된 버전의 surface부터 확인 |
| component API | `component Button` | agent도 추측 전 실행 |
| 검색 | `search "form validation"` | docs의 semantic entry point |
| token 문서 | `docs tokens` | theme edit 전 current token 확인 |
| theme 추가 | `theme add neutral` | base package theme 선택 |
| SSR artifact | `theme build` | CSS/ESM/types 생성 후 app에 연결 |
| skeleton | `template dashboard --skeleton` | composition 초안으로 사용 |
| source ownership | `swizzle` | local modification 필요 시에만 |
| update | `upgrade --apply` | 별도 change로 test/rebuild |
| health | `doctor` | CI에 연결 |

실행 시에는 `npx @astryxdesign/cli <command>` 형태를 사용하며, 세부 option은 해당 설치 버전의 `--help`에서 확인한다.

## Decision rules

- token 차이: `defineTheme({ extends: baseTheme, ... })`
- SSR production: runtime injection만 믿지 말고 `theme build`
- custom component: 먼저 override, 구조적 divergence가 지속될 때만 `swizzle`
- agent: API를 prompt에 고정하지 말고 CLI에서 current docs를 검색
- Beta upgrade: lockfile 변경 → `upgrade --apply` → theme build → test/visual review → `doctor`

## Sources

- https://github.com/meta/astryx/blob/main/packages/cli/README.md
- https://www.npmjs.com/package/@astryxdesign/cli
