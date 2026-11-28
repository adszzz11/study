---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 화면 상태를 작업 근거로 설명하기

## Layout과 Topology

Layout은 좌표·간격·배치다. Topology는 실제 작업 전달·의존 관계다. 중앙 노드가 존재한다고 중앙 제어가 확인되는 것은 아니다.

1. 동일한 T-001 실행 기록을 원형 배치와 격자 배치에 표시한다.
2. 좌표만 바꾸고 Task 의존 관계와 이벤트는 고정한다.
3. 별도 합성 실행 R-002에서는 writer가 researcher 결과를 기다리도록 의존 관계를 바꾼다.
4. 두 경우의 차이를 이벤트와 의존 관계 표로 설명한다. 화살표에도 “의존”, “메시지”, “시각적 연결” 중 의미를 붙인다.

## Progress와 Success

| 실행 상태 | 검증 상태 | 해석 |
|---|---|---|
| running | pending | 작업 중, 결과 미판정 |
| completed | failed | 단계 종료, 요구사항 불충족 |
| completed | passed | 지정 버전·기준에 대한 검증 통과 |
| unknown | unknown | 기록 없음, 성공·실패 판정 불가 |

검증 통과도 해당 산출물 버전과 평가 범위에 한정된다. 회사 전체 운영 능력이나 이후 버전의 품질로 확대하지 않는다.

## Metric 정의 연습

아래는 영상 수치의 해석이 아니라 설계 예시다.

| Metric | 정의 | 단위·구간 | 주의점 |
|---|---|---|---|
| 완료 Task 수 | 종료 상태인 고유 Task ID 개수 | 건, 최근 1시간 | 성공률과 다름 |
| 검증 통과율 | 통과 Task / 검증 완료 Task | %, 동일 시간·범위 | 검증 대기 수 별도 표시 |
| 처리 시간 | Task 종료 시각 − 시작 시각 | 초, Task별 | 대기·재시도 포함 정책 명시 |

분모가 0이면 통과율은 N/A로 표시한다. 재시도 Run 수를 고유 Task 수와 섞지 않는다. 어떤 숫자든 단위·집계 구간·계산식·데이터 출처·갱신 시각을 기록한다.

## Trace 연결과 한계

```text
Task T-001
  Run R-001
    researcher → artifact E1
    writer(E1) → artifact D1
    reviewer(S1, E1, D1) → report V1: failed
```

이벤트에는 event ID, Task/Run ID, Agent ID, 시각, 상태, 입력·출력 참조를 붙인다. 필요하면 parent span ID나 메시지 ID로 호출·전달을 연결한다. Trace는 실행 관계를 추적하는 도구이며, 기록 누락·중복·시계 오차가 있으면 해석이 흔들린다. 로그 부재를 “작업 없음”으로 단정하지 않는다.

## 검증 질문

- 완료 Task 하나를 골라 입력부터 검증 보고까지 따라갈 수 있는가?
- 실패·재시도·사람의 승인이 최종 화면에 남는가?
- 검증 결과가 이전 버전의 산출물에 붙어 있지는 않은가?
- Layout만 바꿨을 때 성과 Metric이 그대로 유지되는가?

## 연결

[[tech/ai/multi-agent-system-visualization/05-projects|실전 프로젝트]] · [[tech/ai/multi-agent-system-visualization/cheatsheet|검토 질문]] · [[tech/ai/multi-agent-system-visualization/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 영상 요약을 재구성한 자료. 원본 영상 URL·게시자·게시일은 미제공이며, 원본을 직접 검증하지 않았다.
- 보충 학습: OpenTelemetry Traces — https://opentelemetry.io/docs/concepts/signals/traces/
- 보충 학습: W3C Trace Context — https://www.w3.org/TR/trace-context/

위 URL은 실행 추적 개념을 학습하는 자료이며, 영상의 JEV 구현이나 홍보 주장을 입증하는 출처가 아니다.
