---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Ecosystem

## 기술 지도

```text
Public-key cryptography
├── Classical
│   ├── ECC
│   │   ├── Key agreement: ECDH, X25519, X448
│   │   ├── Signature: ECDSA, Ed25519, Ed448
│   │   └── Composition: HPKE, TLS ECDHE
│   ├── RSA: RSA-PSS, RSA-OAEP
│   └── Finite-field: DH, DSA
└── Post-quantum
    ├── KEM: ML-KEM
    ├── Signature: ML-DSA
    └── Transition: ECC + PQC hybrid
```

## 경쟁·대안 비교

| 방식 | 기반 문제·대표 scheme | 장점 | 한계 | 2026 권장 위치 |
|---|---|---|---|---|
| ECC | ECDLP; P-256, X25519, ECDSA, Ed25519 | 작은 key/signature, 빠른 handshake, 성숙한 PKI·HSM | 구현 실수·side-channel에 민감, quantum-vulnerable | 기존·단기 classical system의 핵심; 신규 장기 시스템은 agility 필수 |
| RSA | Integer factorization; RSA-PSS/OAEP | 넓은 legacy interoperability, 성숙한 tooling | 128-bit strength에 약 3072-bit key, 큰 certificate, 느린 private operation, quantum-vulnerable | Legacy compatibility나 특정 PKI 요구 |
| Finite-field DH/DSA | Finite-field discrete logarithm | 오래된 표준과 분석 기반 | 큰 parameter/key, 현대 protocol에서 비효율적, quantum-vulnerable | Legacy·제한적 compatibility |
| ML-KEM / ML-DSA | Module lattice | NIST-standardized PQC, quantum-resistant 목표 | Key·ciphertext·signature가 ECC보다 큼, 운영 경험이 새로움 | 장기 기밀성·PQC migration의 주력 |
| ECC + PQC hybrid | X25519+ML-KEM 등 | 한 계열이 깨져도 combiner 설계에 따라 보호 가능 | 큰 ClientHello, 복잡한 negotiation·telemetry·certificate | 2025–2026 transition architecture의 실용적 선택 |
| Symmetric PSK | AES/ChaCha20 및 사전 공유 key | 빠르고 작은 overhead, quantum 공격에도 key 길이 조정 가능 | 안전한 사전 배포·rotation이 어렵고 대규모 identity에 불편 | 제한된 device fleet, 보조 authentication, 폐쇄망 |

## Curve·Scheme 비교

| 선택지 | 목적 | 강점 | 주의점 |
|---|---|---|---|
| P-256 | ECDH, ECDSA | TLS·PKI·HSM·FIPS 지원이 넓음 | Point validation과 encoding 처리 필요 |
| P-384 | ECDH, ECDSA | 더 높은 classical security margin | Key·signature·연산 비용 증가 |
| X25519 | Key agreement | 단순한 API, internet protocol에서 널리 지원 | Signature 용도가 아니며 NIST approval 맥락 별도 확인 |
| Ed25519 | Signature | Deterministic, 고정 encoding, 좋은 ecosystem | Key agreement key로 재사용 금지 |
| secp256k1 | 주로 blockchain signature | Bitcoin ecosystem과 최적화 library | General-purpose PKI 기본값으로 선택하지 않음 |

## Protocol별 위치

| Protocol·영역 | ECC의 역할 | 함께 필요한 요소 |
|---|---|---|
| TLS 1.3 | ECDHE group으로 ephemeral shared secret 생성 | Certificate authentication, HKDF, AEAD |
| SSH | Host/user signature와 key exchange | Host key 검증, negotiation policy |
| X.509 / PKI | CA·leaf certificate의 ECDSA key/signature | Profile, certificate lifecycle, HSM |
| JWT / WebAuthn | ECDSA·EdDSA 기반 assertion signature | Algorithm allowlist, canonical encoding |
| Secure messaging | X25519 계열 ratchet의 key agreement | Identity binding, KDF, forward secrecy |
| Blockchain | secp256k1 등 transaction signature | Canonical signature, wallet key custody |

## 선택 가이드

1. **Protocol profile을 먼저 고른다.** Curve를 독립적으로 고르지 말고 TLS, JOSE, WebAuthn, PKI profile이 허용하는 조합을 확인한다.
2. **Compliance와 interoperability를 분리해 검토한다.** 널리 구현된 X25519가 모든 NIST/FIPS profile에서 승인된다는 뜻은 아니다.
3. **목적별 key를 분리한다.** Signing, static key agreement, ephemeral key agreement에 별도 key pair와 lifecycle을 둔다.
4. **장기 데이터는 hybrid를 검토한다.** Store-now-decrypt-later 위험이 있으면 standardized PQC 또는 hybrid group을 우선 평가한다.
5. **교체 가능성을 설계한다.** Algorithm identifier, key metadata, negotiation, fallback telemetry, rotation runbook을 inventory에 포함한다.

## Hybrid TLS 전환

RFC 9954는 TLS 1.3에서 여러 key exchange mechanism을 결합하는 framework를, RFC 10024는 다음 hybrid group을 정의한다.

```text
X25519MLKEM768
SecP256r1MLKEM768
SecP384r1MLKEM1024
```

Hybrid 도입 시에는 cryptographic strength만 보지 않고 ClientHello 크기, middlebox 호환성, CPU·memory, handshake failure rate, fallback 발생 여부를 함께 관찰한다. Silent fallback은 보안 downgrade를 숨길 수 있으므로 negotiation 결과를 telemetry에 남긴다.

## Sources

- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://www.rfc-editor.org/rfc/rfc8446.html
- https://www.rfc-editor.org/rfc/rfc7748.html
- https://www.rfc-editor.org/rfc/rfc9954.html
- https://www.rfc-editor.org/rfc/rfc10024.html
- https://csrc.nist.gov/projects/post-quantum-cryptography
- https://github.com/bitcoin-core/secp256k1

