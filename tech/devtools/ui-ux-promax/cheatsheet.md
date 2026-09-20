---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — Cheatsheet

[[tech/devtools/ui-ux-promax/README|학습 진입점]]

## 핵심 명령

```bash
# Codex용 skill 설치
npx ui-ux-pro-max-cli init --ai codex

# 설치 결과 확인
find .agents/skills/ui-ux-pro-max -maxdepth 3 -type f | sort
python3 .agents/skills/ui-ux-pro-max/scripts/search.py --help

# Design System 생성
python3 .agents/skills/ui-ux-pro-max/scripts/search.py \
  "B2B fintech analytics dashboard, trustworthy, compact data density" \
  --design-system --stack nextjs

# 팀 기준 저장
python3 .agents/skills/ui-ux-pro-max/scripts/search.py \
  "B2B fintech analytics dashboard, trustworthy, compact data density" \
  --design-system --stack nextjs --persist
```

## Prompt recipe

```text
[product / user job], [surface], [tone], [density],
[brand or technical constraint], [stack]
```

예: `Fintech mobile checkout for returning users, calm trustworthy tone, one-handed flow, existing blue token, React Native`

## 구현 전 확인

- [ ] package version과 공식 release를 확인했다.
- [ ] 필요한 script·data·assistant skill file이 실제 설치됐다.
- [ ] `pattern`, `colors`, `typography`, `anti-patterns`, `accessibility`를 읽었다.
- [ ] 기존 brand token과 business requirement를 output보다 우선했다.
- [ ] 팀 기준은 `MASTER.md`, 예외는 surface별 override로 기록했다.

## UI QA

- [ ] visible keyboard focus
- [ ] readable contrast와 semantic status color
- [ ] loading / empty / error / success feedback
- [ ] reduced motion
- [ ] responsive reflow와 touch target
- [ ] chart·icon·table의 text alternative

## 기억할 구분

| 항목 | UI UX Pro Max의 역할 | 함께 쓰는 도구 |
|---|---|---|
| 디자인 결정 | retrieval 기반 recommendation | 조직 tokens, designer review |
| component 구현 | stack guideline 제공 | Tailwind, shadcn/ui |
| visual QA | check 항목 제공 | Storybook, a11y test |
| 협업·handoff | 직접 대체하지 않음 | Figma |

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/362
