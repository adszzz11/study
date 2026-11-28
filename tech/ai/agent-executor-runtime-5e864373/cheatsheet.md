---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: AX 빠른 참조

## Resource

| Resource | 기억할 역할 |
|---|---|
| Task | 목표 + 실행 profile + 격리 실행 |
| Workspace | Git / MCP server / skill package 준비 |
| Model | 플랫폼 LLM과 credential 연결 |
| Gateway | 접근 host와 credential injection 선언 |

API version: `ax.io/v1alpha1`. Image는 digest로 고정한다.

## 운영 동작

| 동작 | 의미 | 주의 |
|---|---|---|
| `ax apply` | resource 선언 적용 | 새 Task는 Suspended |
| `ax resume task …` | 준비 및 실행 시작 | 첫 실행의 Workspace 초기화 대기 |
| `ax suspend task …` | actor checkpoint 후 중단 | 외부 transaction의 원자성 보장 아님 |
| `ax get` / `ax describe` | 상태 / 상세 정보 조회 | CLI 대기 종료와 실제 실패 구분 |
| `ax ssh` | 실행 중 sandbox 점검 | Task에 `spec.debug: true` 필요 |
| `ax promote` | 다른 context로 연결 resource 복사 후 resume | live memory migration으로 단정 금지 |

각 명령의 인자와 옵션은 선택한 release의 `--help`로 확인한다.

## 실행 전 체크

- [ ] release와 runner 호환성 확인; `v0.4.0-rc.2`는 수집 예시다.
- [ ] image digest와 Git commit 기록.
- [ ] Gateway 접근 범위 및 credential 정책 확인.
- [ ] CPU/memory 제한과 종료 조건 검토.
- [ ] 비용 관찰·중단 기준 별도 마련; 내장 hard budget은 미확인.

## 장애·관측 힌트

- 첫 resume 지연: Git clone과 Workspace 준비 상태부터 확인.
- CLI 대기 종료: `get` / `describe`로 background 진행 여부 확인.
- trace 연계: CLI `--trace`, RPC sampled W3C `traceparent`.
- CLI span export: `OTEL_EXPORTER_OTLP_ENDPOINT` 설정 시 OTLP 사용.
- server 관측: `ax-server` logs·metrics·traces·events.

## 헷갈리기 쉬운 경계

```text
AX: agent resource 의미와 선언
Substrate: actor 배치·격리·snapshot·network 실행
Image digest 고정 ≠ 모든 입력과 결과의 불변성
Suspend/resume ≠ 외부 side effect의 exactly-once
Promote ≠ 확인된 live memory migration
규모 설계 목표 ≠ benchmark
```

## 연결

[[tech/ai/agent-executor-runtime-5e864373/04-learning/01-getting-started|실행 절차]] · [[tech/ai/agent-executor-runtime-5e864373/03-references|근거 확인]] · [[tech/ai/agent-executor-runtime-5e864373/README|학습 진입점]]

## Sources

- https://github.com/google/ax — 제공 dossier의 원 출처 저장소. 본 노트는 dossier 기반이며 현재 원격 저장소와 대조하지 않았다.
- https://github.com/google/ax/releases — 설치 버전과 runner 호환 조건 확인 위치. 수집 예시 `v0.4.0-rc.2`를 최신 버전으로 간주하지 않는다.
