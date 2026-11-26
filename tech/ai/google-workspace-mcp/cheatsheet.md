---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

> **근거 범위**: 제공된 dossier가 요약한 기사 한 편에 근거한다. 원문·Google 공식 약관·문서·제품 동작은 직접 검증하지 않았다. 정책·기능·일정은 기사에 보고된 내용이며, 설계 제안은 별도로 표시한다.

## 빠른 판단

| 질문 | 기억할 기준 |
|---|---|
| OAuth scope가 있으면 충분한가? | tool·partner 자격·정책·승인·quota도 확인 |
| 공개 Gmail로 발송 가능한가? | 기사상 발송·답장·전달·기존 draft 수정은 partner 전용 |
| Drive 보고서 생성 후 전달까지 가능한가? | 이동·공유 등의 public 공백을 별도로 처리 |
| REST로 우회 가능한가? | AI 도구는 기사상 2027-02-01부터 MCP 의무화 |
| 비AI sync도 대상인가? | 기사상 제외. AI model 연결 시 재검토 |
| service account면 무인 실행 가능한가? | approval prompt 가능. 인증과 무인 완료는 별개 |
| Apps Script 기본 client를 쓰는가? | 기사상 MCP에는 custom client 필요 |
| 30일마다 index 재생성이면 충분한가? | active, user-authorized task인지 별도 판단 |

## 일정·숫자

- **2026-11-11**: agentic 표시 없는 OAuth client의 MCP 접근 거부 시작으로 보고됨
- **2026-11-24**: Workspace MCP 서버 8개 정식 공개로 보고됨
- **2027-02-01**: AI 도구 MCP 의무화·직접 REST Standard quota 적용 예정으로 보고됨
- **2027-04-01**: Gmail·Calendar·Drive Scaled tier 과금 시작 예정으로 보고됨
- **5,000 request/일**: Standard, project별·product별
- **10 request/호출**: 기사 예시의 Gmail `search_threads`, `list_drafts`
- **500회 검색/일**: 다른 호출이 전혀 없을 때의 계산상 최대
- **30일**: Google이 적용할 수 있는 보존 상한. 일괄 적용 확정 아님
- **Scaled 단가**: 기사에 미공개. 정확한 월 비용 계산 불가

## 설계 체크

- [ ] 외부 데이터와 사용자 명령을 구분한다.
- [ ] 업무 단계를 public·partner·수동 인계로 매핑한다.
- [ ] 부분 성공을 전체 완료로 표시하지 않는다.
- [ ] tool call 수와 quota 소비량을 구분한다.
- [ ] 원문·embedding·index·profile·graph의 삭제를 연결한다.
- [ ] 연결 해제 처리와 승인 대기·재개 경로를 준비한다.
- [ ] 공식 문서 확인 전 기사 주장을 확정 정책으로 쓰지 않는다.

## 관련 노트

[[tech/ai/google-workspace-mcp/README|학습 진입점]] · [[tech/ai/google-workspace-mcp/03-references|근거 검증]] · [[tech/ai/google-workspace-mcp/04-learning/02-deep-dive|상세 설계]]

## Sources

- https://techstackups.com/articles/google-workspace-ai-agents-mcp/
