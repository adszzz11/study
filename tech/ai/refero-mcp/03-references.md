---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Refero MCP — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Official Sources

| 자료 | 확인할 내용 |
|---|---|
| [Refero MCP landing](https://refero.design/mcp) | product positioning, access, corpus 표기 |
| [refero_skill repository](https://github.com/referodesign/refero_skill) | official package, read-only 설명, 설치 경로 |
| [MCP manifest](https://github.com/referodesign/refero_skill/blob/master/.mcp.json) | hosted endpoint와 secret-free manifest |
| [Refero Design Skill](https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/SKILL.md) | research layers와 workflow |
| [Visual workflow / QA](https://github.com/referodesign/refero_skill/blob/master/skills/refero-design/references/visual-workflow.md) | implementation 후 visual validation |
| [Codex plugin manifest](https://github.com/referodesign/refero_skill/tree/master/.codex-plugin) | Codex distribution 구조 |
| [Repository issue #1](https://github.com/referodesign/refero_skill/issues/1) | tool/API documentation drift 사례 |

## Adjacent and Third-party Sources

- [Fudge comparison](https://design.withfudge.com/share/refero-design-mcp) — Refero와 precise page inspection의 역할 비교.
- [`fidgetcoding/refero-design-mcp`](https://github.com/fidgetcoding/refero-design-mcp) — 공식 hosted server와 별개인 community project. 설치 전 optional write path, local cache, OpenAI key handling을 따로 검토한다.

## Reading Order

1. landing과 README로 product/access boundary를 확인한다.
2. manifest로 endpoint와 OAuth connection model을 확인한다.
3. Skill과 visual workflow로 research-first 방법론을 읽는다.
4. client에서 실제 tool discovery를 실행한다. 공개 문서의 tool name을 고정 계약으로 간주하지 않는다.

## Sources

- https://refero.design/mcp
- https://github.com/referodesign/refero_skill
- https://github.com/fidgetcoding/refero-design-mcp
