---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Instagram Reels 공개 메타데이터·트랜스크립트 수집 파이프라인

> **한 줄 정의**: 공개 Instagram Reel URL에서 허용된 API와 embed 데이터를 확인하고, 권한 있는 영상의 멀티모달 분석 결과를 provenance와 함께 재현 가능하게 저장하는 파이프라인이다.

## Overview

Reel shortcode는 유용한 식별자지만 조회 결과는 로그인·공개 여부·지역·권한에 따라 달라진다. `URL 정규화 → oEmbed → 소유 Professional Account API → 허가된 분석` 순서로 범위를 좁힌다.

```text
Reel URL → canonical URL / shortcode → oEmbed
         → Official Instagram API (소유 계정만)
         → ASR · OCR · vision → provenance 저장 → 검색/분석
```

해당 URL의 계정·캡션·영상 내용은 확인하지 못했으므로, 영상 내용을 사실로 추정하지 않는다.

## Learning Path

- [ ] [[tech/scraping/instagram-reel-analysis/01-overview|Overview]] — 문제와 설계 원칙
- [ ] [[tech/scraping/instagram-reel-analysis/02-ecosystem|Ecosystem]] — 공식 API와 보조 수단 비교
- [ ] [[tech/scraping/instagram-reel-analysis/04-learning/01-getting-started|시작하기]] — canonical URL과 oEmbed 기록
- [ ] [[tech/scraping/instagram-reel-analysis/04-learning/02-deep-dive|심화]] — provenance와 분석 저장 모델
- [ ] [[tech/scraping/instagram-reel-analysis/05-projects|Projects]] — 운영 프로젝트
- [ ] [[tech/scraping/instagram-reel-analysis/03-references|References]] — 공식 문서
- [ ] [[tech/scraping/instagram-reel-analysis/cheatsheet|Cheatsheet]] — 빠른 점검표

## When To Use

- 공개 Reel의 embed 가능 여부와 URL provenance를 기록할 때
- 내가 관리하는 Professional Account의 Reel metadata·engagement를 적재할 때
- 저작권·동의 조건을 충족한 영상에서 ASR, OCR, vision 검색 인덱스를 만들 때

## When Not To Use

- private 계정이나 타인의 콘텐츠를 우회 수집하려는 경우
- oEmbed 응답만으로 원본 영상·완전한 creator metadata를 기대하는 경우
- 삭제·비공개·rate limit을 “콘텐츠 부재”로 단정하는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Scraping]]
- [[tech/scraping/browserless/README|Browserless]]

## Sources

- https://developers.facebook.com/docs/graph-api/reference/instagram-oembed
- https://developers.facebook.com/docs/graph-api/changelog/non-versioned-changes/nvc-2025
- https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/v21.0/
