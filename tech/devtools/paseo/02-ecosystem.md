---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — Ecosystem

> [[01-overview|이전: Overview]] | [[README|목차로 돌아가기]] | [[03-references|다음: References]]

## 포지션

Paseo의 중심 포지션은 **self-hosted, multi-provider agent control plane**이다. remote UX만 제공하거나 worktree GUI에 집중하는 도구와 달리, local daemon 위에서 cross-device control, cross-provider delegation, worktree, terminal/service automation을 함께 다룬다.

## 경쟁·대안 비교

| 도구 | 중심 포지션 | 실행·데이터 모델 | Client | Provider 범위 | Paseo 대비 |
|---|---|---|---|---|---|
| **Paseo** | Self-hosted agent control plane | local daemon, optional E2EE relay | desktop, iOS, Android, web, CLI | Native + 다수 ACP agent | orchestration, mobile, worktree, service 관리가 한 시스템에 결합 |
| **Omnara** | Remote agent command center | local session, optional cloud-backed continuation | desktop, web, mobile, Apple Watch | Claude Code, Codex | remote/mobile UX와 cloud continuation이 강점; provider 폭은 더 좁음 |
| **Conductor** | Parallel desktop coding workspace | task별 Git worktree와 branch | desktop 중심 | Claude Code, Codex, Cursor, OpenCode | worktree·diff·PR UX가 강점; Paseo는 mobile/remote와 agent-driven orchestration 범위가 넓음 |
| **Provider native CLI** | 단일 provider의 coding workflow | local CLI session | terminal, provider별 client | 해당 provider 중심 | setup이 단순하고 native feature가 빠름; cross-provider control과 공통 workspace UX는 직접 구성해야 함 |
| **직접 만든 tmux + worktree workflow** | Unix 조합형 automation | local process와 Git primitives | terminal | 실행 가능한 모든 CLI | 투명하고 vendor-neutral; mobile UX, state API, pairing, agent tools를 직접 구현해야 함 |

## 선택 기준

### Paseo가 맞는 경우

- 두 개 이상의 provider를 실제로 함께 운용한다.
- 사람이 remote에서 관찰하는 것뿐 아니라 agent-to-agent delegation도 필요하다.
- worktree마다 setup, test, dev server, dynamic port를 반복 가능하게 선언하고 싶다.
- code와 credential을 기존 개발환경에 유지하는 self-hosted 운영을 선호한다.

### Omnara를 검토할 경우

- 핵심 문제가 remote/mobile supervision이다.
- Claude Code와 Codex만으로 provider 범위가 충분하다.
- cloud-backed continuation이 중요한 선택 기준이다.

### Conductor를 검토할 경우

- desktop에서 parallel task, diff review, PR workflow가 중심이다.
- cross-device control보다 polished worktree GUI가 우선이다.

### Native CLI 또는 직접 조합이 나은 경우

- 단일 provider와 소수 session만 쓴다.
- daemon이라는 추가 운영 계층을 원하지 않는다.
- tmux, Git worktree, shell script로 필요한 automation을 이미 안정적으로 운영한다.

## Trade-offs

| 축 | Paseo의 이점 | 비용·주의점 |
|---|---|---|
| Provider abstraction | 공통 discovery와 session control | provider-native feature가 adapter에 즉시 반영되지 않을 수 있음 |
| Local-first | 기존 code·credential·subscription 활용 | daemon host의 권한과 secret 관리 책임이 사용자에게 있음 |
| Worktree isolation | edit collision 감소, 병렬 실행 | merge conflict와 shared external resource 충돌까지 없애지는 못함 |
| Remote relay | mobile/web 접근과 E2EE payload | metadata 노출, pairing URL 관리, network hardening 필요 |
| Broad surface | UI·CLI·API 기능 대칭성 | 초기 프로젝트에서 upgrade/testing surface가 커짐 |

## Sources

- [Paseo — Why](https://paseo.sh/docs/why)
- [Paseo — Orchestration](https://paseo.sh/docs/orchestration)
- [Paseo — Git worktrees](https://paseo.sh/docs/worktrees)
- [Omnara Quickstart](https://docs.omnara.com/quickstart)
- [Conductor documentation](https://www.conductor.build/docs)
