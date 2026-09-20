---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: Getting Started]]

## 먼저 읽을 자료

1. [Why Paseo](https://paseo.sh/docs/why) — 해결하려는 문제와 control-plane 관점
2. [Supported providers](https://paseo.sh/docs/supported-providers) — native/ACP 지원 범위
3. [CLI reference](https://paseo.sh/docs/cli) — 사람이 쓰는 workflow와 automation surface
4. [Git worktrees](https://paseo.sh/docs/worktrees) — workspace isolation과 `paseo.json`
5. [Security](https://paseo.sh/docs/security) — process 권한, remote connection, relay threat model

## 공식 문서 지도

| 주제 | 자료 | 확인할 질문 |
|---|---|---|
| 개념 | [Why](https://paseo.sh/docs/why) | Paseo가 agent 자체가 아닌 이유는? |
| Provider | [Providers](https://paseo.sh/docs/providers) | 기존 CLI 인증과 subscription을 어떻게 쓰는가? |
| 지원 범위 | [Supported providers](https://paseo.sh/docs/supported-providers) | native와 ACP adapter의 차이는? |
| 확장 | [Custom providers](https://paseo.sh/docs/custom-providers) | JSON-RPC `initialize`에서 무엇을 보고하는가? |
| Orchestration | [Orchestration](https://paseo.sh/docs/orchestration) | discovery, spawn, follow-up, wait가 어떻게 연결되는가? |
| Workflow | [Orchestration workflows](https://paseo.sh/docs/orchestration-workflows) | same workspace와 new worktree를 언제 나누는가? |
| CLI | [CLI reference](https://paseo.sh/docs/cli) | interactive/CI workflow를 어떤 flag로 구성하는가? |
| Worktree | [Git worktrees](https://paseo.sh/docs/worktrees) | setup, service, dynamic port를 어떻게 선언하는가? |
| Security | [Security](https://paseo.sh/docs/security) | sandbox 경계와 remote trust anchor는 무엇인가? |

## Source Code

- [getpaseo/paseo](https://github.com/getpaseo/paseo) — main monorepo
- [Development / package map](https://github.com/getpaseo/paseo#development) — server, app, CLI, desktop, relay, website 구조
- [GitHub Releases](https://github.com/getpaseo/paseo/releases) — stable/pre-release와 breaking change 확인
- [getpaseo/paseo-relay](https://github.com/getpaseo/paseo-relay) — open-source relay implementation

## Version 체크 기록

| 기준일 | Stable | Pre-release | 판단 |
|---|---|---|---|
| 2026-08-08 | `v0.2.5` | `v0.3.0-beta.4` | 빠르게 개발 중인 초기 프로젝트로 취급 |

> [!tip] 재검증 포인트
> 실제 설치·upgrade 전에는 Releases와 provider compatibility 문서를 다시 확인한다. 이 노트의 버전 정보는 기준일 snapshot이다.

## 비교 자료

- [Omnara Quickstart](https://docs.omnara.com/quickstart)
- [Conductor documentation](https://www.conductor.build/docs)

## Sources

- [Paseo documentation](https://paseo.sh/docs/why)
- [Paseo GitHub repository](https://github.com/getpaseo/paseo)
- [Paseo GitHub Releases](https://github.com/getpaseo/paseo/releases)
- [Paseo relay repository](https://github.com/getpaseo/paseo-relay)
