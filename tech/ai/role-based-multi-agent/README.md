---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 역할 기반 multi-agent 협업의 구조와 적용 조건

> **한 줄 정의**: 역할 기반 multi-agent 협업은 연구·작성·검토·운영 등 서로 다른 책임을 가진 agent들이 하나의 목표를 나누어 수행하도록 구성하는 작업 방식이다.

## Overview

역할을 나누는 목적은 하나의 요청에 섞인 판단 기준을 명확히 하는 것이다. Researcher는 근거, Writer는 전달력, Reviewer는 오류와 누락을 담당한다. 역할 이름뿐 아니라 입력·산출물·완료 조건을 정의해야 한다.

- **업무 기능별:** Grok Bot의 리서치·영업·마케팅·운영 역할.
- **작업 단계별:** Hermes의 연구자·작성자·검토자 역할.
- **조직·모델별:** SkillTree의 여러 부서 agent와 Claude·GPT·Gemini 작업 공간.

위 내용은 제공 자료에 나타난 구성이다. agent 간 메시지, 자동 위임, 공유 상태, 결과 통합은 확인되지 않았다. 아래 실습은 이 구성에서 도출한 설계 제안이며 제품 기능 설명이 아니다.

## Learning Path

- [ ] [[tech/ai/role-based-multi-agent/01-overview|Overview]] — 정의, 역할의 축, 확인 범위 이해
- [ ] [[tech/ai/role-based-multi-agent/02-ecosystem|Ecosystem]] — 역할 분리와 지속 실행의 비교 축 구분
- [ ] [[tech/ai/role-based-multi-agent/03-references|References]] — 근거의 출처와 확인 한계 점검
- [ ] [[tech/ai/role-based-multi-agent/04-learning/01-getting-started|시작하기]] — 사람이 handoff하는 순차 workflow 실습
- [ ] [[tech/ai/role-based-multi-agent/04-learning/02-deep-dive|심화 학습]] — handoff 계약과 비교 실험 설계
- [ ] [[tech/ai/role-based-multi-agent/05-projects|Projects]] — 작은 dossier부터 적용
- [ ] [[tech/ai/role-based-multi-agent/cheatsheet|Cheatsheet]] — 실행 전후 점검표 활용

## When To Use

- 하나의 결과물에 근거 수집·작성·검토처럼 서로 다른 책임이 필요할 때.
- 단계별 산출물과 평가 기준을 명시하고 추적할 수 있을 때.
- 부서별 해석을 모으고 최종 결정 주체를 지정할 수 있을 때.
- 추가 전달·검토 비용을 감수하면서 single-agent 대비 효과를 측정하려 할 때.

## When Not To Use

- 짧고 단순하여 단일 agent로 충분한 작업.
- 입력·출력·완료 조건을 정의하지 못한 상태에서 agent 수만 늘리려는 경우.
- 자동 협업, shared memory, 무인 실행을 자료 확인 없이 전제하는 경우.
- 비용·개인정보 보호·실행 권한이 중요하지만 제품별 조건을 아직 확인하지 못한 경우.

## Related Notes

- [[MOCs/Index]] — 요청된 vault 진입점. 현재 작업 폴더에는 대상 파일이 없어 연결 여부 확인이 필요하다.
- [[MOCs/AI]] — 요청된 AI MOC. 현재 작업 폴더에는 대상 파일이 없어 연결 여부 확인이 필요하다.
- [[tech/ai/role-based-multi-agent/01-overview|역할·모델·메모리 개념]] — 이 폴더에 생성한 관련 tech 노트.

## Sources

- 사용자 제공 dossier 및 그 안의 영상 요약. 원본 제목·제작자·출처 URL은 제공되지 않았다.
- 출처 URL: 미제공. 외부 검색이나 URL 열기는 수행하지 않았으며, 동명 제품의 사이트를 근거로 대체하지 않았다.
