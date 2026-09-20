---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# awesome-design-md — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. Contract architecture

`DESIGN.md`는 값 목록이 아니라 세 계층을 잇는 contract다.

```text
Intent / rationale
        ↓ constrains
Semantic tokens
        ↓ map to
Component tokens
        ↓ drive
Platform implementation
```

| 계층 | 예 | 변경 이유 |
|---|---|---|
| Primitive | `gray-950`, `space-4` | raw scale 관리 |
| Semantic | `text-primary`, `surface-muted`, `danger` | 의미와 theme 분리 |
| Component | `button-primary-bg`, `dialog-radius` | component별 결정과 예외 명시 |

가능하면 component가 primitive를 직접 참조하지 않고 semantic token을 거치게 한다. 그래야 dark theme이나 rebrand에서 component 전체를 다시 쓰지 않아도 된다.

```yaml
colors:
  neutral-950: "#171717"
  action-primary: "{colors.neutral-950}"
components:
  button-primary:
    backgroundColor: "{colors.action-primary}"
```

## 2. Normative와 explanatory content

- YAML은 tool이 검사·변환할 **normative data**다.
- Markdown은 사용 의도, 예외, anti-pattern을 설명하는 **human-readable guidance**다.
- 같은 규칙이 두 영역에서 충돌하면 agent와 사람이 다른 결론을 낼 수 있으므로 review에서 함께 변경한다.

나쁜 예:

```text
YAML: button-primary.radius = 16px
Markdown: Controls use restrained 4px corners.
```

좋은 review 질문:

- token 변경에 대응하는 rationale 변경이 있는가?
- prose에서 언급한 semantic role이 schema에 존재하는가?
- component exception이 전체 원칙을 무력화하지 않는가?

## 3. CLI를 CI에 연결하기

```yaml
name: design-contract
on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npx @google/design.md@<pinned-version> lint DESIGN.md
      - run: npx @google/design.md@<pinned-version> export --format dtcg DESIGN.md > /tmp/tokens.json
```

핵심 원칙:

- `alpha` 도구는 exact version으로 pin한다.
- `lint`와 `export`는 별도 step으로 둔다.
- dependency update PR에서 schema, output diff, migration note를 검토한다.
- generated output을 commit한다면 재생성 방법과 drift check를 정한다.

## 4. Diff를 design review로 만들기

단순한 line diff를 넘어서 영향 범위를 기록한다.

| 변경 | 검토할 영향 |
|---|---|
| Color token | contrast, status meaning, light/dark theme |
| Typography | wrapping, localization, layout shift |
| Spacing | density, touch target, viewport overflow |
| Radius/elevation | hierarchy, nested container proliferation |
| Component token | 모든 state와 variant, disabled/focus/hover |

```bash
npx @google/design.md diff DESIGN.md DESIGN-v2.md
npx @google/design.md lint DESIGN-v2.md
```

## 5. Accessibility boundary

CLI의 WCAG contrast 검사는 유용하지만 전체 accessibility test가 아니다.

- keyboard navigation과 logical tab order
- visible focus와 focus management
- semantic HTML, label, name/role/value
- error identification과 recovery
- reduced motion preference
- zoom, reflow, responsive layout
- screen reader announcement

따라서 contract review 후 component test, browser audit, manual keyboard/screen-reader check를 병행한다.

## 6. Security와 provenance

외부 `DESIGN.md`는 문서이면서 agent input이다. 다음 boundary를 둔다.

1. trusted maintainer가 내용을 review한다.
2. design token과 rationale 외 지시는 제거한다.
3. 외부 URL과 executable command를 별도로 확인한다.
4. credential, private source, repository 밖 경로 접근을 허용하지 않는다.
5. reference URL, retrieval date, local modification을 기록한다.

## 7. Brand/IP boundary

- MIT license는 collection repository 문서의 license다.
- 상표, logo, proprietary font, 사진, product copy의 권리를 자동으로 주지 않는다.
- “inspired by” reference는 design principle 탐색에 쓰고, 소비자가 공식 제품으로 오인할 정도의 identity 복제는 피한다.
- 최종 contract에는 자사 brand constraint와 허용된 asset만 남긴다.

## 8. 운영 모델

```text
Reference review
   ↓
Project DESIGN.md proposal
   ↓ lint + security/IP review
Implementation PR
   ↓ Storybook + visual + a11y tests
Approved contract/version
   ↓
Periodic drift audit
```

### Drift audit 체크리스트

- [ ] 구현된 color와 spacing이 contract에서 벗어나지 않았는가?
- [ ] 새 component token이 문서 없이 hard-code되지 않았는가?
- [ ] prose와 YAML이 같은 결정을 표현하는가?
- [ ] spec/CLI update로 lint 결과가 달라지지 않았는가?
- [ ] reference가 아니라 제품 자체의 needs와 research가 결정을 이끄는가?

## Sources

- https://github.com/google-labs-code/design.md
- https://www.w3.org/community/design-tokens/
- https://github.com/VoltAgent/awesome-design-md

