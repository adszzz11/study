---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Whisper 기반 온디바이스 음성 인식과 로컬 음성 기록 설계

> **한 줄 정의**: Whisper를 사용자 기기에서 실행해 음성을 텍스트로 변환하는 방식으로, 수집 자료의 Sokki는 Mac 내부 음성 처리와 로컬 SQLite 기록 저장을 명시한다.

## Overview

이 study는 **모델 실행 위치·오디오 전송 범위·기록 저장 위치**를 나누어 살펴본다. Sokki의 개인 받아쓰기와 Damso의 회의 기록을 사례로 삼되, 두 제품의 공통 엔진이나 아키텍처를 가정하지 않는다.

| 사례 | 자료가 설명하는 구성 | 남은 확인 사항 |
|---|---|---|
| Sokki | 온디바이스 Whisper, 오디오 외부 미전송, 로컬 SQLite | 정확도·지연·리소스, 저장 항목과 보호 방식 |
| Damso | 화자 분리, 누적 화자 프로필, 녹음 전 사용자 확인 | 모델·처리 위치·저장 구조 |

화면과 README 설명은 설계 방향을 분석하는 근거다. 성능 측정이나 네트워크 관찰 결과로 취급하지 않는다.

## Learning Path

- [ ] [[tech/ai/whisper-on-device-speech/01-overview|Overview]] — 개념과 근거 수준 이해
- [ ] [[tech/ai/whisper-on-device-speech/02-ecosystem|Ecosystem]] — 받아쓰기와 회의 기록 비교
- [ ] [[tech/ai/whisper-on-device-speech/03-references|References]] — 출처와 미확인 항목 확인
- [ ] [[tech/ai/whisper-on-device-speech/04-learning/01-getting-started|시작하기]] — 짧은 한국어 발화 평가
- [ ] [[tech/ai/whisper-on-device-speech/04-learning/02-deep-dive|심화 학습]] — 데이터 경계·저장·상태 전이 조사
- [ ] [[tech/ai/whisper-on-device-speech/05-projects|Projects]] — 실전 산출물 작성
- [ ] [[tech/ai/whisper-on-device-speech/cheatsheet|Cheatsheet]] — 검증 항목 빠르게 복습

## When To Use

- 개인 노트 작성에서 로컬 받아쓰기의 수정 부담을 평가할 때.
- 음성 처리와 기록 저장의 데이터 경계를 문서화할 때.
- 회의 녹음 승인과 화자 정보 관리 workflow를 설계할 때.

## When Not To Use

- 검증된 한국어 정확도나 지연 수치가 즉시 필요한 제품 선정 근거로 사용할 때.
- 모든 데이터의 외부 미전송, 암호화, 완전 삭제가 입증된 자료가 필요할 때.
- Obsidian·ChatGPT Work 전용 연동 또는 Damso의 Whisper 사용을 전제로 구현할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/whisper-on-device-speech/04-learning/02-deep-dive|로컬 음성 기록의 데이터 경계와 저장 검증]]

필수 MOC 링크는 vault 규약에 따라 표기했다. 현재 작업 폴더에는 기존 vault 파일이 없어 대상 존재 여부는 확인하지 못했다.

## Sources

- 사용자 제공 dossier: Sokki·Damso 화면 및 README 설명을 정리한 수집 자료. 원문 URL과 제품 버전은 제공되지 않았다. 이 노트는 제품을 직접 실행하거나 원문을 독립 검증한 결과가 아니다.
- Whisper 공식 저장소: https://github.com/openai/whisper — 엔진 학습용 보충 자료이며 Sokki·Damso 구현의 증거는 아니다.
- SQLite 공식 문서: https://www.sqlite.org/docs.html — 저장 계층 학습용 보충 자료이며 제품 schema의 증거는 아니다.
