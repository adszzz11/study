---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — Deep Dive

[[tech/devtools/ui-ux-promax/README|학습 진입점]] · 이전: [[tech/devtools/ui-ux-promax/04-learning/01-getting-started|Getting started]]

## Retrieval과 신뢰도

`core.py`는 BM25 ranking과 regex를 결합해 data domain을 검색한다. 최신 버전은 query rewrite, typo recovery, confidence-based abstention, legacy framework routing을 강화했다. confidence가 낮은 결과는 정답처럼 강제하지 않고 product context 또는 조직 tokens를 추가해 다시 질의한다.

```text
좋은 입력 = product + user/job + surface + tone + density + constraint + stack

예: "mobile checkout for returning customers, calm and trustworthy,
     one-handed use, existing blue brand token, react native"
```

## Persistent Design System

페이지 단위 결과를 매번 독립적으로 채택하면 color role과 type scale이 흔들릴 수 있다. 팀에서는 master를 먼저 저장하고 페이지별 예외만 기록한다.

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py \
  "B2B fintech analytics dashboard, trustworthy, compact data density" \
  --design-system --stack nextjs --persist
```

`design-system/<project>/MASTER.md`는 agent context의 기준일 뿐, Figma library나 조직 design token을 자동 대체하지 않는다. 변경 시에는 이유, 영향 surface, rollback 가능한 이전 token을 review한다.

## QA guardrails를 acceptance criteria로

| 영역 | 검증 질문 |
|---|---|
| Contrast | text·icon·status가 배경 위에서 충분히 구분되는가? |
| Keyboard | 모든 interactive control에 visible focus가 있는가? |
| Motion | reduced motion 사용자가 안전하게 animation을 줄일 수 있는가? |
| Feedback | loading, empty, error, success state가 각각 있는가? |
| Reflow | 작은 viewport와 확대에서 정보·action이 사라지지 않는가? |
| Data UI | chart legend, icon-only control, table state가 text 대안을 제공하는가? |

## 실무 loop

1. product constraints와 existing tokens를 입력한다.
2. Design System 결과에서 선택 근거와 anti-pattern을 review한다.
3. `MASTER.md`를 저장하고 구현 agent가 참조하게 한다.
4. surface별 override를 최소화해 기록한다.
5. rendered UI에서 keyboard·contrast·state·responsive QA를 수행한다.

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/core.py
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/search.py
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases
