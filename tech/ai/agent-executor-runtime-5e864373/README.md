---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Google AX: 선언형 Agent Workload 실행과 격리 아키텍처

> **한 줄 정의**: AX(Agent Executor)는 Task·Workspace·Model·Gateway를 선언형 manifest로 관리하고, Agent Substrate 위에서 agent workload의 격리 실행과 suspend/resume을 조율하는 Google의 공개 orchestration runtime이다.

## Overview

Agent는 실행 중 상태를 축적하고 model API와 tool server를 호출하며 신뢰하기 어려운 코드를 실행할 수 있다. AX는 이를 상태·실행 환경·접근 권한을 함께 관리하는 infrastructure 문제로 다룬다.

- YAML과 `ax apply`로 목표와 준비 환경을 선언한다.
- AX는 agent 중심 resource model을, Agent Substrate는 scheduling·isolation·snapshot·networking을 담당한다.
- Task는 `Suspended`로 생성되며 명시적인 resume 후 실행된다.
- heavy development 단계다. stable release 전 core concept·protocol·specification의 큰 breaking change가 가능하다.
- cluster당 수백만 task는 설계 목표이며, 제공 자료에 benchmark는 없다.

## Learning Path

- [ ] [[tech/ai/agent-executor-runtime-5e864373/01-overview|Overview]] — 문제 정의와 resource 역할 이해
- [ ] [[tech/ai/agent-executor-runtime-5e864373/02-ecosystem|Ecosystem]] — 기존 workload와 실행 계층 비교
- [ ] [[tech/ai/agent-executor-runtime-5e864373/03-references|References]] — 근거와 미확인 사항 확인
- [ ] [[tech/ai/agent-executor-runtime-5e864373/04-learning/01-getting-started|시작하기]] — 설치 전 점검과 첫 실행 절차
- [ ] [[tech/ai/agent-executor-runtime-5e864373/04-learning/02-deep-dive|심화 학습]] — 상태·격리·재현성 경계 분석
- [ ] [[tech/ai/agent-executor-runtime-5e864373/05-projects|Projects]] — 단계별 검증 프로젝트
- [ ] [[tech/ai/agent-executor-runtime-5e864373/cheatsheet|Cheatsheet]] — 운영 동작과 주의점 빠른 참조

## When To Use

- 상태를 보존하며 agent를 중단·재개하는 운영 실험이 필요할 때.
- Git·MCP server·skill package를 공통 환경으로 준비하고 여러 목표에 재사용할 때.
- sandbox·egress·credential injection 정책과 agent 실행을 함께 검토할 때.
- Kind, GKE, customer cluster, on-prem 사이의 portable 운영 방식을 평가할 때.

## When Not To Use

- stable API와 검증된 운영 보장이 필수인 production 도입을 즉시 결정할 때.
- token hard budget, exactly-once 외부 호출, 완전한 감사 보장이 이미 구현되었다고 가정해야 할 때.
- 단순 stateless service나 일회성 batch로 충분할 때.
- model 품질이나 reasoning algorithm 자체를 개선하는 도구가 필요할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-executor-runtime-5e864373/01-overview|AX resource model과 실행 계층]]

필수 MOC 링크는 vault에 이미 있는 관리 노트를 대상으로 하는 규약이다. 현재 작업 폴더에서는 대상의 존재를 확인할 수 없었으며, 관리 파일은 생성하거나 수정하지 않았다.

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
