# 04. program.md 설계 패턴

## 📌 핵심 개념

`program.md`는 autoresearch에서 가장 혁신적인 아이디어다. Karpathy는 이를 **"super lightweight skill"** 이라 부른다. 사람이 Python 코드를 직접 작성하는 대신, **에이전트의 행동 규칙을 Markdown으로 프로그래밍**한다.

> "You are not touching any of the Python files like you normally would as a researcher. Instead, you are programming the `program.md` Markdown files that provide context to the AI agents and set up your autonomous research org."

## program.md의 구조 분석

### 전체 섹션 맵

```
program.md
├── Setup              — 실험 환경 초기화 절차
├── Experimentation    — 규칙: 할 수 있는 것 / 없는 것 / 목표
├── Output format      — 결과 파싱 방법
├── Logging results    — results.tsv 포맷
└── The experiment loop — 무한 루프 동작 규칙
```

### 섹션별 핵심 설계

#### 1. Setup — 재현 가능한 초기화

```markdown
1. Agree on a run tag: propose a tag based on today's date (e.g. `mar5`)
2. Create the branch: `git checkout -b autoresearch/<tag>`
3. Read the in-scope files
4. Verify data exists
5. Initialize results.tsv
6. Confirm and go
```

**설계 의도**:
- 매 실험 세트마다 새 브랜치 → 깔끔한 실험 격리
- 파일 읽기 강제 → 에이전트가 전체 맥락 이해 후 시작
- 명시적 확인 단계 → 데이터 누락 등 사전 방지

#### 2. Experimentation — 명확한 경계 설정

```markdown
**What you CAN do:**
- Modify `train.py` — everything is fair game

**What you CANNOT do:**
- Modify `prepare.py`
- Install new packages
- Modify the evaluation harness
```

**설계 원칙**: **허용 목록(allowlist) + 금지 목록(denylist)** 모두 명시.

추가 기준들:

| 기준 | 설명 |
|------|------|
| **목표** | val_bpb를 최소화 |
| **VRAM** | 소프트 제약 (의미 있는 개선이면 증가 허용) |
| **단순성** | 동일 성능이면 더 단순한 코드 승리 |

#### 3. Output format — 파싱 가능한 결과

```markdown
Once the script finishes it prints a summary like this:
---
val_bpb:          0.997900
training_seconds: 300.1
...

Extract the key metric: `grep "^val_bpb:" run.log`
```

**설계 의도**: 에이전트가 정규식으로 결과를 추출할 수 있도록 **기계 판독 가능한 포맷**을 지정.

#### 4. Logging — 구조화된 기록

```markdown
commit	val_bpb	memory_gb	status	description
```

**TSV 선택 이유**: description에 쉼표가 올 수 있으므로 CSV 대신 TSV.

#### 5. The experiment loop — 자율성의 핵심

```markdown
LOOP FOREVER:
1. Look at the git state
2. Tune train.py
3. git commit
4. Run the experiment
...
9. If val_bpb is equal or worse, git reset back

**NEVER STOP**: The human might be asleep...
The loop runs until the human interrupts you, period.
```

## 설계 패턴: "Autonomous Agent Skill"

program.md를 일반화하면 **자율 에이전트 스킬**의 보편적 패턴이 드러난다:

### 보편적 레시피

```markdown
1. 수정 가능한 파일 1개 정의
2. 최적화할 메트릭 1개 정의
3. 고정된 평가 예산 1개 정의
4. keep/discard 규칙 정의
5. 에이전트를 무한 루프로 실행
```

### 적용 가능한 도메인

| 도메인 | 수정 대상 | 메트릭 | 평가 방법 |
|--------|----------|--------|----------|
| LLM 학습 | train.py | val_bpb | 5분 학습 |
| 프롬프트 최적화 | prompt.md | 정확도/F1 | 테스트 세트 평가 |
| CI/CD 최적화 | pipeline.yml | 빌드 시간 | 파이프라인 실행 |
| 웹 성능 | config.js | Lighthouse 점수 | Lighthouse 실행 |
| CSS 최적화 | styles.css | 번들 크기 | 빌드 |
| 테스트 최적화 | test.py | 커버리지/속도 | 테스트 실행 |

## program.md 작성 가이드

### 필수 요소 체크리스트

```markdown
□ 명확한 목표 메트릭 (무엇을 최적화?)
□ 수정 가능/불가 범위 (무엇을 건드릴 수 있는지)
□ 평가 방법 (어떻게 결과를 측정?)
□ 결과 파싱 방법 (어떻게 메트릭을 추출?)
□ keep/discard 규칙 (언제 유지/폐기?)
□ 기록 포맷 (결과를 어디에 어떻게 저장?)
□ 자율성 지시 (멈추지 말 것)
□ 타임아웃/크래시 처리 규칙
```

### 좋은 program.md vs 나쁜 program.md

| 좋은 패턴 | 나쁜 패턴 |
|-----------|----------|
| 구체적 메트릭: "val_bpb를 최소화" | 모호한 목표: "모델을 개선해" |
| 명시적 경계: "train.py만 수정 가능" | 암묵적 가정: 에이전트가 알아서 판단 |
| 파싱 가능한 출력: `grep "^val_bpb:"` | 비정형 출력: "결과를 확인해봐" |
| 판단 기준: "0.001 개선 + 20줄 → 스킵" | 기준 없음: "좋으면 유지" |
| "NEVER STOP" | "적당할 때 멈춰" |

### 실전 팁

1. **첫 번째 실행은 항상 baseline**: 변경 없이 원본 실행 → 기준점 확립
2. **출력 리다이렉트 강제**: `> run.log 2>&1` — 컨텍스트 오염 방지
3. **크래시 복구 규칙 명시**: 간단한 버그 → 수정, 근본적 문제 → 스킵
4. **실험 격리**: 브랜치 기반 관리, reset으로 깔끔한 복귀

## 💻 나만의 program.md 작성 예시

### 프롬프트 최적화용

```markdown
# Prompt Optimization Program

## Target
- Modify: `system_prompt.md`
- Metric: accuracy on `eval_set.json` (higher is better)
- Budget: 30 seconds per evaluation

## Rules
- DO NOT modify eval_set.json or evaluate.py
- Keep the prompt under 2000 tokens
- Simpler prompts are preferred

## Loop
1. Modify system_prompt.md
2. Run: python evaluate.py > run.log 2>&1
3. Parse: grep "^accuracy:" run.log
4. If improved → keep. If not → discard (git reset).
5. NEVER STOP.
```

## ✅ 체크포인트

- [ ] program.md가 왜 "skill"인지 설명할 수 있는가?
- [ ] program.md의 5개 핵심 섹션을 나열할 수 있는가?
- [ ] 자율 에이전트 스킬의 보편적 레시피 5가지를 설명할 수 있는가?
- [ ] 자기 도메인에 맞는 program.md를 초안 작성할 수 있는가?

## ⚠️ 흔한 실수 & 해결법

| 실수 | 해결 |
|------|------|
| 메트릭을 정의하지 않음 | 반드시 단일 숫자 메트릭 명시 |
| 수정 범위를 명시하지 않음 | CAN DO / CANNOT DO 목록 필수 |
| 파싱 방법 누락 | grep 가능한 출력 포맷 지정 |
| "적당히" 같은 모호한 기준 | 구체적 임계값으로 대체 |
| 자율성 지시 누락 | NEVER STOP 명시 |

## 🔗 더 알아보기

- [[03-model-architecture|이전: GPT 모델 & Muon 옵티마이저]]
- [[05-apply-to-your-domain|다음: 나의 도메인에 적용하기]]
- [program.md 원문](https://github.com/karpathy/autoresearch/blob/master/program.md)
- [Autoresearch를 Universal Skill로 변환](https://medium.com/@k.balu124/i-turned-andrej-karpathys-autoresearch-into-a-universal-skill-1cb3d44fc669)
- [Builder's Playbook](https://sidsaladi.substack.com/p/autoresearch-101-builders-playbook)
