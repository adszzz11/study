# 01. 3-파일 아키텍처 심층 분석

## 📌 핵심 개념

Autoresearch의 핵심 설계 철학은 **극단적 단순함**이다. 전체 시스템이 3개 파일로 구성된다:

```
autoresearch/
├── prepare.py   ← 고정 인프라 (사람도 에이전트도 건드리지 않음)
├── train.py     ← 실험 대상 (에이전트만 수정)
└── program.md   ← 연구 전략 (사람만 수정)
```

이 구조는 **관심사의 분리(Separation of Concerns)** 를 극한까지 밀어붙인 결과다.

## 각 파일 상세 분석

### 1. `prepare.py` — 고정 인프라 (읽기 전용)

**역할**: 실험의 "물리 법칙" 역할. 모든 실험에 공통인 불변 요소를 담당한다.

```python
# 고정 상수
MAX_SEQ_LEN = 2048       # 컨텍스트 길이
TIME_BUDGET = 300        # 학습 시간 예산 (5분)
EVAL_TOKENS = 40 * 524288  # 검증 토큰 수
```

**포함 요소**:

| 요소 | 설명 |
|------|------|
| `download_data()` | HuggingFace에서 parquet 학습 데이터 다운로드 |
| `train_tokenizer()` | rustbpe로 BPE 토크나이저 학습 (vocab=8192) |
| `Tokenizer` 클래스 | 토크나이저 래퍼 (인코딩/디코딩) |
| `make_dataloader()` | BOS-aligned 데이터로더 (best-fit packing) |
| `evaluate_bpb()` | **평가 함수** — val_bpb 계산 (이것이 Ground Truth) |

**왜 고정?** 평가 기준이 바뀌면 실험 간 비교가 불가능해진다. 과학 실험에서 측정 도구를 바꾸지 않는 것과 같다.

### 2. `train.py` — 실험 대상 (에이전트가 수정)

**역할**: 에이전트의 "실험실". 모든 것이 수정 가능하다.

```python
# 에이전트가 수정할 수 있는 영역들
DEPTH = 8                    # 트랜스포머 레이어 수
ASPECT_RATIO = 64            # model_dim = depth × aspect_ratio
TOTAL_BATCH_SIZE = 2**19     # ~524K tokens/step
MATRIX_LR = 0.04             # Muon 학습률
WINDOW_PATTERN = "SSSL"      # 슬라이딩 윈도우 패턴
```

**에이전트가 바꿀 수 있는 모든 것**:

| 카테고리 | 예시 |
|---------|------|
| **아키텍처** | 레이어 수, 차원, 헤드 수, 어텐션 패턴 |
| **옵티마이저** | 학습률, 모멘텀, weight decay, 스케줄 |
| **학습 루프** | 배치 크기, gradient accumulation, warmup |
| **활성화 함수** | ReLU².square(), GeLU, SiLU 등 |
| **정규화** | RMSNorm, LayerNorm 등 |
| **새로운 기법** | Value Embedding, 잔차 연결 변형 등 |

**핵심**: 에이전트는 Python 코드를 직접 수정한다. 하이퍼파라미터 탐색이 아니라 **코드 수준의 변경**이다.

### 3. `program.md` — 연구 전략 (사람이 수정)

**역할**: 에이전트 조직의 "운영 매뉴얼". Karpathy는 이를 "super lightweight skill"이라 부른다.

**program.md의 핵심 섹션**:

| 섹션 | 내용 |
|------|------|
| Setup | 브랜치 생성, 파일 읽기, 데이터 확인 |
| Experimentation | 수정 가능/불가 범위, 목표 메트릭, 단순성 기준 |
| Output format | 결과 파싱 방법 (grep "^val_bpb:" run.log) |
| Logging | results.tsv 포맷 (commit, val_bpb, memory, status, description) |
| Experiment loop | 무한 루프 규칙 — **절대 멈추지 말 것** |

**가장 중요한 지시**:
```
NEVER STOP: Once the experiment loop has begun, do NOT pause to ask the human
if you should continue. The human might be asleep... The loop runs until
the human interrupts you, period.
```

## 설계 원칙

### 1. "수정 가능한 파일은 하나뿐"

```
에이전트가 수정할 수 있는 것: train.py (1개)
에이전트가 읽을 수 있는 것: prepare.py, README.md, train.py, program.md
에이전트가 할 수 없는 것: 패키지 설치, prepare.py 수정, 평가 함수 변경
```

→ 범위를 좁혀서 에이전트의 실수 영향을 제한하고, diff를 리뷰 가능하게 만든다.

### 2. "사람은 코드가 아닌 전략을 프로그래밍한다"

```
기존 연구 방식:
  사람 → Python 코드 수정 → 실험 실행 → 결과 확인 → 반복

autoresearch 방식:
  사람 → program.md 수정 → 에이전트가 Python 수정 → 실험 실행 → 자동 반복
```

### 3. "Git = 실험 관리 시스템"

```bash
# 실험 시작
git checkout -b autoresearch/mar29

# 실험 성공 (keep)
git commit -m "increase LR to 0.04, val_bpb 0.993"

# 실험 실패 (discard)
git reset --hard HEAD  # 이전 상태로 복귀
```

## ✅ 체크포인트

- [ ] 3개 파일 각각의 역할을 설명할 수 있는가?
- [ ] prepare.py가 왜 고정인지 이해했는가?
- [ ] 에이전트가 train.py에서 바꿀 수 있는 것과 없는 것을 구분할 수 있는가?
- [ ] program.md가 "스킬"인 이유를 설명할 수 있는가?

## ⚠️ 흔한 실수 & 해결법

| 실수 | 해결 |
|------|------|
| prepare.py를 수정하려 함 | program.md에 "DO NOT MODIFY"가 명시됨 |
| 새 패키지 설치 시도 | pyproject.toml에 있는 것만 사용 가능 |
| 결과를 터미널에 출력 | `> run.log 2>&1` 로 리다이렉트 (컨텍스트 오염 방지) |
| results.tsv를 커밋함 | untracked 상태로 유지해야 함 |

## 🔗 더 알아보기

- [[02-experiment-loop|다음: 실험 루프 메커니즘]]
- [program.md 원문](https://github.com/karpathy/autoresearch/blob/master/program.md)
- [Autoresearch Pattern 분석](https://www.mager.co/blog/2026-03-14-autoresearch-pattern/)
