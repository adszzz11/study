# Part 5: 실전 프로젝트

## 프로젝트 1: Autoresearch 직접 실행 (입문)

### 목표
H100 또는 포크를 사용하여 autoresearch를 직접 돌려보고, 에이전트가 수행한 실험을 분석한다.

### 난이도: 🟢 입문

### 필요 환경
- NVIDIA GPU (H100 권장, RTX 시리즈는 포크 사용)
- 또는 macOS (MLX/MPS 포크)
- Claude Code, Codex CLI 등 AI 코딩 에이전트

### 단계별 가이드

```bash
# 1. 환경 설정
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch
uv sync
uv run prepare.py

# 2. Baseline 확인
uv run train.py
# val_bpb: 0.9979 (H100 기준)

# 3. 에이전트 실행
# Claude Code에서:
# "Read program.md and let's kick off a new experiment!"

# 4. 1시간 후 결과 확인
cat results.tsv
git log --oneline
```

### 분석 포인트
- [ ] 에이전트가 몇 건의 실험을 수행했는가?
- [ ] keep/discard 비율은?
- [ ] 가장 큰 개선을 가져온 변경은 무엇인가?
- [ ] 에이전트가 시도한 아이디어의 패턴은?

---

## 프로젝트 2: 소규모 GPU 환경 적응 (중급)

### 목표
macOS MPS 또는 작은 NVIDIA GPU에서 autoresearch가 의미 있게 동작하도록 하이퍼파라미터를 조정한다.

### 난이도: 🟡 중급

### Karpathy 권장 조정 사항

```python
# 1. 데이터셋 변경 → TinyStories (낮은 엔트로피)
# prepare.py의 BASE_URL을 TinyStories로 교체

# 2. vocab_size 축소
vocab_size = 2048  # 또는 1024, 256 (byte-level)

# 3. MAX_SEQ_LEN 축소
MAX_SEQ_LEN = 256  # 기본 2048 → 256

# 4. EVAL_TOKENS 축소
EVAL_TOKENS = 5 * 524288  # 검증 데이터 축소

# 5. DEPTH 축소
DEPTH = 4  # 기본 8 → 4

# 6. WINDOW_PATTERN 단순화
WINDOW_PATTERN = "L"  # SSSL 대신 전체 윈도우만

# 7. TOTAL_BATCH_SIZE 축소
TOTAL_BATCH_SIZE = 2**14  # ~16K tokens
```

### 성공 기준
- [ ] 5분 학습이 크래시 없이 완료됨
- [ ] val_bpb가 의미 있는 수치 (수렴 징후)
- [ ] 에이전트가 3건 이상 자율 실험 완료

---

## 프로젝트 3: 나만의 autoresearch 만들기 (고급)

### 목표
autoresearch 패턴을 ML 학습이 아닌 **자기 도메인**에 적용한다.

### 난이도: 🔴 고급

### 예시: 시스템 프롬프트 자동 최적화

```
my-prompt-research/
├── evaluate.py     ← 고정: LLM 호출 + 채점
├── prompt.md       ← 수정 대상: 시스템 프롬프트
├── eval_set.json   ← 고정: 평가 데이터
├── program.md      ← 에이전트 지시서
└── results.tsv     ← 실험 기록
```

**evaluate.py 핵심**:
```python
import json, os
from anthropic import Anthropic

def evaluate():
    with open("prompt.md") as f:
        system_prompt = f.read()
    with open("eval_set.json") as f:
        eval_cases = json.load(f)

    client = Anthropic()
    correct = 0
    for case in eval_cases:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            system=system_prompt,
            messages=[{"role": "user", "content": case["input"]}],
            max_tokens=500
        )
        if case["expected"] in response.content[0].text:
            correct += 1

    accuracy = correct / len(eval_cases)
    print("---")
    print(f"accuracy: {accuracy:.4f}")
    print(f"num_cases: {len(eval_cases)}")

if __name__ == "__main__":
    evaluate()
```

### 단계별 가이드

1. **도메인 선택**: 자동 측정 가능한 메트릭이 있는 문제
2. **3-파일 설계**: evaluate / target / program
3. **Baseline 실행**: 현재 상태의 메트릭 측정
4. **program.md 작성**: 규칙, 메트릭, 루프 정의
5. **에이전트 실행**: 1시간 동안 자율 실험
6. **결과 분석**: 어떤 변경이 효과적이었는지 리뷰

---

## 프로젝트 4: 멀티 에이전트 실험 (도전)

### 목표
여러 에이전트를 동시에 실행하여 병렬 실험을 수행한다.

### 난이도: 🔴🔴 도전

### 아이디어
- 각 에이전트에게 다른 탐색 방향 지정
- 에이전트 A: 아키텍처 탐색 / 에이전트 B: 옵티마이저 탐색
- 브랜치 전략: `autoresearch/mar29-arch`, `autoresearch/mar29-optim`
- 주기적으로 best 결과를 merge

---

## Best Practices 체크리스트

### 실험 설계
- [ ] Baseline을 먼저 확립했는가?
- [ ] 메트릭이 자동으로 측정되는가?
- [ ] 평가 코드가 수정 불가로 보호되는가?
- [ ] keep/discard 규칙이 명확한가?

### 에이전트 관리
- [ ] 컨텍스트 오염 방지 (출력 리다이렉트)?
- [ ] 타임아웃 규칙이 있는가?
- [ ] 크래시 복구 절차가 명시되어 있는가?
- [ ] "NEVER STOP" 지시가 있는가?

### 결과 관리
- [ ] 실험 기록이 구조화되어 있는가 (TSV)?
- [ ] Git 히스토리로 모든 변경을 추적하는가?
- [ ] 주기적으로 결과를 분석하는가?

### 안전장치
- [ ] 과적합 방지 (hold-out set)?
- [ ] 비용 한도 (API 호출 수)?
- [ ] 리소스 한도 (VRAM, 디스크)?
