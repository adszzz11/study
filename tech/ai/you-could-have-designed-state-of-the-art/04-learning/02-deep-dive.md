---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - rope
  - long-context
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# RoPE 심화

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]] | [[../05-projects|다음: 프로젝트]]

---

## 1. RoPE의 수학적 핵심

RoPE는 vector dimension을 2개씩 묶고, 각 pair를 position-dependent angle로 회전한다.

```text
[x_1, x_2] -> [
  x_1 cos(m theta) - x_2 sin(m theta),
  x_1 sin(m theta) + x_2 cos(m theta)
]
```

복소수로 보면 더 간단하다.

```text
z_m = x_1 + i x_2
RoPE(z_m) = z_m * exp(i * m * theta)
```

여기서 `m`은 position, `theta`는 dimension pair별 frequency다.

---

## 2. 왜 dot product에 relative position이 들어가는가?

position `m`의 query와 position `n`의 key를 각각 회전한다고 하자.

```text
q_m' = q_m * exp(i * m theta)
k_n' = k_n * exp(i * n theta)
```

복소수 inner product 관점에서는 두 phase의 차이가 남는다.

```text
phase difference = (m - n) * theta
```

즉 attention score는 absolute `m`, `n` 자체보다 `m-n` relative distance에 민감해진다.

| 관점 | 의미 |
|------|------|
| Absolute tracking | 각 vector는 자신의 position angle로 회전된다. |
| Relative modeling | `Q_m · K_n` score에는 phase difference가 반영된다. |
| Norm preservation | rotation은 vector length를 바꾸지 않는다. |
| Frequency bank | 여러 dimension pair가 서로 다른 wavelength를 담당한다. |

---

## 3. RoPE base와 frequency

RoPE의 inverse frequency는 보통 다음처럼 만든다.

```python
inv_freq = 1.0 / (base ** (torch.arange(0, head_dim, 2) / head_dim))
```

| 값 | 의미 |
|----|------|
| `base` | frequency range를 정하는 hyperparameter |
| `head_dim` | attention head 안의 feature dimension |
| 낮은 dimension pair | 높은 frequency, short-range sensitivity |
| 높은 dimension pair | 낮은 frequency, long-range sensitivity |

Base를 키우면 긴 context에서 천천히 변하는 frequency가 늘어날 수 있지만, 모든 문제가 해결되지는 않는다. 2026년 연구들은 base 선택이 position 구분, token 구분, precision 사이 tradeoff를 만든다고 분석한다.

---

## 4. RoPE scaling

### Direct extrapolation

학습 때 `0..4095` position만 봤는데 inference에서 `0..32767`을 그대로 넣는 방식이다.

- 구현은 쉽다.
- 그러나 phase range가 학습 분포를 크게 벗어난다.
- attention score가 불안정해질 수 있다.

### Position Interpolation

긴 position을 학습 구간 안으로 압축한다.

```python
def interpolate_position(pos, train_len, target_len):
    return pos * train_len / target_len
```

장점:

- extrapolation보다 안정적이다.
- pretrained RoPE LLM의 context window 확장에 실용적이다.

약점:

- position resolution이 낮아질 수 있다.
- 보통 fine-tuning이 필요하다.

### YaRN

YaRN은 RoPE scaling을 더 compute-efficient하게 다듬은 방식이다.

- 일부 frequency band를 다르게 조정한다.
- 적은 token/step으로 context extension을 목표로 한다.
- 구현별 hyperparameter 해석이 중요하다.

### LongRoPE

LongRoPE는 non-uniform interpolation과 progressive extension을 결합한다.

```text
original context
  -> non-uniform interpolation
  -> mid-length fine-tuning
  -> second interpolation
  -> very-long context
  -> short-context readjustment
```

핵심은 모든 dimension과 position을 같은 비율로 늘리지 않는다는 점이다.

---

## 5. Long-context failure modes

| Failure mode | 설명 | 확인 방법 |
|--------------|------|-----------|
| Aliasing | 먼 position들이 비슷한 phase pattern을 가질 수 있다. | position similarity heatmap |
| Locality bias collapse | 가까운 token을 선호하는 bias가 긴 길이에서 약해진다. | distance별 attention score 분석 |
| Precision erasure | float precision 한계로 phase 변화가 구분되지 않는다. | dtype별 phase delta 측정 |
| Token-position confusion | position 이동/토큰 교체에도 score가 비슷해질 수 있다. | controlled synthetic task |
| Effective context gap | window는 길지만 실제 retrieval 성능이 낮다. | passkey, needle, long QA benchmark |

---

## 6. nD RoPE

Text는 1D sequence지만 image/video는 좌표축이 여러 개다.

```text
Text:  position = t
Image: position = (x, y)
Video: position = (x, y, t)
```

nD RoPE의 원칙:

- 각 axis의 relative offset을 독립적으로 표현한다.
- x축과 y축 rotation을 무작정 섞지 않는다.
- head dimension을 axis별로 나눌지, head별로 axis를 담당하게 할지 설계가 필요하다.

| 데이터 | 좌표 | 설계 포인트 |
|--------|------|-------------|
| Text | `t` | token order와 distance |
| Image | `x, y` | horizontal/vertical relative position |
| Video | `x, y, t` | spatial relation + temporal order |
| Audio | `t`, frequency bin | time-frequency representation |

---

## 7. 실전 구현 체크

```python
def validate_rope_shapes(q, k, cos, sin):
    assert q.shape == k.shape
    assert q.shape[-1] % 2 == 0
    assert cos.shape[-1] == q.shape[-1]
    assert sin.shape[-1] == q.shape[-1]
```

체크리스트:

- [ ] `head_dim`이 짝수인가?
- [ ] `cos/sin` dtype과 device가 `q/k`와 맞는가?
- [ ] `position_ids`가 packed sequence/KV cache에서 올바른가?
- [ ] FlashAttention 등 fused attention backend 전에 RoPE가 적용되는가?
- [ ] long-context scaling config가 tokenizer/model max length와 함께 맞춰졌는가?
- [ ] evaluation이 단순 max length가 아니라 retrieval/QA/summarization을 포함하는가?

---

## 관련 노트

- [[study/tech/ai/litellm]] - long-context 모델을 실제 서비스에서 선택/라우팅하는 문제
- [[study/tech/ai/model-context-protocol-mcp]] - context를 모델 안에 넣을지 tool로 가져올지의 설계
- [[study/tech/ai/ai-ecosystem]] - Transformer 계열 architecture 변화 추적

