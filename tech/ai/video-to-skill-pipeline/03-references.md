---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# References

| 자료 | 용도 |
|---|---|
| [원본 Instagram Reel](https://www.instagram.com/reel/DdLedEbz1DX/) | study의 출발점; 게시물과 화면 맥락 확인 |
| [원문 가이드](https://lazyowen.com/guides/claude-youtube-skill) | tutorial을 Claude Skill로 바꾸는 세팅의 공개 설명 |
| [claude-video](https://github.com/bradautomates/claude-video) | Watch Skill의 설치·source 검토 |
| [Watch SKILL.md](https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md) | engine, timestamp, security behavior 확인 |
| [Gemini Video Understanding](https://ai.google.dev/gemini-api/docs/video-understanding?hl=en) | video input과 timestamp 질의 API |
| [Claude Skills](https://support.claude.com/en/articles/12512176-what-are-skills) | instruction, script, resource 묶음의 개념 |
| [Claude Marketplace](https://claude.com/marketplace/plugins) | plugin distribution과 검토 대상 |
| [yt-dlp README](https://github.com/yt-dlp/yt-dlp/blob/master/README.md) | media/caption 수집 도구 |

## 읽는 순서

1. 원본 Reel과 가이드로 의도·범위를 확인한다.
2. Gemini 문서 또는 Watch `SKILL.md`로 video evidence 처리 방식을 확인한다.
3. Claude Skills와 Marketplace 자료로 packaging 및 공급망 경계를 검토한다.
4. 구현 전 [[tech/ai/video-to-skill-pipeline/cheatsheet|Cheatsheet]]의 안전 checklist를 적용한다.

## Sources

- https://www.instagram.com/reel/DdLedEbz1DX/
- https://lazyowen.com/guides/claude-youtube-skill
- https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md
