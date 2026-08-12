---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Deep Dive

## 1. Arithmetic에서 Protocol까지

ECC security는 curve equation 하나가 아니라 여러 layer의 조건이 함께 만족될 때 성립한다.

```text
Field arithmetic / scalar multiplication
                ↓
Curve·point·subgroup·encoding validation
                ↓
ECDH, ECDSA, EdDSA primitive
                ↓
KDF, hash, AEAD, domain separation
                ↓
TLS, SSH, HPKE, PKI protocol state machine
                ↓
Key custody, rotation, telemetry, migration
```

아래 layer가 안전해도 위 layer에서 peer authentication, transcript binding, downgrade prevention이 빠지면 전체 시스템은 안전하지 않다.

## 2. Scalar Multiplication과 Side-channel

Public key `Q = dG`에서 private scalar `d`는 secret이다. 실행 시간, cache access, power consumption이 `d`의 bit pattern에 따라 달라지면 공격자가 반복 관측으로 정보를 복구할 수 있다.

필수 원칙:

- Secret-dependent branch와 table lookup을 피하는 constant-time 구현 사용
- 검증된 library의 high-level API 사용
- Blinding, hardened scalar multiplication, platform-specific assembly를 library에 위임
- Error message와 timing이 secret·validation 상태를 과도하게 드러내지 않도록 설계
- Hardware fault injection 대상이면 fault detection과 device security profile을 함께 평가

## 3. Public Input Validation

Peer가 제공한 public key와 signature는 공격자 입력이다.

| 입력 | 검증 항목 | 실패 시 위험 |
|---|---|---|
| Weierstrass public point | Encoding, field range, curve membership, infinity, subgroup | Invalid-curve·small-subgroup attack |
| X25519 input/output | 정확한 길이, library policy, all-zero shared secret 처리 | Low-order input으로 약한 결과 유도 |
| ECDSA signature | DER/raw format, `r·s` range, canonical policy | Parser confusion, malleability |
| EdDSA signature/key | Canonical encoding, 길이, subgroup 관련 library validation | 다른 구현 간 검증 불일치 |

Protocol마다 허용 encoding과 rejection rule이 다르므로 독자적인 “관대한 parser”를 만들지 않는다.

## 4. ECDSA Nonce Failure

ECDSA signature `(r, s)`는 message hash `z`, private key `d`, per-signature nonce `k`와 관계한다.

```text
s = k⁻¹(z + r·d) mod n
```

같은 `k`로 서로 다른 message를 서명하면 두 식에서 `k`와 `d`를 풀 수 있다. `k`가 편향되거나 일부 bit가 유출되어도 lattice attack으로 위험해질 수 있다.

방어:

- RFC 6979 deterministic ECDSA 또는 검증된 library의 안전한 nonce generation 사용
- Hardware RNG failure와 VM snapshot·rollback 상황을 threat model에 포함
- Signature key를 HSM/KMS에 두고 nonce generation implementation을 검증
- Duplicate `r` monitoring은 보조 탐지 수단으로 활용

## 5. KDF와 Domain Separation

Raw ECDH output은 균일한 application key, identity binding, key confirmation을 자동 제공하지 않는다. HKDF의 `salt`와 `info`는 해당 protocol specification에 따라 transcript와 context를 묶는 데 사용한다.

```text
info = protocol-name || version || cipher-suite || role || transcript-hash
```

서로 다른 목적의 key는 독립 label로 유도한다.

```text
client_write_key
server_write_key
client_write_nonce
server_write_nonce
exporter_secret
```

같은 shared secret에서 같은 label을 재사용하거나 client/server role을 생략하면 reflection, cross-protocol key reuse 위험이 커진다.

## 6. Forward Secrecy와 Authentication

| 구성 | Authentication | Forward secrecy | 비고 |
|---|---|---|---|
| Static ECDH만 사용 | 없음 | 없음 | 설계 피하기 |
| Ephemeral ECDH만 사용 | 없음 | 가능 | Active MITM에 취약 |
| Certificate + ECDHE | Certificate chain·signature | 있음 | TLS 1.3의 일반적 구성 |
| PSK + ECDHE | PSK possession | 있음 | PSK identity·rotation 필요 |
| Authenticated HPKE mode | Sender authentication 구성 | Mode·key 사용법에 의존 | RFC profile을 정확히 따름 |

Forward secrecy는 ephemeral private key가 session 후 삭제되고 long-term key와 분리될 때 의미가 있다.

## 7. Crypto Agility와 PQC Hybrid

ECC 교체 가능성을 config flag 하나로 축소하지 않는다. Agility는 다음 operational capability를 포함한다.

- Service, library, certificate, HSM, protocol별 cryptographic inventory
- Algorithm·parameter·key usage·expiration을 담는 machine-readable metadata
- Negotiation allowlist와 downgrade-resistant policy
- Hybrid group 지원 여부, handshake size·latency·failure telemetry
- Certificate·key rotation rehearsal와 rollback plan
- Store-now-decrypt-later 위험에 따른 data-class별 migration deadline

2026년 TLS hybrid group은 ECC가 즉시 제거되기보다 ML-KEM과 함께 전환기에 사용됨을 보여준다. 다만 “두 algorithm을 이어 붙이면” hybrid가 되는 것은 아니다. RFC가 정의한 encoding, shared-secret combination, transcript binding을 그대로 구현한다.

## 8. Threat Modeling 질문

- 공격자가 public key, certificate, signature bytes를 완전히 제어할 수 있는가?
- Long-term signing key와 ephemeral agreement key의 custody가 분리되어 있는가?
- RNG failure, VM clone, rollback, process fork가 nonce·ephemeral key에 미치는 영향은 무엇인가?
- Protocol negotiation이 downgrade되면 감지·차단되는가?
- Private key compromise 시 과거 session과 미래 artifact에 어떤 영향이 있는가?
- 오늘 수집된 ciphertext가 quantum-capable 미래까지 민감한가?

## 실습 과제

- [ ] RFC test vector와 Wycheproof corpus로 positive·negative test 구성
- [ ] ECDSA signature corpus에서 중복 `r` 탐지기 작성
- [ ] TLS endpoint의 negotiated group과 certificate algorithm inventory 생성
- [ ] Hybrid group 활성화 전후 handshake size·latency·failure rate 비교
- [ ] Key rotation·revocation tabletop exercise 수행

## Sources

- https://www.rfc-editor.org/rfc/rfc6979.html
- https://www.rfc-editor.org/rfc/rfc7748.html
- https://www.rfc-editor.org/rfc/rfc8446.html
- https://www.rfc-editor.org/rfc/rfc9180.html
- https://www.rfc-editor.org/rfc/rfc9954.html
- https://www.rfc-editor.org/rfc/rfc10024.html
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final

