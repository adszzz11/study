---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo Deep Dive

> [[01-getting-started|이전: 시작하기]] · [[../README|목차]] · [[../05-projects|다음: 프로젝트]]

## 1. Task decomposition과 topology

좋은 swarm task는 output이 독립적이고 검증 기준이 명확하다.

| 작업 성격 | topology 후보 | 설계 포인트 |
|---|---|---|
| 여러 가설을 동시에 조사 | `mesh` | 결과 형식을 통일하고 중복 탐색 제한 |
| architecture → implementation → review | `hierarchical` | coordinator가 dependency와 승인 순서 관리 |
| module별 구현 + cross-review | `hierarchical-mesh` | file ownership과 integration gate 지정 |
| workload가 예측 불가 | `adaptive` | topology 변경 조건과 max concurrency 제한 |

분해하지 말아야 할 신호는 한 파일의 미세 수정, 강한 sequential dependency, shared mutable state, agent 간 설명 비용이 실제 작업보다 큰 경우다.

## 2. Memory lifecycle

```text
Task/context
  → RETRIEVE: 관련 trajectory와 pattern 검색
  → JUDGE: 현재 task에 맞는지 평가
  → DISTILL: 재사용 가능한 lesson으로 축약
  → CONSOLIDATE: namespace와 provenance를 붙여 저장
```

| 위험 | 방어 |
|---|---|
| stale memory | TTL/version metadata, 최근 source 우선 |
| poisoned instruction | retrieved memory를 untrusted context로 취급 |
| secret persistence | write 전 redaction, sensitive namespace 차단 |
| cross-project leakage | project/user namespace 분리 |
| 잘못된 success pattern | test evidence와 reviewer approval을 함께 저장 |
| retrieval noise | top-k 제한, threshold, provenance 표시 |

Memory 품질은 저장량보다 **무엇을 저장하지 않을지**에서 결정된다. raw transcript 대신 decision, evidence, failure mode, reusable constraint를 저장한다.

## 3. Hook 설계

| Hook | 가능한 역할 | 필수 guardrail |
|---|---|---|
| `PreToolUse` | routing, schema/policy 검사 | default deny, argument normalization |
| `PostToolUse` | result 평가, telemetry, memory 후보 생성 | secret/PII redaction |
| `PreCompact` | compact 전 핵심 context 보존 | provenance와 size limit |
| `Stop` | outcome 정리, learning 반영 | 실패를 성공 pattern으로 저장하지 않기 |

Hook은 deterministic check와 model judgment를 구분한다. path allowlist, secret pattern, budget, schema는 deterministic gate에서 처리하고 “결과 품질” 같은 판단만 model-assisted evaluation에 맡긴다.

## 4. Guidance enforcement 검증

문서의 component 존재만으로 enforcement를 신뢰하지 않는다. 다음 adversarial test를 직접 수행한다.

- [ ] allowlist 밖 파일 write를 차단하는가?
- [ ] symlink/path traversal 우회도 차단하는가?
- [ ] environment secret 출력 요청을 거부·redact하는가?
- [ ] 같은 destructive request의 retry가 idempotent한가?
- [ ] token/tool budget 초과 시 `throttle` 또는 `stop`하는가?
- [ ] audit event의 hash chain과 timestamp를 검증할 수 있는가?
- [ ] memory namespace를 넘어선 read/write가 거부되는가?

## 5. Observability와 evaluation

```text
run_id
├─ task_id / agent_role / model
├─ prompt + retrieved memory provenance
├─ tool calls + approvals + latency
├─ file diff + test evidence
├─ token/cost budget
└─ final verdict + human correction
```

핵심 metric은 agent 수가 아니라 task success rate, escaped defect, rollback rate, human review time, total cost다. project 자체 speedup claim은 같은 workload와 baseline으로 재현한다.

## 6. Production readiness gate

| 영역 | 통과 조건 |
|---|---|
| Version | exact version과 lockfile, upgrade test, rollback 확보 |
| Dependency | 내부 alpha package와 transitive risk 검토 |
| Security | least privilege, secret isolation, denial test 통과 |
| Memory | retention, deletion, namespace, poisoning 대응 |
| Reliability | agent crash, partial result, retry, conflict 처리 |
| Audit | user/task/tool/result provenance 재구성 가능 |
| Cost | per-run budget와 hard stop 검증 |

## Sources

- https://github.com/ruvnet/ruflo/blob/main/SKILL.md
- https://github.com/ruvnet/ruflo/blob/main/plugins/ruflo-agentdb/README.md
- https://github.com/ruvnet/ruflo/blob/main/v3/%40claude-flow/guidance/docs/guides/architecture-overview.md
- https://github.com/ruvnet/ruflo/blob/main/package.json

