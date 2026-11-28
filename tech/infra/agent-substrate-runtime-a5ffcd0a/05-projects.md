---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 검증 프로젝트

아래는 공식 기능 목록이 아니라 학습용 실험 제안이다.

| 프로젝트 | 구현·관찰 | 완료 기준 |
|---|---|---|
| Stateful Counter | 메모리 값+파일 변경 후 suspend·resume | 상태 일치, Worker 이동 여부 분리 기록 |
| 격리된 coding environment | 실험용 파일과 shell state 유지 | resume 후 작업 연속성 확인 |
| Sandboxed MCP server | 테스트 MCP server를 Actor로 배포 | 허용된 egress만 성공, client 호환성 기록 |
| Credential mediation | 테스트 API와 최소 권한 credential 사용 | sandbox에 원문 전달 없이 승인 요청 성공 |
| 밀도 benchmark | 대기 비율과 Worker 수를 바꿔 반복 | latency·오류율·자원·조건을 함께 보고 |
| 포화와 재시도 | WorkerPool 포화 및 외부 요청 재시도 | parking·timeout·중복 작업을 구분 |

## 권장 진행

1. [[tech/infra/agent-substrate-runtime-a5ffcd0a/04-learning/01-getting-started|Counter 실습]]으로 상태 연속성을 확인한다.
2. [[tech/infra/agent-substrate-runtime-a5ffcd0a/04-learning/02-deep-dive|Deep Dive]]로 정책·포화·장애 경계를 확인한다.
3. 실제 도입 판단에 필요한 workload 하나를 선택해 성능과 운영 부담을 기록한다.

## 결과 보고 양식

```text
검증 날짜 / commit:
Backend / node 사양 / Worker 수:
Actor 수 / 동시 활성 비율 / 대기 패턴:
Snapshot 크기 / 저장 조건:
성공률 / timeout / p50·p95·p99:
상태 연속성 / 외부 작업 중복 여부:
관찰된 한계 / 다음 검증:
```

프로젝트 주장의 재현 여부와 자체 환경에서 얻은 수치를 구분한다. 실제 credential·민감한 snapshot 내용은 공개 vault에 기록하지 않는다.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
