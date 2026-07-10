---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - positional-encoding
  - rope
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# Positional Encoding - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - positional encoding이란?

`positional encoding`은 Transformer가 token의 **순서(order)**, **위치(position)**, **거리(distance)** 를 사용할 수 있도록 sequence representation에 넣는 신호다.

Transformer의 self-attention은 기본적으로 다음 형태다.

```text
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
```

여기서 `Q`, `K`, `V`는 token embedding에서 선형 변환으로 만들어진다. 만약 두 위치에 같은 token이 있고 positional signal이 없다면, 같은 embedding에서 나온 `Q/K/V`도 같아지기 쉽다. 그래서 모델은 “첫 번째 dog”와 “두 번째 dog”처럼 같은 token이 문장 안에서 다른 역할을 하는 상황을 구분하기 어렵다.

### 한 줄 요약

| 관점 | 설명 |
|------|------|
| 문제 | Self-attention만으로는 token order가 구조적으로 들어오지 않는다. |
| 목표 | 각 token representation에 위치/거리 정보를 주입한다. |
| 현대 표준 | LLM에서는 `RoPE(Rotary Position Embedding)`가 널리 쓰인다. |
| 최신 쟁점 | long context에서는 RoPE scaling, aliasing, precision limit가 핵심이다. |

---

## 2. Why - 왜 필요한가?

### Self-attention의 위치 문제

Self-attention은 sequence를 처리하지만, 연산 자체는 token 간 pairwise similarity를 보는 쪽에 가깝다. 위치 정보를 넣지 않으면 input token의 순서를 바꿔도 attention 구조가 그 차이를 안정적으로 알기 어렵다.

```text
The dog chased another dog
    ^                   ^
  dog #1              dog #2
```

두 `dog`는 같은 token일 수 있지만, 문장 안 역할은 다르다.

- `dog #1`: chase의 주체
- `dog #2`: chase의 대상
- 필요한 정보: absolute index 자체보다 `chased`를 기준으로 왼쪽/오른쪽, 가까움/멀어짐 같은 relation

### 좋은 positional encoding의 조건

Hugging Face 글은 설계 조건을 다음처럼 잡는다.

| 조건 | 의미 |
|------|------|
| Unique encoding | 서로 다른 위치를 구분할 수 있어야 한다. |
| Sequence-length consistency | position 5는 길이 10 문장에서도, 길이 10,000 문장에서도 같은 의미여야 한다. |
| Learnable relation | `p`와 `p+k`의 관계를 모델이 쉽게 배울 수 있어야 한다. |
| Extrapolation | training context보다 긴 sequence에도 어느 정도 버텨야 한다. |
| Deterministic process | encoding 생성 규칙이 안정적이고 학습 가능해야 한다. |
| nD extensibility | text 1D뿐 아니라 image/video/audio 좌표계로 확장 가능해야 한다. |

---

## 3. 설계 흐름

### 3.1 Integer encoding

가장 단순한 생각은 position index를 embedding에 더하는 것이다.

```python
x_with_pos = token_embedding + position_index
```

문제는 position 값의 magnitude가 token embedding scale을 압도한다는 점이다. semantic information과 positional information이 additive하게 섞여 signal-to-noise ratio가 나빠진다.

### 3.2 Binary encoding

position을 binary vector로 표현하면 값 범위와 uniqueness는 좋아진다.

```text
position 252 -> 11111100
```

하지만 binary bit는 위치가 조금만 바뀌어도 discrete jump가 크다. Neural network optimization은 smooth하고 연속적인 signal을 더 선호한다.

### 3.3 Sinusoidal positional encoding

원래 Transformer는 `sin/cos` absolute PE를 token embedding에 더했다.

```text
PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
```

장점:

- deterministic하다.
- 위치마다 여러 frequency의 phase를 갖는다.
- `pos + k` shift가 2D rotation matrix로 표현될 수 있다.
- 학습한 sequence length보다 긴 길이에 대한 extrapolation 가능성을 기대할 수 있다.

한계:

- absolute position vector를 embedding에 더하므로 semantic signal과 position signal이 섞인다.
- attention에서 실제로 중요한 것은 absolute index보다 relative distance인 경우가 많다.

### 3.4 Relative position encoding

Relative PE는 “token i가 몇 번째인가”보다 “token i와 j가 얼마나 떨어져 있는가”를 직접 모델링한다.

```text
score(i, j) = q_i · k_j + bias(i - j)
```

Shaw et al.의 relative position representation, T5-style relative bias, ALiBi 같은 방식이 이 계열에 있다.

### 3.5 RoPE

`RoPE(Rotary Position Embedding)`는 position vector를 embedding에 더하지 않는다. 대신 attention의 `Q`와 `K`를 위치에 따라 회전한다.

```text
q_m' = rotate(q_m, m)
k_n' = rotate(k_n, n)
score(m, n) = q_m' · k_n'
```

핵심 직관:

- feature dimension을 2D pair로 나눈다.
- 각 pair를 position과 frequency에 따라 회전한다.
- rotation은 vector norm을 보존한다.
- dot product 안에 `m - n` relative position 정보가 자연스럽게 들어간다.

복소수 관점에서는 다음처럼 볼 수 있다.

```text
RoPE(x_m) = x_m * exp(i * m * theta)
```

---

## 4. RoPE가 중요한 이유

| 특징 | 설명 |
|------|------|
| Relative signal | `Q_m · K_n` 안에 `m-n` 거리 정보가 들어간다. |
| Norm preservation | rotation은 norm을 바꾸지 않아 additive PE보다 semantic magnitude를 덜 오염시킨다. |
| Efficiency | attention score bias table보다 구현이 간단하고 cache 친화적이다. |
| LLM adoption | LLaMA, Mistral, Qwen 등 현대 decoder-only LLM에서 널리 채택됐다. |
| Extensibility | 2D/3D/nD 좌표별 rotation으로 multimodal model에 확장 가능하다. |

Hugging Face Transformers의 RoFormer 문서도 RoPE가 absolute position tracking과 relative position dependency를 함께 다룰 수 있다고 설명한다.

---

## 5. Long context에서의 긴장

RoPE는 현대 LLM의 기본값에 가깝지만, 긴 context의 완성형은 아니다.

| 이슈 | 설명 |
|------|------|
| Direct extrapolation failure | 학습한 context 밖 position을 그대로 쓰면 attention score가 불안정해질 수 있다. |
| Aliasing | 서로 다른 먼 위치가 phase 관점에서 구분되기 어려워질 수 있다. |
| RoPE base tradeoff | base를 키우면 token 구분과 position 구분 사이 tradeoff가 생긴다. |
| Floating-point precision | 너무 큰 base/position에서는 작은 phase 변화가 수치적으로 사라질 수 있다. |
| Locality bias collapse | 긴 context에서 가까운 위치를 선호하는 inductive bias가 약해질 수 있다. |

그래서 `Position Interpolation`, `YaRN`, `LongRoPE` 같은 RoPE scaling 기법이 등장했다.

---

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - Transformer component로서 positional encoding 위치 잡기
- [[study/tech/ai/litellm]] - long-context model 선택과 provider routing 관점
- [[study/tech/ai/llm-wiki-study]] - 긴 문서 처리에서 context와 retrieval의 역할 분리

---

## References

- [Hugging Face Blog: You could have designed state of the art positional encoding](https://huggingface.co/blog/designing-positional-encoding)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)
- [Hugging Face Transformers: RoFormer](https://huggingface.co/docs/transformers/model_doc/roformer)
