---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# SkillSpector — AI Agent Skill 공급망 보안 스캐너

> **한 줄 정의**: SkillSpector는 `SKILL.md`, 실행 스크립트, dependency, MCP metadata를 함께 분석해 AI agent skill을 설치·배포 전에 검사하는 security scanner다.

## Overview

Agent skill은 자연어 instruction만이 아니라 code, reference, asset, permission metadata를 함께 담는 capability package다. SkillSpector는 이 복합 artifact의 선언과 실제 행위를 함께 살펴 pre-install / pre-publication security gate를 제공한다.

- Python CLI와 LangGraph workflow 기반의 통합 분석기
- static pattern/YARA, Python AST, lightweight taint, OSV lookup, MCP 검사 지원
- terminal·JSON·Markdown·SARIF 2.1.0 report 및 `scan_skill()` MCP integration 제공
- score는 판단 보조다. runtime sandbox나 malware detonation을 대체하지 않는다.

## Learning Path

- [ ] [[tech/devtools/agent-skill-security-scanner/01-overview|Overview]] — 문제와 핵심 기능 이해
- [ ] [[tech/devtools/agent-skill-security-scanner/02-ecosystem|Ecosystem]] — 보완 도구와 역할 분리
- [ ] [[tech/devtools/agent-skill-security-scanner/04-learning/01-getting-started|시작하기]] — static-only scan 실행
- [ ] [[tech/devtools/agent-skill-security-scanner/04-learning/02-deep-dive|심화 학습]] — finding, CI, MCP guardrail 설계
- [ ] [[tech/devtools/agent-skill-security-scanner/05-projects|Projects]] — registry와 onboarding 적용
- [ ] [[tech/devtools/agent-skill-security-scanner/03-references|References]] — 원문·사양 읽기
- [ ] [[tech/devtools/agent-skill-security-scanner/cheatsheet|Cheatsheet]] — 명령과 운영 기준 빠른 참조

## When To Use

- 외부 skill의 Git URL, ZIP, directory를 agent에 설치하기 전
- skill registry publication PR과 catalog onboarding을 검토할 때
- MCP tool description, permission, executable script의 불일치를 찾아야 할 때
- CI에서 skill-specific 위험을 SARIF 기반으로 추적할 때

## When Not To Use

- 실행 중 행위 관찰, sandbox 격리, active malware detonation이 목적일 때
- application code만 심층 SAST하려는 경우 — Semgrep 같은 도구를 병행한다.
- dependency CVE나 leaked secret만을 완전하게 판정하려는 경우 — OSV-Scanner와 TruffleHog를 보완한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/agent-skill-security-scanner/02-ecosystem|Agent skill security ecosystem]]

## Sources

- https://github.com/NVIDIA/skillspector
- https://docs.nvidia.com/skills/scanning-agent-skills
- https://openreview.net/pdf?id=rVAPXHmGHN
