---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC References

## 읽는 순서

| 단계 | 자료 | 확인할 질문 |
|---|---|---|
| 1 | NIST SP 800-57 Part 1 Rev.5 | Security strength와 key lifecycle은 어떻게 대응하는가? |
| 2 | RFC 7748, RFC 8032 | X25519와 Ed25519의 API·encoding은 어떻게 다른가? |
| 3 | RFC 8446, RFC 9180 | Primitive가 TLS·HPKE protocol에 어떻게 조합되는가? |
| 4 | RFC 6979 | ECDSA nonce failure를 deterministic 방식이 어떻게 줄이는가? |
| 5 | NIST IR 8547, CSWP 39 | PQC transition과 crypto agility를 운영에 어떻게 반영하는가? |
| 6 | RFC 9954, RFC 10024 | TLS hybrid key exchange가 무엇을 결합하는가? |

## 표준·권고

| 문서 | 범위 | 메모 |
|---|---|---|
| [NIST SP 800-57 Part 1 Rev.5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) | Key management와 security strength | ECC와 RSA parameter 비교의 기준 |
| [RFC 7748](https://www.rfc-editor.org/rfc/rfc7748.html) | X25519, X448 | Montgomery curve Diffie–Hellman function |
| [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html) | Ed25519, Ed448 | Edwards-curve Digital Signature Algorithm |
| [RFC 6979](https://www.rfc-editor.org/rfc/rfc6979.html) | Deterministic DSA/ECDSA | Per-signature nonce를 결정적으로 생성 |
| [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html) | TLS 1.3 | ECDHE group, HKDF, handshake 구조 |
| [RFC 9180](https://www.rfc-editor.org/rfc/rfc9180.html) | HPKE | KEM + KDF + AEAD composition |

## PQC Transition·Crypto Agility

| 문서 | 상태·의미 |
|---|---|
| [NIST IR 8547](https://csrc.nist.gov/pubs/ir/8547/ipd) | 2026-08 기준 Initial Public Draft. 제시 연도는 확정 규정이 아님 |
| [NIST 2025 SP 800-56A/56C 결정 제안](https://www.nist.gov/news-events/news/2025/07/nist-proposes-update-sp-800-56a-and-revise-sp-800-56c) | 기존 ECC scheme 정비와 PQC 전환 우선순위의 compliance 맥락 |
| [NIST CSWP 39upd1](https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final) | Inventory, API, negotiation, migration control 지침 |
| [RFC 9954](https://www.rfc-editor.org/rfc/rfc9954.html) | TLS 1.3 multiple key exchange mechanism framework |
| [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024.html) | TLS 1.3 ECDHE-MLKEM hybrid group |

## 구현·Library 자료

| 자료 | 용도 | 확인 포인트 |
|---|---|---|
| [libsodium public-key cryptography](https://doc.libsodium.org/public-key_cryptography) | High-level X25519·Ed25519 ecosystem | Low-level primitive보다 목적별 API 우선 |
| [Google Tink](https://developers.google.com/tink) | Keyset·primitive 중심 high-level API | Algorithm choice와 key rotation 추상화 |
| [OpenSSL EVP](https://docs.openssl.org/3.0/man7/evp/) | 범용 cryptographic operation | Low-level EC API 대신 EVP 사용 |
| [libsecp256k1](https://github.com/bitcoin-core/secp256k1) | secp256k1 구현 | Blockchain-specific 최적화와 test |
| [Wycheproof](https://github.com/C2SP/wycheproof) | Known attack·edge-case test vector | Malformed·non-canonical input negative test |

## 검토 체크리스트

- 문서의 publication date와 status가 final인지 draft인지 확인한다.
- Standard가 algorithm을 정의하는지, 특정 compliance regime이 승인하는지 구분한다.
- Curve name뿐 아니라 scheme, encoding, hash, KDF, AEAD 조합까지 기록한다.
- Library 예제는 현재 high-level API인지, deprecated low-level API인지 확인한다.
- Test vector는 정상 경로뿐 아니라 invalid point, low-order input, non-canonical signature를 포함한다.

## Sources

- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://www.rfc-editor.org/rfc/rfc7748.html
- https://www.rfc-editor.org/rfc/rfc8032.html
- https://www.rfc-editor.org/rfc/rfc9180.html
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final

