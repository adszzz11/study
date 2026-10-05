---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# fast-jev-compaction

> **한 줄 정의**: `fast-jev-compaction`은 TypeSafe Jev가 coding agent의 과거 `tool_use`/`tool_result`를 keep·truncate·drop으로 선별해, 새 summary를 만들지 않고 context를 줄이는 Claude Code plugin 및 TypeScript library다.

## Overview

> 명칭 확인: 공개된 정확한 `Fest-jev-compaction` 프로젝트는 찾지 못했다. 이 노트는 2026년 9월 공개된 [`tamaratran/fast-jev-compaction`](https://github.com/tamaratran/fast-jev-compaction)을 가리킨다는 dossier의 해석을 따른다.

- 긴 agent session의 파일 읽기·test log·shell output을 **extractive pruning**한다.
- 유지한 evidence는 verbatim이지만, 이는 lossless compression이 아니다. 잘못 drop한 근거는 사라진다.
- Jev 판정에 transcript state가 TypeSafe endpoint로 전송되므로, private source·credential·민감 output에는 redaction과 data policy 검토가 선행돼야 한다.

## Learning Path

- [ ] [[01-overview|What / Why / 특징]]을 읽고 summary와 extractive pruning의 차이를 설명한다.
- [ ] [[02-ecosystem|Ecosystem 비교]]로 native compaction·fresh context·RAG의 경계를 정한다.
- [ ] [[04-learning/01-getting-started|Getting started]]에서 live API 없이 synthetic transcript를 관찰한다.
- [ ] [[04-learning/02-deep-dive|Deep dive]]에서 pairing, state fitting, threshold를 점검한다.
- [ ] [[05-projects|Projects]]의 benchmark 설계를 하나 선택해 재현한다.
- [ ] [[cheatsheet|Cheatsheet]]으로 운영 전 점검 항목을 확인한다.

## When To Use

- debugging처럼 정확한 file path, stack trace, command가 이후에도 필요한 긴 tool-heavy session
- native summary가 세부 evidence를 자주 놓치는 workflow의 실험·benchmark
- raw transcript 보관, fallback, redaction 정책을 운영할 수 있는 agent harness

## When Not To Use

- transcript를 외부 판단 endpoint로 보낼 수 없거나 민감 output을 redaction할 수 없는 경우
- 안정적 production 표준, 무손실 압축, 즉시 비용 절감이 요구되는 경우
- filesystem state/progress note만으로 새 context에서 충분히 재개할 수 있는 짧은 작업

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/ripgrep/README|ripgrep]]

## Sources

- https://github.com/tamaratran/fast-jev-compaction
- https://github.com/tamaratran/fast-jev-compaction/blob/main/README.md
- https://code.claude.com/docs/ko/env-vars
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
