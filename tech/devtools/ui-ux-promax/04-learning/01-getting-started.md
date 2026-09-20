---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — Getting Started

[[tech/devtools/ui-ux-promax/README|학습 진입점]] · 다음: [[tech/devtools/ui-ux-promax/04-learning/02-deep-dive|Deep dive]]

## 목표

Codex용 skill을 설치하고, component 구현 전에 B2B fintech dashboard의 Design System을 생성한다. Node.js와 Python 3가 필요하다. package name과 실제 skill path는 설치 직전에 공식 README·release에서 재확인한다.

## 1. 설치

프로젝트 root에서 실행한다.

```bash
npx ui-ux-pro-max-cli init --ai codex
```

설치 뒤에는 CLI 성공 여부와 별개로 파일을 확인한다.

```bash
find .agents/skills/ui-ux-pro-max -maxdepth 3 -type f | sort
python3 .agents/skills/ui-ux-pro-max/scripts/search.py --help
```

필요한 script·data·assistant skill file이 없다면 구현을 시작하지 말고 설치 version과 [Issue #362](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/362)를 확인한다.

## 2. Design System 먼저 생성

```bash
python3 .agents/skills/ui-ux-pro-max/scripts/search.py \
  "B2B fintech analytics dashboard, trustworthy, compact data density" \
  --design-system --stack nextjs
```

## 3. 결과를 구현 요구사항으로 변환

| 출력 | 구현 전에 결정할 것 |
|---|---|
| `pattern` | dashboard information hierarchy와 table/chart 배치 |
| `colors` | semantic color role, contrast target, status color |
| `typography` | title·metric·body scale과 number readability |
| `anti-patterns` | 피해야 할 과도한 장식 또는 모호한 interaction |
| `accessibility` | focus, loading/error, reduced motion acceptance criteria |

그 뒤에만 “Next.js + shadcn/ui로 dashboard를 구현하라”고 요청한다. UI code가 디자인 결정을 덮어쓰지 않도록 결과 요약을 prompt 또는 project context에 포함한다.

## 학습 체크

- [ ] 설치된 skill의 script와 data를 직접 확인했다.
- [ ] 구현 요청보다 먼저 `--design-system` 결과를 읽었다.
- [ ] accessibility 항목을 testable acceptance criteria로 바꿨다.

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/cli
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/362
