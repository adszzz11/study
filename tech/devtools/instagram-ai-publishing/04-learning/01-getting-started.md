---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: draft-first 콘텐츠 루프

[[tech/devtools/instagram-ai-publishing/README|README]] · [[tech/devtools/instagram-ai-publishing/cheatsheet|Cheatsheet]]

## 1. voice.md를 먼저 만든다

브랜드의 독자, 어조, 금지 표현, CTA 원칙, 잘된 기존 게시물 예시를 기록한다. 이 파일은 “그럴듯한 범용 caption”을 계정 고유 문장으로 교정하는 기준이다.

```md
# Voice
- 독자: 1인 창업자와 콘텐츠 운영자
- 어조: 구체적이고 차분함, 과장 금지
- 금지: 보장, 무조건, 충격적인
- CTA: 질문 하나로 끝낸다
```

## 2. 수동 조사로 swipe file을 만든다

6–12개 경쟁 계정에서 각각 10–12개 Reel을 사람이 관찰한다. 최근 median views와 개별 views를 기록해 outlier multiple을 계산한다.

```text
outlier multiple = reel views / account의 최근 median views
```

3x 이상을 재현 후보로 표시하되, hook·주제·편집 리듬을 기록하는 조사 신호로만 사용한다.

## 3. Reel 초안을 생성하고 검토한다

`/ig-reel`에 주제 하나를 주고 hook 3개, script, beat sheet, screen text를 만든다. 그다음 사실성, voice 적합성, 표현 위험을 사람이 검토한다. 아직 publishing service에는 보내지 않는다.

## 4. 첫 연결은 read와 draft로 제한한다

Uplika MCP 연결 시 먼저 account 조회와 draft 저장만 검증한다. `accounts:read`, `posts:read`가 기대한 계정만 보이는지 확인한 뒤에만 `posts:write`로 범위를 넓힌다.

## Sources

- https://github.com/Jakeschincariol/instagram-agent-skill
- https://github.com/Jakeschincariol/instagram-agent-skill/blob/main/skills/ig-viral/SKILL.md
- https://uplika.com/en/docs
