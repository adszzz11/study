---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Counter Demo

## 목표와 준비

Counter의 값이 suspend·resume 이후 이어지는지 관찰하며 inbound routing → activation → 실행 → snapshot 흐름을 이해한다. 개발 prerequisites로 자료에 명시된 것은 **Go, `kubectl`, Docker**다. 버전·cluster·backend 요구사항은 저장소에서 추가 확인해야 한다.

```sh
# 로컬 도구 유무 확인용이며 Substrate 설치 명령이 아니다.
go version
kubectl version --client
docker version
```

현재 dossier에는 완전한 quickstart가 없다. CRD YAML, plugin 설치법, 배포·Counter 실행 명령은 원문에서 확인한 뒤 사용한다. 이 노트에 실행 성공을 기록한 것은 아니다.

## 실습 순서

1. 저장소의 README와 Counter Demo 절차를 읽고 commit SHA를 기록한다.
2. 해당 버전이 요구하는 cluster·backend·권한·storage 조건을 확인한다.
3. 공식 절차대로 구성요소와 demo를 배포하고 WorkerPool ready 상태를 확인한다.
4. Counter 요청을 여러 번 보내 응답 값과 Actor 식별 정보를 기록한다.
5. 공식 절차의 suspend 조건을 적용하고 snapshot·Worker 반환을 관찰한다.
6. 같은 Actor를 다시 호출해 값이 이어지는지 확인한다.
7. 다른 Worker에서 resume했는지 별도로 확인한다. 상태 연속성만으로 Teleport 성공을 단정하지 않는다.
8. 생성한 demo 자원만 공식 정리 절차로 제거한다.

## 관찰 기록

| 항목 | 기록할 값 |
|---|---|
| 재현 조건 | commit·backend·node 사양·Worker 수 |
| Actor | Actor·Atespace 식별 정보 |
| 상태 | suspend 전/후 Counter 값 |
| 실행 위치 | 전/후 Worker 식별 정보 |
| 시간 | 최초 요청·resume 요청 latency, 반복 횟수 |
| snapshot | 크기·저장 위치·오류 |

## 완료 기준

- [ ] 같은 Actor의 Counter가 resume 후 이어진다.
- [ ] 유휴 Actor와 Worker 점유의 차이를 설명한다.
- [ ] 상태 복원과 외부 서비스 연결 복원을 구분한다.
- [ ] 오류가 나면 router·WorkerPool·atelet·backend·snapshot storage를 순서대로 추적한다.

## Navigation

- [[tech/infra/agent-substrate-runtime-a5ffcd0a/README|학습 진입점]]

## Sources

- https://github.com/agent-substrate/substrate
- 작성 근거: 사용자 제공 dossier. 원문 checkout 및 실행 검증은 수행하지 않았다.
