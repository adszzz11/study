---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 해석

## Primary Reference

| 자료 | URL | 읽을 관점 |
|---|---|---|
| Agent Substrate repository | https://github.com/agent-substrate/substrate | README, architecture, demo, 설치 prerequisites와 실제 명령 확인 |

이 노트 묶음은 제공된 dossier를 정리한 draft다. 원문 최신 버전, commit SHA, 실행 결과는 검증하지 않았다. dossier는 Counter Demo의 prerequisites 이후 문장 중간에서 끝나므로 설치·배포 명령을 추정하지 않는다.

## Evidence Map

| 항목 | 근거 수준 | 후속 확인 |
|---|---|---|
| Actor/Worker 분리·snapshot·외부 egress | 자료에 명시된 설계 | 현재 구현과 배포 구성 |
| resume <500ms·activation >500/s | 프로젝트 성능 주장 | 하드웨어·부하·snapshot 크기·percentile |
| 10배 밀도·10–30배 oversubscription | 프로젝트 성능 주장 | baseline·동시 활성 비율·자원 한도 |
| 약 250 Actor / 8 physical Pod | demo 범위 | 재현 절차·실제 요청량 |
| CPU 지속 사용 시 공유 이점 감소 | 구조로부터의 추론 | workload별 측정 |
| 외부 연결 생존·exactly-once | 제공 자료에 보장 없음 | 실패·재시도·idempotency 실험 |

## 읽기 체크리스트

- [ ] 참조할 commit SHA와 확인 날짜 기록.
- [ ] demo 경로·명령·필요 권한을 해당 버전 README에서 확인.
- [ ] backend별 host 요구사항과 snapshot storage 구성 확인.
- [ ] egress interception의 protocol·client 지원 범위 확인.
- [ ] API stability·license·운영 지원 범위를 도입 전에 확인.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
