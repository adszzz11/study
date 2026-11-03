---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 사람 승인형 콘텐츠 loop

## 1. Context repository 만들기

프로젝트 폴더에 다음 파일을 만들고, 매 초안 작업 전에 읽도록 한다.

```text
context/
  voice.md           # 어조, 금지 표현, 문장 길이
  audience.md        # 독자 역할, 문제, 용어 수준
  proof-points.md    # 검증 가능한 제품·고객 근거와 URL
  content-rubric.md  # claim, CTA, 민감정보 검수 기준
  performance-log.md # 게시일, 주제, format, 가설, 성과
```

`proof-points.md`에는 추측이나 경쟁사 소문을 넣지 않는다. source URL, 확인 날짜, 사용 가능한 표현을 함께 기록한다.

## 2. 최초 Skill contract

`linkedin-post` Skill의 출력 계약을 작게 고정한다.

```text
입력: 주제 + context 파일
출력:
1) 서로 다른 hook 3개
2) LinkedIn post 초안 2개
3) 각 claim의 source/검증 필요 여부
4) 이미지 brief 1개
5) 사람이 결정할 항목과 게시 금지 사유
```

## 3. 2주간 수동 게시

처음에는 게시 연동을 만들지 않는다. `초안 → 사람 편집 → 수동 게시 → 성과 기록`을 2주 실행하고, 주간 review에서 topic·format·CTA 가설을 한 번에 하나씩 수정한다. 좋은 결과는 인과가 아니라 다음 실험의 후보로 취급한다.

## 완료 기준

- [ ] 모든 초안이 context 파일을 참조한다.
- [ ] 외부 claim마다 source 또는 검증 필요 표기가 있다.
- [ ] 사람 편집본과 성과가 `performance-log.md`에 남는다.
- [ ] scraping, browser bot, 자동 DM은 사용하지 않는다.

## Related Notes

- [[tech/ai/claude-linkedin-workflows/README|README]]
- [[tech/ai/claude-linkedin-workflows/04-learning/02-deep-dive|Deep Dive]]
- [[tech/ai/claude-linkedin-workflows/cheatsheet|Cheatsheet]]

## Sources

- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/skills
- https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en
