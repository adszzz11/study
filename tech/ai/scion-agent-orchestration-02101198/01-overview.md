---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion Overview

## What

Scion의 단위는 독립적인 identity를 가진 Agent다. Agent가 사용하는 harness를 대체하지 않고, 팀 실행과 협업에 필요한 환경을 그 바깥에서 제공한다. Project는 agent들을 묶는 namespace이며 일반적으로 Git repository와 1:1로 대응한다.

## Why

긴 작업에서는 누가 어떤 파일을 수정하는지, 발견을 어디에 남기는지, 누가 통합 완료를 선언하는지가 문제가 된다. Scion은 이를 실행 환경·identity·통신·관찰의 문제로 다룬다. “less is more” 철학에 따라 협업 절차는 templates와 instructions로 표현하고 agent는 skills와 help text를 통해 CLI를 사용한다.

## 핵심 구성 요소

| 구성 요소 | 역할 | 학습 시 확인할 점 |
|---|---|---|
| Agent | 보통 container에서 harness를 실행하는 worker | 역할·설정·credentials의 단위 |
| Project | Agent namespace | Repository와 팀의 연결 |
| Template | System prompt와 skills를 묶은 blueprint | 재사용할 역할과 완료 기준 |
| Hub | State·identity·dispatch의 control plane | CLI도 Hub를 통해 실행 |
| Runtime Broker | Hub를 대신해 containerized agent provision·실행 | 제어와 실행 책임의 분리 |
| Runtime | Docker, Podman, Apple Container, Kubernetes, Cloud Run | 모드·버전별 지원 조건 |

```text
사람 / Agent
  → CLI · Web UI · API · 연결된 채팅
  → Hub (state · identity · dispatch)
  → Runtime Broker
  → Runtime 안의 Agent Harness
  → Workspace · skills · tools
```

위 경로는 containerized agent의 개념도다. 지원 provider API를 사용하는 managed-agent 경로도 언급되므로 모든 agent가 이 단계를 거친다고 일반화하지 않는다.

## 운영 모드

| 모드 | 자료에 제시된 구성·사용 방식 |
|---|---|
| Local | CLI 중심 agent 실행 |
| Workstation | 개인용 local Hub·Runtime Broker·Web UI |
| Single-node hosted | VM 또는 Cloud Run에서 networked Hub 공유 |
| HA hosted | Replicated Hub·Postgres·shared storage |

Local은 Hub가 없다는 뜻이 아니다. Quick Start는 `scion server start`로 시작한다. Workstation, hosted Hubs, Kubernetes runtime은 지원되고 사용 중이라고 설명되지만, 로컬 성공이 hosted 환경의 권한·저장소·장애 대응까지 검증하지는 않는다.

## 협업·관찰·확장

- Workspace는 shared directories, Git worktrees, separate clones 중 선택한다. 공유 방식에 맞춰 동시 수정과 결과 통합 규칙을 정한다.
- Native web chat과 Telegram, Discord, Slack, Google Chat, Microsoft Teams 연결이 소개된다. 실제 설정·인증 조건은 선택한 버전에서 확인한다.
- 지원되는 interactive harness에 직접 attach할 수 있다. `scion attach`는 실행 중인 agent의 tmux session에 연결한다.
- Logs, session metrics, system health를 관찰한다. Hosted에서는 roles, access boundaries, scoped secrets, federated identity가 추가된다.
- CLI, APIs, lifecycle hooks, MCP configuration, A2A bridge가 확장 지점이다.
- Harness configuration bundles는 provisioning·authentication을 core 밖에서 정의한다. Skill Bank는 skills의 publishing·versioning 및 GitHub·외부 registry resolution을 지원한다.

## 확인된 한계

Metrics 세부 항목, 감사 로그 보존, 상세 권한 모델, sandbox 보안 수준은 제공 자료에서 확인되지 않았다. Container·credentials 분리를 보안 보장으로 확대 해석하지 않는다. Relics의 telemetry 재생 사례도 모든 배포의 기본 분석 UI를 의미하지 않는다.

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
