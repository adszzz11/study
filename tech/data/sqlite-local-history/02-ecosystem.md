---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: Sokki와 Damso의 역할 비교

## 비교 범위

수집 자료에는 경쟁 database나 대체 저장 방식의 구현 사례가 없다. 따라서 성능·비용 우열 대신 함께 소개된 제품의 역할과 확인 범위를 비교한다. 직접적인 경쟁 관계인지도 판단하지 않는다.

| 항목 | Sokki | Damso |
|---|---|---|
| 목적 | 음성의 텍스트 입력·받아쓰기 | 회의 기록 |
| 화면·기능 | 파형, 경과 시간, 한국어 텍스트 | 화자 분리, 누적 화자 프로필 |
| 기기 내 처리 | 음성 인식·Whisper 실행 명시 | 자료에 명시 없음 |
| SQLite | 기록의 로컬 저장 명시 | 자료에 명시 없음 |
| 오디오 외부 전송 | Mac 밖으로 나가지 않는다고 명시 | 자료에 명시 없음 |
| 녹음 전 사용자 확인 | 자료에 명시 없음 | 회의 감지 후 녹음 전에 질문 |

## 기록 설계에 주는 시사점

Sokki는 받아쓰기 결과, Damso는 회의와 화자 구분을 중심으로 소개된다. 전자는 한 번의 입력 세션을, 후자는 회의·발화 구간·화자 프로필을 구분하는 모델을 생각해 볼 계기가 된다. 이는 설계 제안이며 실제 schema에 관한 주장이 아니다.

“명시 없음”은 기능이 없다는 뜻이 아니다. Damso가 SQLite를 사용하거나 Sokki와 저장 구조를 공유한다고 추정하지 않는다.

## 다음 학습

[[tech/data/sqlite-local-history/05-projects|기록 단위별 프로젝트]] · [[tech/data/sqlite-local-history/README|학습 경로]]

## Sources

- 제공 dossier의 제품 비교. 원자료 URL 미제공으로 제품 공식 출처 URL은 기재할 수 없다.
- SQLite 배경 문서(제품 비교 근거 아님): https://www.sqlite.org/about.html
