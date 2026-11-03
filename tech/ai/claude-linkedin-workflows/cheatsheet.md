---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — LinkedIn 콘텐츠 운영 checklist

## 초안 입력

- `voice.md`: 허용 어조, 금지 표현, formatting 규칙
- `audience.md`: 독자의 역할·상황·익숙한 용어
- `proof-points.md`: source URL과 확인된 claim
- `content-rubric.md`: evidence·risk·CTA 판정 기준

## Skill output contract

```text
topic → hooks 3개 → drafts 2개 → claim verification list
      → image brief → human decision needed → approval state
```

## Publish gate

- [ ] claim마다 source 또는 검증 보류가 있는가?
- [ ] 공개 불가 정보·개인정보·근거 없는 수치가 없는가?
- [ ] brand voice와 CTA가 audience에 맞는가?
- [ ] 사람이 명시적으로 승인했는가?
- [ ] 조직 Page라면 공식 API access, scope, version, audit log를 확인했는가?

## 제외할 자동화

| 제외 대상 | 이유 |
|---|---|
| LinkedIn scraping | 약관·개인정보·데이터 품질 위험 |
| Browser bot 게시·댓글·좋아요 | 무단 자동 활동 위험 |
| 대량 DM·connection 요청 | spam과 계정 위험 |
| 사람 검수 없는 즉시 게시 | 사실 오류와 brand risk |

## Related Notes

- [[tech/ai/claude-linkedin-workflows/README|README]]
- [[tech/ai/claude-linkedin-workflows/04-learning/01-getting-started|시작하기]]
- [[tech/ai/claude-linkedin-workflows/05-projects|Projects]]

## Sources

- https://code.claude.com/docs/en/skills
- https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?tabs=curl&view=li-lms-2026-06
