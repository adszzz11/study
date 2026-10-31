---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] | [[README|목차로 돌아가기]] | [[cheatsheet|다음: Cheatsheet]]

## Project 1 — Portable Judge Spike

### 목표

작은 CLI 또는 HTTP endpoint 하나에 대해 source/target 공용 contract와 parity harness를 만든다. production migration은 하지 않는다.

### 산출물

- test inventory와 observable/internal 분류
- canonical fixture 5–10개
- stdout/status/file/response normalizer
- structured parity report
- 최소 3개 mutation을 잡는 증거

### 완료 조건

- [ ] original baseline이 반복해서 통과한다.
- [ ] intentionally broken target이 실패한다.
- [ ] nondeterministic field 제거 근거가 문서화됐다.
- [ ] CI에서 10분 이내 반복 가능하다.

## Project 2 — Disposable Language Port

### 목표

대표 파일 2–5개를 독립적으로 두 번 port해 rulebook과 gap inventory를 만든 뒤 code는 폐기한다.

```text
Scope: parser + error boundary
Agent A: source structure와 rulebook을 엄격히 보존
Agent B: target language senior engineer 관점
Agent C: A/B diff에서 missing rule 추출
Reviewer: behavior, security, performance 반례 제시
Keep: rulebook, gap inventory, judge improvements
Discard: both implementations
```

### 평가 질문

- 두 구현이 다르게 해석한 source semantic은 무엇인가?
- compiler가 잡았지만 reviewer가 놓친 문제와 그 반대는 무엇인가?
- target idiom을 적용하면서 behavior를 바꾼 부분은 무엇인가?
- 대량 batch 전에 새로 필요한 contract test는 무엇인가?

## Project 3 — Dependency-aware Batch Migration

### 목표

한 package 또는 leaf module을 isolated workspace에서 migration하고 queue와 phase gate를 검증한다.

| Phase | 작업 | Gate |
|---|---|---|
| Discover | import/build/generated/global edge 수집 | batch dependency 승인 |
| Translate | implementer fan-out | patch와 uncertainty TODO 존재 |
| Review | 독립 reviewer 2명 + resolver | unresolved high-risk finding 0 |
| Compile | compiler error cluster 처리 | compile pass |
| Run | smoke·contract·parity | 승인되지 않은 diff 0 |
| Qualify | security·performance | budget 충족 또는 명시적 waiver |

### 운영 제한 예시

```yaml
budget:
  max_concurrency: 8
  max_attempts_per_batch: 3
  max_wall_time_minutes: 180
  max_ci_minutes: 600
safety:
  isolated_workspace_per_batch: true
  shared_git_index_writers: 1
  human_approval_before_merge: true
```

## Project 4 — Migration Feasibility Dossier

### 목표

아직 code를 바꾸지 않고 `Migrate / Investigate / Don't migrate` 결론을 낸다.

### 보고서 구조

1. Business/technical reason과 non-goal
2. Port 대 redesign 결정
3. test portability와 judge gap
4. dependency·generated code·FFI risk
5. target ecosystem와 hiring/security/runtime 편익
6. token·CI·review·dual-maintenance 비용
7. pilot scope와 rollback/stop condition
8. 최종 결정과 evidence

## Production 전 체크포인트

- [ ] 원본 branch의 feature·security patch를 target에 동기화할 전략이 있다.
- [ ] high-risk boundary에는 human owner가 있다.
- [ ] merge 전 CI pass 외에 post-merge canary와 rollback이 있다.
- [ ] parity가 잡지 못하는 latency, memory, concurrency, security gate가 있다.
- [ ] 생성된 대규모 diff가 아니라 rulebook·judge·risk artifact를 중심으로 review한다.
- [ ] 성공 metric과 migration 종료 후 제거할 bridge/dual-run code가 명시됐다.

## 회고 Template

```markdown
## Batch
- ID / rulebook version / source revision / target revision

## Result
- compile / smoke / contract / parity / security / performance

## Repeated failures
- symptom / root cause / affected batches

## Process change
- rulebook / judge / dependency map / orchestration 변경

## Decision
- regenerate / manual exception / redesign / stop migration
```

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://bun.com/blog/bun-in-rust
