---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - positional-encoding
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# Positional Encoding 시작하기

> [[../README|목차로 돌아가기]] | [[../03-references|이전: 참고자료]] | [[02-deep-dive|다음: 심화]]

---

## 목표

이 문서는 positional encoding을 수식 암기가 아니라 작은 구현으로 이해하는 경로다.

- Self-attention이 왜 position 없이 약한지 확인한다.
- Sinusoidal PE를 직접 만든다.
- RoPE의 핵심 연산인 2D pair rotation을 구현한다.
- `embedding에 더하기`와 `Q/K를 회전하기`의 차이를 구분한다.

---

## 1. Self-attention의 position blindness

같은 token embedding이 여러 위치에 등장하고 position signal이 없으면, 같은 weight에서 나온 query/key/value도 같아질 수 있다.

```python
import torch

torch.manual_seed(0)

d = 8
dog = torch.randn(d)
tokens = torch.stack([
    torch.randn(d),  # The
    dog,             # dog #1
    torch.randn(d),  # chased
    torch.randn(d),  # another
    dog,             # dog #2
])

Wq = torch.randn(d, d)
Wk = torch.randn(d, d)
Wv = torch.randn(d, d)

Q = tokens @ Wq
K = tokens @ Wk
V = tokens @ Wv

scores = Q @ K.T / (d ** 0.5)
attn = scores.softmax(dim=-1)
out = attn @ V

print(torch.allclose(out[1], out[4], atol=1e-6))
```

이 toy example은 실제 모델 전체를 대변하지는 않지만, positional signal이 왜 필요한지 보여준다.

---

## 2. Sinusoidal positional encoding

원래 Transformer의 PE는 dimension pair마다 다른 frequency를 갖는 `sin/cos` signal이다.

```python
import torch

def sinusoidal_pe(seq_len: int, dim: int, base: float = 10000.0):
    position = torch.arange(seq_len).float().unsqueeze(1)
    div_term = torch.exp(
        torch.arange(0, dim, 2).float() * (-torch.log(torch.tensor(base)) / dim)
    )

    pe = torch.zeros(seq_len, dim)
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe

pe = sinusoidal_pe(seq_len=8, dim=16)
print(pe.shape)
```

| 포인트 | 설명 |
|--------|------|
| `position` | token index |
| `div_term` | dimension별 frequency |
| `sin/cos pair` | shift를 rotation으로 표현할 수 있게 한다. |
| `base=10000` | frequency range를 정하는 hyperparameter |

---

## 3. Embedding에 더하기

Sinusoidal PE는 token embedding에 더한다.

```python
batch = 2
seq_len = 8
dim = 16

x = torch.randn(batch, seq_len, dim)
pe = sinusoidal_pe(seq_len, dim)

x_with_pos = x + pe.unsqueeze(0)
print(x_with_pos.shape)
```

장점:

- 구현이 매우 쉽다.
- position vector가 deterministic하다.
- 학습 parameter가 없다.

주의점:

- semantic embedding과 positional signal이 additive하게 섞인다.
- attention score에서 relative distance를 직접 넣는 방식은 아니다.

---

## 4. RoPE 최소 구현

RoPE는 dimension을 2D pair로 나눠 회전한다.

```python
import torch

def rotate_half(x):
    x1 = x[..., ::2]
    x2 = x[..., 1::2]
    return torch.stack((-x2, x1), dim=-1).flatten(-2)

def rope_cache(seq_len: int, dim: int, base: float = 10000.0):
    pos = torch.arange(seq_len).float()
    inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
    freqs = torch.einsum("i,j->ij", pos, inv_freq)
    emb = torch.repeat_interleave(freqs, repeats=2, dim=-1)
    return emb.cos(), emb.sin()

def apply_rope(x, cos, sin):
    return (x * cos) + (rotate_half(x) * sin)

seq_len = 8
head_dim = 16
q = torch.randn(seq_len, head_dim)
k = torch.randn(seq_len, head_dim)

cos, sin = rope_cache(seq_len, head_dim)
q_rot = apply_rope(q, cos, sin)
k_rot = apply_rope(k, cos, sin)

scores = q_rot @ k_rot.T
print(scores.shape)
```

핵심은 `Q`와 `K`에만 적용한다는 점이다. 보통 `V`에는 RoPE를 적용하지 않는다.

---

## 5. Sinusoidal PE vs RoPE

| 항목 | Sinusoidal PE | RoPE |
|------|---------------|------|
| 적용 위치 | input embedding | attention의 `Q`, `K` |
| 방식 | additive | multiplicative rotation |
| 상대 위치 | shift 구조를 통해 간접 표현 | dot product 안에 직접 반영 |
| norm | embedding norm 변경 가능 | rotation이라 norm 보존 |
| 현대 LLM | 기초/교육용으로 중요 | decoder-only LLM 표준 축 |

---

## 6. 체크포인트

- [ ] `sin/cos` pair가 왜 2D rotation과 연결되는지 설명할 수 있다.
- [ ] RoPE가 `Q/K`에 적용되고 `V`에는 보통 적용되지 않는 이유를 말할 수 있다.
- [ ] `position_ids`가 바뀌면 RoPE 결과도 바뀐다는 점을 이해한다.
- [ ] `base`, `head_dim`, `seq_len`이 cos/sin cache shape에 어떤 영향을 주는지 확인한다.

---

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - Transformer 구조 안에서 attention component 복습
- [[study/tech/ai/llm-wiki-study]] - 긴 sequence를 그대로 넣는 방식과 retrieval 방식 비교

