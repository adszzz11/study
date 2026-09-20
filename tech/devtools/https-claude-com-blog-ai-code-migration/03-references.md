---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Code Migration — References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: Getting Started]]

## 핵심 자료

| 자료 | 성격 | 읽을 포인트 |
|---|---|---|
| [AI Code Migration](https://claude.com/blog/ai-code-migration) | Anthropic 사례·방법론 | portable judge, rulebook, stress test, iterative loop, 내부 사례 수치 |
| [Migration Starter Kit](https://github.com/anthropics/code-migration-kit-with-claude-code) | 실행 template | read-only feasibility, migration artifact와 단계 구성 |
| [Bun is being rewritten in Rust](https://bun.com/blog/bun-in-rust) | 대상 프로젝트 기술 보고 | Zig → Rust mapping, CI 결과, memory·binary·performance, `unsafe` 비율 |
| [CODEMENV](https://aclanthology.org/2025.findings-acl.140/) | ACL 2025 benchmark | one-shot code migration의 낮은 `pass@1`, 검증 필요성 |
| [Dynamic Workflows 소개](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) | orchestration 배경 | parallel subagent, resume, token·permission 운영 주의 |

## 출처별 신뢰도 메모

| Claim 유형 | 우선 출처 | 해석 원칙 |
|---|---|---|
| Anthropic migration 처리량 | Anthropic 원문 | vendor 자체 보고로 표시하고 일반화하지 않는다. |
| Bun 성능·memory·binary | Bun 기술 보고 | benchmark 환경과 workload 범위 안에서만 해석한다. |
| LLM translation 정확도 | peer-reviewed CODEMENV | package·language·model 범위를 확인한다. |
| 실행 절차 | starter kit | template이지 repository 독립 보증은 아니다. |
| workflow 기능·비용 | Dynamic Workflows 원문 | preview 상태와 최신 제한은 실행 시 다시 확인한다. |

## 핵심 Claim Map

| Claim | 근거 | 연결 노트 |
|---|---|---|
| one-shot translation은 production migration에 부족하다 | CODEMENV 평균 `pass@1` 26.50%, 최고 43.84% | [[01-overview]] |
| portable judge를 translation보다 먼저 만들어야 한다 | Anthropic 원문, starter kit | [[04-learning/01-getting-started]] |
| 반복 오류는 file patch보다 rulebook 수정으로 해결한다 | Anthropic 원문 | [[04-learning/02-deep-dive]] |
| 대형 build는 agent마다 실행하지 말고 직렬화할 수 있다 | Anthropic 원문 | [[04-learning/02-deep-dive]] |
| Bun port의 최종 수치는 약 100만 줄, merge 전 CI 100% pass다 | Anthropic 원문 | [[01-overview]] |
| CI pass 후에도 production regression이 발생했다 | Anthropic 원문 | [[cheatsheet]] |

## 읽는 순서

1. CODEMENV로 one-shot translation의 한계를 먼저 확인한다.
2. Anthropic 원문에서 전체 pipeline과 사례를 읽는다.
3. Starter Kit의 feasibility 질문을 자신의 repository에 대입한다.
4. Bun 기술 보고에서 language-specific gap과 성능 claim을 분리해 본다.
5. Dynamic Workflows 글에서 orchestration의 비용·권한 조건을 확인한다.

## 검증 질문

- `100% test pass`가 어떤 suite와 시점을 뜻하는가?
- production regression 19건은 judge의 어떤 blind spot을 드러내는가?
- 약 4%의 `unsafe`는 기존 FFI·pointer semantics와 어떤 관련이 있는가?
- 처리량 claim에 human preparation, CI, review 비용이 포함되었는가?
- 내 repository에서 같은 pipeline을 막는 가장 큰 artifact 부족은 무엇인가?

## Sources

- https://claude.com/blog/ai-code-migration
- https://github.com/anthropics/code-migration-kit-with-claude-code
- https://bun.com/blog/bun-in-rust
- https://aclanthology.org/2025.findings-acl.140/
- https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
