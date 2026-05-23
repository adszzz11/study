# Autoresearch Cheat Sheet

## 빠른 설치 & 실행

```bash
# 설치
git clone https://github.com/karpathy/autoresearch.git && cd autoresearch
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# 데이터 준비 (최초 1회)
uv run prepare.py

# 학습 실행 (baseline)
uv run train.py

# 에이전트 실행 (Claude Code에서)
# "Read program.md and let's kick off a new experiment!"
```

## 3-파일 구조

| 파일 | 역할 | 수정 |
|------|------|------|
| `prepare.py` | 데이터, 토크나이저, 평가 함수 | **읽기 전용** |
| `train.py` | 모델, 옵티마이저, 학습 루프 | **에이전트** |
| `program.md` | 에이전트 지시서 | **사람** |

## 핵심 상수 (prepare.py)

```python
MAX_SEQ_LEN = 2048       # 컨텍스트 길이
TIME_BUDGET = 300        # 5분 고정
EVAL_TOKENS = 40 * 524288  # 검증 토큰 수
VOCAB_SIZE = 8192        # BPE vocab
```

## 기본 하이퍼파라미터 (train.py)

```python
DEPTH = 8                # 레이어 수
ASPECT_RATIO = 64        # dim = depth × ratio
HEAD_DIM = 128           # 어텐션 헤드 차원
TOTAL_BATCH_SIZE = 2**19 # ~524K tokens/step
DEVICE_BATCH_SIZE = 128  # GPU 배치 크기
MATRIX_LR = 0.04         # Muon LR
EMBEDDING_LR = 0.6       # 임베딩 AdamW LR
WEIGHT_DECAY = 0.2       # Cautious WD
WINDOW_PATTERN = "SSSL"  # 슬라이딩 윈도우
WARMDOWN_RATIO = 0.5     # 후반 50% LR 감소
```

## 결과 파싱

```bash
# 핵심 메트릭 추출
grep "^val_bpb:\|^peak_vram_mb:" run.log

# 크래시 디버그
tail -n 50 run.log

# 전체 결과 요약
cat results.tsv
```

## 실험 루프 명령어

```bash
# 브랜치 생성
git checkout -b autoresearch/mar29

# 실험 실행 (출력 리다이렉트 필수!)
uv run train.py > run.log 2>&1

# 결과 좋으면 → keep (자동 전진)
# 결과 나쁘면 → discard
git reset --hard HEAD~1
```

## results.tsv 포맷

```tsv
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR
c3d4e5f	0.000000	0.0	crash	double width (OOM)
```

## Keep/Discard 판단 기준

```
val_bpb 감소          → keep
val_bpb 동일/증가     → discard
크래시 (간단한 버그)   → 수정 후 재실행
크래시 (OOM/설계 결함) → crash 로깅, 스킵
```

## Simplicity Criterion

```
작은 개선 + 많은 복잡도 추가 → 스킵 가능
코드 삭제 + 동일 성능        → 확실한 킵!
동일 성능 + 더 단순한 코드   → 킵
```

## 소규모 환경 조정 가이드

```python
# 작은 GPU/MPS에서 실행 시
DEPTH = 4               # 8 → 4
MAX_SEQ_LEN = 256       # 2048 → 256
TOTAL_BATCH_SIZE = 2**14 # 524K → 16K
WINDOW_PATTERN = "L"     # SSSL → L
vocab_size = 2048        # 8192 → 2048
# + TinyStories 데이터셋 사용
```

## 자율 최적화 루프 범용 공식

```
1. 수정 가능한 파일 1개
2. 측정 가능한 메트릭 1개
3. 고정된 평가 예산
4. keep/discard 규칙
5. 무한 루프 (NEVER STOP)
```

## 주요 링크

| 리소스 | URL |
|--------|-----|
| GitHub | https://github.com/karpathy/autoresearch |
| nanochat | https://github.com/karpathy/nanochat |
| macOS 포크 | https://github.com/miolini/autoresearch-macos |
| MLX 포크 | https://github.com/trevin-creator/autoresearch-mlx |
| Windows 포크 | https://github.com/jsegov/autoresearch-win-rtx |
| AMD 포크 | https://github.com/andyluo7/autoresearch |
| awesome 목록 | https://github.com/alvinunreal/awesome-autoresearch |
