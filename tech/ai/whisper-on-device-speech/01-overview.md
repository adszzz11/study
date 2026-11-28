---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

Whisper 기반 온디바이스 음성 인식은 사용자 기기에서 음성을 텍스트로 변환하는 접근이다. 수집 자료는 Sokki가 Mac에서 Whisper를 실행하고 기록을 로컬 SQLite에 저장한다고 설명한다. 특정 Whisper 구현체·모델 크기·하드웨어 요구사항은 제시하지 않는다.

## Why

음성 입력을 작업 흐름에 넣을 때는 인식 결과뿐 아니라 데이터가 어디에서 처리되고 남는지 알아야 한다. 영상에는 Obsidian과 ChatGPT Work가 등장하지만, 전용 플러그인·API·자동 삽입 방식까지 확인된 것은 아니다.

Damso의 회의 기록은 전사 이후의 문제를 보여준다. 한 회의 안의 화자 구분과 여러 회의에 걸친 화자 프로필 관리는 별개이며, 회의 감지 후 녹음 전 확인은 수집 시작을 사용자 결정에 연결한다.

## 특징과 아키텍처

```text
Sokki / Mac 내부 (README 설명)
음성 → Whisper → 인식 텍스트
                 ├─ 오버레이: 파형·경과 시간·한국어 텍스트
                 └─ 기록: 로컬 SQLite
오디오: Mac 밖으로 나가지 않는다고 명시
텍스트의 전체 이동 경로·로그·백업·동기화: 미확인
```

위 그림은 개념 정리이며 실제 내부 호출 순서나 schema를 뜻하지 않는다.

| 속성 | 구분해야 하는 이유 |
|---|---|
| 온디바이스 실행 | 모델 실행 위치에 관한 설명 |
| 오디오 외부 미전송 | 특정 데이터의 이동 범위에 관한 설명 |
| 로컬 저장 | 영속화 위치에 관한 설명; 암호화나 삭제 정책과는 별개 |
| 오버레이 출력 | 상태와 결과를 보여줌; streaming inference의 구현 증거는 아님 |

## 근거 수준

- **화면 소개:** Sokki의 파형·경과 시간·한국어 출력, Damso의 화자 분리·누적 프로필.
- **README 설명:** Sokki의 로컬 실행·SQLite·오디오 미전송, Damso의 녹음 전 확인.
- **검증 결과 없음:** 정확도, 지연, 리소스, 네트워크 관찰, 저장 데이터 보호 방식.

## Sources

- 사용자 제공 dossier: Sokki·Damso 화면 및 README 설명을 정리한 수집 자료. 원문 URL과 제품 버전은 제공되지 않았다. 이 노트는 제품을 직접 실행하거나 원문을 독립 검증한 결과가 아니다.
- Whisper 공식 저장소: https://github.com/openai/whisper — 엔진 학습용 보충 자료이며 Sokki·Damso 구현의 증거는 아니다.
- SQLite 공식 문서: https://www.sqlite.org/docs.html — 저장 계층 학습용 보충 자료이며 제품 schema의 증거는 아니다.

## Navigation

[[tech/ai/whisper-on-device-speech/README|학습 경로로 돌아가기]]
