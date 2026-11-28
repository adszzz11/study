---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: AX가 관리하는 것

## What

AX는 agent workload를 선언하고 운영하는 runtime이다. 모든 resource는 `ax.io/v1alpha1` manifest로 표현하고 `ax apply`로 적용한다.

| Resource | 역할 | 해석 경계 |
|---|---|---|
| Task | 목표와 실행 profile, 격리된 agent 실행 | Workspace profile 상속 가능 |
| Workspace | Git repository·MCP server·skill package 준비 | 단순 코드 디렉터리가 아님 |
| Model | 플랫폼 자체의 LLM 및 credential 연결 | agent의 모든 model 호출을 강제 통제한다는 근거 없음 |
| Gateway | 접근 host와 credential injection 설정 | 실제 network 집행은 Substrate 책임과 연결 |

README의 “three small primitives”라는 표현과 별개로, 기능 설명에 등장하는 네 resource를 함께 학습한다.

## Why

- **환경 일관성:** agent가 준비된 repository와 tool 환경에서 시작하도록 한다.
- **자원·접근 통제:** CPU/memory limit, network egress 정책, credential injection을 조합한다.
- **상태 보존:** idle agent를 suspend하고 이전 상태에서 resume한다.
- **운영 이식성:** 로컬 Kind부터 remote cluster까지 같은 운영 경험을 지향한다.

반복 실행은 비용을 누적시킬 수 있다. 이 문제를 동기로 제시한다는 사실과 token hard budget 기능을 제공한다는 주장은 구분한다.

## Architecture

```text
CLI / AX Studio (local web app)
        | CLI: gRPC
        v
AX control plane
  Task / Workspace / Model / Gateway
        |
        v
Agent Substrate
  actor scheduling / isolation / snapshot
  suspend / resume / networking / egress / credential injection
        |
        v
Worker: sandboxed actor / task container
```

AX는 workload의 의미와 선언을, Substrate는 실행 기반을 맡는다. 자료는 task execution 외에는 두 시스템이 orthogonal하다고 설명한다. AX를 sandbox 구현 자체로 설명하거나 Substrate를 단순 내부 scheduler로 축소하지 않는다.

## Lifecycle과 특징

1. `apply`로 Task를 생성하면 `Suspended` 상태다.
2. 첫 `resume`에서 Workspace 초기화와 Git clone을 기다린다.
3. 실행 중 상태를 확인하고 필요하면 suspend한다.
4. suspend는 actor state를 checkpoint하고 중단한다.
5. resume으로 다시 실행한다. 외부 API side effect의 중복 방지는 별도 검토한다.

Task image는 digest로 고정한다. 지정 위치는 `spec.profile.image`, `spec.profile.ateTemplate.name` 또는 Workspace의 `spec.profile`이다. digest만으로 Git branch, model 응답, 외부 tool 결과까지 고정되지는 않는다.

## 확인되지 않은 사항

- 동일 Workspace를 참조하는 Task 간 파일 공유·동시성·충돌 처리.
- checkpoint 주기, 장애 복구 보장, 구체적인 multi-tenant 보안 경계.
- runner contract의 상세 내용 및 버전별 호환 조건.
- 대규모 실행 benchmark와 token 비용 자동 차단.

## 다음 읽기

[[tech/ai/agent-executor-runtime-5e864373/02-ecosystem|구성요소와 대안 비교]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
