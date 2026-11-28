---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Agent Dashboard 검토 질문

## 빠른 구분

| 화면에서 보이는 것 | 즉시 결론 내릴 수 없는 것 | 확인할 근거 |
|---|---|---|
| 이름 붙은 Node | 실제 Agent 실행 | Run·호출 기록 |
| 중앙 JEV | 중앙 Orchestrator | 지시·응답·라우팅 기록 |
| 37개라는 숫자 | 37개 동시 실행 | 인스턴스 목록·중첩 실행 시각 |
| 노드 이동 | Topology 변경 | 의존 관계·메시지 변화 |
| Progress 100% | 성공 | 산출물 버전·검증 결과 |
| 증가하는 Metric | 생산성·품질 개선 | 정의·단위·분모·측정 구간 |
| Claude 명칭 | 특정 API·모델 구성 | 연동 명세·호출 기록 |

## 최소 검토 순서

```text
관찰인가, 홍보 주장인가, 설계 제안인가?
→ Node의 역할은 정의됐는가?
→ Task ID와 Run ID가 있는가?
→ 실행·전달 기록을 따라갈 수 있는가?
→ 산출물 버전과 검증 결과가 연결되는가?
→ 사람의 개입과 실패도 포함됐는가?
```

## 지표 체크

- [ ] 단위·집계 구간·계산식·데이터 출처·갱신 시각이 있다.
- [ ] 완료와 검증 통과를 별도로 집계한다.
- [ ] Task와 재시도 Run을 구분한다.
- [ ] 분모 0은 N/A, 기록 부재는 미확인으로 표시한다.
- [ ] 합성 데이터와 실제 실행 데이터를 구별한다.

## 안전한 서술 예시

- 관찰: “제공 요약에는 중앙 노드와 주변 Agent가 나타난다.”
- 주장: “자료는 37개 AI Agent 팀의 회사 운영 능력을 홍보한다.”
- 한계: “실행 로그·산출물·검증 결과가 없어 운영 능력은 미확인이다.”
- 제안: “운영 평가를 위해 Node와 Task·Trace·산출물·검증을 연결한다.”

자료에 없는 Frontend, Backend, Agent Framework, 통신 방식, 저장소는 추정하여 채우지 않는다.

## 연결

[[tech/ai/multi-agent-system-visualization/01-overview|확인 범위]] · [[tech/ai/multi-agent-system-visualization/03-references|출처 상태]] · [[tech/ai/multi-agent-system-visualization/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 영상 요약을 재구성한 자료. 원본 영상 URL·게시자·게시일은 미제공이며, 원본을 직접 검증하지 않았다.
- 보충 학습: OpenTelemetry Traces — https://opentelemetry.io/docs/concepts/signals/traces/
- 보충 학습: W3C Trace Context — https://www.w3.org/TR/trace-context/

위 URL은 실행 추적 개념을 학습하는 자료이며, 영상의 JEV 구현이나 홍보 주장을 입증하는 출처가 아니다.
