---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

[[tech/devtools/instagram-ai-publishing/README|README]] · [[tech/devtools/instagram-ai-publishing/04-learning/02-deep-dive|심화]]

## 운영 순서

```text
manual research → outlier multiple → draft → QA → human approval
→ draft/schedule/publish → get_post polling → insights → iteration
```

## 빠른 참조

| 항목 | 규칙 |
|---|---|
| outlier multiple | `views / 최근 median views`; 3x+는 조사 신호 |
| Reel | video 1개 필요 |
| Carousel | media 2–10개 |
| Caption | 최대 2,200자 |
| 예약 | `scheduledAt`에 timezone offset 명시 |
| 최종 상태 | publish 응답이 아니라 `get_post`의 `published`/`failed` |
| 재시도 | 실패한 target에만 `retry_post` |

## 발행 전 checklist

- [ ] 올바른 account와 채널인가?
- [ ] media, aspect/형식, caption 길이를 검증했는가?
- [ ] voice·사실·금칙어·AI media label을 확인했는가?
- [ ] `scheduledAt`과 timezone이 명확한가?
- [ ] 사람이 approval payload를 검토하고 명시적으로 승인했는가?

## 발행 후 checklist

- [ ] `get_post`로 `published` 상태와 URL을 확인했는가?
- [ ] `failed` target만 재시도했는가?
- [ ] insight를 다음 hook·CTA 실험의 가설과 연결했는가?

## Sources

- https://uplika.com/en/docs/instagram
- https://uplika.com/en/docs/agent-publish
- https://github.com/Jakeschincariol/instagram-agent-skill/blob/main/skills/ig-viral/SKILL.md
