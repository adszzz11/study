---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 첫 Task의 상태 전이 관찰

## 목표와 준비

목표는 설치 성공 자체보다 `apply → Suspended → resume → suspend → resume`을 관찰하는 것이다. 아래 명령은 dossier에 등장한 동작을 바탕으로 한 안내이며 현재 release에서 실행 검증하지 않았다.

- [ ] 공식 README와 release notes에서 설치 방법과 지원 환경을 확인한다.
- [ ] 선택한 release의 CLI·control plane·Substrate·runner 호환성을 맞춘다.
- [ ] 연습용 Kind 또는 격리된 cluster와 Kubernetes context를 준비한다.
- [ ] 읽기 전용 실습 repository와 최소 권한 credential을 준비한다.
- [ ] image digest 및 repository ref를 기록한다. 가능하면 Git commit을 고정한다.

```sh
# 설치 후: 지원되는 옵션과 resource 문법부터 확인
ax --help
ax apply --help
ax resume --help
ax suspend --help
ax get --help
ax describe --help
```

설치 스크립트와 완성 YAML schema는 dossier에 없어 임의로 만들지 않는다. 선택한 release의 공식 예제를 가져와 `task.yaml`로 저장하고 필수 필드와 resource 참조를 검토한다.

## Manifest 점검

| 항목 | 확인 내용 |
|---|---|
| API | `ax.io/v1alpha1` |
| Workspace | Git, MCP server, skill package 준비 내용 |
| Task | 목표, Workspace 참조, 실행 profile |
| Image | image digest 고정; prebuilt image의 runner volume 요구 확인 |
| Gateway | 필요한 host만 허용, credential injection 범위 확인 |
| Debug | sandbox 점검이 필요한 실습에서만 `spec.debug: true` 고려 |

## 실행 순서

다음 문법은 release의 `--help`와 대조한 뒤 사용한다. `<task-name>`은 실제 Task 이름으로 바꾼다.

```sh
ax apply -f task.yaml
ax get task <task-name>
ax describe task <task-name>
ax resume task <task-name>
ax describe task <task-name>
ax suspend task <task-name>
ax resume task <task-name>
```

1. apply 직후 `Suspended`인지 기록한다.
2. 첫 resume은 Git clone 등 Workspace 초기화를 기다린다.
3. CLI가 대기를 끝내도 background 준비가 진행될 수 있다. `get` / `describe`로 실제 상태를 확인한다.
4. 작은 로컬 파일 변경 등 관찰 가능한 상태를 만든 뒤 suspend/resume 전후를 비교한다.
5. 완료 후 선택한 release의 정리 절차로 실습 resource와 credential을 정리한다. suspend를 resource 삭제와 동일시하지 않는다.

## 성공 기준

- 선언과 실행 시작이 별도 단계임을 확인했다.
- CLI timeout과 workload 실패를 구분할 수 있다.
- 보존되는 상태를 관찰했으며 외부 side effect의 exactly-once를 추정하지 않았다.

## 다음 읽기

[[tech/ai/agent-executor-runtime-5e864373/04-learning/02-deep-dive|심화 학습]] · [[tech/ai/agent-executor-runtime-5e864373/cheatsheet|운영 참조]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
