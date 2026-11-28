---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# CRM 및 에이전트 성과 대시보드와 통합 운영 구조

> **한 줄 정의**: CRM 및 에이전트 성과 대시보드는 고객 관계 정보와 AI 에이전트의 활동·성과를 함께 파악하기 위한 운영 화면이다.

## Overview

Orbit Agents는 지식 그래프 기반 메모리, 사전 구성 에이전트, CRM, 성과 대시보드, 부서별 조직도를 하나의 시스템으로 소개한다. 핵심 학습 질문은 **고객·활동·에이전트·결과가 어떤 근거로 연결되는가**이다.

- **소개 확인:** CRM 화면(00:48), 에이전트 성과 대시보드(00:53), 지식 그래프, 사전 구성 에이전트, 조직도.
- **제품 구상:** Claude·Codex 등 여러 AI 클라이언트가 하나의 메모리에 연결된다.
- **미확인:** 실제 CRM 연동, 실행 결과, 지표 정의·집계 정확성, 업무 성과 개선. DB·Backend·Frontend·분석 엔진도 자료에 없다.

이 노트의 데이터 모델과 계산식은 제품 사용법이 아닌 **설계 연습용 제안**이다.

## Learning Path

- [ ] [[tech/data/crm-agent-performance-dashboard/README|전체 지도]]에서 범위와 증거 수준 확인
- [ ] [[tech/data/crm-agent-performance-dashboard/01-overview|Overview]]에서 What/Why와 구조 학습
- [ ] [[tech/data/crm-agent-performance-dashboard/02-ecosystem|Ecosystem]]에서 비교의 한계 확인
- [ ] [[tech/data/crm-agent-performance-dashboard/03-references|References]]에서 자료와 미확인 질문 점검
- [ ] [[tech/data/crm-agent-performance-dashboard/04-learning/01-getting-started|시작하기]]에서 가상 데이터 연결
- [ ] [[tech/data/crm-agent-performance-dashboard/04-learning/02-deep-dive|심화 학습]]에서 집계·기여 배분 검산
- [ ] [[tech/data/crm-agent-performance-dashboard/05-projects|Projects]]에서 완료 기준을 갖춘 실습 수행
- [ ] [[tech/data/crm-agent-performance-dashboard/cheatsheet|Cheatsheet]]로 지표와 검토 항목 복습

## When To Use

- 고객 발굴·접촉을 수행하는 에이전트의 실행과 고객 관계 변화를 함께 검토할 때.
- 활동량, 품질, 운영 비용을 분리하고 수치에서 원본 기록까지 추적하는 대시보드를 설계할 때.
- 통합 제품의 화면 소개를 실제 데이터 통합 검증 질문으로 바꿀 때.

## When Not To Use

- Orbit Agents의 설치법, API 사양, 실제 연동 지원 여부가 필요할 때: 이 자료로는 확인할 수 없다.
- 실행 완료 수를 매출 또는 고객 관계 개선의 대리 지표로 곧바로 사용하려 할 때.
- 제품 간 우열이나 성과 개선 효과를 입증하려 할 때: 비교·실험 근거가 부족하다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Data]]
- 관련 tech 학습 주제: CRM 데이터 모델링, Agent Observability, Knowledge Graph. 기존 노트 경로를 확인할 수 없어 링크를 생략한다.
- [[tech/data/crm-agent-performance-dashboard/04-learning/02-deep-dive|지표 정의와 근거 추적]]

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·영상 제목·게시일은 제공되지 않았다. 영상 시점은 dossier의 표기를 따른다.
- Obsidian 공식 도움말: https://help.obsidian.md/ — 비교 대상의 일반 학습용 참고이며 Orbit Agents의 기능이나 연동을 입증하는 출처가 아니다.
