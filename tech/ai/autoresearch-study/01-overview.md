# Part 1: Overview

## Autoresearch란?

Andrej Karpathy가 2026년 3월 7일 공개한 오픈소스 프로젝트로, **AI 코딩 에이전트가 밤새 자율적으로 ML 실험을 반복**하여 모델 성능을 개선하는 프레임워크다.

핵심 아이디어는 단순하다:

> 에이전트에게 학습 코드를 주고 → 코드 수정 → 5분 학습 → 결과 평가 → 유지 or 폐기 → 반복

사람이 잠든 동안 **시간당 ~12건, 하룻밤 ~100건**의 실험이 자동으로 수행된다.

## 탄생 배경

- **nanochat** (Karpathy의 소형 ChatGPT 학습 코드)에서 파생
- "코드 에이전트가 충분히 좋아졌으니, 연구자 역할도 시켜보자"는 발상
- 630줄 Python + 1개 Markdown으로 극단적 단순함 추구

```
"One day, frontier AI research used to be done by meat computers
in between eating, sleeping, having other fun... That era is long gone."
— Karpathy, README 서문
```

## 핵심 개념

### 1. 3-파일 아키텍처

| 파일 | 역할 | 수정 가능 |
|------|------|-----------|
| `prepare.py` | 데이터 다운로드, 토크나이저, 평가 함수 (고정) | **X** (읽기 전용) |
| `train.py` | 모델, 옵티마이저, 학습 루프 | **O** (에이전트가 수정) |
| `program.md` | 에이전트 지시서 (실험 규칙) | **O** (사람이 수정) |

### 2. 고정 시간 예산 (Fixed Time Budget)

- 모든 실험은 정확히 **5분** 동안 실행
- 모델 크기, 배치 크기, 아키텍처가 달라도 동일 시간 → **공정한 비교** 가능
- 플랫폼(GPU) 종류에 따라 절대 성능은 다르지만, 같은 GPU 내에서는 비교 가능

### 3. 단일 메트릭: val_bpb

- **Validation Bits Per Byte** — 낮을수록 좋음
- vocab size에 독립적 → 아키텍처 변경해도 비교 가능
- 기본 baseline (H100): ~0.9979

### 4. Keep/Discard 규칙

```
if val_bpb_new < val_bpb_current:
    git commit (keep, 브랜치 전진)
else:
    git reset (discard, 원래 상태로 복귀)
```

### 5. Simplicity Criterion

> 동일 성능이면 더 단순한 코드가 승리. 코드를 삭제해서 성능이 같거나 나아지면? → 확실한 킵.

## 장단점

| 장점 | 단점 |
|------|------|
| 극단적 단순함 (630줄) | NVIDIA GPU 필수 (기본) |
| 밤새 100건+ 실험 자동화 | 검증 세트 과적합(overfitting) 위험 |
| 에이전트 종류 무관 (Claude, Codex 등) | 5분 예산으로는 대형 모델 실험 불가 |
| 결과가 git 히스토리로 자동 추적 | 발견된 개선이 다른 규모로 전이 불확실 |
| "연구 조직을 Markdown으로 프로그래밍" | 에이전트 비용 (API 호출) 발생 |
| MIT 라이선스 | 단일 GPU 한정 (분산 미지원) |

## 주요 사용 사례

### 1. 자율 ML 연구
- LLM 학습 최적화 (아키텍처, 하이퍼파라미터 탐색)
- Karpathy 본인: 700건 실험 → 20개 개선 발견 → **11% 속도 향상**

### 2. 하룻밤 실험 자동화
- Shopify CEO Tobi Lütke: 37건 실험 → **19% 성능 향상**
- 분산 에이전트 35개: 333건 실험 자율 수행

### 3. 자율 연구 패턴의 템플릿
- 프롬프트/스킬 최적화
- CI/CD 파이프라인 성능 개선
- 시스템 프롬프트 자동 튜닝

## 채택 / 영향력

| 지표 | 수치 |
|------|------|
| GitHub Stars | 59,600+ (2026-03-29 기준) |
| Forks | 7,400+ |
| 공개 후 5일 만에 | 25,000 Stars |
| X 발표 조회수 | 8,600,000+ |
| 주요 포크 | macOS, Windows, AMD, MLX, WebGPU |

> "All LLM frontier labs will do this. It's the final boss battle." — Karpathy

## val_bpb 개선 기록 (H100)

| 실험 횟수 | 시작 val_bpb | 최종 val_bpb | 개선율 |
|-----------|-------------|-------------|--------|
| 89건 | 0.9979 | 0.9773 | -2.06% |
| 126건 | 0.9979 | 0.9697 | -2.82% |
| ~910건 (클러스터) | 1.003 | 0.974 | -2.87% |
