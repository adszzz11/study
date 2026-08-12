---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Cheatsheet

## 한눈에 보기

| 목적 | 권장 개념 | 하지 말 것 |
|---|---|---|
| Key agreement | ECDHE/X25519 → HKDF → AEAD | Raw shared secret을 key로 직접 사용 |
| Signature | ECDSA 또는 Ed25519/Ed448 | Signature를 encryption으로 오해 |
| Hybrid encryption | 표준 HPKE profile | EC point에 message 직접 매핑 |
| Forward secrecy | Session별 ephemeral private key | Static ECDH만 사용 |
| PQC transition | Standardized ECC+PQC hybrid, crypto agility | ECC-only 장기 고정 |

## 핵심 식·용어

```text
Public key: Q = dG
d: private scalar
G: base point
Q: public point
ECDLP: G와 Q로 d를 찾기 어려운 문제
```

- P-256/X25519의 `256`은 대략 128-bit classical security 범주이지 256-bit security가 아니다.
- ECDH는 shared secret을 만들지만 peer authentication을 자동 제공하지 않는다.
- Signature는 authenticity·integrity를 제공하지만 confidentiality를 제공하지 않는다.
- ECC는 Shor's algorithm에 취약하므로 quantum-resistant가 아니다.

## Scheme 선택

| Scheme | 용도 | 대표 맥락 |
|---|---|---|
| P-256 ECDH/ECDSA | Agreement / signature | PKI, HSM, FIPS profile |
| P-384 ECDH/ECDSA | 더 높은 classical margin | 특정 compliance·high assurance |
| X25519 | Agreement only | TLS, SSH, secure messaging |
| Ed25519 | Signature only | Artifact, identity, application signature |
| secp256k1 | 주로 blockchain | Bitcoin ecosystem |

## 안전한 Key Agreement Pipeline

```text
Generate ephemeral key
  → parse·validate peer key
  → ECDH/X25519
  → reject invalid/all-zero result per protocol
  → HKDF-Extract/Expand with context
  → derive separate directional keys/nonces
  → AEAD
  → erase ephemeral private material
```

## 구현 체크리스트

- [ ] 직접 curve arithmetic을 구현하지 않고 high-level library를 사용한다.
- [ ] Secret-dependent branch·memory access가 없는 hardened implementation을 사용한다.
- [ ] Public key, point, subgroup, encoding을 protocol 규칙대로 검증한다.
- [ ] ECDSA nonce 재사용을 막고 deterministic ECDSA를 검토한다.
- [ ] ECDH output에 HKDF와 protocol/context binding을 적용한다.
- [ ] Signing, agreement, encryption key를 분리한다.
- [ ] Private key를 HSM/KMS/secure store에 보관하고 rotation한다.
- [ ] Malformed, low-order, non-canonical input negative test를 포함한다.
- [ ] Algorithm inventory, negotiation, migration, rollback을 운영한다.

## ECDSA 사고 대응 단서

```text
동일 signing key에서 signature의 r 중복 발견
  → nonce reuse 가능성
  → signing 즉시 중단
  → key revoke·rotate
  → 영향받은 signature와 artifact 조사
```

`r` 중복이 없다고 nonce가 안전하다는 뜻은 아니다. Bias나 partial leakage도 위험하므로 검증된 deterministic implementation을 사용한다.

## 자주 하는 실수

| 실수 | 수정 |
|---|---|
| `X25519 == Ed25519`로 간주 | 역할·encoding이 다른 별도 key를 생성 |
| ECDH만으로 authenticated channel 구성 | Certificate, PSK, authenticated protocol 결합 |
| Curve 이름만 inventory에 기록 | Scheme, usage, KDF, hash, owner, expiry도 기록 |
| 모든 invalid input을 normalize해 수용 | RFC와 library의 strict rejection rule 적용 |
| “PQC 준비”를 algorithm config로만 처리 | Negotiation, telemetry, certificate, rollout 포함 |
| Draft timeline을 확정 규정으로 취급 | 문서 status와 적용 compliance profile 확인 |

## 표준 바로가기

- Security strength: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- X25519/X448: https://www.rfc-editor.org/rfc/rfc7748.html
- Deterministic ECDSA: https://www.rfc-editor.org/rfc/rfc6979.html
- Ed25519/Ed448: https://www.rfc-editor.org/rfc/rfc8032.html
- TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446.html
- HPKE: https://www.rfc-editor.org/rfc/rfc9180.html
- TLS hybrid framework: https://www.rfc-editor.org/rfc/rfc9954.html
- ECDHE-MLKEM groups: https://www.rfc-editor.org/rfc/rfc10024.html

## Sources

- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://www.rfc-editor.org/rfc/rfc7748.html
- https://www.rfc-editor.org/rfc/rfc6979.html
- https://www.rfc-editor.org/rfc/rfc8032.html
- https://www.rfc-editor.org/rfc/rfc9180.html
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final

