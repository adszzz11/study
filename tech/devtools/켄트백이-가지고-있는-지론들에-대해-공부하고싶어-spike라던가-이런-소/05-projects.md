---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - projects
type: tech-tool-study
parent: "[[README]]"
---

# Kent Beck의 지론들 - 실전 프로젝트

> [[README|목차로 돌아가기]]

---

## 1. 프로젝트 아이디어

| 프로젝트 | 난이도 | 학습 포인트 |
|----------|--------|-------------|
| Spike log template | ⭐ | 질문, timebox, 실험 방법, 결정, 남은 리스크 |
| TDD refactor kata | ⭐ | test list, failing test, behavior/tidy commit 분리 |
| Tidy First bot rule | ⭐⭐ | PR에서 formatting/refactor/behavior change 혼합 감지 |
| 3X 진단 | ⭐⭐ | Explore/Expand/Extract 단계와 metric 재설계 |
| AI-assisted spike | ⭐⭐ | agent에게 조사시키되 runnable proof와 decision record로 제한 |

---

## 2. 프로젝트 1 - Spike Log Template

### 목표

팀 ticket template에 `spike` 유형을 추가한다. 산출물은 코드가 아니라 decision log다.

```markdown
## Question
- 

## Timebox
- 

## Experiment Method
- 

## Learned
- 

## Decision
- 

## Remaining Risks
- 

## Follow-up
- 
```

### 완료 기준

- [ ] feature ticket과 spike ticket의 정의가 분리됨
- [ ] spike에는 timebox와 question이 필수
- [ ] PR merge 여부보다 decision 기록을 완료 기준으로 둠
- [ ] 남은 risk가 follow-up ticket으로 연결됨

---

## 3. 프로젝트 2 - TDD Refactor Kata

### 목표

작은 기존 모듈을 골라 test list부터 만들고, behavior change와 tidy commit을 분리해 PR을 작성한다.

| 단계 | 작업 |
|------|------|
| 1 | 작은 모듈 하나 선택 |
| 2 | 현재 behavior를 test list로 정리 |
| 3 | characterization test 추가 |
| 4 | 작은 tidying commit 수행 |
| 5 | 새 behavior test 추가 |
| 6 | implementation commit 작성 |
| 7 | PR에서 commit 의도를 설명 |

### PR 설명 예시

```markdown
## Summary
- tidy: extracted invoice status predicate without behavior change
- test: added overdue notification coverage
- feat: sends notification for overdue invoices

## Verification
- npm test -- invoice

## Review Notes
- Commit 1 is structural only.
- Commit 3 changes behavior.
```

---

## 4. 프로젝트 3 - Tidy First Bot Rule

### 목표

PR에서 formatting, refactor, behavior change가 과도하게 섞이면 label이나 checklist를 붙인다.

| 감지 신호 | 대응 |
|-----------|------|
| formatting-only file이 기능 변경과 섞임 | `mixed-change` label |
| rename diff가 많은데 test가 없음 | reviewer checklist 추가 |
| refactor commit과 feature commit 구분 없음 | PR template에서 commit grouping 요구 |
| generated code가 대량 추가됨 | AI output review checklist 요구 |

### GitHub Action 방향

```yaml
name: change-shape-check
on: [pull_request]
jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Detect mixed change shape
        run: |
          echo "Check formatting/refactor/behavior change boundaries"
```

처음부터 완전 자동 판정하려고 하지 않는다. 초기 목표는 reviewer가 "이 PR은 어떤 change shape인가?"를 묻게 만드는 것이다.

---

## 5. 프로젝트 4 - 3X 진단

### 목표

현재 제품/팀이 `Explore`, `Expand`, `Extract` 중 어디에 가까운지 분류하고 metric을 재설계한다.

| 질문 | Explore | Expand | Extract |
|------|---------|--------|---------|
| 가장 큰 risk | 문제/해결책 불확실성 | 성장과 품질 균형 | 효율과 안정성 |
| 좋은 work item | spike, prototype | feature slice, CI/CD | automation, reliability, cost tuning |
| 나쁜 metric | feature count | busy time | velocity only |
| 좋은 metric | validated learning | cycle time, activation | reliability, cost, defect rate |

### 산출물

- [ ] 현재 단계 판단 근거
- [ ] 버려야 할 metric
- [ ] 새로 볼 metric
- [ ] 다음 2주 동안 할 작은 실험

---

## 6. 프로젝트 5 - AI-assisted Spike

### 목표

새 library나 API를 AI agent로 조사시키되, 최종 산출물은 runnable proof, 실패 사례, security note, decision record로 제한한다.

```markdown
## Prompt Boundary
- Goal:
- Non-goals:
- Timebox:
- Allowed files:
- Verification command:

## Result
- Runnable proof:
- Failure cases:
- Security note:
- Decision:
- Remaining risks:
```

### 운영 원칙

- 작은 task로 시작한다.
- repo context를 좁게 준다.
- test-first 또는 verification command를 명시한다.
- agent 결과는 human review를 통과해야 한다.
- rollback 가능한 commit 단위로 남긴다.

---

## 7. 관련 노트

- [[study/tech/ai/lazy-codex]] - AI-assisted spike 운영에 직접 연결
- [[study/tech/ai/agent-orchestration/cli-agents]] - 여러 CLI agent를 작은 실험 단위로 운용
- [[study/tech/ai/model-context-protocol-mcp]] - protocol/library spike 대상으로 활용
