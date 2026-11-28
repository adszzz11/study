---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Workspace MCP 의무화와 AI Agent의 권한·비용·데이터 설계

> **한 줄 정의**: Google Workspace MCP 의무화는 AI Agent의 Workspace 접근을 Google이 운영하는 MCP 서버로 통합해, OAuth 권한 외에 작업별 정책·승인·감사·데이터 사용 제한을 적용하려는 접근 통제 체계다.

## Overview

> **근거 범위**: 제공된 dossier가 요약한 기사 한 편에 근거한다. 원문·Google 공식 약관·문서·제품 동작은 직접 검증하지 않았다. 정책·기능·일정은 기사에 보고된 내용이며, 설계 제안은 별도로 표시한다.

기사에 따르면 Google은 2026년 11월 24일 Workspace MCP 서버 8개를 정식 공개했고, **2027년 2월 1일부터 AI가 구동하는 Workspace 접근 도구에 Google MCP 사용을 요구**한다. 비AI 앱은 기사상 제외된다.

핵심은 API 교체보다 **접근 판단 위치의 이동**이다. OAuth token과 scope 외에도 공개 tool 범위, partner access, 관리자 정책, 승인, quota가 실행 가능성을 결정한다.

- **권한**: 유효한 token은 현재 작업에 대한 사용자 의도를 보장하지 않는다.
- **기능**: 공개 Gmail MCP에는 발송·답장·전달·기존 draft 수정이 없다. Drive도 이동·공유 등이 빠져 있다.
- **비용**: Standard tier는 project별·product별 하루 5,000 MCP request다. 사용자별 할당량이 아니다.
- **데이터**: 원문과 embedding·memory index 등 파생 데이터의 삭제·보존을 함께 설계해야 한다.

## Learning Path

- [ ] [[tech/ai/google-workspace-mcp/README|학습 진입점]]에서 범위와 근거 한계를 확인한다.
- [ ] [[tech/ai/google-workspace-mcp/01-overview|Overview]]에서 일정·권한 구조·제품별 기능을 읽는다.
- [ ] [[tech/ai/google-workspace-mcp/02-ecosystem|Ecosystem 비교]]로 public MCP·partner·REST의 선택 조건을 구분한다.
- [ ] [[tech/ai/google-workspace-mcp/04-learning/01-getting-started|시작하기]]로 기존 workflow의 전환 가능성을 점검한다.
- [ ] [[tech/ai/google-workspace-mcp/04-learning/02-deep-dive|Deep Dive]]에서 승인·quota·데이터 생명주기를 설계한다.
- [ ] [[tech/ai/google-workspace-mcp/05-projects|Projects]]의 모의 실험으로 설계를 검증한다.
- [ ] [[tech/ai/google-workspace-mcp/cheatsheet|Cheatsheet]]로 운영 판단 기준을 복습한다.
- [ ] [[tech/ai/google-workspace-mcp/03-references|References]]에서 출처와 공식 검증 과제를 확인한다.

## When To Use

- Workspace에 연결된 AI Agent의 MCP 전환 범위와 기능 손실을 평가할 때
- OAuth만으로 설명되지 않는 승인·정책·감사 경계를 설계할 때
- 다중 사용자 제품의 quota 예산과 memory 삭제 정책을 검토할 때

## When Not To Use

- 공식 약관 해석이나 출시 승인 근거가 필요할 때: 공식 문서와 계약 검증이 선행되어야 한다.
- partner 승인이나 공개 Gmail 발송을 이미 확보했다고 가정하는 구현 계획
- 비AI deterministic sync에 AI 적용 규칙을 그대로 단정할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/google-workspace-mcp/04-learning/02-deep-dive|관련 tech 노트: Agent 권한·비용·데이터 설계]]

MOC 두 링크는 요청된 vault 진입점이다. 현재 작업 공간에는 기존 vault가 없어 대상 존재 여부를 확인하지 못했다. 기존 관련 tech 노트 대신 이 묶음에서 생성한 설계 노트에 연결했다.

## Sources

- 제공 dossier의 단일 기사: https://techstackups.com/articles/google-workspace-ai-agents-mcp/
- 이 노트는 공식 문서·실제 서버 동작의 독립 검증 결과가 아니다.
