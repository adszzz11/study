---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach

> **한 줄 정의**: Agent Reach는 AI Agent에 웹·소셜·영상 플랫폼의 검색·읽기 능력을 연결하기 위해 upstream CLI와 MCP 도구의 선택·설치·설정·상태 진단을 제공하는 open-source capability layer다.

## Overview

- 조사 대상: **[Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)**. 이름이 비슷한 다른 프로젝트와 구분한다.
- 핵심 가치: 플랫폼별 도구 선택, 인증 조건, 실행 명령, 실패 시 대처를 `SKILL.md`와 references에 정리한다.
- 일반적인 검색·읽기는 Agent가 `gh`, `twitter`, `yt-dlp`, `mcporter`, OpenCLI 등을 직접 호출한다. Agent Reach CLI는 설치·진단을 맡고, `transcribe` 같은 별도 실행 기능도 제공한다.
- 기준일은 **2026-09-09**다. 제공된 dossier와 공식 문서·소스를 바탕으로 **배포된 v1.5.0과 이후 `main`**을 구분했다. 설치 및 플랫폼별 성공률을 직접 측정한 노트는 아니다.

| 구분 | 이 노트에서의 의미 |
|---|---|
| v1.5.0, 2026-06-11 | ordered backend list, OpenCLI 통합, command probe, `active_backend` 도입 |
| 이후 `main` | 기본 설치의 check-only 동작, 인증 진단 제한 등을 포함한 개발 상태 |
| 성공 기준 | 목표 URL에서 작업에 맞는 비어 있지 않은 본문·자막·검색 결과 확보 |

“one CLI”를 모든 플랫폼의 통합 data API로 해석하지 않는다. `doctor`의 성공은 목표 콘텐츠를 이미 가져왔다는 뜻이 아니다. [설치 모델](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md)

## Learning Path

- [ ] [[tech/devtools/agent-reach/01-overview|Overview]] — What/Why, 구조와 버전 차이 이해
- [ ] [[tech/devtools/agent-reach/02-ecosystem|Ecosystem]] — 직접 CLI·MCP·browser 경로와 비교
- [ ] [[tech/devtools/agent-reach/03-references|References]] — 문서·release·소스·이슈의 근거 구분
- [ ] [[tech/devtools/agent-reach/04-learning/01-getting-started|Getting started]] — 환경 점검 후 공개 URL 한 개 검증
- [ ] [[tech/devtools/agent-reach/04-learning/02-deep-dive|Deep dive]] — backend 선택, probe, fallback 추적
- [ ] [[tech/devtools/agent-reach/05-projects|Projects]] — 작은 조사·진단 프로젝트 설계
- [ ] [[tech/devtools/agent-reach/cheatsheet|Cheatsheet]] — 명령과 실패 해석 복습

## When To Use

- 여러 플랫폼을 조사하며 도구별 설치·인증 방법을 반복해서 찾고 있을 때.
- Agent가 CLI와 MCP를 직접 사용할 수 있고, 플랫폼별 fallback 절차가 필요할 때.
- 지원 채널을 한눈에 점검하면서 실제 데이터 수집 결과까지 따로 검증하려 할 때.

## When Not To Use

- `gh` 하나처럼 이미 익숙한 도구만으로 작업이 끝날 때.
- 모든 플랫폼에서 동일한 response schema, 가용성 보장, 완전한 댓글 수집이 필요할 때.
- 로그인 없이 모든 소셜 콘텐츠를 읽거나, browser가 없는 서버에서 desktop backend를 그대로 쓰려 할 때.
- 외부 서비스로 데이터를 보낼 수 없는 작업에 Jina·Exa·외부 transcription 경로를 적용하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/ai/claude/07-mcp|MCP 학습 노트]] — 외부 도구 연결 개념
- [[tech/devtools/ripgrep/README|ripgrep]] — Agent의 로컬 파일 검색과 외부 콘텐츠 읽기 비교

## Sources

- [공식 English README](https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md)
- [v1.5.0 release](https://github.com/Panniantong/Agent-Reach/releases/tag/v1.5.0)
- [현재 설치 가이드](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md)
- [doctor 구현](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py)
