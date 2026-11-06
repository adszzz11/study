---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Corevis Overview

[[tech/ai/corevis-construction-glasses/README|README]]로 돌아가기.

## What

Corevis는 현장 관리자가 safety glasses에서 BIM layer, code/spec 근거, 과거 기록, 협업 대상을 확인하도록 설계 중인 AI/AR 플랫폼이다. 창업자는 Black Rock Construction의 Stephan Stanfill이며, 초기 현장 검증을 강조한다.

공식 BIM alignment 흐름은 다음과 같다.

```text
Stereo + LiDAR capture → live point cloud → ICP alignment against BIM
→ depth-correct waveguide projection
```

## Why

현장에서는 도면·BIM·코드·사진·무전·RFI가 도구별로 분산된다. 이 분절은 문서화 지연, spec/code 누락, 재작업, 협업 단절로 이어진다. Corevis의 핵심 가설은 시공물을 보는 순간 관련 evidence를 제공하면 발견과 처리를 앞당길 수 있다는 것이다.

## 주요 특징과 검증 상태

| 영역 | 표방 기능 | 검증 시 유의점 |
|---|---|---|
| AR Blueprint Overlay | BIM 360, IFC, RVT와 architectural/structural/MEP layer를 음성 전환 | 모델 version·좌표 보정·occlusion 품질을 별도 시험 |
| Code Detection | IBC, ADA, fire/life-safety, spec 차이를 code section·shop drawing·cut sheet와 제시 | RAG citation과 jurisdiction/version 분리가 필수 |
| Collaboration | Whisper 기반 음성, WebRTC, Geo-IMU로 issue payload 전달 | 전송 안정성·개인정보·승인 책임을 확인 |
| Reality Capture | stereo 12MP 2개와 LiDAR 30Hz fusion, point cloud/photogrammetry export | capture completeness와 비교 기준을 샘플로 검증 |
| Hardware target | monocular waveguide 124° FOV/60Hz, 21 TOPS NPU, IP67, hot-swap 12시간 | 목표 사양이며 ANSI Z87+, OSHA, FCC/CE/UKCA는 ‘designed to meet’ 단계 |

`sub-millimeter alignment`, `0.4mm drift`는 독립 benchmark가 아닌 Corevis의 목표치/주장이다. Mission Control SaaS와 Forge SDK/open API도 향후 방향이며 Forge는 개발 중이다.

## 다음 읽기

- [[tech/ai/corevis-construction-glasses/04-learning/01-getting-started|시작하기]]
- [[tech/ai/corevis-construction-glasses/02-ecosystem|Ecosystem 비교]]

## Sources

- https://corevis.ai/
- https://corevis.ai/features
- https://corevis.ai/glasses
- https://corevis.ai/about

