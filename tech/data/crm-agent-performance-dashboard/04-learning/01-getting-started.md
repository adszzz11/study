---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 고객과 실행을 분리해 연결하기

## 목표와 준비

제품 설치가 아닌 가상 데이터 설계 연습이다. Spreadsheet 또는 로컬 SQL 도구로 시작할 수 있다. 실제 고객 정보 대신 합성 데이터를 사용한다.

## 1. 엔터티 정의

| 엔터티 | 기본 키 | 주요 필드·관계 |
|---|---|---|
| Lead | lead_id | 현재 상태, 생성 시점 |
| Agent | agent_id | 역할, 소속 |
| Run | run_id | agent_id, 시작·종료 시점, 실행 상태 |
| Activity | activity_id | lead_id, run_id, 종류, 발생 시점, 외부 이벤트 ID |
| Outcome | outcome_id | lead_id, 결과 종류, 발생 시점, 근거 activity_id |

Lead의 현재 상태와 Activity의 사건 기록을 분리한다. 한 실행이 여러 고객을 다룰 수 있고 한 고객에게 여러 실행이 관여할 수 있다.

## 2. 가상 흐름 만들기

```text
Agent A: Lead Finder / Run R1
  Activity E1: L1 발견
Agent B: Email Outreach Agent / Run R2
  Activity E2: L1용 메시지 생성
  Activity E3: L1에 실제 발송
  Activity E4: L1 응답 수신, E3와 연결
Outcome O1: L1 유효 응답 판정, 근거 E4
```

메시지 생성만으로 접촉 수를 늘리지 않는다. 재시도는 실행 이력에 남기되 같은 발송 이벤트의 재수집은 외부 이벤트 ID로 제거한다.

## 3. 지표 계약 작성

- 관측 기간: UTC 기준 반개구간 `[시작, 종료)`.
- 접촉 고객 수: 기간 내 실제 발송된 고유 lead_id 수.
- 응답률: 해당 접촉 고객 중 발송 후 7일 이내 응답한 고유 고객 수 / 접촉 고객 수.
- 관측 종료: 마지막 접촉 후 7일까지 기다려 확정한다. 아직 창이 닫히지 않은 값은 잠정치로 표시한다.
- 분모가 0이면 `N/A`로 표시한다.

이는 학습용 계약이다. 실제 운영에서는 도달 여부, 채널, 유효 응답 기준도 합의해야 한다.

## 4. 손으로 검산

L1에 두 번 발송하고 L2에 한 번 발송하되 L1만 응답했다고 가정한다. 메시지 생성 수가 4라면 생성 4건, 발송 3건, 접촉 고객 2명, 응답 고객 1명, 응답률 50%다. 생성·발송·고객 수를 혼용하면 다른 값이 나온다.

## 완료 확인

- [ ] 모든 Activity에서 Lead와 Run, Agent를 찾을 수 있다.
- [ ] 실패·재시도와 고객 중복을 구분했다.
- [ ] 50%의 분모·기간·응답 기준을 설명할 수 있다.

## Related Notes

- [[tech/data/crm-agent-performance-dashboard/README|학습 지도]]
- [[tech/data/crm-agent-performance-dashboard/04-learning/02-deep-dive|설계 실습]]

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·영상 제목·게시일은 제공되지 않았다. 영상 시점은 dossier의 표기를 따른다.
- Obsidian 공식 도움말: https://help.obsidian.md/ — 비교 대상의 일반 학습용 참고이며 Orbit Agents의 기능이나 연동을 입증하는 출처가 아니다.
