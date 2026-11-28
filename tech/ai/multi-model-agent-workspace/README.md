---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 여러 모델과 부서별 agent를 통합하는 Workspace

> **한 줄 정의**: 여러 부서의 agent와 Claude·GPT·Gemini 같은 모델을 하나의 작업 공간에 모아 업무를 수행하도록 구성한 AI workspace다.

## Overview

제공 자료에서 이 구성을 가장 직접적으로 보여주는 도구는 **SkillTree**다. 여러 부서의 agent와 Claude·GPT·Gemini가 같은 workspace에 등장한다. 다만 agent별 모델 지정, 자동 routing, agent 간 협업 방식은 확인되지 않는다.

- **역할의 축:** 어떤 부서·업무를 담당하는 agent인가.
- **모델의 축:** 어떤 모델로 작업하는가.
- **평가의 핵심:** 한 화면에서 접근하는 것과 업무 결과가 연결되는 것을 구분한다.

부서별 도구 분산과 반복적인 맥락 입력을 줄일 가능성은 구성에서 도출한 **기대 가치**이며, 검증된 제품 효능은 아니다.

## Learning Path

- [ ] [[tech/ai/multi-model-agent-workspace/README|README: 개요와 학습 경로]]
- [ ] [[tech/ai/multi-model-agent-workspace/01-overview|Overview: What·Why·구조]]
- [ ] [[tech/ai/multi-model-agent-workspace/02-ecosystem|Ecosystem: 비교 축]]
- [ ] [[tech/ai/multi-model-agent-workspace/03-references|References: 근거와 한계]]
- [ ] [[tech/ai/multi-model-agent-workspace/04-learning/01-getting-started|시작하기: 역할과 모델 분리 실험]]
- [ ] [[tech/ai/multi-model-agent-workspace/04-learning/02-deep-dive|Deep Dive: 인계·맥락·실행 제어]]
- [ ] [[tech/ai/multi-model-agent-workspace/05-projects|Projects: 실전 평가]]
- [ ] [[tech/ai/multi-model-agent-workspace/cheatsheet|Cheatsheet: 빠른 점검]]

## When To Use

- 여러 부서의 업무를 역할별로 나누고 결과를 연결하는 방식을 학습할 때.
- 같은 역할에서 모델 선택의 영향을 비교할 때.
- 도입 후보의 통합 수준을 증거에 따라 점검할 때.

## When Not To Use

- 검증된 SkillTree 설치·API 사용법이나 운영 보장을 찾을 때: 해당 자료가 없다.
- 가격, 개인정보 보호, 배포 방식의 확정 비교가 필요할 때.
- 단일 역할·단일 모델만으로 충분하고 인계 비용이 더 클 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/multi-model-agent-workspace/01-overview|역할과 모델을 분리하는 개념 정리]]
- [[tech/ai/multi-model-agent-workspace/02-ecosystem|AI workspace 비교 관점]]

## Sources

- 제공된 dossier: SkillTree 및 함께 소개된 도구의 영상 요약. 원본 URL은 제공되지 않았다.
- 출처 URL: 미제공. 영상 제목·시점의 구체 값도 현재 dossier에 없어 원문 대조가 불가능하다. URL을 추정하거나 새 출처를 추가하지 않았다.
