---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — 도구와 실행 경로 비교

| 선택지 | 강점 | 한계·적합한 역할 |
|---|---|---|
| Claude Code + Skills + MCP | 파일·도구·반복 절차를 함께 다루는 깊은 context workflow | LinkedIn 행동 실행 권한을 자동으로 주지 않는다 |
| ChatGPT/Claude web chat | 빠른 아이디어와 단발성 초안 | 브랜드 지식·검수 과정의 재현성이 낮다 |
| n8n/Make/Zapier | trigger, schedule, CRM 연결 | 모델 품질·brand voice·정책 gate는 별도 설계가 필요하다 |
| LinkedIn Community Management API | 조직 Page의 공식 게시·분석 경로 | vetting, access tier, 권한 제약이 있다 |
| Browser bot/scraper | 겉보기에는 빠른 prospecting·대량 행동 | 약관·계정·개인정보 리스크로 비권장 |

## 권장 조합

```text
Markdown context + Claude Code Skill
             ↓
허가된 MCP (CRM / docs / analytics)
             ↓
human review queue
             ↓
조직 Page: LinkedIn Posts API
```

MCP는 데이터를 복사·붙여넣기하지 않게 해 주는 연결 표준이지, 권한 관리 장치 자체는 아니다. 연결하는 각 server에 대해 credential, read/write 범위, audit log, 보존 정책을 별도로 정해야 한다.

조직 Page 게시가 필요하면 Community Management API의 vetting과 tier를 확인하고, Posts API의 조직 게시 권한인 `w_organization_social`을 최소 권한으로 다룬다. 개인 계정의 자동 조작을 대체하는 수단으로 API를 가정해서는 안 된다.

## Related Notes

- [[tech/ai/claude-linkedin-workflows/README|README]]
- [[tech/ai/claude-linkedin-workflows/03-references|References]]

## Sources

- https://code.claude.com/docs/en/mcp
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?tabs=curl&view=li-lms-2026-06
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-02
