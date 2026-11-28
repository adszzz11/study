---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 지속 실행 agent 평가

## 용어 빠른 구분

| 용어 | 확인할 질문 |
|---|---|
| Interaction | 어디에서 요청하는가? |
| Background execution | 사용자가 화면을 보지 않는 동안 처리되는가? |
| Service lifecycle | 요청이 없을 때 서비스는 어떻게 대기하는가? |
| Persistence / durable execution | 중단 뒤 어디서 어떻게 복구되는가? |
| Memory | 어떤 정보를 얼마나 오래 기억하는가? |
| Execution state | 어느 단계까지 완료했는가? |
| Role handoff | 누가 무엇을 다음 역할에 전달하는가? |
| Model configuration | 어떤 모델을 어떤 역할에 지정하는가? |

## 도구별 조사 출발점

| 목적 | dossier의 사례 |
|---|---|
| 사용자 부재 중 작업 | Dots |
| 채팅과 서비스 | OpenClaw |
| 일상 업무·장기 목표 | Muse |
| 직무별 역할 | Grok Bot |
| 연구·작성·검토와 설정 | Hermes |
| 부서 agent·여러 모델 작업 공간 | SkillTree |

## 오해 방지

- Background 실행 ≠ 장애 후 복구.
- Memory 설정 ≠ execution checkpoint.
- 여러 역할 표시 ≠ 자동 위임·병렬 처리.
- 장기 목표 저장 ≠ 예약 시점의 실제 실행.
- 한 번 완료 ≠ 무중단·무기한 실행 보장.
- 자료에 없음 ≠ 미지원.

## 실행 전후 체크

- [ ] 제품 식별·버전·공식 근거를 확보했는가?
- [ ] 이탈 조건과 관찰 시각을 기록했는가?
- [ ] 결과·근거·완료/진행/실패를 구별할 수 있는가?
- [ ] 중단·재개·재시도·중복 방지를 확인했는가?
- [ ] 외부 행동의 권한·승인 범위를 확인했는가?
- [ ] 가격·배포·데이터 위치는 확인된 값만 적었는가?

## 기술스택 요약

- 실행·접점: Dots의 ChatGPT 내부 작업 지속, OpenClaw의 백그라운드 서비스·채팅 요청 처리가 관찰됐다.
- 업무 구성: 일상 업무와 리서치·영업·마케팅·운영, 연구자·작성자·검토자 역할이 제시됐다.
- 모델·메모리: Hermes의 모델·메모리 설정, SkillTree의 Claude·GPT·Gemini 통합이 소개됐다.
- 검증 경계: runtime, 저장소, queue, scheduler 등 실제 구현 스택과 복구 정책은 확인되지 않았다.

## 연결

[[tech/ai/persistent-background-agents/README|전체 학습 경로]] · [[tech/ai/persistent-background-agents/03-references|출처와 한계]]

## Sources

- 사용자 제공 dossier: Dots·Muse·Grok Bot·OpenClaw·Hermes·SkillTree 소개 영상의 수집 요약. 원본 영상 제목·게시자·게시일·URL은 제공되지 않았다.
- 출처 URL: **미제공**. 제품명으로 공식 사이트나 특정 제품을 추정하여 연결하지 않았다.
- 아래 내용은 dossier의 관찰 범위와 분석·실습 제안을 구분한 정리이며, 공식 문서 또는 직접 실행으로 검증한 제품 사양이 아니다.
