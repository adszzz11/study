---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — Ecosystem과 비교

> [[01-overview|이전: Overview]] | [[README|목차로 돌아가기]] | [[03-references|다음: References]]

## 포지셔닝

AI code migration은 단일 제품보다 **migration system design**에 가깝다. LLM coding agent를 deterministic toolchain과 결합하고, repository마다 rulebook·judge·task graph를 설계한다.

```text
Transformation layer: AST codemod + LLM agents + manual exceptions
Control layer: dependency graph + queue + isolated workspaces + budget
Verification layer: compiler + tests + parity diff + security/performance
Governance layer: phase gates + audit trail + human approval
```

## 접근법 비교

| 접근법 | 강점 | 약점 | 적합한 상황 |
|---|---|---|---|
| Manual rewrite | 높은 domain judgment, redesign 자유도 | 느리고 diff 규모가 커지며 drift 위험 | business rule이 불명확한 핵심 영역 |
| AST/codemod | deterministic, 빠름, review하기 쉬움 | semantic gap과 cross-file behavior에 약함 | 규칙적인 API rename, syntax upgrade |
| One-shot LLM translation | 시작 비용이 낮고 다양한 code 처리 | 결과 편차, hallucination, weak verification | throwaway prototype와 rule 탐색 |
| AI code migration pipeline | 대량 병렬화와 반복 수렴, 복합 semantic 처리 | judge·orchestration 구축 비용, token·CI 비용 | testable한 대규모 language/framework port |
| Strangler/점진 교체 | production risk와 branch drift를 줄임 | bridge·dual-run 운영 복잡도 | 전체 rewrite를 한 번에 merge하기 어려울 때 |

실무에서는 한 가지 방식만 택하기보다 AST transformation으로 확실한 80%를 처리하고, LLM agent가 semantic exception을 다루며, human이 high-risk boundary를 승인하는 hybrid가 합리적이다.

## Port와 Redesign 비교

| 기준 | Structure-preserving port | Redesign |
|---|---|---|
| 우선 목표 | observable behavior 보존 | architecture와 behavior 개선 |
| judge | 원본/target 공용 contract와 parity diff | 새 specification, acceptance test |
| rulebook | source construct의 target mapping | 새 domain boundary와 design rule |
| 위험 | 원본 latent bug까지 복제 | scope 팽창, equivalence 기준 상실 |
| stress test | 대표 파일 mini-port | disposable end-to-end vertical slice |

둘을 한 migration에서 암묵적으로 섞으면 failure가 translation 때문인지 design 변경 때문인지 판별하기 어렵다.

## 도구 역할 비교

| 구성요소 | 하는 일 | 하지 못하는 일 |
|---|---|---|
| LLM coding agent | mapping 적용, exception 추론, review | 독립적 correctness oracle 제공 |
| Compiler/type checker | syntax/type/borrow error 탐지 | 외부 behavior와 성능 보증 |
| Unit/contract tests | 알려진 contract 검증 | 관측하지 않은 behavior 증명 |
| Scenario parity harness | 실제 input/output 차이 탐지 | 어느 쪽 behavior가 옳은지 결정 |
| Mutation testing | judge가 알려진 결함을 잡는지 확인 | 모든 mutation과 production fault 포괄 |
| Human reviewer | risk acceptance와 domain intent 판정 | 수백만 줄을 일일이 정확히 검토 |
| Orchestrator/build daemon | queue, retry, concurrency, build 중복 제어 | 잘못 설계된 rulebook을 자동으로 옳게 만듦 |

## 선택 기준

| 질문 | Yes라면 | No라면 |
|---|---|---|
| 반복 가능한 syntactic rule이 대부분인가? | codemod를 먼저 사용 | LLM/human semantic 분석 비중 증가 |
| portable contract test를 만들 수 있는가? | parity-driven port 가능 | 먼저 characterization test 구축 |
| dependency boundary가 분명한가? | 병렬 batch 확대 | 순차 migration 또는 modularization 선행 |
| redesign이 목표인가? | design doc와 새 acceptance criteria 우선 | source behavior를 oracle로 활용 |
| CI와 review 예산이 충분한가? | agent fan-out 검토 | concurrency와 scope 축소 |

## Dynamic Workflows와의 관계

[[tech/devtools/claude의-dynamic-workflow에-대해-알려줘/README|Claude Dynamic Workflows]]는 이 pipeline을 실행할 수 있는 orchestration 수단 중 하나다. prompt를 task graph로 분해해 implementer와 reviewer를 병렬 실행하고 중단된 작업을 재개할 수 있지만, 다음은 migration 팀이 별도로 정의해야 한다.

- cost ceiling, concurrency, timeout
- filesystem·Git 권한과 workspace isolation
- phase별 deterministic pass/fail gate
- rulebook version과 재생성 대상 추적
- human approval이 필요한 risk boundary

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
- https://aclanthology.org/2025.findings-acl.140/
