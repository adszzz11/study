---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive — integration과 publishing boundary

## Skill을 검수 gate로 설계하기

생성 prompt와 검수 prompt를 분리한다. 생성 단계는 다양한 angle을 넓게 만들고, linter 단계는 다음 항목만 판정한다.

| 검사 | 통과 기준 |
|---|---|
| Brand voice | `voice.md`의 허용 어조와 불일치하지 않음 |
| Evidence | 수치·고객 사례·제품 claim에 근거가 있음 |
| Risk | 민감정보, 미공개 정보, 경쟁사 비방이 없음 |
| CTA | 독자에게 맞고 과도한 약속이 없음 |
| Publishability | 사람 승인 없이는 `ready-to-publish`가 아님 |

## MCP와 data governance

MCP 연결은 `read-only`를 기본으로 시작한다. CRM에는 동의된 first-party data만 사용하고, 문서 저장소에는 작업에 필요한 최소 범위만 노출한다. server별로 owner, token 범위, 입력·출력 log, 데이터 보존 기간을 문서화한다.

```text
Claude Code → MCP server → approved CRM / docs / analytics
                   │
                   └→ scope · audit log · revocation owner
```

## 공식 publishing 경로

조직 Page에서만 필요한 경우, 승인 queue를 통과한 payload를 공식 Posts API로 전달한다. 운영 checklist에는 API access tier, `w_organization_social`, version sunset, rate limit, 오류 재시도, audit log를 넣는다. API 인증 실패나 승인 누락 시에는 게시하지 않고 queue에 되돌린다.

이 경로는 browser automation의 우회책이 아니다. 개인 계정의 브라우저 조작과 자동 engagement는 policy risk 때문에 제외한다.

## Related Notes

- [[tech/ai/claude-linkedin-workflows/README|README]]
- [[tech/ai/claude-linkedin-workflows/01-overview|Overview]]
- [[tech/ai/claude-linkedin-workflows/05-projects|Projects]]

## Sources

- https://code.claude.com/docs/en/mcp
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?tabs=curl&view=li-lms-2026-06
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-api-migration-guide?view=li-lms-2026-07
