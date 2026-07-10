---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - positional-encoding
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# Positional Encoding - 치트시트

> [[README|목차로 돌아가기]]

---

## 핵심 문장

- Self-attention은 position signal 없이는 token order를 구조적으로 알기 어렵다.
- Sinusoidal PE는 `sin/cos` absolute vector를 embedding에 더한다.
- Relative PE는 `i-j` distance를 attention에 직접 넣는다.
- RoPE는 `Q`, `K`를 position-dependent rotation으로 바꿔 dot product 안에 relative position을 넣는다.
- Long context에서 RoPE는 scaling이 필요하지만, scaling만으로 모든 문제가 해결되지는 않는다.

---

## 공식

### Sinusoidal PE

```text
PE(pos, 2i)   = sin(pos / base^(2i / d_model))
PE(pos, 2i+1) = cos(pos / base^(2i / d_model))
base = 10000
```

### Attention

```text
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
```

### ALiBi

```text
score(i, j) = q_i · k_j + slope_head * distance_bias(i, j)
```

### RoPE

```text
rotate([x1, x2], angle) =
[
  x1 cos(angle) - x2 sin(angle),
  x1 sin(angle) + x2 cos(angle)
]

angle = position * theta_i
```

### Complex view

```text
RoPE(z_m) = z_m * exp(i * m * theta)
phase difference in Q_m · K_n = (m - n) * theta
```

---

## 방식 비교

| 방식 | 어디에 넣나 | 기억할 점 |
|------|-------------|-----------|
| Learned absolute PE | embedding | 쉽지만 train length 밖 약함 |
| Sinusoidal PE | embedding | deterministic, smooth, shift 가능 |
| Relative PE | attention score/value | 거리 관계 직접 모델링 |
| ALiBi | attention score bias | 단순하고 extrapolation 강한 baseline |
| RoPE | Q/K rotation | 현대 LLM 표준, relative position 내장 |
| PI/YaRN/LongRoPE | RoPE scaling | pretrained LLM context extension |
| nD RoPE | axis-wise Q/K rotation | multimodal coordinate에 적합 |

---

## 구현 키워드

```python
keywords = {
    "rotate_half": "[-x2, x1] pair rotation helper",
    "inv_freq": "dimension별 inverse frequency",
    "position_ids": "token별 logical position",
    "cos/sin cache": "position별 rotation cache",
    "rope_theta": "RoPE base",
    "rope_scaling": "long-context scaling config",
}
```

| 체크 | 이유 |
|------|------|
| `head_dim % 2 == 0` | 2D pair rotation이 필요하다. |
| q/k에만 적용 | attention score의 dot product에 position을 넣기 위함이다. |
| dtype/device 일치 | cos/sin cache와 q/k mismatch 방지 |
| KV cache position | decoding에서 과거/현재 position 일관성 필요 |
| scaling config | tokenizer/model/server max length와 함께 맞춰야 한다. |

---

## Long-context 주의점

| 용어 | 뜻 |
|------|-----|
| Context window | 모델이 받을 수 있는 최대 token 수 |
| Effective context | 실제로 정보를 찾아 쓰는 능력 |
| Direct extrapolation | 학습 범위 밖 position을 그대로 사용 |
| Position Interpolation | position index를 학습 범위 안으로 압축 |
| Aliasing | 다른 먼 position의 phase가 비슷해지는 문제 |
| Precision limit | float precision 때문에 phase 차이가 사라지는 문제 |
| Locality bias | 가까운 token을 더 보려는 경향 |

---

## 선택 기준

| 내가 하는 일 | 먼저 고를 것 |
|--------------|--------------|
| 개념 학습/강의 | Sinusoidal PE -> RoPE |
| 작은 Transformer 구현 | Sinusoidal PE 또는 RoPE |
| decoder-only LLM 구현 | RoPE |
| long-context baseline | ALiBi, Position Interpolation |
| pretrained LLM context 확장 | YaRN, LongRoPE 계열 |
| multimodal position | 2D/nD RoPE, M-RoPE |
| RoPE 한계 연구 | CARoPE, Selective RoPE, 2026 theory papers |

---

## 흔한 오해

| 오해 | 정정 |
|------|------|
| RoPE는 absolute position을 버린다. | 각 Q/K는 absolute position으로 회전되고, dot product에서 relative difference가 드러난다. |
| Context window가 길면 long-context 능력이 좋다. | effective retrieval/reasoning은 별도 평가가 필요하다. |
| RoPE base를 키우면 무조건 좋아진다. | position 구분, token 구분, precision 사이 tradeoff가 있다. |
| V에도 RoPE를 적용해야 한다. | 일반적으로 Q/K에 적용해 score에 position을 넣는다. |
| Sinusoidal PE는 RoPE와 무관하다. | sin/cos pair와 rotation 구조가 RoPE 직관의 출발점이다. |

---

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - Transformer/LLM 구성요소 맵
- [[study/tech/ai/litellm]] - long-context model 운영과 routing
- [[study/tech/ai/model-context-protocol-mcp]] - context를 모델 입력이 아니라 tool/resource로 다루는 패턴
