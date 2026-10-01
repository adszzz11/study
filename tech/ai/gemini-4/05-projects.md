---
date: 2026-10-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Gemini 4 Argon — Projects

> [[README|목차로 돌아가기]]

## 1. Large-codebase Migration Copilot

Java/C++ 모듈을 Rust 또는 최신 framework로 단계 이관한다. dependency graph, test suite, lint/security check를 연결하고, 각 PR은 compile·test·security 검사와 human review를 통과해야 한다.

**성공 지표**: build pass rate, test coverage 변화, regression 수, review 시간, migration당 token cost.

## 2. Finance/Legal Research Workspace

문서 OCR, RAG, source citation, human sign-off를 결합해 계약서 비교·규정 변화 요약·투자 리서치 초안을 만든다. 출력은 의사결정 근거가 아니라 검토 초안이며, source freshness와 인용 위치를 반드시 표시한다.

**성공 지표**: citation fidelity, 사실 오류율, 검토자 수정률, 처리 시간.

## 3. Defensive Vulnerability Triage

승인된 조직의 repository 또는 staging URL에서 취약점 후보, reproduction test, patch candidate를 만든다. 고성능 cyber workflow는 CodeMender/Fairwind 접근권이 있을 때만 연결하며, production patch는 human security review 없이는 반영하지 않는다.

**성공 지표**: 재현 가능한 finding 비율, false positive, test 통과 patch 비율, triage 시간.

## 4. Multimodal Operations Analyst

dashboard screenshot, incident timeline, runbook, 회의 녹화를 함께 분석해 장애 요약·원인 가설·검증 체크리스트를 만든다. 추론과 관측 사실을 분리하고, 각 가설에 확인할 telemetry를 연결한다.

**성공 지표**: MTTA/MTTR 변화, 근거 누락률, runbook 준수율, human escalation 정확도.

## 5. Argon Readiness Harness

현재 공개 Gemini API 모델로 task set, 품질 rubric, latency/cost dashboard를 먼저 구축한다. Argon이 공개되면 endpoint만 바꿔 같은 prompt, tool policy, time budget으로 A/B evaluation한다.

```text
Task set + rubric + sandbox + telemetry
                 │
   Current public model baseline
                 │
     Argon available? ── yes → controlled A/B evaluation
```

**완료 조건**: 모델 교체 뒤에도 평가 task, 권한, tool set, metric 계산이 바뀌지 않고 결과 비교가 가능하다.

## Sources

- https://deepmind.google/models/gemini/
- https://deepmind.google/models/gemini/cyber/
- https://ai.google.dev/gemini-api/docs/models
