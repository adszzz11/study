---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo

> **한 줄 정의**: Paseo는 기존 coding-agent CLI를 로컬에서 실행·감독하고 desktop·mobile·web·CLI에서 통합 제어하는 open-source, self-hostable orchestration platform이다.

## Overview

Paseo는 Claude Code, Codex, OpenCode, Pi와 ACP-compatible agent를 대체하지 않는다. 사용자가 이미 설치하고 인증한 CLI 위에 공통 **control plane**을 제공한다.

- local-first daemon이 agent process, terminal, workspace, service를 관리한다.
- provider별 차이를 adapter와 공통 session/control API로 정규화한다.
- Git worktree로 parallel agent의 disk-level edit collision을 줄인다.
- MCP tools와 CLI로 cross-provider delegation과 automation을 구성한다.
- desktop, iOS, Android, web, CLI에서 같은 daemon을 제어한다.
- remote 접속에는 선택적 E2EE relay를 사용할 수 있다.

> [!warning] 이름 구분
> 이 노트의 Paseo는 [`getpaseo/paseo`](https://github.com/getpaseo/paseo)이며 **Polkadot Paseo TestNet**과 다른 프로젝트다.

2026-08-08 기준 latest stable은 `v0.2.5`, latest pre-release는 `v0.3.0-beta.4`다. 개발 속도는 빠르지만 version number상 초기 프로젝트로 보고 upgrade 전 release note와 backup·rollback 경로를 확인하는 편이 안전하다.

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why와 핵심 특징 파악
- [ ] [[02-ecosystem|Ecosystem]] — Omnara, Conductor 및 native workflow와 비교
- [ ] [[03-references|References]] — 공식 문서와 repository source map 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — 첫 agent 실행·감독 workflow 실습
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — adapter, worktree, relay, orchestration 구조 이해
- [ ] [[05-projects|Projects]] — parallel implementation과 remote supervision 적용
- [ ] [[cheatsheet|Cheatsheet]] — 자주 쓰는 명령과 보안 점검표 익히기

## When To Use

- Claude Code, Codex 등 여러 provider를 한 화면과 공통 CLI에서 다뤄야 할 때
- 여러 task를 별도 branch/worktree에서 병렬 실행해야 할 때
- 장시간 agent 작업을 mobile이나 다른 client에서 확인·추가 지시할 때
- agent가 다른 provider의 agent에게 하위 작업을 위임해야 할 때
- terminal, dev server, diff, PR, agent conversation을 workspace 단위로 묶고 싶을 때
- 기존 provider subscription과 로컬 credential을 유지하며 self-hosted control plane이 필요할 때

## When Not To Use

- 단일 agent의 짧은 interactive session만으로 충분할 때
- agent process에 대한 강한 security sandbox가 필요한데 별도 container/VM 정책이 없을 때
- 조직 정책상 local credential을 읽을 수 있는 subprocess 실행을 허용하지 않을 때
- worktree를 쓸 수 없는 repository이거나 branch 통합 비용이 병렬화 이익보다 클 때
- 초기 버전의 빠른 변경과 운영·upgrade 부담을 감수하기 어려울 때
- 완전 managed cloud execution과 SLA가 핵심 요구사항일 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../../ai/codex/README|Codex tool-study]] — Paseo가 감독할 수 있는 coding-agent CLI
- [[../../ai/agent-orchestration/cli-agents|CLI agents]] — CLI agent orchestration의 broader context

## Sources

- [Paseo — Why](https://paseo.sh/docs/why)
- [Paseo GitHub repository](https://github.com/getpaseo/paseo)
- [Supported providers](https://paseo.sh/docs/supported-providers)
- [Orchestration](https://paseo.sh/docs/orchestration)
- [Security](https://paseo.sh/docs/security)
- [GitHub Releases](https://github.com/getpaseo/paseo/releases)
