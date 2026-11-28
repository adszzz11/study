---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 온디바이스 음성 처리와 데이터 보관의 경계

> **한 줄 정의**: 온디바이스 음성 처리는 음성 인식을 사용자 기기 내부에서 수행하는 방식이며, 데이터 보관 여부는 처리 위치와 별도로 확인해야 하는 데이터 수명주기 문제다.

## Overview

Lightning-SimulWhisper는 제공된 영상 요약에서 무료·오픈소스 Mac 전용 실시간 받아쓰기 엔진으로 소개된다. 마이크·녹음 파일을 Mac에서 처리하고, 확실한 부분부터 텍스트를 출력한다고 설명한다. 이 노트는 제품 설치 매뉴얼이 아니라 그 설명을 평가하는 tool-study다.

- **처리 위치:** Mac 내부 처리 및 녹음의 서버 미전송을 설명한다. 실제 통신 관찰 결과는 없다.
- **출력 시점:** 점진적 출력이 소개되지만 지연시간 측정값과 출력 수정 규칙은 없다.
- **보관 수명:** 음성·전사·임시 데이터·로그의 저장 및 삭제 정책은 미확인이다.

“서버로 전송되지 않는다”는 설명만으로 무보관, 자동 삭제, 완전한 오프라인 동작을 보장할 수 없다. 기능 소개와 분석 관점, 직접 관찰 결과를 구분해서 읽는다.

## Learning Path

- [ ] [[tech/ai/on-device-speech-retention/01-overview|Overview]] — What/Why, 기능과 근거의 경계
- [ ] [[tech/ai/on-device-speech-retention/02-ecosystem|Ecosystem]] — 처리 위치·출력 시점·보관 정책 비교
- [ ] [[tech/ai/on-device-speech-retention/03-references|References]] — 출처 상태와 검증할 주장
- [ ] [[tech/ai/on-device-speech-retention/04-learning/01-getting-started|시작하기]] — 샘플·환경·관찰 기록 준비
- [ ] [[tech/ai/on-device-speech-retention/04-learning/02-deep-dive|심화 학습]] — 모델·언어·통신·파일 수명주기 평가
- [ ] [[tech/ai/on-device-speech-retention/05-projects|Projects]] — 평가 기록·보관 현황표·정책 초안
- [ ] [[tech/ai/on-device-speech-retention/cheatsheet|Cheatsheet]] — 주장과 검증 체크리스트

## When To Use

- Mac에서 한국어 받아쓰기의 지연과 품질을 자신의 조건으로 평가할 때
- 로컬 처리와 데이터 보관 정책을 따로 검토할 때
- 업무용 전사의 저장·내보내기·삭제 규칙을 설계할 때

## When Not To Use

- 검증 없이 무보관이나 완전한 오프라인 동작을 보장해야 할 때
- 최대 18배·15배 주장을 근거로 제품 우위나 전체 처리 속도를 확정할 때
- 공식 설치 명령, 지원 macOS 버전, 모델별 메모리 요구량이 필요한 경우: 현재 자료로는 제공할 수 없다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/on-device-speech-retention/01-overview|온디바이스 음성 처리의 기능과 근거]] — 관련 기술 개념
- [[tech/ai/on-device-speech-retention/04-learning/02-deep-dive|음성 데이터 수명주기 검증]] — 보관·삭제 분석

## Sources

- 사용자 제공 dossier 및 그 안에 인용된 영상 요약. 원본 영상 URL, 저장소 URL, 공식 문서 URL은 제공되지 않았다.
- 출처 URL: **미제공**. 제품명만으로 공식 주소를 추정하지 않는다. URL 확보 전에는 기능 소개를 독립적으로 검증한 사실로 취급하지 않는다.
