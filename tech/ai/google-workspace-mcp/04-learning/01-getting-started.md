---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Workflow 전환 점검

> **근거 범위**: 제공된 dossier가 요약한 기사 한 편에 근거한다. 원문·Google 공식 약관·문서·제품 동작은 직접 검증하지 않았다. 정책·기능·일정은 기사에 보고된 내용이며, 설계 제안은 별도로 표시한다.

## 목표와 준비

목표는 API 호출 성공보다 **사용자 업무가 어디까지 끝나는지** 확인하는 것이다. 아래는 설계용 절차다. 실제 SDK 명령이나 인증 endpoint는 검증하지 않았으므로 실행 예제로 제시하지 않는다.

준비물: 기존 workflow 목록, OAuth client 정보, 사용자 승인 요구사항, 제품별 tool 목록, 예상 사용자 수. 실험은 가짜 메일과 모의 데이터로 시작한다.

## 1. 적용 대상 분류

- Workspace 데이터가 LLM에 전달되는가?
- model 결과가 Workspace 조회·변경 계획에 영향을 주는가?
- connector·proxy·CLI를 거쳐도 AI가 구동하는 도구에 해당하는가?

단순 script라는 이름만으로 비AI 예외를 가정하지 않는다. hobby use 경계는 공식 확인 대상으로 남긴다.

## 2. 인증 조건 확인

| 유형 | 기사상 주의점 |
|---|---|
| 일반 OAuth client | agentic 표시 필요. 기준일 이전 생성 후 제때 표시하지 않은 client는 재생성 필요하다고 설명 |
| Domain-wide delegation service account | agentic flag 설정 불가. 그것만으로 MCP 요청이 거부되지는 않지만 approval prompt 발생 |
| Apps Script 기본 client | agentic 표시 불가. MCP에는 custom client 필요 |

구체적인 기존 client 기준일·변경 기한은 제공 자료에 없으므로 추정하지 않는다.

## 3. 기능 매핑

| 업무 단계 | 공개 Gmail MCP | 제품 처리 제안 |
|---|---|---|
| 검색·thread 읽기 | 가능 | 승인 작업 범위 안에서 조회 |
| 답장 내용으로 새 draft 생성 | draft 생성 가능 | 발송 완료와 구분 |
| 피드백으로 기존 draft 수정 | 불가 | 사용자 수정 또는 새 draft와 중복 관리 |
| 발송·답장·전달 | partner 전용 | Gmail 수동 인계 또는 partner 확인 |

Drive의 생성·이동·공유도 각 단계로 분리한다. 전체 “보고서 전달”을 생성 tool 하나로 완료 처리하지 않는다.

## 4. 최소 용량 계산

기사 예시: `search_threads`, `list_drafts`는 호출당 10 request를 소비한다.

```text
Standard: 5,000 request / project / product / day
검색만 실행할 때: 5,000 / 10 = 500회/일
100명 × 하루 5회 × 가중치 10 = 5,000 request/일
```

이는 다른 호출·재시도가 없는 조건이다. 실제 배포에서는 여유분과 tool별 가중치를 따로 확인한다.

## 5. 완료 조건

- [ ] 모든 단계에 public tool·partner 의존·수동 인계를 표시했다.
- [ ] 승인 거절·quota 부족 때 중단하고 사용자에게 남은 단계를 알린다.
- [ ] 외부 이메일의 지시를 사용자 명령으로 승격하지 않는다.
- [ ] 연결 해제 시 원문·파생 데이터 삭제 경로를 정의했다.
- [ ] 공식 문서에서 미확인 조건을 검증하기 전 출시 확정 근거로 쓰지 않는다.

## 관련 노트

[[tech/ai/google-workspace-mcp/04-learning/02-deep-dive|심화 설계]] · [[tech/ai/google-workspace-mcp/05-projects|모의 프로젝트]] · [[tech/ai/google-workspace-mcp/README|학습 진입점]]

## Sources

- https://techstackups.com/articles/google-workspace-ai-agents-mcp/
