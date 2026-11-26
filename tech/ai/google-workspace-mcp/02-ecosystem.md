---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 접근 경로 비교

> **근거 범위**: 제공된 dossier가 요약한 기사 한 편에 근거한다. 원문·Google 공식 약관·문서·제품 동작은 직접 검증하지 않았다. 정책·기능·일정은 기사에 보고된 내용이며, 설계 제안은 별도로 표시한다.

## 비교

| 경로·사례 | 기능과 장점 | 제약·불확실성 | 적용 판단 |
|---|---|---|---|
| Google public MCP | 공식 정책·승인·감사 경로, 제품별 tool | Gmail·Drive 공백, quota, 데이터 제한 | 공개 tool로 업무를 완결할 수 있는 Agent |
| Google partner access | 공개 Gmail에서 제한된 기능에 접근 가능 | 자격 기준·일반 공개 일정 미확인 | 조기 검토하되 승인·가용성 가정 금지 |
| Claude Workspace connector | 기사상 이메일 발송·답장·전달, Drive 이동·trash 광고 | 권한 제공 방식·계약 세부 미확인 | public MCP와 기능 범위가 다른 관측 사례 |
| 직접 REST: AI 도구 | 기존 API 기능을 구현한 제품이 있을 수 있음 | 기사상 2027-02-01 MCP 의무화 및 Standard quota | 기능이 동작해도 준수 가능한 우회로라고 단정 불가 |
| 직접 REST: 비AI 도구 | deterministic backup·CRM sync·script의 기존 경로 | AI model 결합 시 재검토 필요 | 실제 AI 사용 여부에 따라 분류 검토 |
| 사용자 수동 인계 | Gmail UI에서 수정·발송 등 마무리 가능 | 자동화 완결성 감소, 인계 상태 필요 | 설계 제안: public 기능 공백을 명시적으로 처리 |

REST 행과 수동 인계는 제공 dossier의 다른 설명에서 도출한 비교다. dossier의 원래 비교표는 REST 항목 도중 끝나며, 누락된 행 내용을 복원한 것이 아니다.

## 선택 순서

1. 업무를 검색·읽기·생성·수정·이동·공유·발송으로 분해한다.
2. 각 동작을 public tool과 대조한다.
3. 공백이 있으면 partner 확인 또는 사용자 인계로 제품 흐름을 다시 정의한다.
4. 관리자 승인·OAuth client·데이터 조건을 확인한다.
5. quota 가중치와 사용자 수로 용량을 계산한다.

문서 편집 Agent와 이메일 실행 Agent는 같은 “Workspace 지원”이어도 손실이 다르다. connector의 광고 기능만으로 public MCP와 동일한 계약·권한을 가진다고 추론하지 않는다.

## 관련 노트

[[tech/ai/google-workspace-mcp/01-overview|기능 표]] · [[tech/ai/google-workspace-mcp/04-learning/01-getting-started|전환 점검]] · [[tech/ai/google-workspace-mcp/README|학습 진입점]]

## Sources

- https://techstackups.com/articles/google-workspace-ai-agents-mcp/
