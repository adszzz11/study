---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 역할 기반 협업 점검

## 개념 빠른 구분

| 용어 | 질문 |
|---|---|
| Role | 어떤 책임과 산출물을 맡는가? |
| Model | 어떤 모델이 수행하는가? |
| Memory | 무엇을 유지하고 누가 참조하는가? |
| Workspace | agent와 작업을 어디에 모으는가? |
| Orchestration | 배정·순서·재작업·종료를 누가 제어하는가? |

## 최소 workflow

```text
목표·근거 범위 고정
→ Researcher: 주장 / 근거 / 확인 수준 / 미확인 사항
→ Writer: 근거 ID를 연결한 초안
→ Reviewer: 오류 위치 / 수정 요청 / 승인 판단
→ 수정 또는 사람 승인 (반복 한도 명시)
```

## 실행 전

- [ ] 역할별 입력·출력·완료 조건이 있는가?
- [ ] 같은 원자료와 버전을 사용하는가?
- [ ] handoff 형식과 수신자가 정해져 있는가?
- [ ] 검토자에게 원자료가 전달되는가?
- [ ] 통합·최종 승인 주체와 재작업 한도가 있는가?

## 과장 방지

| 관찰 | 확정하면 안 되는 주장 |
|---|---|
| 여러 agent가 화면에 존재 | 자동 협업이 구현됨 |
| 메모리 설정 존재 | shared memory 지원 |
| 여러 모델 배치 | 자동 모델 선택·역할 분리 |
| 백그라운드 실행 | multi-agent 협업 |
| 역할 목록 존재 | 장시간 무인 실행 보장 |

## 실행 후

- [ ] 관찰·해석·제안을 구분했는가?
- [ ] 미확인 기능을 확정적으로 쓰지 않았는가?
- [ ] 근거 없는 주장·누락·수정 횟수를 기록했는가?
- [ ] 사람 검토 시간과 전체 시간을 구분했는가?
- [ ] single-agent 기준선과 같은 조건으로 비교했는가?

## 연결

[[tech/ai/role-based-multi-agent/01-overview|개념 설명]] · [[tech/ai/role-based-multi-agent/04-learning/01-getting-started|실습]] · [[tech/ai/role-based-multi-agent/README|학습 지도]]

## Sources

- 사용자 제공 dossier 및 그 안의 영상 요약. 원본 제목·제작자·출처 URL은 제공되지 않았다.
- 출처 URL: 미제공. 외부 검색이나 URL 열기는 수행하지 않았으며, 동명 제품의 사이트를 근거로 대체하지 않았다.
