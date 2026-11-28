---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — mock 승인 gate

## 목표와 준비

실제 음성을 수집하기 전에 detection과 authorization을 분리한다. 가상 이벤트, 승인 입력, 호출 횟수만 세는 mock recorder를 사용한다. 제품 설치법이나 Damso API 실습이 아니다.

## 최소 실습

1. `meeting_detected(session_id)`로 후보를 만들고 질문 대기 상태로 전환한다.
2. 같은 session의 명시적 승인만 recorder에 전달한다.
3. 거부·무응답에서는 시작하지 않는다.
4. 회의 종료로 미결 요청을 무효화한다.
5. 반복 감지와 중복 승인을 보내도 같은 session이 한 번만 시작하는지 확인한다.

```python
# 학습용 의사코드: 단일 실행 흐름만 표현한다.
active, pending, started = set(), set(), set()
record_calls = []

def detected(sid):
    active.add(sid)
    if sid not in started:
        pending.add(sid)  # 실제 UI에서는 같은 요청을 중복 표시하지 않는다.

def decide(sid, answer):
    if sid not in pending or sid not in active:
        return
    pending.remove(sid)
    if answer == "approve" and sid not in started:
        started.add(sid)
        record_calls.append(sid)  # 오디오 접근 없는 mock

def ended(sid):
    active.discard(sid)
    pending.discard(sid)
```

거부·timeout에는 `decide(sid, "reject")`, `decide(sid, "timeout")`을 사용한다. 이 최소 예제는 거부 후 재감지를 다시 허용한다. 실제 정책에서는 cooldown이나 세션 종료까지 억제할지 별도로 정한다. 이미 시작한 녹음의 중지·실패 복구·멀티스레드 경합은 이 예제의 범위 밖이다.

## 검증 시나리오

| 입력 | 기대 결과 |
|---|---|
| 감지만 발생 | recorder 호출 0회 |
| 감지 → 승인 | 해당 session 1회 |
| 감지 → 거부 또는 timeout | 0회 |
| 감지 → 회의 종료 → 늦은 승인 | 0회 |
| 반복 감지 → 승인 → 중복 승인 | 총 1회 |
| A 감지 → B 승인 | A·B 모두 시작 안 함 |

각 행은 초기화된 상태에서 실행한다. 핵심은 질문 표시 여부보다 **승인 없이 시작되는 경로가 있는지**다.

## 다음 단계

[[tech/ai/meeting-detection-recording-consent/04-learning/02-deep-dive|비동기 경합과 데이터 정책]] · [[tech/ai/meeting-detection-recording-consent/05-projects|프로젝트]] · [[tech/ai/meeting-detection-recording-consent/README|진입점]]

## Sources

- 사용자 제공 dossier: Damso README 및 영상 요약에 관한 수집 설명, Sokki README에 관한 수집 설명.
- **출처 URL: 제공되지 않음.** 원문 README와 영상 URL을 확인할 수 없어 링크를 기재하지 않았다. 이 노트는 원문을 직접 검증한 결과가 아니다.
- 상태 모델·실습·프로젝트는 dossier에 근거한 **설계 제안**이며, Damso의 실제 구현이나 검증된 성능을 뜻하지 않는다.
