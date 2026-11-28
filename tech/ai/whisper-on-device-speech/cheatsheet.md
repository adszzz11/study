---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 로컬 음성 기록 검증

## 핵심 구분

| 개념 | 기억할 점 |
|---|---|
| On-device inference | 모델 실행 위치 |
| Audio egress | 오디오 이동 범위 |
| Local persistence | 기록 저장 위치 |
| Streaming inference | 화면 갱신만으로 확정 불가 |
| Speaker diarization | 한 회의의 화자 구간 구분 |
| 누적 화자 프로필 | 회차 간 화자 정보 연결; 구현 방식 미확인 |

## 사례 요약

- **Sokki:** README상 Mac 내부 Whisper·로컬 SQLite·오디오 외부 미전송. 오버레이에는 파형·경과 시간·한국어 출력.
- **Damso:** 화자 분리·누적 프로필·회의 감지 후 녹음 전 확인. Whisper 사용·처리 위치는 자료에 없음.
- **공통 한계:** 정확도·지연·리소스·네트워크·데이터 보호 검증 결과 없음.

## 빠른 점검

- [ ] 앱·모델·기기·언어·소음 조건 기록
- [ ] 기준 문장과 누락·오인식·띄어쓰기·문장부호 비교
- [ ] 최초 텍스트 표시와 최종 확정의 지연 분리
- [ ] 실행 위치·오디오 전송·텍스트 전송·저장 위치 분리
- [ ] DB schema·오디오 보존·삭제·암호화·백업 확인
- [ ] 화자 구간 평가와 회차 간 프로필 평가 분리
- [ ] 감지·대기·승인·거절·무응답 관찰
- [ ] README 주장과 실제 관찰 결과의 근거 구분

## 기록 틀

```text
조건 / 버전:
자료상 설명:
관찰 결과:
측정 방법과 단위:
미확인 항목:
다음 확인 작업:
```

## Sources

- 사용자 제공 dossier: Sokki·Damso 화면 및 README 설명을 정리한 수집 자료. 원문 URL과 제품 버전은 제공되지 않았다. 이 노트는 제품을 직접 실행하거나 원문을 독립 검증한 결과가 아니다.
- Whisper 공식 저장소: https://github.com/openai/whisper — 엔진 학습용 보충 자료이며 Sokki·Damso 구현의 증거는 아니다.
- SQLite 공식 문서: https://www.sqlite.org/docs.html — 저장 계층 학습용 보충 자료이며 제품 schema의 증거는 아니다.

## Navigation

[[tech/ai/whisper-on-device-speech/README|학습 경로로 돌아가기]]
