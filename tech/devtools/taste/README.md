---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# taste

> **한 줄 정의**: `taste`는 AI coding agent가 관성적인 template 대신 실제 codebase·artifact·audience를 근거로 판단하도록 만드는, 실행 runtime 없는 instruction-only Agent Skill이다.

## Overview

- 이 노트는 동명의 다른 제품이 아닌 **Hmbown/taste v1.0.0 Agent Skill**을 다룬다.
- 핵심 목표는 model에 미적 취향을 새로 주입하는 것이 아니라 `grounding`, `specificity`, `finish calibration`을 작업 절차로 강제하는 것이다.
- `SKILL.md`가 공통 workflow를 정의하고, `references/DOMAINS.md`와 `references/REVIEW.md`를 필요한 순간에만 읽는 progressive disclosure 구조다.
- code, UI, document, data/chart, system design의 생성과 critique에 적용할 수 있다.
- 별도 runtime이나 deterministic 검사기는 없으며 결과 품질은 model과 exemplar에 의존한다.

```text
Ground → Route by domain → Create or Critique → Stop at sufficient finish
```

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why와 핵심 원칙 이해
- [ ] [[02-ecosystem|Ecosystem]] — 대안과 역할 경계 비교
- [ ] [[03-references|References]] — 원문과 보안 검토 지점 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — source 검토, 설치, 첫 적용
- [ ] [[04-learning/02-deep-dive|Deep dive]] — domain routing과 critique 구조 분석
- [ ] [[05-projects|Projects]] — 실제 artifact로 효과 평가
- [ ] [[cheatsheet|Cheatsheet]] — prompt와 판단 순서 빠른 참조

## When To Use

- 결과가 사실상 맞지만 generic하거나 “AI-generated”처럼 느껴질 때
- 기존 codebase, design system, 문서 관행에 자연스럽게 편입해야 할 때
- 외부 공개 문서, UI, architecture proposal처럼 judgment가 중요한 작업
- 여러 설계안을 비교하거나 artifact를 짧고 구체적으로 critique할 때
- source에 없는 가격·정책·feature를 발명하지 않도록 제약해야 할 때

## When Not To Use

- verbatim transformation이나 exhaustive extraction이 목표일 때
- compiler, linter, test, accessibility audit처럼 deterministic 검증이 필요할 때
- exemplar 없이 자유로운 speculative ideation을 넓게 탐색해야 할 때
- 조직 규칙의 자동 학습·영구 저장 또는 강한 품질 보증을 기대할 때
- 검토하지 않은 third-party Skill과 script를 곧바로 production 환경에 설치하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../../ai/codex/README|Codex]] — Agent Skill을 호출할 수 있는 coding agent
- [[../ripgrep/README|ripgrep]] — 실제 repository exemplar와 인접 code를 찾는 도구
- [[../../ai/claude/05-skills|Claude Skills]] — Agent Skills 운용 맥락

## Sources

- [Hmbown/taste README](https://github.com/Hmbown/taste#readme)
- [Hmbown/taste SKILL.md](https://raw.githubusercontent.com/Hmbown/taste/main/SKILL.md)
- [Agent Skills specification](https://agentskills.io/)
- [Anthropic Engineering — Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [OpenAI Academy — Skills](https://openai.com/academy/skills/)

