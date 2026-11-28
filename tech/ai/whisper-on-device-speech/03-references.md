---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 출처와 검증 범위

## 수집 자료

| 자료 | 활용 범위 | 한계 |
|---|---|---|
| 제공 dossier의 Sokki 화면 설명 | 오버레이·한국어 출력 소개 | 원본 영상 URL·시점 미제공 |
| 제공 dossier의 Sokki README 요약 | Whisper 실행·오디오 이동·SQLite 설명 | 원문 URL·버전·직접 검증 없음 |
| 제공 dossier의 Damso 화면·README 요약 | 화자 기능·녹음 전 확인 소개 | 모델·처리 위치·구현 세부 미제공 |

제품 원문 URL이 없어 임의의 저장소나 동명의 제품을 출처로 연결하지 않는다. 공식 보충 문서는 일반 기술 학습에 사용하며 제품 주장과 분리한다.

## 원문 확보 후 확인할 항목

- 저장소 또는 제품 URL, README 버전·commit, 영상 시점.
- Sokki의 모델 구현체·설치 방법·지원 환경·권한 요구사항.
- 원본 오디오 보존 여부, SQLite schema, 암호화·백업·삭제 정책.
- 텍스트·진단 로그의 전송 경로와 외부 서비스 사용 여부.
- Damso의 처리 위치, 사용 모델, 화자 프로필 연결 기준, 감지 신호.

## 인용 원칙

‘README에 명시’, ‘화면에서 소개’, ‘실습으로 관찰’을 구분해 기록한다. 기능 설명을 성능·보안 검증으로 확대하지 않는다.

## Sources

- 사용자 제공 dossier: Sokki·Damso 화면 및 README 설명을 정리한 수집 자료. 원문 URL과 제품 버전은 제공되지 않았다. 이 노트는 제품을 직접 실행하거나 원문을 독립 검증한 결과가 아니다.
- Whisper 공식 저장소: https://github.com/openai/whisper — 엔진 학습용 보충 자료이며 Sokki·Damso 구현의 증거는 아니다.
- SQLite 공식 문서: https://www.sqlite.org/docs.html — 저장 계층 학습용 보충 자료이며 제품 schema의 증거는 아니다.

## Navigation

[[tech/ai/whisper-on-device-speech/README|학습 경로로 돌아가기]]
