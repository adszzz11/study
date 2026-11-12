---
date: 2026-11-13
tags: [tech]
type: tech-tool-study
status: draft
---

# Astryx — Deep Dive

> [[tech/devtools/astryx-design-system/README|목차로 돌아가기]] · [[tech/devtools/astryx-design-system/05-projects|다음: Projects]]

## Theme extension과 compiler

custom theme은 base package theme을 fork하기보다 extension으로 시작한다.

```ts
const brandTheme = defineTheme({
  extends: importedTheme,
  // accent, typography, radius 등 브랜드 차이만 선언
});
```

runtime theme은 hydration 시 style을 주입할 수 있다. Next.js/Remix 같은 SSR production 환경에서는 component override의 flash를 피하도록 build artifact를 만든다.

```bash
npx @astryxdesign/cli theme build
```

build 결과의 CSS, ESM, TypeScript declaration을 versioned artifact로 검토하고 application build에 연결한다. 정확한 output path는 현재 CLI docs로 확인한다.

## Ownership 경계

| 요구 | 우선 선택 | 이유 |
|---|---|---|
| token만 다름 | `extends` | upstream theme update를 계속 받는다. |
| 정해진 override가 필요 | theme/component override | 유지보수 surface가 작다. |
| component 구조 자체가 제품 고유 | `swizzle` | source를 project가 완전히 소유한다. |
| 영구 독립 fork | `eject` | update lineage를 끊는 비용을 감수한다. |

`eject`는 마지막 수단이다. source ownership이 생기면 security/accessibility fix와 upstream API 변경도 팀의 migration 책임이 된다.

## Agent-ready delivery loop

```text
agent request
  → component/search/docs로 설치 버전 조회
  → template 또는 composition 초안 생성
  → test·visual review
  → doctor로 project health 점검
  → upgrade --apply 후 custom theme rebuild
```

CLI가 text/JSON surface를 제공하더라도 agent가 만든 UI를 자동 승인해서는 안 된다. interaction, keyboard navigation, contrast, domain authorization은 사람이 test와 review로 책임진다.

## CI와 upgrade

```bash
npx @astryxdesign/cli doctor
npx @astryxdesign/cli upgrade --apply
npx @astryxdesign/cli theme build
```

CI에서는 `doctor`, typecheck, test, compiled theme artifact drift 확인을 묶는다. Beta package upgrade는 separate change로 처리하고, release note·CLI docs·SSR screenshot을 함께 검토한다.

## Sources

- https://astryx.atmeta.com/docs/theme
- https://github.com/meta/astryx/blob/main/packages/cli/README.md
- https://engineering.fb.com/2025/11/11/web/stylex-a-styling-library-for-css-at-scale/
