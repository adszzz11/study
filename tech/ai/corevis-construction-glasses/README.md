---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis — AI-powered construction safety glasses

> **한 줄 정의**: Corevis는 BIM·현장 영상·건축 코드·음성 협업을 결합해 건설 현장의 품질관리와 의사결정을 지원하려는 AI/AR safety-glasses 플랫폼이다.

## Overview

Corevis는 `EARLY ACCESS · V0.1` 단계의 pre-production 제품이다. 도면, BIM, 코드, 사진, 무전, RFI가 흩어진 현장에서 작업자가 실제 시공물을 볼 때 관련 근거를 heads-up으로 제시한다는 가설을 둔다.

- 목표: AR BIM overlay, code-reference AI, reality capture, hands-free collaboration을 하나의 wearable workflow로 연결
- 주의: 공개 정보만으로 상용 출하, 독립 성능 benchmark, 공식 파트너십은 확인되지 않았다. 정밀도·인증·연동은 벤더의 목표 또는 주장으로 취급한다.
- 자세한 정의와 제약은 [[tech/ai/corevis-construction-glasses/01-overview|Overview]]에서 확인한다.

## Learning Path

- [ ] [[tech/ai/corevis-construction-glasses/01-overview|Overview]] — 문제와 제품 가설을 파악한다.
- [ ] [[tech/ai/corevis-construction-glasses/02-ecosystem|Ecosystem]] — 직접 경쟁 제품과 system of record를 비교한다.
- [ ] [[tech/ai/corevis-construction-glasses/04-learning/01-getting-started|시작하기]] — BIM 좌표계와 field workflow의 기초를 익힌다.
- [ ] [[tech/ai/corevis-construction-glasses/04-learning/02-deep-dive|Deep Dive]] — registration, RAG, human review 설계를 학습한다.
- [ ] [[tech/ai/corevis-construction-glasses/05-projects|Projects]] — 작은 검증 pilot을 설계한다.
- [ ] [[tech/ai/corevis-construction-glasses/cheatsheet|Cheatsheet]] — 핵심 용어와 검증 질문을 빠르게 참조한다.
- [ ] [[tech/ai/corevis-construction-glasses/03-references|References]] — 원문과 비교 대상의 근거를 확인한다.

## When To Use

- BIM 모델과 현장 상태의 차이를 조기에 발견하고, 사진·위치·element ID를 증거로 남겨야 할 때
- 작업자의 손을 쓰지 않고 observation을 issue, RFI, punch item 초안으로 전환하고 싶을 때
- 한정된 구역과 trade에서 AR/vision workflow의 ROI와 안전성을 pilot으로 검증할 때

## When Not To Use

- 안전 인증, 정확도, 장시간 착용성, 엔터프라이즈 integration이 이미 계약 조건인 즉시 대규모 배포
- AI가 code compliance 또는 schedule impact를 사람의 검토 없이 최종 판정·변경해야 하는 workflow
- BIM version, 현장 좌표계, 코드 jurisdiction이 정리되지 않아 evidence provenance를 보장할 수 없는 프로젝트

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/ai-ecosystem/README|AI Ecosystem]]
- [[tech/ai/corevis-construction-glasses/02-ecosystem|Construction AI ecosystem]]

## Sources

- https://corevis.ai/
- https://corevis.ai/glasses
- https://corevis.ai/features
- https://corevis.ai/missions/bim
- https://corevis.ai/partners

