---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent·MCP·콘텐츠 자동화 시스템: Projects

[[tech/ai/ai-agent-automation-systems/README|README]] · [[tech/ai/ai-agent-automation-systems/cheatsheet|Cheatsheet]]

| 프로젝트 | 최소 실행 단위 | 승인 경계 |
|---|---|---|
| AI Research Briefing | web 자료를 URL 포함으로 요약해 Notion/Slack draft 생성 | 공유·발송 전 승인 |
| Content Factory | trend → script → asset → caption → QA 흐름 | scheduler 게시 전 승인 |
| Personal Operating System | calendar·task·email을 읽어 일일 brief와 답장 초안 생성 | 이메일 전송 전 승인 |
| Sales Research Agent | 공개 기업 정보로 ICP score 산출 | outreach 발송 전 승인 |
| Code Review Gate | repo rule·test·security checklist로 report 생성 | merge·배포는 별도 CI/승인 |
| Second Brain | decision·glossary·reference를 retrieval 가능한 구조로 정리 | 원문 변경 전 승인 |

## Content Factory 예시

1. 공개 source에서 trend 후보와 URL을 수집한다.
2. Agent가 target audience에 맞는 script 초안을 만든다.
3. 생성 도구가 visual asset 후보를 만들고 provenance를 기록한다.
4. QA가 사실성·브랜드·저작권·caption을 확인한다.
5. 승인된 asset만 scheduler에 전달하고 성과를 다음 run의 context로 요약한다.

## 프로젝트 공통 Definition of Done

- 입력 source와 생성 결과가 run ID로 연결된다.
- 실패·retry·비용·approval이 조회 가능하다.
- 허용하지 않은 write action은 실행되지 않는다.
- 작은 eval set으로 품질 하락을 탐지한다.

## Sources

- https://lazyowen.com/challenge
- https://n8n.io/ai-agents/
- https://docs.n8n.io/advanced-ai/ai-agents/

