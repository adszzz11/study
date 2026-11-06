---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis Ecosystem

[[tech/ai/corevis-construction-glasses/README|README]] · [[tech/ai/corevis-construction-glasses/03-references|References]]

## 비교

| 제품/범주 | 강점 | Corevis와의 차이 |
|---|---|---|
| Corevis | AR BIM overlay, code-reference AI, 3D capture, voice communication을 한 wearable에 통합하려는 vision | Early-access/pre-production; 상용 성능·인증·연동 범위를 검증해야 함 |
| [XYZ Reality Atom](https://www.xyzreality.com/atom) | construction-certified AR hardhat와 millimeter급 모델 시각화에 집중 | Corevis는 glasses form factor에 code intelligence, comms, capture까지 넓히려 함 |
| [OpenSpace Capture](https://www.openspace.ai/platform/capture/) | 360°/drone/LiDAR reality capture와 BIM coordination | OpenSpace는 capture-centric platform, Corevis는 실시간 first-person heads-up workflow를 목표 |
| [Procore AI Go](https://investors.procore.com/news/news-details/2026/Procore-Launches-Voice-First-AI-Mobile-App-Built-for-the-Jobsite/default.aspx) | 프로젝트 데이터 voice-first Q&A; 2026년 북미 open beta, Meta glasses 연동은 closed beta | Procore는 system of record 중심, Corevis는 dedicated hardware와 BIM/vision inspection 중심 |
| Autodesk Construction Cloud / BIM 360 | 모델·문서·issue의 enterprise system of record | Corevis는 대체보다 source BIM을 읽어 현장 시야·issue workflow로 확장하는 포지션 |

## Integration 해석

Corevis가 표기한 Procore, PlanGrid, Bluebeam, Fieldwire, BIM 360, Trimble Connect, Bentley iTwin은 **compatibility, not partnership**이다. 계약된 공식 integration이나 endorsement로 해석하지 않는다. 구매 또는 pilot 전에 API 범위, 인증 방식, read/write 권한, audit trail 보존을 확인한다.

## 평가 질문

- BIM 360/IFC/RVT의 어떤 version과 element property를 실제로 읽는가?
- 현장 좌표 transform 실패, drift, occlusion 시 작업자에게 어떤 confidence와 fallback을 제시하는가?
- issue가 Procore/Autodesk에 생성될 때 사진·위치·BIM element·code citation의 provenance가 보존되는가?

## Sources

- https://corevis.ai/partners
- https://www.xyzreality.com/atom
- https://www.openspace.ai/platform/capture/
- https://investors.procore.com/news/news-details/2026/Procore-Launches-Voice-First-AI-Mobile-App-Built-for-the-Jobsite/default.aspx

