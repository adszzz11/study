---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Overview

## What

Elliptic Curve Cryptography(ECC)는 유한체 위 elliptic curve의 점 연산을 이용하는 public-key cryptography 계열이다. Curve와 base point를 `E, G`, private key를 `d`, public key를 `Q`라 하면 다음 관계를 사용한다.

```text
private key: d
public key:  Q = dG

쉬운 방향: d와 G로 Q 계산 — scalar multiplication
어려운 방향: G와 Q로 d 복구 — ECDLP
```

적절한 curve와 classical computer를 전제로 순방향 계산은 효율적이지만 Elliptic Curve Discrete Logarithm Problem(ECDLP)은 어렵다는 것이 security의 기반이다. `256-bit curve`가 `256-bit security`를 뜻하지는 않으며, P-256과 X25519는 보통 약 128-bit classical security 범주로 본다.

## Why

같은 classical security strength에서 ECC는 RSA나 finite-field cryptography보다 작은 key를 사용한다. NIST 비교에서 약 128-bit security에 RSA/FFC 3072-bit가 대응하는 반면 ECC는 256–383-bit curve 범주가 대응한다.

| 효과 | 의미 |
|---|---|
| 작은 public key·signature | certificate, token, firmware metadata 크기 절감 |
| 짧은 handshake payload | mobile network와 constrained device의 bandwidth 절감 |
| 효율적인 연산 | TLS handshake, signing, verification 비용 개선 가능 |
| 성숙한 protocol 지원 | TLS 1.3, SSH, X.509/PKI, WebAuthn 등에 통합 |

ECC가 message 전체를 직접 암호화하는 것으로 이해하면 안 된다. 실무에서는 public-key operation으로 shared secret을 만든 뒤 symmetric cryptography를 결합한다.

```text
Ephemeral private key
        ↓ scalar multiplication
ECDH / X25519 shared secret
        ↓ HKDF + protocol/context binding
Symmetric session key
        ↓
AES-GCM 또는 ChaCha20-Poly1305
```

ECDH만으로는 상대방 authentication이 생기지 않는다. Certificate signature, PSK, authenticated HPKE처럼 상위 protocol이 identity를 결합해야 한다. Forward secrecy가 필요한 TLS는 일반적으로 ephemeral ECDHE를 사용한다.

## 핵심 Scheme

### Key agreement

- **ECDH/ECDHE**: 양측 public key와 자신의 private key로 같은 shared secret을 계산한다.
- **X25519/X448**: Montgomery curve 기반 Diffie–Hellman function이다. 단순한 interface와 constant-time 구현에 유리하다.
- **HPKE**: DHKEM, KDF, AEAD를 조합한 표준 hybrid public-key encryption 구조다.

### Digital signature

- **ECDSA**: `hash(message)`와 매 서명마다 필요한 nonce `k`를 사용한다. `k` 재사용·편향은 private key 노출로 이어질 수 있다.
- **Deterministic ECDSA**: RFC 6979 방식으로 message와 private key에서 `k`를 유도해 RNG failure 위험을 낮춘다.
- **EdDSA**: Edwards curve 기반 deterministic signature이며 Ed25519·Ed448이 대표적이다.

> [!important]
> X25519와 Ed25519는 관련된 field를 사용하지만 목적, key encoding, protocol 역할이 다르다. key를 변환·재사용하지 말고 용도별로 별도 생성한다.

## 주요 Curve와 선택 기준

| Curve·scheme | 주 용도 | 선택 맥락 |
|---|---|---|
| P-256 / P-384 / P-521 | ECDH, ECDSA | NIST·ANSI, PKI, HSM, FIPS ecosystem |
| X25519 / X448 | Key agreement | TLS·SSH·secure messaging 등 internet protocol |
| Ed25519 / Ed448 | Signature | 고정 encoding과 비교적 단순한 API가 필요한 경우 |
| secp256k1 | ECDH/ECDSA 계열 | Bitcoin·blockchain compatibility 중심 |

`secp256k1`은 blockchain에서 중요하지만 일반-purpose PKI의 자동 기본값은 아니다. Protocol, compliance profile, hardware support, peer interoperability를 먼저 확인한다.

## 핵심 특징과 한계

### 특징

- 작은 key size 대비 높은 classical security strength
- Key agreement와 digital signature에 각각 특화된 scheme 제공
- TLS, PKI, HSM/KMS에 걸친 성숙한 ecosystem
- Ephemeral key를 이용한 forward secrecy 구성 가능

### 한계

- Invalid point, subgroup, encoding 검증 누락에 민감하다.
- Secret-dependent branch·memory access는 timing/cache side-channel을 만들 수 있다.
- ECDSA nonce 품질 실패는 private key를 직접 노출할 수 있다.
- Protocol composition과 domain separation이 틀리면 안전한 primitive도 안전하지 않다.
- Shor's algorithm의 대상이므로 quantum-resistant가 아니다.

## 2025–2026 전환기 관점

- NIST IR 8547은 quantum-vulnerable public-key algorithm의 단계적 퇴출 방향을 제시하지만, 2026-08 기준 **Initial Public Draft**이다. 제시된 연도를 확정 규정처럼 사용하지 않는다.
- NIST는 2025년 SP 800-56A/56C 개정 제안에서 PQC 전환을 우선하며 X25519/X448을 새로운 NIST-approved scheme으로 추가하지 않는 방향을 제안했다. IETF에서 널리 쓰이는 것과 NIST compliance 승인은 별개다.
- IETF는 2026년 TLS 1.3 hybrid key exchange framework와 `X25519MLKEM768`, `SecP256r1MLKEM768`, `SecP384r1MLKEM1024` group을 표준화했다.
- 운영 설계의 핵심은 특정 algorithm 영구 고정이 아니라 inventory, negotiation, telemetry, migration control을 갖춘 crypto agility다.

## Sources

- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://www.rfc-editor.org/rfc/rfc7748.html
- https://www.rfc-editor.org/rfc/rfc6979.html
- https://www.rfc-editor.org/rfc/rfc8032.html
- https://www.rfc-editor.org/rfc/rfc9180.html
- https://csrc.nist.gov/pubs/ir/8547/ipd
- https://www.nist.gov/news-events/news/2025/07/nist-proposes-update-sp-800-56a-and-revise-sp-800-56c

