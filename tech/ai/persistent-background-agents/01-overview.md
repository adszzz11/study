---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

> 화면을 지켜보지 않아도 되는 작업과, 중단 뒤 복구되는 작업을 구분한다.

## What

지속 실행 AI agent는 단순히 응답을 생성하는 것을 넘어 사용자의 부재 중 업무를 이어가거나 서비스로 요청을 처리하는 운영 방식이다. 이 자료에서 Dots와 OpenClaw가 가장 직접적인 사례지만, 전자는 **작업 연속성**, 후자는 **서비스 대기·실행과 요청 접점**을 설명한다.

## Why

긴 업무를 매번 대화 화면에서 감독하면 사용자의 주의가 실행에 묶인다. 업무를 위임하려면 결과뿐 아니라 진행 상태, 실패, 권한 범위를 확인할 수 있어야 한다. 이들은 평가 기준이며, 소개 도구가 모두 지원한다는 뜻은 아니다.

## 핵심 특징과 경계

| 축 | 의미 | dossier에서 확인되는 범위 |
|---|---|---|
| Interaction | 사용자 요청 접점 | Dots의 ChatGPT 내부 사용, OpenClaw의 채팅 요청 |
| Execution | 요청 이후 처리 방식 | 사용자 부재 중 작업 지속, 백그라운드 서비스 |
| Persistence | 상태 저장·복원 | 구체적인 저장·복원 구조 확인 불가 |

**Background execution ≠ durable execution.** 프로세스가 뒤에서 실행되는 것만으로 checkpoint, 재시작 후 복구, 중복 실행 방지를 추론할 수 없다.

### 역할 기반 구성

- Grok Bot: 리서치·영업·마케팅·운영 역할.
- Hermes: 연구자·작성자·검토자 역할.
- SkillTree: 여러 부서의 agent를 모은 작업 공간.

역할이 여러 개 보인다는 사실만으로 자동 위임·병렬 실행·결과 합의·실패 복구를 입증할 수 없다. 실제 전달 규칙과 orchestration은 미확인이다.

### 모델·메모리·작업 공간

| 구성 축 | 관찰 내용 | 추가 검증 |
|---|---|---|
| Model configuration | Hermes의 모델 설정 | 선택 모델, 역할별 지정 |
| Memory configuration | Hermes의 메모리 설정 | 저장 대상, 유지 기간, 공유 범위 |
| Multi-model workspace | SkillTree의 Claude·GPT·Gemini 통합 | 자동 선택, fallback, 결과 통합 |
| Role configuration | Hermes의 연구·작성·검토 | 순서, 전달 형식, 검토 강제성 |

Memory는 선호나 참고 정보를 기억하는 기능일 수 있다. 실행 진행 지점인 execution state를 저장하는 기능과 별도로 검증해야 한다. Muse의 장기 목표 지원도 상시 실행의 증거는 아니다.

## 분석용 실행 구조

```text
사용자 요청 → 실행 담당 agent 또는 역할 → 업무 처리 → 결과 확인
                    ↓ 평가 질문
          진행 상태 / 중단·재개 / 실패 처리 / 권한
```

이는 비교용 개념도이며 특정 제품의 내부 구현을 재현하지 않는다. 요청 없는 서비스 대기와 개별 작업 실행도 구분한다.

## 다음 학습

[[tech/ai/persistent-background-agents/02-ecosystem|도구별 관찰 비교]] · [[tech/ai/persistent-background-agents/README|학습 경로로 돌아가기]]

## Sources

- 사용자 제공 dossier: Dots·Muse·Grok Bot·OpenClaw·Hermes·SkillTree 소개 영상의 수집 요약. 원본 영상 제목·게시자·게시일·URL은 제공되지 않았다.
- 출처 URL: **미제공**. 제품명으로 공식 사이트나 특정 제품을 추정하여 연결하지 않았다.
- 아래 내용은 dossier의 관찰 범위와 분석·실습 제안을 구분한 정리이며, 공식 문서 또는 직접 실행으로 검증한 제품 사양이 아니다.
