---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — 회의 감지와 녹음 전 승인

## 기술스택 요약

- Damso: 회의 감지 후 녹음 전 사용자 질문, Speaker diarization, 누적 화자 프로필이 소개됨.
- Damso의 감지 알고리즘·모델·저장소·처리 위치는 제공 자료로 확인 불가.
- Sokki: 기기 내 음성 인식·Whisper, 로컬 SQLite, 오디오 외부 미전송이 README 설명으로 제시됨.
- 구현 검토의 핵심은 detection과 recording authorization의 분리이며, 참석자 동의는 별도 요구사항임.

## 빠른 구분

| 표현 | 판단 |
|---|---|
| 회의를 감지했다 | 후보 생성; 시작 권한 아님 |
| 질문을 표시했다 | 승인 완료 아님 |
| 사용자가 승인했다 | 해당 세션·범위·유효성 확인 필요 |
| 모든 참석자가 동의했다 | 별도 절차·근거 필요 |
| 녹음 전에 묻는다 | 승인 전 오디오 접근 부재를 보장하지 않음 |
| Sokki가 로컬 처리한다 | Damso의 로컬 처리를 뜻하지 않음 |
| 거부율이 높다 | 오탐률이 높다고 단정 불가 |

## 검토 체크리스트

- [ ] 감지 이벤트만으로 recorder가 시작하지 않는다.
- [ ] 명시적 승인만 Recording으로 전이한다 — 제안 모델의 조건이다.
- [ ] 거부·무응답은 미시작으로 처리하고 재질문 정책을 정한다.
- [ ] session/request ID로 승인 대상을 묶는다.
- [ ] 종료·만료된 요청의 승인과 중복 시작을 차단한다.
- [ ] 감지 입력·오디오·transcript·프로필 정책을 나눈다.
- [ ] 사용자 승인과 참석자 고지·동의·철회를 분리한다.
- [ ] 미확인 제품 동작을 구현 사실처럼 기술하지 않는다.

```text
자료로 확인된 설명: 감지 → 사용자 질문 → 이후 처리 미확인
학습용 권장 조건: 유효한 명시적 승인 없이는 녹음 시작 금지
```

## 연결

[[tech/ai/meeting-detection-recording-consent/README|전체 학습경로]] · [[tech/ai/meeting-detection-recording-consent/03-references|출처 한계]] · [[tech/ai/meeting-detection-recording-consent/04-learning/02-deep-dive|심화 검토]]

## Sources

- 사용자 제공 dossier: Damso README 및 영상 요약에 관한 수집 설명, Sokki README에 관한 수집 설명.
- **출처 URL: 제공되지 않음.** 원문 README와 영상 URL을 확인할 수 없어 링크를 기재하지 않았다. 이 노트는 원문을 직접 검증한 결과가 아니다.
- 상태 모델·실습·프로젝트는 dossier에 근거한 **설계 제안**이며, Damso의 실제 구현이나 검증된 성능을 뜻하지 않는다.
