---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration

> **한 줄 정의**: LLM agent, compiler·test·diff 기반 deterministic verification, 병렬 orchestration을 결합해 대규모 codebase의 언어·framework·runtime 전환을 자동화하는 software modernization 방식.

## Overview

Anthropic의 AI Code Migration은 파일을 하나씩 번역하는 prompt 기법이 아니라, 대규모 생성물을 **기계적 judge와 반복 process loop로 수렴**시키는 운영 모델이다. 핵심 원칙은 “잘못된 코드를 개별 수정하지 말고, 잘못된 코드를 만든 process loop를 수정하라”이다.

```text
Portable Judge
      ↓
Rulebook → Dependency Map → Gap Inventory
      ↓
Disposable mini-migration / adversarial stress test
      ↓
Parallel implementers
      ↓
Independent reviewers → disagreement resolver
      ↓
Compile → smoke test → behavioral parity test
      ↓
반복 실패 pattern을 Rulebook에 반영 → 영향 batch 재생성
```

이 접근의 성공 조건은 LLM의 one-shot 정확도가 아니라 다음 세 요소의 결합이다.

- **Explicit policy**: type, error, ownership, concurrency, FFI mapping을 Rulebook으로 고정한다.
- **Parallel orchestration**: dependency-aware batch와 역할이 분리된 agent를 병렬 운영한다.
- **Deterministic verification**: compiler, contract test, scenario diff, security·performance gate가 결과를 판정한다.

Anthropic 자체 보고에 따르면 Bun Zig → Rust port는 11일 동안 1,448개 Zig file을 대상으로 진행되어 약 100만 줄 규모에 도달했고 merge 전 CI test 100% pass를 기록했다. Python → TypeScript 사례는 주말 동안 165,000줄을 생성하고 8개 phase gate, 세 번의 adversarial review, 일곱 실제 scenario의 output parity diff를 사용했다. 이 수치는 일반 benchmark가 아니라 성공한 vendor 내부 사례라는 한계를 함께 읽어야 한다.

## Learning Path

- [ ] [[01-overview|1. Overview]] — What/Why, 핵심 특징과 위험 이해
- [ ] [[02-ecosystem|2. Ecosystem]] — manual rewrite, codemod, one-shot LLM과 비교
- [ ] [[03-references|3. References]] — 원문, starter kit, 독립 benchmark 읽기
- [ ] [[04-learning/01-getting-started|4. Getting Started]] — read-only feasibility와 portable judge 설계
- [ ] [[04-learning/02-deep-dive|5. Deep Dive]] — rulebook, orchestration, phase gate 심화
- [ ] [[05-projects|6. Projects]] — 작은 migration 실험부터 production 계획까지
- [ ] [[cheatsheet|7. Cheatsheet]] — 실행 전후 빠른 점검

## When To Use

- source와 target implementation에 동일하게 적용할 contract test 또는 parity harness를 만들 수 있을 때
- migration 단위를 dependency graph에 따라 분리하고 병렬 batch로 운영할 수 있을 때
- ecosystem, hiring, security, runtime 성능 등 장기 편익이 verification 비용보다 클 때
- structure-preserving port처럼 observable behavior를 명확히 보존해야 할 때
- compiler·test·security·performance gate를 CI에서 반복 실행할 예산과 시간이 있을 때

## When Not To Use

- 현재 언어·framework를 떠날 실질적 이유가 없거나 단순 upgrade/codemod로 충분할 때
- 원본 behavior를 설명하는 test와 production scenario가 없어 portable judge를 만들 수 없을 때
- redesign과 behavior-preserving port를 구분하지 않은 채 둘을 한 번에 수행하려 할 때
- 규제·보안상 source code를 agent에 제공하거나 병렬 filesystem/Git 권한을 줄 수 없을 때
- token, CI, human review 비용의 상한과 중단 조건을 정할 수 없을 때
- compile success만으로 behavioral equivalence를 주장해야 하는 상황일 때

`Don't migrate`는 실패가 아니라 정상적인 feasibility 결론이다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/claude의-dynamic-workflow에-대해-알려줘/README|Claude Dynamic Workflows]] — 대규모 parallel agent orchestration
- [[tech/devtools/git/github-repo-merge|GitHub Repository Merge]] — branch와 변경 통합 맥락

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://bun.com/blog/bun-in-rust
- https://aclanthology.org/2025.findings-acl.140/
- https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
