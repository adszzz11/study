# 03. GPT 모델 & Muon 옵티마이저

## 📌 핵심 개념

autoresearch의 `train.py`에는 **완전한 GPT 모델 구현체**와 **커스텀 Muon+AdamW 옵티마이저**가 들어있다. 에이전트가 수정하는 대상이므로, 각 컴포넌트를 이해해야 에이전트의 실험 결과를 해석할 수 있다.

## 모델 아키텍처 (GPTConfig)

### 기본 설정

```python
@dataclass
class GPTConfig:
    sequence_len: int = 2048    # 컨텍스트 길이 (prepare.py의 MAX_SEQ_LEN)
    vocab_size: int = 32768     # 어휘 크기 (실제는 토크나이저에서 결정: 8192)
    n_layer: int = 12           # 트랜스포머 레이어 수
    n_head: int = 6             # 어텐션 헤드 수
    n_kv_head: int = 6          # KV 헤드 수 (GQA 지원)
    n_embd: int = 768           # 임베딩 차원
    window_pattern: str = "SSSL" # 슬라이딩 윈도우 패턴
```

### 하이퍼파라미터에서 Config 생성

```python
DEPTH = 8              # 레이어 수 (주요 복잡도 노브)
ASPECT_RATIO = 64      # model_dim = depth × aspect_ratio
HEAD_DIM = 128         # 어텐션 헤드 차원

# depth=8, aspect_ratio=64 → base_dim=512
# 512를 HEAD_DIM(128)의 배수로 올림 → model_dim=512
# num_heads = 512 / 128 = 4
```

## 주요 구성 요소

### 1. Attention (CausalSelfAttention)

**Rotary Position Embedding (RoPE)**
```python
def apply_rotary_emb(x, cos, sin):
    d = x.shape[3] // 2
    x1, x2 = x[..., :d], x[..., d:]
    y1 = x1 * cos + x2 * sin
    y2 = x1 * (-sin) + x2 * cos
    return torch.cat([y1, y2], 3)
```
- 절대 위치 인코딩 대신 회전 기반 상대 위치 인코딩
- 외삽(extrapolation)이 가능하여 학습 시퀀스보다 긴 입력 처리 가능

**Flash Attention 3**
```python
y = fa3.flash_attn_func(q, k, v, causal=True, window_size=window_size)
```
- GPU 메모리 효율적 어텐션 계산
- Hopper(H100): `varunneal/flash-attention-3`
- 비-Hopper: `kernels-community/flash-attn3`

**슬라이딩 윈도우 패턴 (SSSL)**
```python
WINDOW_PATTERN = "SSSL"
# S = short window (sequence_len // 2 = 1024)
# L = long window (full sequence_len = 2048)
# 마지막 레이어는 항상 L (전체 컨텍스트 참조)
```
- 하위 레이어: 로컬 패턴 학습 (짧은 윈도우)
- 상위 레이어: 글로벌 패턴 학습 (긴 윈도우)
- 메모리 효율과 성능의 균형

### 2. Value Embedding (ResFormer)

```python
def has_ve(layer_idx, n_layer):
    """교대로 Value Embedding 적용 (마지막 레이어 항상 포함)"""
    return layer_idx % 2 == (n_layer - 1) % 2

# 어텐션에서:
if ve is not None:
    gate = 2 * torch.sigmoid(self.ve_gate(x[..., :32]))
    v = v + gate.unsqueeze(-1) * ve
```
- 입력 토큰의 임베딩을 Value에 잔차 연결
- 입력 의존적 게이트로 혼합 비율 조절
- 게이트 초기값 0 → sigmoid(0)=0.5 × 2 = 1.0 (중립)

### 3. Per-Layer Scaling

```python
# forward에서:
for i, block in enumerate(self.transformer.h):
    x = self.resid_lambdas[i] * x + self.x0_lambdas[i] * x0
    x = block(x, ve, cos_sin, self.window_sizes[i])
```
- `resid_lambdas`: 잔차 스트림 스케일링 (초기값 1.0)
- `x0_lambdas`: 초기 임베딩 스킵 연결 (초기값 0.1)
- 레이어별 학습 가능한 스칼라 → 깊은 네트워크 안정화

### 4. MLP

```python
class MLP(nn.Module):
    def forward(self, x):
        x = self.c_fc(x)        # n_embd → 4 × n_embd
        x = F.relu(x).square()  # ReGLU의 변형: ReLU²
        x = self.c_proj(x)      # 4 × n_embd → n_embd
        return x
```
- ReLU² (Squared ReLU): `F.relu(x).square()`
- 일반 ReLU보다 더 뾰족한 활성화 → 스파스한 표현 학습
- GeLU 대비 계산 효율이 높음

### 5. Logit Softcapping

```python
softcap = 15
logits = self.lm_head(x).float()
logits = softcap * torch.tanh(logits / softcap)
```
- 로짓을 [-15, +15] 범위로 제한
- 극단적 확신을 방지하여 학습 안정성 향상
- Gemma 2에서 도입된 기법

## Muon + AdamW 옵티마이저

### 파라미터별 옵티마이저 할당

```python
# 2D 행렬 파라미터 → Muon (Newton 기반)
# 임베딩, 스칼라 등 → AdamW

param_groups = [
    # AdamW 그룹들
    dict(kind='adamw', params=lm_head_params, lr=0.004),      # unembedding
    dict(kind='adamw', params=embedding_params, lr=0.6),       # wte
    dict(kind='adamw', params=value_embeds_params, lr=0.6),    # value embeds
    dict(kind='adamw', params=resid_params, lr=0.005),         # resid_lambdas
    dict(kind='adamw', params=x0_params, lr=0.5),              # x0_lambdas
    # Muon 그룹들 (행렬 shape별)
    dict(kind='muon', params=matrix_params, lr=0.04),          # 트랜스포머 행렬
]
```

### Muon 옵티마이저란?

**Momentum + Orthogonalization + Newton** 의 합성어.

```
1. Nesterov Momentum — 기울기에 모멘텀 적용
2. Polar Express — 기울기를 직교화 (orthogonalize)
3. NorMuon — 분산 기반 스케일링으로 안정화
4. Cautious Weight Decay — 기울기와 파라미터 방향이 같을 때만 decay
```

**핵심 아이디어**: 2D 행렬 파라미터에는 Adam보다 Newton 방법 기반 최적화가 효율적이다. Polar decomposition으로 기울기를 직교 행렬로 투영하여, 파라미터 공간에서 효율적으로 탐색한다.

### 학습률 스케줄

```python
WARMUP_RATIO = 0.0     # 워밍업 없음
WARMDOWN_RATIO = 0.5   # 후반 50%에서 LR 감소
FINAL_LR_FRAC = 0.0    # 최종 LR = 0

# 진행률 기반 (시간 기준, 스텝 기준 아님!)
def get_lr_multiplier(progress):
    if progress < WARMUP_RATIO:
        return progress / WARMUP_RATIO
    elif progress < 1.0 - WARMDOWN_RATIO:
        return 1.0  # 전반 50%: 전체 LR
    else:
        cooldown = (1.0 - progress) / WARMDOWN_RATIO
        return cooldown  # 후반 50%: 선형 감소 → 0
```

### Weight Decay 스케줄

```python
WEIGHT_DECAY = 0.2

def get_weight_decay(progress):
    return WEIGHT_DECAY * (1 - progress)
    # 시작: 0.2, 끝: 0.0 (선형 감소)
```

## 파라미터 규모

| 구성 요소 | 파라미터 수 (DEPTH=8) |
|-----------|---------------------|
| wte (토큰 임베딩) | ~4.2M |
| value_embeds | ~8.4M |
| lm_head | ~4.2M |
| transformer_matrices | ~33M |
| scalars | 16 |
| **총합** | **~50M** |

## 💻 주요 코드 스니펫

### 전체 Forward Pass 흐름

```python
def forward(self, idx, targets=None):
    x = self.transformer.wte(idx)     # 토큰 → 임베딩
    x = norm(x)                        # RMS Norm
    x0 = x                             # 초기 임베딩 보관 (skip connection용)

    for i, block in enumerate(self.transformer.h):
        # Per-layer scaling
        x = resid_lambdas[i] * x + x0_lambdas[i] * x0
        # Value Embedding (교대 레이어)
        ve = value_embeds[str(i)](idx) if has_ve(i) else None
        # Transformer Block (Attention + MLP)
        x = block(x, ve, cos_sin, window_sizes[i])

    x = norm(x)                        # 최종 RMS Norm
    logits = self.lm_head(x).float()   # 임베딩 → 로짓
    logits = 15 * tanh(logits / 15)    # Softcapping

    if targets is not None:
        loss = cross_entropy(logits, targets)
        return loss
    return logits
```

## ✅ 체크포인트

- [ ] RoPE가 무엇이고 왜 사용하는지 설명할 수 있는가?
- [ ] SSSL 윈도우 패턴의 의미를 이해했는가?
- [ ] Muon과 AdamW가 각각 어떤 파라미터에 적용되는지 아는가?
- [ ] ReLU²가 일반 ReLU와 다른 점을 설명할 수 있는가?
- [ ] Logit softcapping의 목적을 이해했는가?

## ⚠️ 에이전트가 자주 시도하는 변경들

| 변경 | 결과 경향 | 비고 |
|------|----------|------|
| DEPTH 증가 (8→12) | 동일 시간에 더 적은 스텝 → 상충 관계 | 시간 예산 고정이므로 최적점 탐색 필요 |
| MATRIX_LR 증가 | 소폭 개선 가능, 너무 높으면 발산 | 0.02~0.08 범위에서 탐색 |
| GeLU → ReLU² | 대체로 ReLU²가 우세 | 이미 기본값 |
| 모델 너비 2배 | OOM 위험 높음 | DEVICE_BATCH_SIZE 줄여야 |
| QK-Norm 스칼라 추가 | Karpathy의 에이전트가 발견한 실제 개선 | 어텐션 분포 개선 |

## 🔗 더 알아보기

- [[02-experiment-loop|이전: 실험 루프 메커니즘]]
- [[04-program-md-design|다음: program.md 설계 패턴]]
- [nanochat (원본 코드)](https://github.com/karpathy/nanochat)
- [Muon Optimizer 논문/설명](https://github.com/KellerJordan/Muon)
