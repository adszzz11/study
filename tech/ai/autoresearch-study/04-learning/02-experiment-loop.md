# 02. 실험 루프 메커니즘

## 📌 핵심 개념

Autoresearch의 심장은 **무한 실험 루프**다. 에이전트가 쉬지 않고 가설 → 구현 → 실행 → 평가 → 의사결정을 반복한다.

```
LOOP FOREVER:
  1. git 상태 확인 (현재 브랜치/커밋)
  2. train.py 수정 (실험 아이디어 구현)
  3. git commit
  4. 실험 실행: uv run train.py > run.log 2>&1
  5. 결과 파싱: grep "^val_bpb:\|^peak_vram_mb:" run.log
  6. 크래시 시: tail -n 50 run.log → 디버그 or 스킵
  7. results.tsv에 기록
  8. val_bpb 개선 → keep (브랜치 전진)
  9. val_bpb 미개선 → discard (git reset)
```

## 루프 플로우차트

```
┌──────────────────┐
│  아이디어 생성    │ ← 에이전트가 이전 실험 결과, 코드, 논문 참고
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  train.py 수정    │ ← 아키텍처, HP, 옵티마이저 등
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  git commit       │ ← 변경사항 기록 (나중에 diff 리뷰 가능)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  실행 (5분 학습)  │ ← uv run train.py > run.log 2>&1
└────────┬─────────┘
         │
         ├──── 크래시? ──→ 디버그 시도 ──→ 실패 시 "crash" 로깅 후 스킵
         │
         ▼
┌──────────────────┐
│  결과 파싱        │ ← val_bpb, peak_vram_mb 추출
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 개선됨?    안됨?
    │         │
    ▼         ▼
  KEEP     DISCARD
 (전진)    (복귀)
    │         │
    └────┬────┘
         │
         ▼
    다음 아이디어 → (루프 처음으로)
```

## 실행 상세

### 1. 실험 실행

```bash
# 모든 출력을 파일로 리다이렉트 (컨텍스트 윈도우 오염 방지!)
uv run train.py > run.log 2>&1
```

**왜 리다이렉트?**
- 학습 로그가 에이전트의 컨텍스트 윈도우를 채우면 이전 맥락을 잊음
- `tee` 사용 금지 — stdout으로 출력하면 안 됨
- 필요한 정보만 `grep`으로 추출

### 2. 결과 파싱

```bash
# 핵심 메트릭만 추출
grep "^val_bpb:\|^peak_vram_mb:" run.log

# 출력 예시:
# val_bpb:          0.993200
# peak_vram_mb:     45060.2
```

**결과가 비어 있으면?** → 크래시. `tail -n 50 run.log`로 스택 트레이스 확인.

### 3. 의사결정 규칙

```python
if val_bpb_new < val_bpb_best:
    # KEEP — 개선! 브랜치를 전진시킨다
    status = "keep"
    val_bpb_best = val_bpb_new
elif val_bpb_new >= val_bpb_best:
    # DISCARD — 미개선. git reset으로 복귀
    status = "discard"
    # git reset --hard HEAD~1
elif crashed:
    # CRASH — 로그 분석 후 판단
    status = "crash"
    # 간단한 버그(타이포, import 누락) → 수정 후 재실행
    # 근본적 문제(OOM, 설계 결함) → 스킵
```

### 4. 결과 기록 (results.tsv)

```tsv
commit	val_bpb	memory_gb	status	description
a1b2c3d	0.997900	44.0	keep	baseline
b2c3d4e	0.993200	44.2	keep	increase LR to 0.04
c3d4e5f	1.005000	44.0	discard	switch to GeLU activation
d4e5f6g	0.000000	0.0	crash	double model width (OOM)
```

**TSV 규칙**:
- 탭으로 구분 (쉼표는 description에서 깨짐)
- results.tsv는 **커밋하지 않음** (untracked 유지)
- val_bpb 0.000000 = 크래시

## 시간 관리

### 고정 5분 예산

```python
TIME_BUDGET = 300  # prepare.py에서 고정

# train.py의 학습 루프
while True:
    # ... 학습 ...
    if step > 10 and total_training_time >= TIME_BUDGET:
        break
```

**시간 예산의 장점**:
1. 모든 실험이 동일 시간 → 공정 비교
2. 시간당 ~12건 실험 예측 가능
3. 모델 크기를 키워도 "5분 안에 최선"을 찾게 됨
4. 해당 GPU에 최적화된 설정을 자동 발견

**타임아웃 규칙**:
- 10분 초과 → kill & crash 처리
- 학습 시작 전 10 step은 warmup (torch.compile 컴파일 시간 제외)

### 실험 처리량

| GPU | 실험/시간 | 하룻밤 (8시간) |
|-----|----------|---------------|
| H100 | ~12 | ~96 |
| H200 | ~12 | ~96 |
| RTX 4090 (포크) | ~10-12 | ~80-96 |
| MPS (포크) | ~8-10 | ~64-80 |

## 💻 실전 실행 예시

### 첫 번째 실험: Baseline 확립

```bash
# 1. 브랜치 생성
git checkout -b autoresearch/mar29

# 2. 원본 train.py 그대로 실행
uv run train.py > run.log 2>&1

# 3. 결과 확인
grep "^val_bpb:" run.log
# val_bpb:          0.997900

# 4. results.tsv 초기화
echo -e "commit\tval_bpb\tmemory_gb\tstatus\tdescription" > results.tsv
# baseline 기록 추가
```

### N번째 실험: 학습률 증가

```bash
# 1. train.py에서 MATRIX_LR = 0.04 → 0.06
# 2. git commit -m "try higher matrix LR 0.06"
# 3. uv run train.py > run.log 2>&1
# 4. grep "^val_bpb:" run.log
#    val_bpb: 0.991500  ← 개선! keep!
# 5. results.tsv에 기록
```

### 크래시 처리 예시

```bash
# 실험: 모델 너비 2배
# uv run train.py > run.log 2>&1
# grep 결과 비어 있음 → 크래시!

tail -n 50 run.log
# RuntimeError: CUDA out of memory.
# Tried to allocate 2.00 GiB...

# OOM → 근본적 문제 → 스킵, "crash" 로깅
# git reset --hard HEAD~1
```

## Simplicity Criterion (단순성 기준)

program.md에 명시된 중요한 판단 기준:

```
"0.001 val_bpb 개선 + 20줄 hacky 코드 추가" → 아마도 keep하지 않음
"0.001 val_bpb 개선 + 코드 삭제"           → 확실히 keep
"~0 개선 + 훨씬 단순한 코드"                → keep
```

핵심: **복잡도 대비 개선 폭**을 평가. 같은 성능이면 단순한 쪽이 승리.

## ✅ 체크포인트

- [ ] 루프의 9단계를 순서대로 설명할 수 있는가?
- [ ] keep/discard 판단 기준을 이해했는가?
- [ ] 왜 출력을 파일로 리다이렉트하는지 설명할 수 있는가?
- [ ] 크래시 시 "수정 후 재실행" vs "스킵" 판단을 설명할 수 있는가?
- [ ] Simplicity Criterion을 적용한 의사결정 예시를 들 수 있는가?

## ⚠️ 흔한 실수 & 해결법

| 실수 | 해결 |
|------|------|
| `tee` 사용하여 stdout에 출력 | `> run.log 2>&1` 만 사용 |
| 에이전트가 "계속할까요?" 물어봄 | program.md에 "NEVER STOP" 명시 |
| 10분 넘는 실험 방치 | 타임아웃 규칙: 10분 초과 → kill |
| results.tsv를 git commit | untracked로 유지해야 함 |
| 모든 크래시에 디버그 시도 | OOM 등 근본적 문제는 바로 스킵 |

## 🔗 더 알아보기

- [[01-three-file-architecture|이전: 3-파일 아키텍처]]
- [[03-model-architecture|다음: GPT 모델 & Muon 옵티마이저]]
- [program.md 원문](https://github.com/karpathy/autoresearch/blob/master/program.md)
