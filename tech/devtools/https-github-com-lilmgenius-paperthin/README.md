---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin

> **한 줄 정의**: Paperthin은 software-engineering 원칙을 `SKILL.md` 기반의 재사용 가능한 “agent reflex”로 패키징해 AI coding agent의 과잉 생성, context drift, 자기검증 실패를 줄이는 vendor-neutral Agent Skills library다.

## Overview

Paperthin은 거대한 agent framework가 아니다. 기존 coding agent에 작은 procedure를 추가해, 실패하기 쉬운 순간에 정리·반론·사실 검증·독립 평가·SSOT 통합을 수행하게 한다.

- 2026-08-27 조사 기준 최신 release: `v0.17.4` (2026-08-18)
- catalog: 28 skills (`depth`, `breadth`, `coil`, `mesh`)
- license: MIT
- 설치 형식: 공개 [Agent Skills specification](https://agentskills.io/specification)을 따르는 `SKILL.md` directory
- 핵심 구분: agent가 자동 선택하는 model-invoked skill과 사람만 실행하는 user-invoked skill
- 평가 주의: README의 `[PROOF]`는 주로 제작자의 dogfooding/case report이며 independent controlled benchmark가 아니다.

```bash
npx skills@latest add LilMGenius/paperthin --global --agent '*'
```

## Learning Path

- [ ] [[01-overview|Overview]] — 문제, 설계 철학, 네 가지 scope
- [ ] [[02-ecosystem|Ecosystem]] — framework, rule file, hook, 개별 skill과 비교
- [ ] [[03-references|References]] — 공식 source와 검증 포인트
- [ ] [[04-learning/01-getting-started|Getting Started]] — 설치, discovery, 안전한 첫 적용
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — invocation boundary, progressive disclosure, CI/SSOT
- [ ] [[05-projects|Projects]] — 실제 repository에 적용하는 실습
- [ ] [[cheatsheet|Cheatsheet]] — skill 선택과 빠른 참조

## When To Use

- agent가 요청보다 많은 파일·option·abstraction을 계속 추가할 때
- README나 설계 문서가 변경 이력처럼 누적되어 현재 상태를 파악하기 어려울 때
- 같은 사실이 여러 문서와 manifest에 복제되어 drift가 생길 때
- “그럴듯한 결과”를 외부 source와 독립적으로 검증하고 싶을 때
- 장기 작업의 다음 action과 학습을 iteration 사이에 보존해야 할 때
- 특정 vendor/model 이름을 durable documentation에서 분리하고 싶을 때

## When Not To Use

- skill procedure 없이도 한 번의 작은 수정과 기존 test로 충분할 때
- Paperthin의 case report를 정량적 성능 보장으로 간주하려 할 때
- repository별 policy, domain expert review, security control을 대체하려 할 때
- 모든 skill을 상시 자동 활성화하려 할 때: `hate`, `prism` 같은 절차는 비용과 chronic doubt를 키울 수 있다.
- global install과 session hook의 filesystem 접근 범위를 검토할 수 없는 환경일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/agent-garden|Agent Garden]]
- [[tech/ai/agent-orchestration/cli-agents|CLI Agents]]

## Sources

- https://github.com/LilMGenius/paperthin
- https://github.com/LilMGenius/paperthin/releases/tag/v0.17.4
- https://github.com/LilMGenius/paperthin/blob/main/docs/invocation.md
- https://agentskills.io/specification

