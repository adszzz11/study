---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 백그라운드 지속 실행 AI agent의 실행 구조와 활용 비교

> **한 줄 정의**: 사용자가 대화 화면을 계속 지켜보지 않아도 작업을 이어가거나, 백그라운드 서비스에서 요청을 처리하는 AI agent 운영 방식이다.

## Overview

이 노트는 “업무를 맡긴 뒤 실행을 어떻게 이어가고, 역할과 상태를 어떻게 관리하는가”를 학습한다. 제공 자료에서 **Dots**는 사용자 부재 중 작업의 연속성, **OpenClaw**는 백그라운드 서비스와 채팅 요청 처리를 직접 보여주는 사례다. 두 설명은 동일한 실행 구조를 뜻하지 않는다.

- **Interaction**: 요청을 전달하는 접점.
- **Execution**: 요청을 처리하는 실행 방식.
- **Persistence**: 상태를 보존하고 중단 뒤 복원하는 방식. 제품별 구현은 확인되지 않았다.

Background execution은 durable execution과 다르다. “지속 실행”은 무기한 실행·무중단 가동·장애 후 자동 복구를 보장하지 않는다. 자료에는 실행 시간 제한과 세션 종료 영향, 재시도 정책, 가용성 정보가 없다.

## Learning Path

- [ ] [[tech/ai/persistent-background-agents/01-overview|Overview — 정의와 실행 구조]]
- [ ] [[tech/ai/persistent-background-agents/02-ecosystem|Ecosystem — 여섯 도구 비교]]
- [ ] [[tech/ai/persistent-background-agents/03-references|References — 출처와 근거 범위]]
- [ ] [[tech/ai/persistent-background-agents/04-learning/01-getting-started|시작하기 — 사용자 부재 중 실행 관찰]]
- [ ] [[tech/ai/persistent-background-agents/04-learning/02-deep-dive|Deep Dive — 상태·메모리·역할 전달 검증]]
- [ ] [[tech/ai/persistent-background-agents/05-projects|Projects — 적용 프로젝트]]
- [ ] [[tech/ai/persistent-background-agents/cheatsheet|Cheatsheet — 평가 질문과 용어]]

## When To Use

- 사용자가 화면을 떠난 뒤에도 업무를 처리하는 방식을 비교할 때.
- 채팅 요청과 서비스 실행, 역할 분담, 모델·메모리 설정을 별개 축으로 설계할 때.
- 리서치·보고서 생성처럼 결과와 근거를 검토하기 쉬운 업무의 실험을 계획할 때.

## When Not To Use

- 자료만으로 24/7 가용성이나 장애 복구를 보장해야 할 때.
- 제품의 가격·self-hosting·개인정보 보호 수준을 확정해야 할 때.
- 승인과 권한 범위를 확인하지 않은 채 결제·예약·양식 제출을 자동화하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/persistent-background-agents/01-overview|관련 tech 노트: Background execution과 Persistence]]

MOC는 요청에 명시된 경로를 사용했다. 현재 작업 폴더에는 기존 vault 파일이 없어 해당 두 노트의 존재 여부는 확인하지 못했다.

## Sources

- 사용자 제공 dossier: Dots·Muse·Grok Bot·OpenClaw·Hermes·SkillTree 소개 영상의 수집 요약. 원본 영상 제목·게시자·게시일·URL은 제공되지 않았다.
- 출처 URL: **미제공**. 제품명으로 공식 사이트나 특정 제품을 추정하여 연결하지 않았다.
- 아래 내용은 dossier의 관찰 범위와 분석·실습 제안을 구분한 정리이며, 공식 문서 또는 직접 실행으로 검증한 제품 사양이 아니다.
