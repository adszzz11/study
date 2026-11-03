---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 안전한 적용 아이디어

## Founder Content Copilot

제품 변경사항과 고객 FAQ를 읽어 weekly thought-leadership 초안 5개를 만든다. 각 초안은 source link, target audience, hook angle, 검증할 claim을 포함하며 founder가 최종 편집한다.

## Brand Voice Linter

게시 전 과장 표현, 근거 없는 수치, 경쟁사 언급, 민감 정보, CTA 부재를 검사한다. 결과는 pass/fail 대신 `수정 제안 + 근거 + 사람 확인 필요`로 돌려줘야 한다.

## Organization Page Publisher

승인 queue의 콘텐츠만 공식 Posts API로 조직 Page에 게시하고 결과 ID와 audit log를 저장한다. 권한·API version·rate limit을 사전 확인하고 실패한 요청은 재승인 대상이 된다.

## Performance Review Agent

허용된 analytics 데이터를 주간 요약하여 다음 주의 topic, format, CTA 가설을 제안한다. 상관관계를 확정 성과 공식으로 표현하지 않고, 다음 실험과 success metric을 남긴다.

## Employee Advocacy Kit

승인된 핵심 메시지를 개인별 말투에 맞게 변형한 **수동 게시용** 초안을 제공한다. 개인 계정 게시·댓글·DM을 자동 실행하지 않는다.

## Related Notes

- [[tech/ai/claude-linkedin-workflows/README|README]]
- [[tech/ai/claude-linkedin-workflows/04-learning/02-deep-dive|Deep Dive]]
- [[tech/ai/claude-linkedin-workflows/cheatsheet|Cheatsheet]]

## Sources

- https://code.claude.com/docs/en/skills
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-02
- https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en
