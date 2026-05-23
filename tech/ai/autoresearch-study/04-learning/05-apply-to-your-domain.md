# 05. 나의 도메인에 적용하기

## 📌 핵심 개념

Autoresearch의 핵심은 LLM 학습이 아니라 **"측정 가능한 것에 대한 자율 최적화 루프"** 패턴이다. 이 패턴은 측정 가능한 메트릭이 있는 모든 도메인에 적용할 수 있다.

## 자율 최적화 루프의 보편적 공식

```
┌─────────────────────────────────────────────┐
│            Universal Autoresearch            │
│                                             │
│  1. 수정 가능한 파일 1개                      │
│  2. 측정 가능한 메트릭 1개                    │
│  3. 고정된 평가 예산                          │
│  4. keep/discard 규칙                        │
│  5. 무한 루프                                │
└─────────────────────────────────────────────┘
```

### 적용 전 체크리스트

```
□ 자동으로 측정 가능한 메트릭이 있는가?
□ 평가를 프로그래밍적으로 실행할 수 있는가?
□ 수정 범위를 1-2개 파일로 좁힐 수 있는가?
□ 실험 1회가 합리적 시간 안에 끝나는가?
□ 개선/미개선을 객관적으로 판단할 수 있는가?
```

## 도메인별 적용 예시

### 1. 프롬프트/시스템 프롬프트 최적화

```
수정 대상: system_prompt.md
메트릭: eval_set에 대한 accuracy (%)
평가 예산: 30초 (API 호출 + 채점)
keep/discard: accuracy 개선 → keep
```

**program.md 스케치**:
```markdown
## Target
- File: system_prompt.md
- Metric: accuracy on eval_set.json (higher = better)

## Loop
1. Modify system_prompt.md (try different phrasings, examples, constraints)
2. Run: python evaluate.py > run.log 2>&1
3. Parse: grep "^accuracy:" run.log
4. If accuracy improved → keep, else → discard
```

**실제 사례**: Claude Code Skills의 자동 개선에 이 패턴을 적용한 사람들이 등장.

### 2. CI/CD 파이프라인 최적화

```
수정 대상: .github/workflows/ci.yml
메트릭: 전체 빌드 시간 (초)
평가 예산: 1회 빌드 시간 (가변)
keep/discard: 빌드 시간 단축 + 테스트 전부 통과 → keep
```

**에이전트가 시도할 수 있는 것들**:
- 캐시 전략 변경
- 병렬화 수준 조정
- 불필요한 스텝 제거
- Docker 레이어 최적화

### 3. 웹 성능 최적화

```
수정 대상: next.config.js + 선택된 컴포넌트
메트릭: Lighthouse Performance 점수
평가 예산: Lighthouse 실행 (~30초)
keep/discard: 점수 개선 → keep
```

### 4. 테스트 스위트 최적화

```
수정 대상: pytest.ini + conftest.py
메트릭: 테스트 실행 시간 (초)
평가 예산: 전체 테스트 실행
keep/discard: 시간 단축 + 0 failures → keep
```

### 5. 데이터베이스 쿼리 최적화

```
수정 대상: queries.sql
메트릭: 총 쿼리 실행 시간 (ms)
평가 예산: 벤치마크 쿼리 세트 실행
keep/discard: 실행 시간 단축 + 결과 동일 → keep
```

### 6. 하이퍼파라미터 탐색 (비ML)

```
수정 대상: config.yaml
메트릭: 도메인별 성능 지표
평가 예산: 시뮬레이션/테스트 실행
keep/discard: 메트릭 개선 → keep
```

## 나만의 autoresearch 만들기 (Step-by-Step)

### Step 1: 3-파일 구조 설계

```
my-autoresearch/
├── evaluate.py    ← 고정: 메트릭 측정 (절대 수정 안 함)
├── target.py      ← 수정 대상: 에이전트가 실험
└── program.md     ← 에이전트 지시서
```

### Step 2: evaluate.py 작성

```python
"""평가 스크립트 — 이 파일은 수정하지 않는다."""

def evaluate():
    # 메트릭 측정 로직
    score = run_benchmark()

    # 기계 판독 가능한 출력 (grep 가능)
    print("---")
    print(f"score: {score:.6f}")
    print(f"time_seconds: {elapsed:.1f}")

if __name__ == "__main__":
    evaluate()
```

**핵심**: `grep "^score:" run.log`로 결과를 추출할 수 있어야 한다.

### Step 3: program.md 작성

```markdown
# My Autoresearch

## Setup
1. Create branch: `git checkout -b experiment/<tag>`
2. Read all files for context
3. Run baseline: `python evaluate.py > run.log 2>&1`
4. Record baseline in results.tsv

## Rules
- **CAN modify**: target.py
- **CANNOT modify**: evaluate.py
- **Goal**: minimize/maximize score
- **Budget**: [N]분 per experiment

## Loop
LOOP FOREVER:
1. Check git state
2. Modify target.py with an experimental idea
3. git commit
4. Run: python evaluate.py > run.log 2>&1
5. Parse: grep "^score:" run.log
6. If improved → keep. If not → git reset.
7. Log to results.tsv
8. NEVER STOP.
```

### Step 4: 실행

```bash
# Claude Code에서:
# "Hi, read program.md and let's kick off experiments!"
```

## 고급 패턴

### 멀티 메트릭 최적화

```markdown
## Goal
Primary: minimize latency_ms
Secondary: keep accuracy above 95%

## Decision
- If latency improved AND accuracy >= 95% → keep
- If latency improved BUT accuracy < 95% → discard
- If latency not improved → discard
```

### 점진적 난이도 (Curriculum)

```markdown
## Phase 1 (experiments 1-20): Quick wins
- Focus on obvious optimizations
- Low-risk changes only

## Phase 2 (experiments 21-50): Structural changes
- Try architectural modifications
- Allow higher risk

## Phase 3 (experiments 51+): Creative exploration
- Combine successful changes
- Try unconventional approaches
```

### 에이전트에게 방향 제시

```markdown
## Exploration hints
- Try changing X before Y (X is usually more impactful)
- If stuck, try combining the last 3 near-misses
- Read the comments in target.py for ideas
- Papers [A], [B] have relevant techniques
```

## ✅ 체크포인트

- [ ] 자기 도메인에서 "자동 측정 가능한 메트릭"을 1개 이상 식별했는가?
- [ ] 3-파일 구조 (evaluate/target/program)를 설계할 수 있는가?
- [ ] grep 가능한 출력 포맷을 정의할 수 있는가?
- [ ] keep/discard 규칙을 구체적으로 명시할 수 있는가?

## ⚠️ 흔한 실수 & 해결법

| 실수 | 해결 |
|------|------|
| 메트릭이 노이즈가 많음 | 여러 번 측정 후 평균, 또는 안정적 메트릭 선택 |
| 평가가 너무 오래 걸림 | 서브샘플링, 프록시 메트릭 사용 |
| 수정 범위가 너무 넓음 | 1-2개 파일로 제한, 나머지는 읽기 전용 |
| 에이전트가 평가 코드 수정 | CANNOT DO에 명시적으로 금지 |
| 과적합 (validation set) | 별도 hold-out set 준비, 주기적 확인 |

## 🔗 더 알아보기

- [[04-program-md-design|이전: program.md 설계 패턴]]
- [Builder's Playbook](https://sidsaladi.substack.com/p/autoresearch-101-builders-playbook)
- [Universal Skill 변환기](https://medium.com/@k.balu124/i-turned-andrej-karpathys-autoresearch-into-a-universal-skill-1cb3d44fc669)
- [MindStudio: Claude Code Skills에 적용](https://www.mindstudio.ai/blog/karpathy-autoresearch-pattern-claude-code-skills)
