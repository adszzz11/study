---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Tool Study

> **한 줄 정의**: ECC(Elliptic Curve Cryptography)는 유한체 위 elliptic curve의 ECDLP를 이용해 작은 key size로 key agreement와 digital signature를 제공하는 public-key cryptography 계열이다.

## Overview

ECC는 하나의 algorithm이 아니라 curve, key agreement, signature, encoding, KDF를 아우르는 기술군이다. 대표적으로 ECDH/X25519는 shared secret을 만들고, ECDSA/EdDSA는 message의 무결성과 발신자를 검증한다.

Classical 128-bit security를 목표로 할 때 RSA/FFC는 대략 3072-bit parameter가 필요한 반면, ECC는 256–383-bit curve로 비슷한 security strength를 제공한다. 따라서 certificate 크기, handshake bandwidth, key storage가 중요한 TLS, SSH, PKI, mobile·IoT 환경에 적합하다.

> [!warning]
> ECC는 quantum-resistant가 아니다. 장기 기밀성이 필요한 신규 시스템은 ECC-only 고정보다 algorithm negotiation과 ECC+PQC hybrid migration을 설계해야 한다.

| 기능 | 대표 scheme | 실제 역할 |
|---|---|---|
| Key agreement | ECDHE, X25519, X448 | shared secret 생성 후 HKDF로 session key 유도 |
| Digital signature | ECDSA, Ed25519, Ed448 | artifact, certificate, transaction의 서명·검증 |
| Hybrid encryption | DHKEM 기반 HPKE | ECC KEM + KDF + AEAD로 recipient에게 암호화 |

## Learning Path

- [ ] [[tech/infra/ecc/01-overview|Overview]] — What/Why와 핵심 primitive 이해
- [ ] [[tech/infra/ecc/02-ecosystem|Ecosystem]] — RSA, PQC, hybrid 방식 비교
- [ ] [[tech/infra/ecc/03-references|References]] — 표준과 검증 자료 찾기
- [ ] [[tech/infra/ecc/04-learning/01-getting-started|Getting Started]] — 안전한 high-level API로 ECDH·서명 실습
- [ ] [[tech/infra/ecc/04-learning/02-deep-dive|Deep Dive]] — validation, side-channel, protocol composition 학습
- [ ] [[tech/infra/ecc/05-projects|Projects]] — inventory·interop·migration 프로젝트 수행
- [ ] [[tech/infra/ecc/cheatsheet|Cheatsheet]] — curve와 구현 점검표 복습

## When To Use

- TLS 1.3, SSH, X.509/PKI처럼 ECC interoperability가 이미 확립된 protocol
- certificate, signature, handshake 크기와 latency가 중요한 mobile·IoT·embedded 환경
- HSM/KMS 및 FIPS 요구 때문에 P-256/P-384 기반의 성숙한 ecosystem이 필요한 경우
- internet protocol에서 단순한 key agreement API와 폭넓은 구현 지원이 필요한 경우의 X25519
- 기존 classical system을 유지하면서 crypto agility와 PQC hybrid 전환을 준비하는 경우

## When Not To Use

- 수십 년 뒤에도 기밀이어야 하는 데이터를 ECC-only로 보호하는 신규 설계
- 검증된 library 없이 curve arithmetic, point parsing, nonce 생성을 직접 구현하려는 경우
- ECDH shared secret을 HKDF나 authentication 없이 곧바로 encryption key로 쓰려는 경우
- legacy interoperability가 RSA만 허용하거나, 반대로 규제 profile이 선택한 curve를 지원하지 않는 경우
- encryption, signing, key agreement에 하나의 key pair를 재사용하려는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/ecc/01-overview|ECC Overview]]
- [[tech/infra/ecc/02-ecosystem|ECC Ecosystem]]

## Sources

- https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- https://www.rfc-editor.org/rfc/rfc8446.html
- https://www.rfc-editor.org/rfc/rfc9180.html
- https://www.rfc-editor.org/rfc/rfc9954.html
- https://www.rfc-editor.org/rfc/rfc10024.html
- https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
