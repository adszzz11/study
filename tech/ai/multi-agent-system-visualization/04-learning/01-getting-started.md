---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 3개 Agent와 하나의 Task

## 목표와 준비

영상 구현을 재현하는 실습이 아니다. 먼저 Markdown 표와 JSON만으로 화면 상태를 설명하는 최소 근거를 만든다. JEV 설치나 Claude API 연결은 필요하지 않다. 아래 데이터는 모두 **합성 예시**이며 실제 실행 실적으로 집계하지 않는다.

## 1. Node와 Agent 구분

제한 업무를 “제공 문서 한 개의 요약 작성”으로 정한다.

| Agent | 역할 | 입력 | 출력 | 완료 조건 |
|---|---|---|---|---|
| researcher | 근거 추출 | 문서 버전 S1 | 근거 목록 E1 | 문장별 원문 위치 기록 |
| writer | 요약 작성 | E1 | 초안 D1 | 요구한 요약 항목 제출 |
| reviewer | 검증 | S1, E1, D1 | 검증 보고 V1 | 근거·누락 항목별 판정 기록 |

표는 역할 정의일 뿐 실행 증거는 아니다. 각 단계의 시작·종료와 전달한 산출물 ID를 따로 기록한다.

## 2. Task와 실행 기록 만들기

```json
{
  "data_kind": "synthetic",
  "task_id": "T-001",
  "run_id": "R-001",
  "agent_id": "writer",
  "input_artifact_id": "E1",
  "output_artifact_id": "D1",
  "execution_status": "completed",
  "progress_percent": 100,
  "validation_status": "failed",
  "validation_report_id": "V1",
  "failure_reason": "필수 항목의 원문 근거 누락"
}
```

여기서 100%는 초안 작성 단계 종료를 뜻한다. 요구사항 검증은 실패했다. 완료와 성공을 같은 색·값으로 표시하지 않는다.

## 3. 화면에 연결하기

1. Node 선택 시 Agent 역할과 T-001을 표시한다.
2. T-001에서 R-001의 시작·종료·전달 이벤트를 연다.
3. D1과 V1을 연결하고 검증 실패 이유를 보여준다.
4. 아직 기록하지 않은 시각·호출은 “미확인”으로 남긴다.

## 완료 확인

- [ ] 각 Agent의 역할·입력·출력·완료 조건이 있다.
- [ ] Task에서 실행 기록과 산출물 버전을 찾을 수 있다.
- [ ] 진행률 100%와 검증 실패를 동시에 표현한다.
- [ ] 합성 데이터라는 표시가 모든 화면에 유지된다.

## 다음 단계

[[tech/ai/multi-agent-system-visualization/04-learning/02-deep-dive|심화 실습]] · [[tech/ai/multi-agent-system-visualization/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 영상 요약을 재구성한 자료. 원본 영상 URL·게시자·게시일은 미제공이며, 원본을 직접 검증하지 않았다.
- 보충 학습: OpenTelemetry Traces — https://opentelemetry.io/docs/concepts/signals/traces/
- 보충 학습: W3C Trace Context — https://www.w3.org/TR/trace-context/

위 URL은 실행 추적 개념을 학습하는 자료이며, 영상의 JEV 구현이나 홍보 주장을 입증하는 출처가 아니다.
