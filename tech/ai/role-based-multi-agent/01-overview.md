---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: 역할 기반 multi-agent 협업

## What

하나의 목표를 여러 agent의 책임으로 나누는 작업 방식이다. 여러 agent가 같은 화면에 있다는 관찰만으로 실제 협업이 검증되지는 않는다.

| 분리 축 | 자료의 사례 | 해석 범위 |
|---|---|---|
| 업무 기능 | Grok Bot: 리서치·영업·마케팅·운영 | 담당 영역을 나누는 구성 |
| 작업 단계 | Hermes: 연구자·작성자·검토자 | 결과물을 만드는 과정의 분리 |
| 조직·모델 | SkillTree: 여러 부서 agent, Claude·GPT·Gemini | agent와 모델을 한 공간에 배치 |

## Why

연구는 근거의 충분성, 작성은 전달력, 검토는 오류와 누락을 우선한다. 책임을 분리하면 각 단계의 평가 기준과 실패 지점을 드러낼 수 있다. 이는 설계적 해석이며 성능 향상이 측정되었다는 뜻은 아니다. 전달 과정에서 정보가 손실되거나 조정 비용이 늘어날 수도 있어 비교 실험이 필요하다.

## 핵심 특징

다음 표는 **실습용 설계안**이다. Hermes의 실제 전달 형식이나 승인 절차를 뜻하지 않는다.

| 역할 | 입력 | 책임·산출물 | 완료 기준 |
|---|---|---|---|
| Researcher | 공통 목표, 원자료 | 주장·근거 장부, 미확인 목록 | 각 주장에 근거 또는 미확인 표시 |
| Writer | 원자료, 근거 장부 | 초안, 주장별 근거 ID | 관찰과 제안을 구분 |
| Reviewer | 원자료, 장부, 초안 | 오류 목록, 수정 요청, 승인 판단 | 근거 없는 확정 주장 제거 |

## 독립적으로 설계할 네 축

- **Role:** 맡는 책임. 이름보다 입력·출력·완료 조건이 중요하다.
- **Model:** 책임을 수행하는 모델. 같은 모델로도 역할을 나눌 수 있다.
- **Memory:** 이후 참조할 정보. Hermes의 메모리 설정은 shared memory의 증거가 아니다.
- **Workspace:** agent와 작업을 모아 관리하는 공간. 한 공간에 있다고 자동 연동되는 것은 아니다.

## 실행 구조의 확인 한계

| 설계 항목 | 필요한 결정 | 자료의 확인 범위 |
|---|---|---|
| Task routing | 작업 배정 주체·규칙 | 역할 예시만 확인 |
| Handoff | 전달 형식·수신 확인 | 미상 |
| Orchestration | 순서·병렬 실행·재작업 제어 | 미상 |
| State / Memory | 공유 대상·접근 권한·보존 기간 | Hermes 설정의 존재만 확인 |
| Review gate | 오류 발생 시 되돌릴 단계 | 검토자 역할만 확인 |
| Completion | 종료 조건·최종 승인 주체 | 미상 |

중앙 coordinator, peer-to-peer 통신, 특정 framework를 사용한다고 단정할 수 없다. Dots의 지속 작업과 OpenClaw의 백그라운드·채팅 방식도 별도의 비교 축이다. 역할 분리는 장시간 실행을 보장하지 않는다.

## 다음 학습

[[tech/ai/role-based-multi-agent/02-ecosystem|도구 비교]] · [[tech/ai/role-based-multi-agent/04-learning/01-getting-started|순차 workflow 실습]] · [[tech/ai/role-based-multi-agent/README|학습 지도]]

## Sources

- 사용자 제공 dossier 및 그 안의 영상 요약. 원본 제목·제작자·출처 URL은 제공되지 않았다.
- 출처 URL: 미제공. 외부 검색이나 URL 열기는 수행하지 않았으며, 동명 제품의 사이트를 근거로 대체하지 않았다.
