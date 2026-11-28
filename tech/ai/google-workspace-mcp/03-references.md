---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 근거와 검증 과제

## 현재 근거

| 자료 | 사용 범위 | 검증 상태 |
|---|---|---|
| TechStackups, “Google Will Make AI Agents Use Its MCP Servers. The Gmail One Can't Send Email” | 일정·기능·정책·quota에 관한 기사 주장 | 제공 dossier를 통해 사용. 원문 직접 확인 안 함 |
| 사용자 제공 dossier | 학습 노트의 사실·수치·주의사항 | 단일 기사 기반의 2차 정리 |

독립된 복수 출처가 아니다. 아래 목록은 **추가 확인 과제**이며 확인 완료된 근거가 아니다.

## 공식 검증 과제

- [ ] Google 공식 Workspace MCP 문서에서 8개 서버의 실제 tool 목록과 지원 범위를 확인한다.
- [ ] 약관 원문에서 AI Agent·AI Harness·AI model 도구의 정의, 시행일, 비AI 예외를 확인한다.
- [ ] OAuth 문서에서 agentic flag, 기존 client 교체 기준일·기한, Apps Script custom client 조건을 확인한다.
- [ ] Domain-wide delegation에서 승인 prompt가 발생하는 조건과 무인 실행 영향을 확인한다.
- [ ] Gmail partner access의 자격·승인 절차·일반 공개 일정을 확인한다.
- [ ] Standard quota의 제품별 가중치·초기화 기준, Scaled tier 단가·과금 개시 조건을 확인한다.
- [ ] “Google Technical Information” 정의, 최대 보존 기간을 적용하는 조건, 연결 해제 삭제 의무를 확인한다.
- [ ] Claude connector의 기능 제공 방식과 계약을 별도로 확인한다.

## 오독 방지

| 표현 | 피해야 할 결론 |
|---|---|
| 보존 기간을 30일로 제한할 수 있음 | 모든 파생 데이터에 이미 일률적인 30일 TTL 적용 |
| Scaled tier 과금 | 단가가 공개되었거나 정확한 월 비용 계산 가능 |
| service account 인증 가능 | human confirmation 없이 완전 무인 실행 보장 |
| REST가 기술적으로 작동 | AI 도구의 준수 가능한 대체 경로 |
| connector의 발송 광고 | public Gmail MCP도 발송 가능 |

## 관련 노트

[[tech/ai/google-workspace-mcp/README|학습 진입점]] · [[tech/ai/google-workspace-mcp/cheatsheet|판단 요약]]

## Sources

- https://techstackups.com/articles/google-workspace-ai-agents-mcp/
- 추가 공식 URL은 직접 확인하지 않았으므로 검증된 출처로 나열하지 않는다.
