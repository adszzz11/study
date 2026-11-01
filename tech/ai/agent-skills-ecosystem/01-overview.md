---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills Overview

## What

Agent Skill은 agent가 특정 상황에서 불러 쓰는 filesystem-native capability package다. 최소 단위는 YAML frontmatter를 포함한 `SKILL.md`이며, 필요에 따라 `scripts/`, `references/`, `assets/`를 같은 폴더에 둔다.

```text
skills/pr-review/
├── SKILL.md          # trigger, 절차, 품질 기준
├── scripts/          # 반복 검증·리포트 자동화
├── references/       # 길거나 전문적인 지식
└── assets/           # template, fixture, diagram source
```

## Why

거대한 `AGENTS.md`나 긴 prompt는 모든 지침을 매 task의 context에 싣는다. 이는 비용과 주의력 부담을 높이고, task별 지침을 유지보수하기 어렵게 한다. Skills는 다음 순서로 정보를 늦게 연다.

```text
metadata(name, description) → SKILL.md → 필요한 references/scripts/assets
```

이 구조는 agent가 필요한 전문 workflow만 읽도록 하며, 같은 작업 방식을 repository와 제품 경계를 넘어 재사용하게 한다.

## 핵심 특징

| 특징 | 의미 | 설계 포인트 |
|---|---|---|
| Discovery contract | `description`으로 언제 쓸지를 판단 | 작업과 trigger를 구체적으로 쓴다 |
| Progressive disclosure | 필요한 정보만 단계적으로 로드 | 긴 지식은 `references/`로 분리 |
| Composition | 여러 Skill을 한 task에 조합 | baseline 규칙과 조건부 workflow를 구분 |
| Executable workflow | script 실행 결과를 context로 회수 | prose보다 재현 가능한 검증을 우선 |
| Portability | `SKILL.md` 중심 포맷이 확산 | 제품별 path·sandbox 차이는 확인 |
| Security boundary | 실행 가능한 공급망 패키지 | 설치 전 모든 파일과 권한을 audit |

## 핵심 구분

- **`AGENTS.md` / custom instructions**: 항상 적용되는 build, style, security baseline.
- **Skill**: 특정 조건에서만 필요한 순서화된 전문 workflow.
- **MCP**: 외부 시스템의 data와 action을 제공하는 tool connection.

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/04-learning/01-getting-started|시작하기]]
- [[tech/ai/agent-skills-ecosystem/02-ecosystem|Ecosystem]]

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://developers.openai.com/api/docs/guides/tools-skills
