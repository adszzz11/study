---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - positional-encoding
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# Positional Encoding - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

---

## 프로젝트 1. PE 시각화 노트북

### 목표

Integer, binary, sinusoidal PE를 같은 축에서 시각화해 왜 sinusoidal PE가 smooth한지 확인한다.

| 항목 | 내용 |
|------|------|
| 난이도 | 초급 |
| 산출물 | Jupyter notebook 또는 Python script |
| 핵심 개념 | uniqueness, smoothness, frequency |

```python
import matplotlib.pyplot as plt

pe = sinusoidal_pe(seq_len=128, dim=32)
plt.imshow(pe.T, aspect="auto", cmap="coolwarm")
plt.xlabel("position")
plt.ylabel("dimension")
plt.colorbar()
plt.show()
```

체크:

- [ ] binary encoding의 discontinuity를 시각화한다.
- [ ] sinusoidal PE의 dimension별 wavelength 차이를 확인한다.
- [ ] position similarity matrix를 만든다.

---

## 프로젝트 2. RoPE attention score 실험

### 목표

RoPE를 적용하기 전/후 attention score가 relative distance에 따라 어떻게 달라지는지 본다.

| 항목 | 내용 |
|------|------|
| 난이도 | 초급-중급 |
| 산출물 | score heatmap |
| 핵심 개념 | Q/K rotation, relative phase, dot product |

```python
q = torch.randn(128, 64)
k = torch.randn(128, 64)
cos, sin = rope_cache(128, 64)

plain_scores = q @ k.T
rope_scores = apply_rope(q, cos, sin) @ apply_rope(k, cos, sin).T
```

확장:

- [ ] 같은 content vector를 모든 position에 반복해 position effect만 분리한다.
- [ ] `base=10000`, `base=500000` 차이를 비교한다.
- [ ] score를 `abs(i-j)` distance별로 평균낸다.

---

## 프로젝트 3. RoPE scaling toy benchmark

### 목표

Position Interpolation과 direct extrapolation의 차이를 toy retrieval task에서 비교한다.

| 항목 | 내용 |
|------|------|
| 난이도 | 중급 |
| 산출물 | length별 accuracy plot |
| 핵심 개념 | extrapolation, interpolation, effective context |

```text
Task:
  input: random tokens + "KEY=abc123" + query
  output: abc123 위치를 찾아 반환

Compare:
  - no scaling
  - position interpolation
  - larger RoPE base
```

주의:

- Toy task는 실제 LLM long-context 성능을 완전히 대변하지 않는다.
- 같은 context window라도 retrieval, summarization, multi-hop reasoning 성능은 다를 수 있다.

---

## 프로젝트 4. Hugging Face model code 읽기

### 목표

실제 LLM 구현에서 RoPE가 어디에 들어가는지 읽는다.

| 파일/키워드 | 볼 것 |
|-------------|-------|
| `apply_rotary_pos_emb` | q/k에 cos/sin을 적용하는 위치 |
| `rotate_half` | pair rotation 구현 |
| `LlamaRotaryEmbedding` | `inv_freq`, cache, scaling |
| `position_ids` | batch/KV cache에서 position 관리 |
| `rope_scaling` | linear, dynamic, yarn 등 config |

```python
# grep 예시
rg "apply_rotary_pos_emb|rotate_half|rope_scaling|inv_freq" transformers
```

체크:

- [ ] RoPE가 attention projection 후, attention score 계산 전에 적용되는지 확인한다.
- [ ] `past_key_values`가 있을 때 position이 어떻게 증가하는지 본다.
- [ ] model config의 `max_position_embeddings`와 `rope_theta`를 확인한다.

---

## 프로젝트 5. 2D RoPE toy ViT

### 목표

image patch grid에서 x/y axis를 분리해 2D RoPE를 적용한다.

| 항목 | 내용 |
|------|------|
| 난이도 | 중급-고급 |
| 산출물 | toy ViT attention visualization |
| 핵심 개념 | nD coordinate, axis-wise rotation |

```text
patch embedding shape:
  [batch, height, width, dim]

2D position:
  x_position -> dim slice A
  y_position -> dim slice B
```

설계 질문:

- [ ] head dimension을 x/y에 반씩 나눌 것인가?
- [ ] 모든 head가 x/y를 모두 볼 것인가, head별로 나눌 것인가?
- [ ] resolution extrapolation에서 interpolation을 어떻게 할 것인가?

---

## 프로젝트 6. Long-context 논문 요약 카드

### 목표

RoPE scaling과 RoPE 한계 논문을 한 장짜리 비교표로 정리한다.

| 논문 | 구현 변화 | 주장 | 검증할 점 |
|------|-----------|------|-----------|
| Position Interpolation | position index scaling | 32K context extension | short-context retention |
| YaRN | efficient RoPE extension | token/step 효율 | config 민감도 |
| LongRoPE | non-uniform interpolation | 2M token window | effective context |
| Phase Modulation | theory bounds | base feasibility region | 실제 model case와 일치 여부 |
| RoPE limitations | provable failure | long context에서 구분력 한계 | practical severity |

---

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - 논문 읽기와 architecture map 연결
- [[study/tech/ai/litellm]] - long-context model을 실제 API로 비교할 때 참고
- [[study/tech/ai/llm-wiki-study]] - 긴 문서 처리 실험과 연결

