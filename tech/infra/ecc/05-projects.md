---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Projects

## 프로젝트 목록

| 난이도 | 프로젝트 | 결과물 | 핵심 학습 |
|---|---|---|---|
| 입문 | Ed25519 artifact verifier | CLI, test vector, trust-key 문서 | Signature와 trust distribution 분리 |
| 입문 | X25519 + HKDF lab | 양측 key derivation test | Raw shared secret, context binding |
| 중급 | TLS ECC inventory | CSV/JSON inventory와 dashboard | Negotiated group, certificate algorithm |
| 중급 | ECC negative-test harness | Malformed input regression suite | Parser·validation boundary |
| 고급 | ECC→hybrid migration lab | Benchmark, rollout·rollback plan | Crypto agility, telemetry, downgrade |

## Project 1: Artifact Signature Verifier

### 목표

Build artifact digest를 Ed25519로 서명하고 배포 단계에서 검증한다. “서명이 유효하다”와 “신뢰한 release key가 서명했다”를 별도 조건으로 다룬다.

### 요구사항

- Artifact 자체 대신 SHA-256 digest와 metadata를 canonical serialization으로 서명
- Trusted public key fingerprint를 repository 외부 trust channel로 배포
- Unknown key, altered artifact, malformed signature, wrong context negative test
- Private signing key는 CI secret store 또는 HSM/KMS에 보관
- Key ID, created_at, expires_at, revoked_at를 inventory에 기록

```text
artifact ──SHA-256──> digest + release metadata
                          │
Ed25519 private key ──sign┘
                          ↓
artifact + metadata + signature + key_id
                          ↓
trusted public key ──verify──> deploy / reject
```

### 완료 조건

- [ ] 1-byte 변조 artifact가 거부된다.
- [ ] 다른 environment의 valid signature가 context mismatch로 거부된다.
- [ ] Revoked key로 만든 signature가 cryptographically valid여도 policy에서 거부된다.

## Project 2: TLS Cryptographic Inventory

### 수집 항목

| 필드 | 예시 |
|---|---|
| Service owner | `payments-platform` |
| Endpoint | `api.example.com:443` |
| TLS version | `TLS 1.3` |
| Negotiated group | `X25519` |
| Certificate public key | `id-ecPublicKey / P-256` |
| Signature algorithm | `ecdsa_secp256r1_sha256` |
| Certificate expiry | ISO 8601 timestamp |
| Library/runtime | OpenSSL·JDK·Go version |
| Hybrid readiness | supported / blocked / unknown |

### 주의사항

- 외부·내부 endpoint 모두 조사하되 승인된 범위에서만 scanning한다.
- Certificate key algorithm과 ephemeral key exchange group을 혼동하지 않는다.
- Client별 negotiation 결과가 다를 수 있으므로 representative runtime으로 측정한다.
- Inventory snapshot만 만들지 말고 owner, refresh cadence, alert rule을 지정한다.

## Project 3: PQC Hybrid Migration Lab

### 실험 설계

1. Baseline TLS 1.3 ECDHE handshake를 측정한다.
2. RFC 10024 hybrid group을 지원하는 isolated test environment를 구성한다.
3. Handshake bytes, CPU time, latency, memory, failure rate를 비교한다.
4. Unsupported peer와 middlebox 동작, negotiated group, fallback telemetry를 기록한다.
5. Canary → staged rollout → rollback decision gate를 문서화한다.

| 지표 | Baseline | Hybrid | 허용 기준 |
|---|---:|---:|---:|
| ClientHello bytes | 측정 | 측정 | Network profile별 정의 |
| p95 handshake latency | 측정 | 측정 | SLO budget 내 |
| Handshake failure rate | 측정 | 측정 | Error budget 내 |
| Hybrid negotiation rate | 0% | 측정 | 대상 client cohort 기준 |
| Silent fallback | 측정 | 측정 | 원칙적으로 0, 사유 추적 |

### Rollout 원칙

- Draft identifier나 private code point를 production standard처럼 고정하지 않는다.
- Supported group allowlist와 library version을 함께 배포한다.
- Rollback은 service availability뿐 아니라 downgrade exposure도 평가한다.
- Data lifetime이 긴 workload부터 우선순위를 높인다.

## 공통 Best Practices

- High-level, maintained cryptographic library를 사용한다.
- Test key와 production key를 완전히 분리한다.
- 정상 test보다 malformed·boundary·cross-context negative test를 먼저 설계한다.
- Log에 private key, raw shared secret, derived session key를 남기지 않는다.
- Benchmark 결과에 CPU architecture, library version, curve·scheme을 기록한다.
- Security review에는 protocol state machine, key lifecycle, failure behavior를 포함한다.

## Sources

- https://www.rfc-editor.org/rfc/rfc8032.html
- https://www.rfc-editor.org/rfc/rfc8446.html
- https://www.rfc-editor.org/rfc/rfc10024.html
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- https://github.com/C2SP/wycheproof

