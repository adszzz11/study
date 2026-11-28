---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 음성 인식 입력 방식과 모델 크기 선택

> **한 줄 정의**: 음성 인식의 입력 경로인 마이크·녹음 파일과 출력 시점인 실시간·녹음 후 변환을 구분하고, 사용 목적과 검증 결과에 따라 모델 크기를 선택하는 설계 문제다.

## Overview

Lightning-SimulWhisper는 제공 자료에서 무료·오픈소스 Mac 전용 실시간 받아쓰기 엔진으로 소개된다. 핵심은 녹음이 끝나기를 기다리지 않고 **인식이 확실한 부분부터 먼저 출력한다**는 설명이다. 공개 저장소와 실제 동작은 확인하지 않았다.

- **입력 경로**: 마이크 / 기존 녹음 파일.
- **출력 시점**: 녹음 후 변환 / 음성이 이어지는 동안 부분 출력.
- **모델 크기**: 화면에서 tiny부터 large까지 선택 가능. 크기별 성능 우열은 미검증.

이 세 축은 별개다. 파일 입력이 반드시 녹음 후 처리인 것도, 마이크 입력이 반드시 실시간 출력인 것도 아니다. 자료는 모든 조합을 검증하지 않는다. 최초 출력 지연과 최종 결과 도달 시간도 따로 평가해야 한다.

## Learning Path

- [ ] [[tech/ai/speech-input-model-sizing/01-overview|Overview: 개념과 근거의 범위]]
- [ ] [[tech/ai/speech-input-model-sizing/02-ecosystem|비교: 입력·출력·모델 선택지]]
- [ ] [[tech/ai/speech-input-model-sizing/03-references|References: 자료와 미확인 항목]]
- [ ] [[tech/ai/speech-input-model-sizing/04-learning/01-getting-started|시작하기: 입력별 출력 관찰]]
- [ ] [[tech/ai/speech-input-model-sizing/04-learning/02-deep-dive|심화: 동일 파일로 모델 비교]]
- [ ] [[tech/ai/speech-input-model-sizing/05-projects|프로젝트: 내 사용 조건의 선택 기준]]
- [ ] [[tech/ai/speech-input-model-sizing/cheatsheet|Cheatsheet: 실험 전후 점검]]

## When To Use

- 발화 중 결과를 읽어야 하는 받아쓰기에서 출력 지연과 수정 빈도를 평가할 때.
- 기존 녹음의 전사 초안을 만들고 검수 절차를 설계할 때.
- 내 Mac과 한국어 발화에 맞는 모델을 동일 조건으로 비교할 때.
- 음성 처리 위치가 중요해 로컬 처리 설명과 실제 네트워크 동작을 확인할 때.

## When Not To Use

- 한국어 정확도·최대 파일 길이·메모리 요구량의 검증된 수치가 즉시 필요할 때.
- 수정될 수 있는 부분 출력을 확정 텍스트로 간주해야만 성립하는 작업.
- 완전한 offline 동작, API, 일괄 처리, 외부 연동이 보장되어야 하지만 아직 확인하지 않은 도입 결정.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/speech-input-model-sizing/01-overview|관련 tech 노트: 입력과 출력 정책의 분리]]
- [[tech/ai/speech-input-model-sizing/04-learning/02-deep-dive|관련 tech 노트: 모델 비교 실험 설계]]

## Sources

- 사용자 제공 dossier: Lightning-SimulWhisper 소개 영상의 수집 요약. 원본 영상·저장소·공식 문서 URL은 제공되지 않았다.
- 출처 URL: 미제공. 제품 기능과 성능 주장은 독립적으로 검증되지 않았으며, 아래 실습 절차는 이 자료를 바탕으로 구성한 평가 제안이다.
