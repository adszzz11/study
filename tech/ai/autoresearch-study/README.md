# Autoresearch Study

> **한 줄 정의**: AI 에이전트가 밤새 자율적으로 ML 실험을 반복하여 모델을 개선하는 Karpathy의 자율 연구 프레임워크

## 3줄 요약

1. AI 코딩 에이전트에게 단일 GPU 학습 코드를 주고, 5분 고정 시간 예산으로 코드 수정 → 학습 → 평가 → 유지/폐기 루프를 **무한 반복**시킨다
2. 사람은 `program.md`(에이전트 지시서)만 작성하고 잠들면, 아침에 **~100건의 실험 결과**와 개선된 모델을 받는다
3. 630줄 Python + 1개 Markdown 파일이라는 극단적 단순함으로, "자율 연구"의 **설계 패턴**을 누구나 자기 도메인에 적용할 수 있게 만들었다

## 핵심 키워드

`#autonomous-agent` `#self-improving-loop` `#LLM-training` `#Karpathy` `#single-GPU` `#nanochat` `#val_bpb` `#program.md` `#keep-or-discard`

## Quick Start (30초 체험)

```bash
# 1. 클론
git clone https://github.com/karpathy/autoresearch.git && cd autoresearch

# 2. uv 설치 & 의존성
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# 3. 데이터 준비 (~2분)
uv run prepare.py

# 4. 수동 학습 실행 (~5분, baseline 확인)
uv run train.py

# 5. 자율 연구 모드 (Claude Code 등 에이전트에서)
# "Hi have a look at program.md and let's kick off a new experiment!"
```

## 전체 목차

| Part | 파일 | 내용 |
|------|------|------|
| 1 | [01-overview.md](01-overview.md) | 핵심 개념, 아키텍처, 장단점, 사용 사례 |
| 2 | [02-ecosystem.md](02-ecosystem.md) | 관련 기술, 경쟁 도구 비교, 최신 트렌드 |
| 3 | [03-references.md](03-references.md) | 공식 문서, 학습 자료, 커뮤니티 |
| 4-1 | [04-learning/01-three-file-architecture.md](04-learning/01-three-file-architecture.md) | 3-파일 아키텍처 심층 분석 |
| 4-2 | [04-learning/02-experiment-loop.md](04-learning/02-experiment-loop.md) | 실험 루프 메커니즘 |
| 4-3 | [04-learning/03-model-architecture.md](04-learning/03-model-architecture.md) | GPT 모델 & Muon 옵티마이저 |
| 4-4 | [04-learning/04-program-md-design.md](04-learning/04-program-md-design.md) | program.md 설계 패턴 |
| 4-5 | [04-learning/05-apply-to-your-domain.md](04-learning/05-apply-to-your-domain.md) | 나의 도메인에 적용하기 |
| 5 | [05-projects.md](05-projects.md) | 실전 프로젝트 아이디어 |
| - | [cheatsheet.md](cheatsheet.md) | 빠른 참조 |

## 학습 플랜

| Day | 목표 | 파일 |
|-----|------|------|
| Day 1 | 전체 개요 파악 + Quick Start 실행 | `01-overview.md` |
| Day 2 | 3-파일 구조 이해 + 코드 읽기 | `04-learning/01-three-file-architecture.md` |
| Day 3 | 실험 루프 메커니즘 + program.md 분석 | `04-learning/02-experiment-loop.md`, `04-learning/04-program-md-design.md` |
| Day 4 | GPT 모델 & Muon 옵티마이저 이해 | `04-learning/03-model-architecture.md` |
| Day 5 | 나의 도메인에 적용 + 프로젝트 설계 | `04-learning/05-apply-to-your-domain.md`, `05-projects.md` |

---

*생성일: 2026-03-29 | GitHub Stars: 59,600+ | License: MIT*
