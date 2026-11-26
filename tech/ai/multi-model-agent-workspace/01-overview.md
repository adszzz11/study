---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What · Why · 특징

## What

SkillTree는 여러 부서의 agent와 Claude·GPT·Gemini를 한 workspace에 모으는 구성으로 소개된다. **Agent role과 model selection은 별개의 축**이다. Agent가 역할별 prompt 대화창인지, 도구 실행 단위인지, 장기 작업 주체인지는 미확인이다.

## Why

아래는 관찰에서 도출한 분석이며 제품의 실증된 효능이 아니다.

| 문제 | 기대 가치 | 성립 조건 |
|---|---|---|
| 부서별 도구·화면 분산 | 공통 환경에서 업무 탐색·실행 | 공통 탐색·작업 관리 |
| 모델별 사용 환경 차이 | 선택·사용 과정의 일관성 | 모델 차이를 처리하는 UI |
| 역할 사이 전달 비용 | 역할 분담과 결과 연결 | 명시적 handoff와 산출물 구조 |
| 맥락 반복 입력 | 필요한 agent에 맥락 전달 | Context 관리와 접근 범위 |

## 특징과 확인 범위

**관찰:** 여러 부서의 agent, Claude·GPT·Gemini, 하나의 작업 공간 구성.

**미확인:** 모델 routing, 자동 업무 분배, agent 통신, 공유 memory, 외부 연동, 자율 실행 수준.

Hermes의 연구자·작성자·검토자 및 모델·메모리 설정 화면을 SkillTree 기능의 근거로 사용하면 안 된다.

## 개념적 계층

다음은 평가를 위한 논리적 구조이며 SkillTree 내부 아키텍처가 아니다.

| 계층 | 역할 | SkillTree 근거 |
|---|---|---|
| Workspace | 공통 접근 환경 | 통합 구성 관찰 |
| Agent | 부서·업무 역할 | 여러 부서 agent 관찰 |
| Model | 이해·생성 수행 | 세 모델 계열 등장 |
| Orchestration | 분해·선택·순서·인계 | 미확인 |
| Context·Memory | 입력·이력·지속 정보 | 미확인 |
| Governance·Observability | 권한·비용·기록·승인 | 미확인 |

통합 인터페이스만으로 자동 협업이나 공동 목표 실행을 보장하지 않는다. 모델을 누가 고르는지, 결과가 어떤 형식으로 전달되는지, 자료 경계와 중단·재시도·승인 지점이 어디인지 확인해야 한다.

[[tech/ai/multi-model-agent-workspace/README|학습 경로로 돌아가기]]

## Sources

- 제공된 dossier: SkillTree 및 함께 소개된 도구의 영상 요약. 원본 URL은 제공되지 않았다.
- 출처 URL: 미제공. 영상 제목·시점의 구체 값도 현재 dossier에 없어 원문 대조가 불가능하다. URL을 추정하거나 새 출처를 추가하지 않았다.
