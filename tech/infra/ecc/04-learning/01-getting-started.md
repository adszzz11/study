---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC Getting Started

## 학습 목표

- Key agreement와 digital signature의 목적 차이를 설명한다.
- X25519 shared secret에 HKDF를 적용해 symmetric key를 유도한다.
- Ed25519 key로 message를 서명·검증한다.
- Key separation, authentication, nonce·encoding 검증의 필요성을 이해한다.

> [!warning]
> 아래 예제는 학습용 protocol skeleton이다. Production에서는 TLS 1.3, HPKE, Noise 같은 검토된 protocol과 high-level library를 사용한다.

## 1. 환경 준비

Python의 `cryptography` package가 제공하는 high-level primitive로 실습한다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install cryptography
```

Private key를 파일에 평문 저장하거나 예제 key를 재사용하지 않는다. 실무에서는 KMS/HSM, OS key store, secret manager와 rotation policy를 사용한다.

## 2. X25519 Key Agreement

양측은 자신의 private key와 상대방 public key로 같은 shared secret을 계산한다. Shared secret 자체는 encryption key가 아니므로 HKDF에 protocol context를 넣어 목적별 key를 유도한다.

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

alice_private = X25519PrivateKey.generate()
bob_private = X25519PrivateKey.generate()

alice_shared = alice_private.exchange(bob_private.public_key())
bob_shared = bob_private.exchange(alice_private.public_key())
assert alice_shared == bob_shared

context = b"ecc-study/v1 client-to-server"

def derive_session_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,  # 실제 protocol의 specification을 따른다.
        info=context,
    ).derive(shared_secret)

alice_key = derive_session_key(alice_shared)
bob_key = derive_session_key(bob_shared)
assert alice_key == bob_key
```

### 무엇이 아직 빠졌는가

- 상대방 public key가 진짜 Alice/Bob의 것인지 확인하는 **authentication**
- Handshake message를 묶는 **transcript binding**
- Key confirmation, replay protection, error handling
- Derived key를 사용할 AEAD와 unique nonce 관리

따라서 이 코드를 임의의 network protocol로 확장하지 말고 TLS 또는 HPKE를 선택한다.

## 3. Ed25519 Signature

Signature는 message를 숨기지 않는다. Private key 소유자가 message에 서명했고 message가 바뀌지 않았음을 public key로 검증한다.

```python
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

signing_key = Ed25519PrivateKey.generate()
verify_key = signing_key.public_key()

message = b"artifact:sha256:0123456789abcdef"
signature = signing_key.sign(message)

try:
    verify_key.verify(signature, message)
    print("valid")
except InvalidSignature:
    print("invalid")
```

검증자는 public key를 신뢰할 근거가 필요하다. X.509 certificate chain, WebAuthn registration, out-of-band fingerprint처럼 trust establishment가 별도로 있어야 한다.

## 4. 용도별 Key Separation

```text
Identity signing key ── Ed25519 ── identity·artifact signature

Static agreement key ── X25519 ── authenticated protocol이 요구할 때만

Ephemeral key ───────── X25519 ── 한 session의 forward secrecy
```

같은 key material을 signing과 key agreement에 재사용하지 않는다. 목적별 key에는 별도 identifier, owner, creation date, algorithm, rotation·revocation 상태를 기록한다.

## 5. Negative Test

```python
tampered = b"artifact:sha256:ffffffffffffffff"

try:
    verify_key.verify(signature, tampered)
    raise AssertionError("tampered message was accepted")
except InvalidSignature:
    pass
```

추가로 malformed public key, 잘못된 길이, non-canonical signature, low-order input, protocol context mismatch를 검증한다. 직접 test vector를 발명하기보다 Wycheproof와 표준 RFC vector를 사용한다.

## 체크포인트

- [ ] ECDH가 encryption과 authentication을 단독으로 제공하지 않는 이유를 설명할 수 있다.
- [ ] Shared secret과 session key의 차이를 설명할 수 있다.
- [ ] HKDF `info`에 protocol name, version, role을 binding할 수 있다.
- [ ] Ed25519 signing key와 X25519 agreement key를 분리했다.
- [ ] 변조 message 검증이 실패하는 negative test를 실행했다.
- [ ] Production에서는 표준 protocol을 선택해야 함을 설명할 수 있다.

## Sources

- https://www.rfc-editor.org/rfc/rfc7748.html
- https://www.rfc-editor.org/rfc/rfc8032.html
- https://www.rfc-editor.org/rfc/rfc5869.html
- https://cryptography.io/en/latest/hazmat/primitives/asymmetric/x25519/
- https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/

