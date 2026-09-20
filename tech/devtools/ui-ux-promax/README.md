---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max

> **한 줄 정의**: UI UX Pro Max는 AI coding assistant가 UI를 임의 생성하지 않도록, 로컬 curated design data와 검색·reasoning engine으로 디자인 시스템 결정을 보조하는 open-source Agent Skill/CLI다.

## Overview

React·Tailwind가 구현 속도를 높여도 hierarchy, palette, typography, density, interaction, accessibility의 일관성은 자동으로 생기지 않는다. UI UX Pro Max는 style·color·typography·landing pattern·UX rule·stack guideline을 검색해 이 **design taste/consistency gap**을 줄인다.

- Python 3 검색 엔진(BM25 + regex)과 CSV design database를 로컬 skill 경로에 설치하는 local-first 도구다.
- prompt에서 product type, surface, style hint, intent를 읽어 pattern·tokens·type·UX checks를 포함한 Design System을 만든다.
- `--persist`는 `design-system/<project>/MASTER.md`에 결정을 저장해 agent session 간 visual drift를 줄인다.
- 2026-08-13 기준 공식 최신 release는 **v2.15.0**이며 192 product type, 79 searchable style, 119 UX guideline, 22 stack 및 1,260 stack-specific guideline을 명시한다.

이는 component library의 대체재가 아니라 **upstream design-decision layer**다. 예컨대 shadcn/ui로 구현 재료를 고르고, UI UX Pro Max로 tone·density·color role의 방향을 정한다. [Release v2.15.0](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases)

## Learning Path

- [ ] [[tech/devtools/ui-ux-promax/01-overview|1. Overview]] — What/Why와 검색 기반 의사결정 이해하기
- [ ] [[tech/devtools/ui-ux-promax/02-ecosystem|2. Ecosystem]] — component·styling·design 도구와 역할 구분하기
- [ ] [[tech/devtools/ui-ux-promax/03-references|3. References]] — 공식 source-of-truth와 설치 검증 지점 확인하기
- [ ] [[tech/devtools/ui-ux-promax/04-learning/01-getting-started|4. Getting started]] — Codex skill 설치와 첫 Design System 생성하기
- [ ] [[tech/devtools/ui-ux-promax/04-learning/02-deep-dive|5. Deep dive]] — retrieval, persistence, QA guardrail 적용하기
- [ ] [[tech/devtools/ui-ux-promax/05-projects|6. Projects]] — 제품 surface별 실전 과제 수행하기
- [ ] [[tech/devtools/ui-ux-promax/cheatsheet|7. Cheatsheet]] — 명령·점검표·문제 해결 복습하기

## When To Use

- 여러 AI agent session에서 제품의 visual language를 일관되게 유지해야 할 때
- dashboard, checkout, landing page처럼 product·surface별 UX pattern 선택이 중요한 때
- Next.js, Tailwind, shadcn/ui 등 구현 전에 tokens와 accessibility acceptance criteria를 정할 때
- 기존 디자인 token을 제약으로 삼아 legacy UI의 responsive·accessibility를 개선할 때

## When Not To Use

- 단일 component를 빠르게 추가할 뿐 별도 디자인 방향 결정이 필요 없을 때
- Figma 중심 협업·승인·prototype workflow 자체가 주된 문제일 때
- 조직의 brand guideline이 충분히 정리되어 있고 retrieval layer의 운영 비용이 이득보다 클 때
- 결과를 검토할 designer 또는 product owner 없이 tool 출력만으로 고위험 UX 결정을 확정하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/claude-observer/README|Claude Observer]] — agent skill의 관찰·운영 관점에서 함께 볼 수 있는 도구

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/CLAUDE.md
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/search.py
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/core.py
