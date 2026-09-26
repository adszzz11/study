---
date: 2026-09-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Claudian

> **한 줄 정의**: Claudian은 Obsidian Desktop vault를 workspace로 삼아 Claude Code·Codex 같은 local AI coding agent를 sidebar chat과 inline edit에서 실행하는 MIT 오픈소스 plugin이다.

## Overview

Claudian은 “현재 노트와 대화하는 chat UI”보다 넓은 도구다. 선택한 native CLI에 vault 경로를 전달해 파일 읽기·쓰기, 검색, Bash, MCP, multi-step workflow를 수행하게 하므로, Markdown 지식 저장소를 agent workspace로 바꾼다.

```text
Obsidian vault → Claudian UI/adapter → native agent CLI → files · search · Bash · MCP
                                                    ↘ provider approval policy
```

2026-09-27 기준 main manifest는 `2.3.5`, Obsidian `1.13.0+` Desktop 전용이다. 실제 모델, 승인, history 규칙은 Claudian이 재정의하지 않고 provider CLI의 규칙을 따른다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, 작동 방식, 핵심 특징
- [ ] [[02-ecosystem|Ecosystem]] — fork·대안·적용 경계 비교
- [ ] [[03-references|References]] — 공식 문서와 권장 읽기 순서
- [ ] [[04-learning/01-getting-started|Getting Started]] — disposable vault에서 안전하게 첫 작업 실행
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — adapter, context, MCP/Skills, approval 설계
- [ ] [[05-projects|Projects]] — 지식 관리·문서 유지보수 프로젝트
- [ ] [[cheatsheet|Cheatsheet]] — UI, 안전 점검, prompt 빠른 참조

## When To Use

- 여러 Markdown 노트를 검색·재구성하고 wikilink 후보까지 제안받고 싶을 때
- 이미 Claude Code, Codex 등 CLI 인증과 MCP/Skills 환경을 갖췄을 때
- diff를 검토하며 frontmatter 정규화, broken link 검사, 조사 노트 정리를 반복할 때
- vault-local instruction과 CLI approval을 이용해 agent 작업 경계를 관리할 수 있을 때

## When Not To Use

- 단일 노트의 요약·초안만 필요하고 file-system agent 권한이 과도할 때
- 개인 비밀, credential, 민감한 기록을 provider로 전송할 위험을 통제할 수 없을 때
- Obsidian Mobile 또는 Obsidian Desktop `1.13.0` 미만 환경일 때
- CLI 설치·로그인·PATH·provider approval을 운영할 의사가 없을 때
- 검토 없이 agent가 vault 또는 shell 변경을 자율 적용해야 하는 업무일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/claude/README|Claude]] — Claude Code와 agent workflow의 기반
- [[tech/ai/model-context-protocol-mcp/README|Model Context Protocol (MCP)]] — MCP 도구 연결의 배경

## Sources

- [Claudian GitHub repository / README](https://github.com/YishenTu/claudian)
- [Claudian manifest.json](https://raw.githubusercontent.com/YishenTu/claudian/main/manifest.json)
- [Claudian Community Plugin listing](https://community.obsidian.md/plugins/realclaudian)
- [Obsidian — Community plugins security](https://help.obsidian.md/community-plugins)
