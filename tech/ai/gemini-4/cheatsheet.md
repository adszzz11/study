---
date: 2026-10-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Gemini 4 Argon — Cheatsheet

> [[README|목차로 돌아가기]]

## Snapshot (2026-10-01)

| 항목 | 내용 |
|---|---|
| Provider | Google DeepMind |
| Position | closed managed frontier model |
| Focus | long-horizon reasoning, multimodality, agentic coding, defensive cybersecurity |
| Access | 일반 공개 API 없음; Fairwind Program 중심 제한 배포 |
| Output claim | 최대 1M output tokens |
| Announced price | input $2/1M, output $10/1M; 이후 $4/$20 예정 |

## Published Metrics (Provider-reported)

| Benchmark | 발표 수치 |
|---|---:|
| LVBench long-video understanding | 91.7% |
| DeepSWE v1.1 | 77.9% |
| CWE-bench v1 | 68% |
| Vals Index | 68.9% |
| GraphWalks 1M context | 84.2% |

> 이 수치는 Google이 선택·공개한 benchmark다. 독립 재현 또는 조직 업무 성능과 동일시하지 않는다.

## Deployment Rules

- 공개 endpoint가 확인되기 전에는 Argon을 production dependency로 두지 않는다.
- 긴 model output을 executable authority로 취급하지 않는다.
- tool은 allowlist, scoped credential, least privilege로 제한한다.
- untrusted content는 data로 격리하고 prompt injection을 검사한다.
- write, deploy, 보안 영향 action은 sandbox 검증과 human approval 뒤에만 수행한다.

## Evaluation Formula

```text
Adoption decision = task success + evidence quality + safety
                  + latency/cost + human-review efficiency
```

## Current Practical Stack

`Google Gen AI SDK` + `Vertex AI` + `RAG/agent orchestration` + `sandboxed tool execution` + `evaluation harness`

현재는 이 조합으로 공개 Gemini API 모델의 기준선을 만들고, Argon이 공개될 때 controlled A/B evaluation을 수행한다.

## Sources

- https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
- https://deepmind.google/models/gemini/
- https://deepmind.google/fairwind-program/
