---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — 시작하기

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/04-learning/02-deep-dive|다음: Deep Dive]]

## 1. 설치와 초기화

React 19+ project에서 package를 설치하고 CLI가 만드는 agent index를 확인한다.

```bash
npm install @astryxdesign/core @astryxdesign/theme-neutral @stylexjs/stylex
npm install -D @astryxdesign/cli
npx @astryxdesign/cli init
```

`init` 뒤에는 `AGENTS.md` 또는 `CLAUDE.md`에 추가된 component index를 검토한다. 이는 문서의 정답을 복제하는 파일이 아니라 agent가 local CLI docs를 찾도록 안내하는 entry point여야 한다.

## 2. Component 문서 탐색

```bash
npx @astryxdesign/cli component --list
npx @astryxdesign/cli component Button
npx @astryxdesign/cli search "form validation"
```

agent에게는 “API를 추측하지 말고 먼저 `component` 또는 `search`를 실행하라”고 지시한다. 그러면 package version과 불일치한 예제를 prompt에서 재생산할 위험이 줄어든다.

## 3. 첫 Theme 적용

Neutral theme을 추가하고 application root에서 `<Theme>` provider를 사용한다. `mode="system"`으로 OS preference를 따르게 한 뒤, light/dark token tuple과 component rendering을 함께 확인한다.

```bash
npx @astryxdesign/cli theme add neutral
```

정확한 import path와 provider option은 설치 버전의 CLI docs를 source of truth로 삼는다.

## 4. 첫 화면 만들기

```bash
npx @astryxdesign/cli template dashboard --skeleton
```

생성한 skeleton에 Button, form, Table 등 component를 조합한다. 이 단계의 목표는 pixel-perfect page가 아니라 theme이 바뀌어도 behavior/accessibility layer가 보존되는지 경험하는 것이다.

## 완료 기준

- component 목록과 Button docs를 CLI에서 직접 찾았다.
- system light/dark mode가 적용된 한 화면을 만들었다.
- agent가 CLI-first 규칙을 따르도록 project instruction을 검토했다.
- 다음 단계인 [[tech/devtools/astryx-design-system/04-learning/02-deep-dive|Deep Dive]]에서 custom theme과 SSR artifact를 다룰 준비가 됐다.

## Sources

- https://github.com/meta/astryx/blob/main/packages/cli/README.md
- https://astryx.atmeta.com/docs/theme
