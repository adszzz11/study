---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]]

## 학습 목표

- direct route, saved Combo, Auto-Combo의 선택 과정을 설명한다.
- account, model, system layer의 failure를 분리해 재현한다.
- telemetry를 근거로 routing policy를 평가한다.
- credential, network, log, upstream data boundary를 threat model에 반영한다.

## 1. Routing target을 정확히 모델링하기

OmniRoute에서 provider 이름만으로 route를 설명하면 account-level fallback을 놓친다.

```text
Candidate
├─ provider
├─ model
├─ connection/account
├─ health and circuit state
├─ quota headroom and reset window
├─ price
├─ latency distribution
└─ capability/context fit
```

동일 model이라도 connection별 quota와 health가 다르고, provider endpoint별 price와 latency도 다르다. 따라서 평가 단위는 “model A vs model B”가 아니라 실제 candidate tuple이어야 한다.

## 2. Strategy 선택

| 목표 | 우선 검토 | Trade-off |
|---|---|---|
| 명시적 primary/fallback | `priority` | 앞 target에 traffic 집중 |
| quota를 순차 소진 | `fill-first` | 뒤 target 검증이 늦어짐 |
| 비율 분배 | `weighted` | weight tuning 필요 |
| 균등 순환 | `round-robin` | health·cost 차이를 충분히 반영하지 못할 수 있음 |
| 낮은 현재 부하 | `p2c`, `least-used` | load signal 품질에 의존 |
| quota 연속성 | `headroom`, `reset-aware` | 품질·latency가 후순위가 될 수 있음 |
| 비용 최소화 | `cost-optimized` | quality와 latency trade-off |
| 긴 context | `context-optimized`, `context-relay` | provider 간 semantic 차이 |
| prompt cache 활용 | `cache-optimized` | connection affinity가 분산보다 우선 |
| 성공 route 유지 | `lkgp` | 더 나은 새 candidate 탐색이 줄 수 있음 |
| 동적 다목적 선택 | `auto` | scoring과 telemetry를 이해해야 함 |
| 복수 model 합성 | `fusion` | fan-out 비용 + judge 비용 + latency |
| 단계형 변환 | `pipeline` | 앞 step 오류가 뒤로 전파 |

정책은 이름보다 invariant로 정의한다.

```text
예:
- coding request는 quality-fit candidate만 허용한다.
- quota headroom이 10% 아래면 primary를 제외한다.
- request budget을 넘으면 expensive fallback을 금지한다.
- 동일 session은 가능하면 last-known-good connection을 유지한다.
```

## 3. Auto-Combo 해석

Auto-Combo는 저장된 chain이 아니라 현재 connection으로 만든 virtual combo다.

| Model ID | 우선 목표 |
|---|---|
| `auto` | balanced + LKGP |
| `auto/coding` | coding quality |
| `auto/fast` | low latency |
| `auto/cheap` | low token cost |
| `auto/offline` | quota headroom |
| `auto/smart` | quality + exploration |

Category와 tier를 조합한 `auto/coding:fast`, `auto/reasoning:pro`, `auto/multimodal:free` 같은 형태도 문서화되어 있다. 다만 filter가 일치하는 candidate를 찾지 못할 때 fail-open으로 더 넓은 pool을 사용할 수 있으므로, suffix만 보고 capability constraint가 절대적으로 강제된다고 가정하지 않는다.

### 요청 단위 override

```bash
curl -i http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY" \
  -H "Content-Type: application/json" \
  -H "X-OmniRoute-Mode: coding" \
  -H "X-OmniRoute-Budget: 0.02" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "이 patch를 review해줘."}]
  }'
```

header 이름과 허용 값은 설치 version의 API Reference에서 확인한다. proxy가 custom header를 제거하지 않는지도 함께 검증한다.

## 4. Failure injection

### Layer 1: Connection/account

1. 같은 provider에 test connection 두 개를 준비한다.
2. 한 connection을 비활성화하거나 test quota limit에 도달시킨다.
3. 같은 provider의 다른 connection으로 전환되는지 확인한다.
4. call log에서 첫 failure와 선택된 fallback을 연결한다.

### Layer 2: Combo/model

1. primary와 secondary provider로 saved Combo를 만든다.
2. primary를 test 환경에서 unavailable 상태로 만든다.
3. secondary model로 fallback되는지 확인한다.
4. streaming이 duplicate prefix 없이 정상 종료되는지 본다.

### Layer 3: System

1. 동일 `Idempotency-Key`로 짧은 시간 안에 같은 요청을 보낸다.
2. deduplication response header와 upstream call 수를 비교한다.
3. 연속 실패로 circuit이 열리는지 관찰한다.
4. cooldown 이후 half-open probe와 recovery를 확인한다.

> [!CAUTION]
> failure injection은 test account와 staging에서 수행한다. production account를 고의로 lockout하거나 upstream 약관을 위반하는 부하를 만들지 않는다.

## 5. Observability로 policy 검증

단일 평균값보다 distribution과 failure sequence를 본다.

| Signal | 질문 |
|---|---|
| p50/p95/p99 latency | tail latency가 특정 provider/connection에 집중되는가? |
| success/error rate | retry 뒤 성공을 최초 성공처럼 숨기고 있지 않은가? |
| quota headroom | route가 reset window를 고려하는가? |
| estimated cost | provider invoice와 어느 정도 오차가 있는가? |
| `X-OmniRoute-Decision` | 문서화한 strategy와 실제 target이 일치하는가? |
| circuit/lockout state | restart 뒤 상태가 합리적으로 복원되는가? |
| fallback depth | 너무 많은 fallback이 latency와 비용을 키우는가? |

최소 실험 결과 schema:

```text
timestamp
request_id / session_id
requested_model_or_combo
strategy
selected_provider / model / connection
attempt_count
status
input_tokens / output_tokens
estimated_cost
latency_ms
fallback_reason
```

## 6. Security threat model

### Credential at rest

- SQLite의 API key와 OAuth token은 `STORAGE_ENCRYPTION_KEY` 설정 시 AES-256-GCM으로 암호화된다.
- key가 없으면 plaintext passthrough mode다.
- database backup과 encryption key backup의 access control을 분리한다.
- OAuth token refresh와 revocation을 정기적으로 시험한다.

### Network boundary

- local-only면 `127.0.0.1` binding을 유지한다.
- remote access는 TLS, reverse proxy, dashboard auth, scoped API key를 적용한다.
- management route와 client route를 같은 권한으로 공개하지 않는다.
- proxy log와 access log에서 `Authorization` header를 redaction한다.

### Prompt와 output

- external provider를 선택하면 request/response data가 upstream으로 이동한다.
- provider별 retention, training, region, DPA를 별도로 검토한다.
- local-first를 data residency 보장으로 표현하지 않는다.

### Guardrails

prompt-injection detector와 PII masking은 defense-in-depth다. 문서도 injection guard를 best-effort heuristic으로 설명하며 false positive와 false negative가 가능하다. tool permission, sandbox, output validation, human approval을 대체하지 않는다.

## 7. Fusion과 Pipeline

### Fusion

```text
Prompt
  ├─ Model A ─┐
  ├─ Model B ─┼─ Judge model → synthesized answer
  └─ Model C ─┘
```

평가할 것:

- fan-out target 수에 따른 총 token cost
- 가장 느린 branch가 만드는 tail latency
- judge가 minority의 올바른 답을 버리는지
- 동일 prompt가 여러 provider로 전송되는 data exposure

### Pipeline

```text
Input → Step 1: extract → Step 2: critique → Step 3: rewrite → Output
```

평가할 것:

- step별 input/output contract
- 앞 step의 hallucination 전파
- 중간 artifact logging과 민감정보
- 부분 retry가 idempotent한지
- 각 step의 model을 비싼 model로 쓸 필요가 있는지

## 운영 readiness 체크리스트

- [ ] version과 container image를 pin했다.
- [ ] SQLite, config, encryption key의 backup/restore drill을 수행했다.
- [ ] account-level, model-level, system-level failure를 각각 재현했다.
- [ ] client의 streaming, tool call, structured output을 acceptance test에 넣었다.
- [ ] p95/p99 latency와 fallback depth alert를 정의했다.
- [ ] provider 약관과 data handling을 connection별로 검토했다.
- [ ] dashboard와 management API를 public client endpoint와 분리했다.
- [ ] upgrade 전 migration note와 rollback 절차를 확인했다.
- [ ] SQLite single-node 구조가 availability 목표에 맞는지 승인했다.

## Sources

- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/routing/AUTO-COMBO.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/RESILIENCE_GUIDE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/API_REFERENCE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/architecture/ARCHITECTURE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/SECURITY.md

