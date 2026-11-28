---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 회의 감지와 녹음 전 동의 절차

> **한 줄 정의**: 회의 가능성을 감지한 뒤 사용자에게 녹음 여부를 물어, 감지와 실제 녹음 시작 사이에 명시적인 승인 단계를 두는 흐름이다.

## Overview

Damso에는 회의를 감지한 뒤 녹음 전에 사용자에게 묻는 동작이 소개되어 있다. 핵심은 **Meeting detection과 recording authorization의 분리**다. 감지 정확도가 높아도 녹음 권한이 자동으로 생기지는 않는다.

- **확인 범위:** 제공 dossier가 전달하는 README 설명. 감지 기준, 승인 화면, 승인 이후 처리는 확인되지 않았다.
- **설계상 기대:** 도구를 직접 실행하는 부담을 줄이고 오탐이나 원치 않는 기록을 승인 단계에서 걸러낸다. 실제 개선 효과는 검증되지 않았다.
- **동의의 범위:** 사용자의 시작 승인과 모든 참석자의 동의 확보는 별개다. 제목의 동의 절차를 참석자 동의나 법적 요건 충족으로 해석하지 않는다.
- **데이터 경계:** 녹음 전 질문이 승인 전 오디오 접근까지 없다는 뜻은 아니다.

## Learning Path

- [ ] [[tech/ai/meeting-detection-recording-consent/README|개요와 학습경로]]에서 범위와 근거 한계를 확인한다.
- [ ] [[tech/ai/meeting-detection-recording-consent/01-overview|Overview]]에서 What/Why와 제안 상태 모델을 익힌다.
- [ ] [[tech/ai/meeting-detection-recording-consent/02-ecosystem|Ecosystem]]에서 승인과 로컬 처리라는 독립된 평가 축을 비교한다.
- [ ] [[tech/ai/meeting-detection-recording-consent/03-references|References]]에서 출처의 확인 수준을 점검한다.
- [ ] [[tech/ai/meeting-detection-recording-consent/04-learning/01-getting-started|시작하기]]에서 mock event로 승인 gate를 실습한다.
- [ ] [[tech/ai/meeting-detection-recording-consent/04-learning/02-deep-dive|심화 학습]]에서 경합과 데이터 경계를 설계한다.
- [ ] [[tech/ai/meeting-detection-recording-consent/05-projects|Projects]]에서 완료 기준이 있는 prototype을 구상한다.
- [ ] [[tech/ai/meeting-detection-recording-consent/cheatsheet|Cheatsheet]]로 검토 항목을 복습한다.

## When To Use

- 회의 후보를 자동으로 찾되 녹음 시작은 사용자 결정으로 남기려 할 때.
- 승인 없는 시작, 중복 감지, 오래된 승인 같은 상태 관리 문제를 학습할 때.
- 감지 입력과 원본 오디오·transcript·speaker profile의 정책을 따로 검토할 때.

## When Not To Use

- 검증된 Damso 설치법·API·감지 정확도·지원 앱 목록이 필요할 때: 제공 자료로 확인할 수 없다.
- 사용자 승인만으로 참석자 동의나 법적 요건까지 충족했다고 판단하려 할 때.
- Damso의 로컬 처리·저장을 보장하는 근거가 필요할 때: Sokki의 속성을 전이할 수 없다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/meeting-detection-recording-consent/01-overview|회의 감지와 녹음 권한 분리 — 관련 tech 개요]]

현재 작업 공간에 기존 vault 노트가 없어 외부 관련 tech 노트는 확인하지 못했다. 위 tech 링크는 이 폴더에 생성되는 개요 노트다. MOC 링크는 요청된 경로이며, 대상 파일의 존재는 현재 작업 공간에서 확인할 수 없다.

## Sources

- 사용자 제공 dossier: Damso README 및 영상 요약에 관한 수집 설명, Sokki README에 관한 수집 설명.
- **출처 URL: 제공되지 않음.** 원문 README와 영상 URL을 확인할 수 없어 링크를 기재하지 않았다. 이 노트는 원문을 직접 검증한 결과가 아니다.
- 상태 모델·실습·프로젝트는 dossier에 근거한 **설계 제안**이며, Damso의 실제 구현이나 검증된 성능을 뜻하지 않는다.
