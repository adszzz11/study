---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute Projects

## Project 1 — Local gateway smoke lab

### 목표

OmniRoute를 local에서 실행하고 OpenAI-compatible client 하나를 direct model과 `auto`에 연결한다.

### 범위

- npm 또는 Docker 설치
- `STORAGE_ENCRYPTION_KEY` 설정
- provider connection 하나
- `/v1/models`, non-streaming, streaming 호출
- `X-OmniRoute-Decision`과 dashboard log 확인

### 산출물

```text
omniroute-smoke/
├── README.md
├── smoke.sh
├── client.py
└── results/
    └── routing-observations.md
```

### 완료 조건

- [ ] secret이 repository와 shell output에 노출되지 않는다.
- [ ] direct model과 `auto`가 모두 성공한다.
- [ ] streaming response가 정상 종료된다.
- [ ] request와 routing decision을 dashboard에서 추적할 수 있다.

## Project 2 — Quota-aware coding route

### 목표

두 개 이상의 connection을 묶어 coding workload의 quota continuity를 검증한다.

### 실험 설계

| 단계 | 작업 | 측정 |
|---|---|---|
| Baseline | 각 target을 직접 10회 호출 | success rate, p50/p95 latency, cost |
| Auto | `auto/coding`으로 동일 corpus 호출 | target distribution, quality rubric |
| Quota event | test limit 또는 connection disable | account fallback time |
| Provider event | primary unavailable simulation | model/provider fallback |
| Recovery | cooldown 후 복구 | circuit state와 LKGP 변화 |

### Test corpus

- 작은 bug fix
- unit test 생성
- unfamiliar code explanation
- structured JSON output
- tool call이 포함된 agent request
- 긴 context의 code review

### 완료 조건

- [ ] connection failure와 provider failure를 구분해 기록한다.
- [ ] fallback 뒤에도 output contract와 streaming이 유지된다.
- [ ] latency와 cost 증가를 수치로 설명한다.
- [ ] `auto/coding`이 항상 최고 품질이라는 전제를 두지 않고 rubric으로 평가한다.

## Project 3 — Routing strategy benchmark

### 목표

`priority`, `round-robin`, `headroom`, `cost-optimized`, `lkgp`, `auto`를 동일 workload에서 비교해 workload별 policy를 선택한다.

### 결과 표

| Strategy | Success % | p50 | p95 | Estimated cost | Fallback depth | 비고 |
|---|---:|---:|---:|---:|---:|---|
| `priority` |  |  |  |  |  |  |
| `round-robin` |  |  |  |  |  |  |
| `headroom` |  |  |  |  |  |  |
| `cost-optimized` |  |  |  |  |  |  |
| `lkgp` |  |  |  |  |  |  |
| `auto` |  |  |  |  |  |  |

### 분석 질문

- 평균 latency는 낮지만 p99가 나쁜 strategy는 무엇인가?
- retry를 포함한 실제 request cost는 어떻게 달라지는가?
- quota reset 직전과 직후에 target distribution이 변하는가?
- session affinity가 quality와 cache hit에 어떤 영향을 주는가?
- restart 뒤 routing state 복원이 결과에 영향을 주는가?

## Project 4 — Secure remote deployment review

### 목표

VPS deployment를 실제 공개하기 전에 security review 문서와 복구 절차를 만든다.

### 필수 통제

- TLS reverse proxy
- dashboard authentication
- scoped API key와 rotation
- loopback/private management route
- encrypted credential storage
- redacted access/application log
- SQLite와 encryption key의 분리 backup
- provider별 data flow와 terms 기록
- pinned version과 rollback image

### Threat model 표

| Asset | Threat | Control | 검증 방법 |
|---|---|---|---|
| OAuth refresh token | DB 또는 backup 탈취 | AES-256-GCM, access control | restore 후 ciphertext 확인 |
| Endpoint API key | log 유출 | header redaction, short scope | log scan |
| Dashboard | public brute force | auth, TLS, network restriction | external port scan |
| Prompt/output | upstream data exposure | provider policy와 route allowlist | route별 data-flow review |
| Routing state | restart 시 잘못된 복원 | backup, state inspection | restart drill |

### 완료 조건

- [ ] internet-facing port와 route inventory가 있다.
- [ ] backup/restore와 key rotation을 실제로 수행했다.
- [ ] external upstream으로 이동하는 data를 diagram으로 설명한다.
- [ ] enterprise compliance를 built-in security feature와 혼동하지 않는다.

## Project 5 — Fusion vs Pipeline opt-in experiment

### 목표

일반 fallback으로 해결할 문제와 multi-model orchestration이 필요한 문제를 구분한다.

| 실험 | 구성 | 기대하는 가치 | 주요 비용 |
|---|---|---|---|
| Fallback | primary → secondary | availability | retry latency |
| Fusion | model panel → judge | 관점/답변 합성 | 병렬 token + judge + tail latency |
| Pipeline | extract → critique → rewrite | 단계별 specialization | 오류 전파 + 중간 data |

### 중단 기준

- single model baseline 대비 quality gain이 rubric 오차보다 작다.
- cost 또는 p95 latency가 workload budget을 넘는다.
- 민감한 prompt가 허용하지 않은 provider로 fan-out된다.
- 중간 step 실패의 partial retry가 안전하지 않다.

## 공통 Best Practices

- `latest` 대신 검증한 version을 pin한다.
- 먼저 direct target을 검증한 뒤 Combo와 Auto-Combo를 추가한다.
- provider/model/account를 모두 log dimension으로 남긴다.
- synthetic failure test와 real provider outage를 구분한다.
- cost telemetry를 invoice와 대조한다.
- production credential로 destructive quota test를 하지 않는다.
- quick release cadence를 고려해 staging과 rollback을 유지한다.

## Sources

- https://github.com/diegosouzapw/OmniRoute
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/routing/AUTO-COMBO.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/RESILIENCE_GUIDE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/SECURITY.md

