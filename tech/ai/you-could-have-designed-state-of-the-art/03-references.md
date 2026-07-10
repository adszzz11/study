---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - positional-encoding
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Positional Encoding - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. 먼저 읽을 자료

| 우선순위 | 자료 | 왜 읽나 |
|----------|------|---------|
| 1 | [Hugging Face Blog: You could have designed state of the art positional encoding](https://huggingface.co/blog/designing-positional-encoding) | integer -> binary -> sinusoidal -> RoPE로 이어지는 설계 흐름 |
| 2 | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | sinusoidal absolute PE의 원전 |
| 3 | [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) | RoPE의 원 논문 |
| 4 | [Hugging Face Transformers: RoFormer docs](https://huggingface.co/docs/transformers/model_doc/roformer) | 라이브러리 문서 관점의 RoPE 설명 |

```text
읽는 순서:
HF blog -> Attention Is All You Need section 3.5 -> RoFormer -> ALiBi/PI/YaRN/LongRoPE
```

---

## 2. Core papers

### Transformer / sinusoidal PE

- [Vaswani et al., 2017, Attention Is All You Need](https://arxiv.org/abs/1706.03762)
  - Transformer가 recurrence/convolution 없이 attention만으로 sequence를 처리한다는 전환점.
  - `sin/cos` absolute positional encoding을 embedding에 더한다.
  - sinusoidal PE가 longer sequence extrapolation에 도움이 될 수 있다고 설명한다.

### Relative position

- [Shaw et al., 2018, Self-Attention with Relative Position Representations](https://arxiv.org/abs/1803.02155)
  - self-attention이 relative distance representation을 고려하도록 확장한다.
  - absolute position보다 token 간 거리 관계를 직접 모델링한다.
  - relation-aware self-attention으로 일반화할 수 있다.

### RoPE

- [Su et al., 2021, RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)
  - `Q`, `K`를 position-dependent rotation으로 변환한다.
  - absolute position을 rotation matrix로 encode하면서 self-attention score 안에 relative position dependency를 넣는다.
  - sequence length flexibility, relative distance decay, linear attention compatibility를 논의한다.

### ALiBi

- [Press et al., 2021, Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409)
  - positional embedding을 더하지 않고 attention score에 distance-proportional linear bias를 추가한다.
  - 짧은 context로 학습하고 긴 context에서 test하는 extrapolation baseline으로 중요하다.

---

## 3. RoPE scaling / long context

| 자료 | 핵심 아이디어 | 메모 |
|------|---------------|------|
| [Chen et al., 2023, Extending Context Window via Positional Interpolation](https://arxiv.org/abs/2306.15595) | 긴 position index를 학습 구간 안으로 down-scale | LLaMA 계열 32K context extension |
| [Peng et al., 2023, YaRN](https://arxiv.org/abs/2309.00071) | 더 적은 token/step으로 RoPE context extension | open LLM long-context recipe에서 자주 등장 |
| [Ding et al., 2024, LongRoPE](https://arxiv.org/abs/2402.13753) | non-uniform interpolation + progressive extension | 2M token context window 보고 |

### 비교 관점

- `context window length`: 모델이 입력으로 받을 수 있는 최대 token 수
- `effective context`: 실제로 정보를 찾아 쓰는 능력
- `fine-tuning cost`: context extension을 위해 필요한 token/step/GPU 비용
- `short-context retention`: 긴 context를 위해 원래 짧은 context 성능을 잃지 않는지

---

## 4. 2025-2026 최신 쟁점

| 자료 | 핵심 |
|------|------|
| [Veisi et al., 2025, Context-aware Rotary Position Embedding](https://arxiv.org/abs/2507.23083) | `CARoPE`: token/context-dependent frequency pattern으로 RoPE를 context-aware하게 확장 |
| [Movahedi et al., 2025, Selective Rotary Position Embedding](https://arxiv.org/abs/2511.17388) | `Selective RoPE`: input-dependent rotary embedding으로 fixed-angle RoPE 일반화 |
| [Liu, 2026, Rotary Positional Embeddings as Phase Modulation](https://arxiv.org/abs/2602.10959) | RoPE를 phase modulation으로 보고 base, aliasing, precision bound 분석 |
| [Du et al., 2026, RoPE Distinguishes Neither Positions Nor Tokens in Long Contexts, Provably](https://arxiv.org/abs/2605.15514) | long context에서 locality bias 붕괴와 position/token 구분 한계 분석 |

### 읽을 때 질문

- RoPE의 frequency가 static하면 어떤 표현 한계가 생기는가?
- RoPE base를 키우는 것은 왜 만능 해결책이 아닌가?
- 긴 context window와 retrieval 성능은 어떻게 다르게 평가해야 하는가?
- float precision이 positional signal에 직접 영향을 주는 구간은 어디인가?

---

## 5. 구현 참고

| 자료 | 용도 |
|------|------|
| [Hugging Face Transformers RoFormer docs](https://huggingface.co/docs/transformers/model_doc/roformer) | RoPE가 absolute/relative position을 함께 다루는 설명 확인 |
| [Hugging Face blog 원문 GitHub 링크](https://huggingface.co/blog/designing-positional-encoding) | 글의 animation/코드/수식 맥락 확인 |
| `transformers` LLaMA/Qwen/Mistral modeling code | `apply_rotary_pos_emb`, `rotate_half`, RoPE scaling config 확인 |

```python
# 구현 읽을 때 찾을 키워드
keywords = [
    "rotary_emb",
    "apply_rotary_pos_emb",
    "rotate_half",
    "position_ids",
    "rope_scaling",
    "inv_freq",
]
```

---

## 6. 관련 노트

- [[study/tech/ai/ai-ecosystem]] - LLM architecture/paper reading 경로 연결
- [[study/tech/ai/litellm]] - long-context provider/model 선택과 운영
- [[study/tech/ai/llm-wiki-study]] - 긴 문서 지식 처리에서 context strategy 비교

