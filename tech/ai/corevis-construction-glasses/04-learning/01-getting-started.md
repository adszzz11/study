---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis 시작하기

[[tech/ai/corevis-construction-glasses/README|README]] · 다음: [[tech/ai/corevis-construction-glasses/04-learning/02-deep-dive|Deep Dive]]

## 목표

제품 구매 전, AR overlay와 issue workflow가 성립할 최소 데이터 조건을 작은 sandbox에서 확인한다.

## Step 1 — BIM 기초

- IFC, RVT, BIM 360, element ID를 구분한다.
- 모델 coordinate system, 현장 control point, version control을 문서화한다.
- architectural, structural, MEP layer별로 확인할 tolerance와 담당 trade를 정한다.

## Step 2 — 발견에서 승인까지

아래의 최소 payload를 정의하고 dummy observation으로 끝까지 전달한다.

```text
observation → photo/video + location + BIM element ID + drawing revision
→ candidate code/spec citation → owner routing → RFI/punch draft
→ PM/field engineer approval → immutable audit trail
```

## Step 3 — 안전한 pilot 기준

- 한 층 또는 한 trade만 대상으로 한다.
- AI의 code 판정은 recommendation으로 표시하고 현장 엔지니어가 최종 승인한다.
- false positive, false negative, time-to-document, rework avoided를 기록한다.
- network outage와 alignment 실패 시 종이/모바일 workflow로 fallback한다.

## Checkpoint

- [ ] BIM revision과 현장 기준점의 소유자가 정해졌다.
- [ ] issue payload와 review gate가 문서화됐다.
- [ ] code corpus의 jurisdiction 및 발효 version을 구분했다.

## Sources

- https://corevis.ai/missions/bim
- https://corevis.ai/features
- https://corevis.ai/story/augmented-foreman

