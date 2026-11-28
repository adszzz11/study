---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: Handoff · Context · Orchestration

## 핵심 개념

| 개념 | 분석용 정의 | 확인 질문 |
|---|---|---|
| Agent role | 업무 목표와 산출물 책임 | 역할별 완료 조건은? |
| Model selection | 실행할 모델 선택 | 수동·고정·자동 routing 중 무엇인가? |
| Context | 현재 실행에 전달되는 정보 | 꼭 필요한 입력은? |
| Memory | 실행 사이에 유지되는 정보 | 저장·수정·삭제 범위는? |
| Handoff | 역할 사이 결과 전달 | 어떤 형식으로 넘기는가? |
| Orchestration | 분해·실행 순서·인계 조율 | 누가 상태와 실패를 관리하는가? |

모두 분석을 위한 개념이며 SkillTree에 구현되었다는 뜻은 아니다.

## 구조화된 인계 실험

자연어 대화만 전달하는 경우와 아래 형식을 사용하는 경우를 같은 업무·모델 조건에서 비교한다.

```yaml
# 실험용 산출물 계약: 제품 설정 파일이 아님
handoff:
  task: 공개 자료 기반 마케팅 초안
  producer_role: researcher
  consumer_role: writer
  evidence: []       # 사실과 근거 위치
  unknowns: []       # 미확인 항목
  deliverable: ""
  acceptance_criteria: []
  review_required: true
```

작성자는 주장과 근거를 연결하고, 검토자는 수정 대상·이유를 반환한다. 추가 질문 횟수, 정보 누락, 재작업량을 기록한다.

## Context 경계 실험

- 공통 자료와 역할 전용 자료를 나눈다.
- 다음 역할에 필요한 최소 정보만 넘긴 경우의 누락을 확인한다.
- 자료 접근 권한과 prompt에 전달한 내용을 구분한다. Prompt 지시만으로 접근 제어가 구현되지는 않는다.
- 지속 memory를 가정하지 말고 다음 실행에서 실제로 유지되는지 확인한다.

## 실행 제어와 추적

상태는 실험용으로 `대기 → 실행 → 검토 → 완료`를 정의하고 실패 시 `중단 → 수정 → 재시도`를 기록한다. 이는 제품의 상태 체계가 아니다. 실행별 입력, 역할, 모델, 출력, 검토, 승인자를 연결한다.

수동 인계가 안정된 뒤 자동화 후보를 검토한다. 자동 routing은 선택 근거와 실패 시 대체 경로까지 확인해야 평가할 수 있다.

[[tech/ai/multi-model-agent-workspace/README|학습 경로로 돌아가기]]

## Sources

- 제공된 dossier: SkillTree 및 함께 소개된 도구의 영상 요약. 원본 URL은 제공되지 않았다.
- 출처 URL: 미제공. 영상 제목·시점의 구체 값도 현재 dossier에 없어 원문 대조가 불가능하다. URL을 추정하거나 새 출처를 추가하지 않았다.
