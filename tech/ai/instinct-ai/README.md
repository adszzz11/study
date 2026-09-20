---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Instinct AI

> **한 줄 정의**: Instinct는 text/call로 받은 요청과 연결된 개인 문맥을 사용해 실제 생활 task를 계획하고 수행하려는 autonomous personal assistant다.

## Overview

Instinct는 대화의 답을 만드는 chatbot보다, email·messaging·screen·audio·location·연결 앱을 바탕으로 일을 **끝내는 것**에 초점을 둔 consumer-facing agent다. 별도 dashboard를 학습하는 대신 평소처럼 문자 또는 전화로 요청하는 UX를 전면에 둔다.

- 가능한 task 예: 놓친 thread follow-up, 공항 이동 수단 예약, handyman 예약
- 핵심 가치: personal context + connected-service action
- 확인된 범위: Google Workspace 연결, Mac OS/mobile app, training opt-out과 Vault의 별도 데이터 경계
- 공개되지 않은 범위: underlying model, orchestration runtime, MCP/API 및 전체 connector catalog

## Learning Path

- [ ] [[tech/ai/instinct-ai/01-overview|Overview]] — 문제와 action-oriented agent 구조 이해
- [ ] [[tech/ai/instinct-ai/02-ecosystem|Ecosystem]] — 유사 agent와 interaction model 비교
- [ ] [[tech/ai/instinct-ai/04-learning/01-getting-started|Getting started]] — 최소 권한으로 저위험 task 검증
- [ ] [[tech/ai/instinct-ai/04-learning/02-deep-dive|Deep dive]] — data lifecycle·approval·failure testing 설계
- [ ] [[tech/ai/instinct-ai/05-projects|Projects]] — personal ops와 safety evaluation 적용
- [ ] [[tech/ai/instinct-ai/cheatsheet|Cheatsheet]] — 실행 전 확인 문구와 점검표

## When To Use

- 개인 email/calendar 기반의 반복적인 생활 행정을 위임할 때
- 조사 → 비교 → 초안처럼, 결과를 사람이 검토한 뒤 실행할 수 있는 workflow일 때
- text/call 중심 interaction이 새 앱 UI보다 자연스러운 경우

## When Not To Use

- 법률·의료·재무 판단처럼 전문적 판단을 대신 맡겨야 하는 경우
- 결제, 계약, 외부 발송처럼 human approval 없이 비가역 action을 실행하려는 경우
- 데이터 삭제·training 정책·연결 계정 권한을 검토할 수 없는 환경

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/agent-garden]]
- [[tech/ai/omniroute]]

## Sources

- https://instinct.com/
- https://instinct.com/privacy-policy
- https://instinct.com/terms
- https://developers.google.com/terms/api-services-user-data-policy

