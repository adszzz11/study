---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis Projects

[[tech/ai/corevis-construction-glasses/README|README]] · 방법론: [[tech/ai/corevis-construction-glasses/04-learning/02-deep-dive|Deep Dive]]

## 1. BIM deviation pilot

한 층 또는 한 trade의 IFC 모델과 LiDAR scan을 비교해 tolerance 밖 drift만 issue 후보로 만든다. 현장 엔지니어가 최종 승인한다.

- 산출물: alignment report, candidate issue, 승인/반려 근거
- 성공 기준: 검토 시간, 승인된 발견 비율, 재측정률

## 2. Code-aware field note assistant

음성 observation에서 위치·사진·도면 element·관련 code citation을 포함한 draft RFI를 만든다. PM이 발송 전 승인한다.

- guardrail: citation 없는 code claim은 draft로도 자동 발송하지 않는다.

## 3. Reality-capture timeline

주간 360°/LiDAR capture를 BIM에 정렬해 날짜별 as-built viewer와 dispute evidence archive를 구축한다.

- 검증: capture 날짜, BIM revision, alignment confidence, retention policy를 함께 저장한다.

## 4. Supply/schedule risk HUD

delivery ETA, crew zone, 작업 진척을 연결한다. Schedule Impact는 자동 변경하지 않고 two-week look-ahead 초안과 승인 workflow까지만 자동화한다.

## Sources

- https://corevis.ai/features
- https://corevis.ai/missions/bim
- https://corevis.ai/about

