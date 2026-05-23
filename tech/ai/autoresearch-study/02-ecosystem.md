# Part 2: Ecosystem

## 관련 용어 맵

```
                    ┌─────────────────────────┐
                    │   Autonomous Research    │
                    │      (자율 연구)          │
                    └──────────┬──────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼──────┐ ┌──────▼───────┐ ┌──────▼───────┐
    │  AI Code Agent │ │  ML Training │ │  Self-Improve │
    │ (코딩 에이전트) │ │  (모델 학습)  │ │  (자기 개선)  │
    └─────────┬──────┘ └──────┬───────┘ └──────┬───────┘
              │               │                │
    ┌─────────▼──────┐ ┌──────▼───────┐ ┌──────▼───────┐
    │ Claude Code    │ │ nanochat     │ │ program.md   │
    │ Codex CLI      │ │ nanoGPT      │ │ CLAUDE.md    │
    │ Aider          │ │ PyTorch      │ │ Skills       │
    │ Cursor Agent   │ │ Flash Attn 3 │ │ Eval Loops   │
    └────────────────┘ └──────────────┘ └──────────────┘
```

## 함께 쓰는 기술 스택

| 계층 | 기술 | 역할 |
|------|------|------|
| **에이전트** | Claude Code, OpenAI Codex, Aider | `program.md`를 읽고 자율 실험 수행 |
| **프레임워크** | PyTorch 2.9+ | 모델 학습 & `torch.compile` |
| **어텐션** | Flash Attention 3 (via `kernels`) | 효율적 어텐션 연산 |
| **패키지 매니저** | uv | 빠른 Python 의존성 관리 |
| **토크나이저** | rustbpe + tiktoken | BPE 토크나이저 학습 & 인코딩 |
| **데이터** | climbmix-400b (HuggingFace) | 학습/검증 데이터셋 |
| **옵티마이저** | Muon + AdamW (커스텀) | 행렬 파라미터(Muon) + 임베딩(AdamW) |
| **GPU** | NVIDIA H100 (권장) | 학습 실행 환경 |
| **버전 관리** | Git branch per experiment | 실험 추적 & keep/discard |

## 경쟁/대안 기술 비교

### Autoresearch vs 관련 도구

| 특성 | Autoresearch | OpenAI Codex | Aider | SWE-Agent |
|------|-------------|-------------|-------|-----------|
| **목적** | 자율 ML 연구 | 범용 코딩 에이전트 | 대화형 코딩 | 이슈 해결 |
| **도메인** | LLM 학습 최적화 | 모든 소프트웨어 | 모든 소프트웨어 | GitHub 이슈 |
| **자율성** | 완전 자율 (무한 루프) | 작업 단위 자율 | 반자율 (대화형) | 작업 단위 자율 |
| **메트릭** | val_bpb | 없음 (범용) | 없음 (범용) | SWE-bench |
| **코드 규모** | 630줄 | 대규모 | 중규모 | 중규모 |
| **특징** | 3-파일 구조, 5분 예산 | 클라우드 샌드박스 | Git 네이티브 | 벤치마크 특화 |

### 자율 최적화 루프 비교

| 프로젝트 | 최적화 대상 | 메트릭 | 루프 방식 |
|---------|-----------|--------|----------|
| **Autoresearch** | LLM 학습 코드 | val_bpb | 코드 수정 → 학습 → 평가 |
| **DSPy** | LLM 프롬프트 | 태스크별 메트릭 | 프롬프트 수정 → 평가 |
| **Optuna** | 하이퍼파라미터 | 사용자 정의 | 파라미터 샘플 → 학습 → 평가 |
| **NNI** | 아키텍처 + HP | 사용자 정의 | NAS/HPO 자동화 |
| **Ray Tune** | 하이퍼파라미터 | 사용자 정의 | 분산 HP 탐색 |

핵심 차이: Autoresearch는 하이퍼파라미터뿐 아니라 **코드 자체**(아키텍처, 옵티마이저, 학습 루프)를 에이전트가 직접 수정한다.

## 주요 포크 & 파생 프로젝트

| 포크 | 플랫폼 | 특징 |
|------|--------|------|
| [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos) | macOS (MPS) | Apple Silicon 지원 |
| [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) | macOS (MLX) | Apple MLX 프레임워크 |
| [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) | Windows | RTX GPU 지원 |
| [andyluo7/autoresearch](https://github.com/andyluo7/autoresearch) | AMD | AMD GPU 지원 |
| [awesome-autoresearch](https://github.com/alvinunreal/awesome-autoresearch) | - | 큐레이션 리스트 |

## 최신 트렌드 및 동향 (2026-03)

### 1. "연구 조직을 코드로 프로그래밍"
- `program.md`는 사실상 **에이전트 조직의 소스코드**
- 연구 전략, 의사결정 규칙, 리소스 할당을 Markdown으로 정의
- "연구 조직 메타-최적화"라는 새로운 영역 개척

### 2. 멀티 에이전트 확장
- SkyPilot: 8시간 동안 ~910건 실험, GPU 클러스터로 확장
- Hyperspace: 35개 에이전트가 P2P 네트워크에서 333건 실험
- H200 검증 + H100 스크리닝 같은 이기종 GPU 전략 등장

### 3. 범용 패턴으로의 확산
- 프롬프트 최적화, 시스템 구성 최적화에 동일 패턴 적용
- Claude Code Skills의 자동 개선에 autoresearch 패턴 활용
- "측정 가능한 모든 것에 적용 가능" — 보편적 자기 개선 루프

### 4. 우려 사항
- 검증 세트 과적합 (val set overfitting) 논쟁
- 에이전트 API 비용 (하룻밤 수백 건 호출)
- 발견된 최적화의 일반화 가능성 의문
