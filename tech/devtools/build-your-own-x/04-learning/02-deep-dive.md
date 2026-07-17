---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X — Deep Dive

> [[01-getting-started|이전: Getting Started]] | [[../README|목차로 돌아가기]] | [[../05-projects|다음: Projects]]

## 1. Catalog architecture 이해

`Build Your Own X`에는 tutorial을 실행하거나 검증하는 중앙 runtime이 없다.

```text
Contributor
  → issue / pull request
  → community review
  → README의 external link
  → third-party tutorial / source repository
  → learner's local environment and tests
```

이 구조는 범위와 language 다양성을 크게 만들지만 다음 책임을 학습자에게 넘긴다.

- prerequisite와 순서 설계
- dependency/version 재현
- correctness test와 benchmark
- broken link와 archived content 대응
- tutorial code의 license와 security 검토

## 2. 따라 치기를 deliberate practice로 바꾸기

각 chapter를 다음 loop로 진행한다.

1. **Predict**: 다음 component의 interface와 invariant를 먼저 예상한다.
2. **Implement**: guide를 참고해 최소 동작을 구현한다.
3. **Probe**: happy path 외에 boundary와 malformed input을 넣는다.
4. **Compare**: 실제 tool 또는 specification의 observable behavior와 비교한다.
5. **Explain**: design choice와 빠진 production concern을 기록한다.

```markdown
## Decision: append-only log

- 선택 이유: write path를 단순하게 유지
- 유지해야 할 invariant: valid record는 length와 checksum으로 구분
- 실패 mode: partial write, corruption, unbounded growth
- 현재 제외: compaction, fsync policy, crash recovery
```

## 3. Black-box verification

공통 grading이 없으므로 public behavior를 중심으로 test oracle을 만든다.

| Test 종류 | 목적 | 예시 |
|---|---|---|
| Golden test | 고정 input/output 검증 | parser output, serialized bytes |
| Differential test | reference tool과 비교 | 같은 input을 mini-Git과 Git에 전달 |
| Property test | 넓은 input space의 invariant 검증 | encode 후 decode하면 원본 복원 |
| Fuzz test | malformed input과 crash 탐색 | protocol parser에 random bytes 입력 |
| Restart test | persistence/durability 확인 | write 후 process 재시작 |
| Concurrency test | ordering, race, deadlock 탐색 | 동시에 여러 client request |

> [!important] 호환성 범위
> reference tool과 결과가 다르다고 항상 bug는 아니다. 구현하려는 protocol/version/subset을 먼저 명시해야 differential test의 의미가 생긴다.

## 4. Benchmark를 학습 도구로 사용하기

benchmark의 목표는 production tool을 이기는 것이 아니라 architecture가 비용을 어디에 지불하는지 확인하는 것이다.

```text
Hypothesis: sequential append는 random update보다 write throughput이 높다.
Variable: record size, batch size, fsync policy
Measure: throughput, p50/p95 latency, file size
Control: runtime version, hardware, warm-up, dataset
Conclusion: 측정 결과와 설명 가능한 bottleneck
```

- 결과에는 hardware, OS, language/runtime version을 함께 기록한다.
- 한 번의 숫자보다 input size에 따른 trend를 본다.
- optimization 전후에 correctness test를 다시 실행한다.
- toy와 production system의 절대 성능 비교를 marketing claim으로 만들지 않는다.

## 5. 분야별 핵심 invariant

| 분야 | 관찰할 invariant / trade-off |
|---|---|
| Database | atomicity boundary, page format, index consistency, recovery |
| Git | content address, immutable object, reference update, DAG reachability |
| Container | isolation boundary, resource accounting, privilege |
| Compiler/VM | grammar, type/value representation, control flow, error location |
| HTTP server | framing, timeout, concurrency, backpressure, malformed request |
| Memory allocator | alignment, fragmentation, metadata integrity, concurrency |

## 6. Production gap analysis

완주 후 기능 목록보다 빠진 운영 요구를 적는다.

- [ ] authentication과 authorization
- [ ] input validation과 resource limit
- [ ] crash consistency와 backup/restore
- [ ] observability: logs, metrics, traces
- [ ] backward compatibility와 migration
- [ ] concurrency control과 overload behavior
- [ ] fuzzing, security review, dependency update
- [ ] packaging, deployment, rollback

이 checklist의 대부분이 비어 있어도 학습 project로는 성공할 수 있다. 중요한 것은 빠진 항목을 알고 production-ready라는 오해를 피하는 것이다.

## 7. Link rot에 강한 학습 기록

- tutorial title, author, URL, 확인일을 남긴다.
- 가능하면 source repository의 commit permalink를 기록한다.
- code를 복사할 때 원문 license와 attribution 요구를 확인한다.
- 핵심 개념은 자신의 말과 diagram으로 정리하되 원문 전체를 복제하지 않는다.
- 외부 link가 깨졌다면 upstream issue에 상태를 확인하고 대체 자료를 기록한다.

## Sources

- [Build Your Own X repository](https://github.com/codecrafters-io/build-your-own-x)
- [Build Your Own X issues](https://github.com/codecrafters-io/build-your-own-x/issues)
- [Build Your Own X pull requests](https://github.com/codecrafters-io/build-your-own-x/pulls)
- [Teach Yourself CS](https://teachyourselfcs.com/)

