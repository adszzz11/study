---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — Overview

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: Ecosystem]]

## What

AI code migration은 LLM을 번역기로만 쓰지 않는다. agent가 code를 대량 생성하되, compiler·test·diff 같은 deterministic signal을 judge로 삼고 orchestration loop가 오류 pattern을 찾아 재생성하는 software modernization 방식이다.

| 구성 요소 | 책임 |
|---|---|
| LLM agent | code 변환, semantic gap 탐색, review, 실패 원인 분류 |
| Rulebook | 반복 가능한 language/framework mapping policy 고정 |
| Dependency Map | migration order, batch, 병렬 작업 경계 결정 |
| Portable judge | original과 target을 같은 contract로 평가 |
| Orchestrator | queue, concurrency, phase gate, retry, budget 관리 |
| Compiler·test·diff | pass/fail을 재현 가능한 signal로 제공 |

## Why

전통적인 language port가 느린 이유는 syntax 변환보다 숨은 의미와 검증 비용에 있다.

- memory ownership, dynamic typing, transaction boundary 같은 암묵적 contract를 찾아야 한다.
- 수천 파일의 dependency order와 안전한 병렬 경계를 결정해야 한다.
- compile success가 behavioral equivalence를 보장하지 않는다.
- 긴 rewrite 동안 원본 제품의 feature·security patch와 migration branch가 drift한다.
- 사람이 수십만~수백만 줄 diff를 일관되게 review하기 어렵다.

Agentic coding은 구현 비용을 낮추지만 one-shot correctness를 보장하지 않는다. ACL 2025 CODEMENV에서 19개 Python·Java package, 922개 사례에 대한 7개 LLM의 평균 `pass@1`은 26.50%, 최고 모델은 43.84%였다. 따라서 compiler, tests, adversarial review가 migration architecture의 본체여야 한다.

## 핵심 특징

### 1. Migration 여부부터 판정

첫 단계는 code 변경이 아닌 read-only feasibility 분석이다.

- 떠날 실질적 이유가 있는가?
- structure-preserving port인가, redesign인가?
- 기존 test를 target에도 재사용할 수 있는가?
- verification 비용보다 장기 편익이 큰가?
- ecosystem, hiring, security, runtime 성능이 장기적으로 개선되는가?

### 2. Portable judge 우선

```text
existing tests
  ├─ observable behavior → reusable contract tests
  └─ implementation detail → rewrite or exclude with rationale

contract tests + production scenarios
  → original 실행
  → intentionally broken target에 mutation test
  → stdout / exit code / file / response diff
```

좋은 judge는 original에서 통과할 뿐 아니라 **알려진 오류를 확실히 실패**시킨다. test가 포착하지 않은 behavior는 동등하다고 증명할 수 없다.

### 3. Rulebook과 semantic gap 분리

| Artifact | 예시 |
|---|---|
| Rulebook | error mapping, ownership, naming, async, FFI, nullability |
| Dependency Map | import graph, manifest, generated code, global state |
| Gap Inventory | 기계적 mapping으로 보존하기 어려운 의미 |

- Zig → Rust: allocator lifetime, `defer`, raw pointer, C ABI를 ownership, `Drop`, borrow checker에 대응한다.
- Python → TypeScript: duck-typed shape를 `interface`, generic, `Promise` contract로 명시한다.
- COBOL → Java: data layout과 transaction boundary보다 먼저 code 속 business rule을 추출한다.

### 4. Disposable stress test

대표 파일을 두 방식으로 독립 변환하고 세 번째 agent와 adversarial reviewer가 차이를 공격한다. 이 단계의 code는 버리고 발견된 rule만 보존한다. 목적은 production code 생산이 아니라 rulebook의 취약점을 싸게 찾는 것이다.

### 5. 역할 분리와 반복 수렴

`implement → review → fix`는 서로 다른 context에서 실행한다. reviewer 두 명의 disagreement는 제3 agent가 판정한다. 같은 오류가 반복되면 개별 파일을 손으로 고치기보다 rulebook을 고치고 영향 batch를 다시 생성한다.

### 6. Phase gate

```text
Compile → Smoke → Behavioral parity → Security → Performance
```

compiler error는 work queue로 만들고, crash는 root cause별로 cluster한다. 비싼 전체 build는 build daemon이 patch를 batch하고 직렬화해 agent 간 중복 실행을 줄인다.

## Anthropic 사례 읽기

| 사례 | 공개 결과 | 해석 시 주의 |
|---|---|---|
| Bun Zig → Rust | 11일, 약 50 workflow, 1,448 Zig file, 약 100만 줄, merge 전 CI 100% pass | production merge 후 regression 19건 수정, Rust code 약 4% `unsafe` |
| Python → TypeScript | 주말, 165,000줄, 수백 agent, 8 phase gate, 3 adversarial review, 7 scenario parity | 내부 성공 사례이며 일반 생산성 benchmark가 아님 |

Bun 보고에서는 2,000회 반복 build memory가 6,745MB에서 609MB로 줄고 binary가 19% 작아졌으며 일부 workload가 2–5% 빨라졌다고 한다. 이 역시 특정 repository와 workload의 vendor 자체 측정치다.

## 한계와 위험

- test blind spot과 원본 latent bug를 target에 그대로 옮길 수 있다.
- implementer와 LLM reviewer가 같은 blind spot을 공유할 수 있다.
- shared worktree·Git index를 수백 agent가 만지면 race와 change loss가 생긴다.
- token·CI·review 비용이 생성 속도보다 더 빠르게 증가할 수 있다.
- compile success는 concurrency, security, latency, memory behavior를 보장하지 않는다.

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://bun.com/blog/bun-in-rust
- https://aclanthology.org/2025.findings-acl.140/
