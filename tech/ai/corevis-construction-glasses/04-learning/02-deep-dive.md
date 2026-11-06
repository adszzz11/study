---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis Deep Dive

[[tech/ai/corevis-construction-glasses/README|README]] · 이전: [[tech/ai/corevis-construction-glasses/04-learning/01-getting-started|시작하기]] · 적용: [[tech/ai/corevis-construction-glasses/05-projects|Projects]]

## 1. Registration / SLAM

Stereo camera, LiDAR depth, IMU의 extrinsic calibration을 이해한다. point cloud를 BIM과 맞추는 ICP registration은 초기 pose, control point, 반복 관측, dynamic object에 민감하다.

- 측정: residual, drift, coverage, occlusion, alignment confidence
- 검토: survey control과 as-designed 모델 revision이 같은 좌표계인지 확인
- UX: confidence가 낮으면 overlay를 확정처럼 보이지 말고 재보정 요청과 reference를 제시

## 2. Vision + QA

Defect detection은 정답 자체가 아니라 triage 후보를 만든다. defect class별 precision/recall, confidence interval, false positive/negative 비용을 기록하고, field engineer review gate를 둔다.

## 3. Construction RAG

code, drawing, specification, submittal을 versioned corpus로 구성한다. 답변에는 code section, drawing revision, page/element reference를 필수 citation으로 붙인다.

```text
query + location + element ID
→ project/jurisdiction/version filter
→ retrieval with citations
→ evidence-backed recommendation
→ human approval
```

Project-specific addendum과 jurisdiction별 code version을 섞지 않는 것이 핵심이다.

## 4. Platform 경계

WebRTC collaboration, WebGL/3D viewer, audit trail, Mission Control SaaS, Forge SDK는 workflow를 확장하는 방향이다. 공개 roadmap은 구현 완료를 뜻하지 않으므로 API와 export를 실제 sandbox에서 시험한다.

## Sources

- https://corevis.ai/features
- https://corevis.ai/missions/bim
- https://corevis.ai/partners

