---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Substrate — Kubernetes 기반 Zero-trust 에이전트 런타임

> **한 줄 정의**: Agent Substrate는 Kubernetes 위에서 서로 신뢰하지 않는 stateful Actor를 gVisor 또는 microVM으로 격리하고, snapshot·resume과 Worker 공유로 실행 밀도를 높이는 framework-agnostic runtime이다.

## Overview

자율 에이전트는 비신뢰 코드와 도구를 실행하며, 모델·외부 도구·사람의 응답을 오래 기다린다. Substrate는 **상태를 가진 Actor와 실제 실행 자원인 Worker를 분리**한다. 유휴 Actor의 RAM·filesystem을 snapshot으로 보관하고, 요청 시 가용 Worker에 복원한다.

- 격리: 전용 gVisor 또는 Cloud Hypervisor microVM sandbox.
- 밀도: 더 많은 Actor를 더 작은 ready Worker pool에 multiplex.
- 상태 연속성: 프로세스 메모리와 파일 변경 보존.
- 접근 통제: sandbox 외부 identity·egress policy·credential injection.

프로젝트가 제시한 수치: resume <500ms, activation >500회/초, 일반 container 대비 10배 밀도, 10–30배 oversubscription. 약 250 Actor/8 physical Pod demo도 소개한다. **측정 조건과 percentile이 없어 도입 성능 보장으로 해석하면 안 된다.**

## Learning Path

- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/01-overview|Overview: What / Why / 특징]]
- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/02-ecosystem|Ecosystem: 비교와 위치]]
- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/03-references|References: 근거와 확인 항목]]
- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/04-learning/01-getting-started|시작하기: Counter Demo]]
- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/04-learning/02-deep-dive|Deep Dive: 격리·상태·운영]]
- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/05-projects|Projects: 검증 프로젝트]]
- [ ] [[tech/infra/agent-substrate-runtime-a5ffcd0a/cheatsheet|Cheatsheet: 빠른 복습]]

## When To Use

- 대부분의 시간을 기다리며 상태를 이어가는 다수의 agent workload.
- 비신뢰 코드·coding environment·MCP server에 강한 실행 경계가 필요할 때.
- Kubernetes 운영 역량과 snapshot·identity·network 관찰 체계를 갖출 수 있을 때.

## When Not To Use

- 모든 Actor가 지속적으로 CPU를 사용해 Worker 공유 이점이 작을 때.
- 단순한 stateless 작업에 별도 control plane 운영 부담을 정당화하기 어려울 때.
- snapshot이 외부 작업의 exactly-once 실행이나 연결 생존까지 보장해야 할 때.
- plain Linux container를 Actor backend로 요구할 때: 지원하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[tech/infra/agent-substrate-runtime-a5ffcd0a/01-overview|Agent Substrate 아키텍처 개요]]

필수 MOC 링크는 대상 vault의 기존 관리 노트를 전제로 한다. 이 작업 공간에는 vault가 없어 존재 여부를 확인하지 못했으며, 관리 파일은 생성하지 않는다.

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
