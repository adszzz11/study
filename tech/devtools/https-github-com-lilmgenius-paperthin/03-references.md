---
date: 2026-08-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Paperthin — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 자료

- [Repository/README](https://github.com/LilMGenius/paperthin) — 문제 정의, quickstart, 전체 index
- [v0.17.4 release](https://github.com/LilMGenius/paperthin/releases/tag/v0.17.4) — 2026-08-18 release
- [package.json](https://github.com/LilMGenius/paperthin/blob/main/package.json) — package metadata
- [MIT License](https://github.com/LilMGenius/paperthin/blob/main/LICENSE)
- [Agent Skills specification](https://agentskills.io/specification) — directory 형식과 progressive disclosure

## 설계와 구현

| 자료 | 확인할 내용 |
|---|---|
| [Invocation design](https://github.com/LilMGenius/paperthin/blob/main/docs/invocation.md) | model-invoked/user-invoked 구분과 capability boundary |
| [Plugin manifest](https://github.com/LilMGenius/paperthin/blob/main/.claude-plugin/plugin.json) | 28개 skill path roster |
| [Catalog source](https://github.com/LilMGenius/paperthin/blob/main/scripts/catalog.cjs) | shared CommonJS catalog, install detection, update state |
| [CI workflow](https://github.com/LilMGenius/paperthin/blob/main/.github/workflows/ci.yml) | Node.js 24 validation과 drift guard |

## 대표 skill source

- [`re0`](https://github.com/LilMGenius/paperthin/blob/main/skills/depth/re0/SKILL.md) — clean v0 rewrite와 no-op invariant
- [`factchk`](https://github.com/LilMGenius/paperthin/blob/main/skills/depth/factchk/SKILL.md) — 양방향 external verification
- [`sip`](https://github.com/LilMGenius/paperthin/blob/main/skills/depth/sip/SKILL.md) — artifact 후 QA routing
- [`re0-loop`](https://github.com/LilMGenius/paperthin/blob/main/skills/coil/re0-loop/SKILL.md) — 장기 iteration과 실제 surface evidence
- [`re0-upgrade`](https://github.com/LilMGenius/paperthin/blob/main/skills/breadth/re0-upgrade/SKILL.md) — catalog convergence와 confirmation

## 읽을 때의 검증 질문

- `[PROOF]`가 독립 benchmark인가, 제작자의 dogfooding/case report인가?
- skill의 `description`이 trigger 조건과 금지 조건을 충분히 구체화하는가?
- `disable-model-invocation: true`가 외부 변경을 동반하는 skill에 적용되는가?
- source, plugin manifest, upgrade roster가 같은 catalog를 가리키는가?
- release artifact와 tag의 provenance를 확인할 수 있는가?
- global install, symlink, session-start hook이 어떤 filesystem 범위를 읽는가?

## 조사 스냅샷

| 항목 | 2026-08-27 기준 |
|---|---|
| 최신 release | `v0.17.4` (2026-08-18) |
| catalog | 28 skills |
| user-invoked | 12 skills |
| license | MIT |
| GitHub 표시 | 약 158 stars, 21 forks |

> 숫자는 시점 의존적이다. 학습 노트의 의미를 유지하되 최신 상태 판단에는 release와 repository를 다시 확인한다.

## Sources

- https://github.com/LilMGenius/paperthin
- https://github.com/LilMGenius/paperthin/releases
- https://agentskills.io/specification

