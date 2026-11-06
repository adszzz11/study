---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis Cheatsheet

[[tech/ai/corevis-construction-glasses/README|README]] · [[tech/ai/corevis-construction-glasses/04-learning/02-deep-dive|Deep Dive]]

## 기술스택 요약

- **Device/edge**: stereo camera + LiDAR, IMU/GNSS, waveguide display, NPU 기반 on-device inference, 5G/Wi-Fi/mesh.
- **Spatial AI**: SLAM/ICP registration, point-cloud fusion, photogrammetry, BIM/IFC/RVT parsing, depth-aware AR rendering.
- **AI/data**: CV defect detection, ASR(예: Whisper), code/spec RAG와 Vector DB, confidence score, human-in-the-loop 승인.
- **Platform**: WebRTC collaboration, WebGL/3D viewer, audit trail, Mission Control SaaS, Procore·BIM 360·Bluebeam·Fieldwire 계열 연동.

## 용어

| 용어 | 현장 적용 의미 |
|---|---|
| IFC / RVT | 교환용 BIM 모델 / Revit 원본 형식. revision과 element ID를 함께 관리한다. |
| ICP | point cloud와 BIM을 반복적으로 정렬하는 알고리즘. 초기 pose가 나쁘면 잘못 맞을 수 있다. |
| Drift | 추정 위치가 실제 위치에서 누적해 벗어나는 오차. overlay 신뢰도를 낮춘다. |
| RAG | 근거 문서를 검색해 답변에 붙이는 방식. code section과 version citation이 핵심이다. |
| Audit trail | 관찰·근거·승인·변경의 이력을 보존하는 기록이다. |

## Pilot 전 질문

- [ ] 대상 BIM revision, coordinate system, control point가 확정됐는가?
- [ ] code/spec corpus가 jurisdiction과 발효 version으로 분리됐는가?
- [ ] AI 결과가 recommendation이며 human approval 없이는 외부 workflow를 변경하지 않는가?
- [ ] alignment, detection, network failure의 fallback이 있는가?
- [ ] ‘compatibility’ 표기가 공식 partnership으로 오해되지 않았는가?

## Sources

- https://corevis.ai/glasses
- https://corevis.ai/features
- https://corevis.ai/partners
