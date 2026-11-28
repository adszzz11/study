---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview

> [[tech/scraping/instagram-reel-analysis/README|목차로 돌아가기]]

## What

Reel URL을 canonical form과 shortcode로 분리하고, 공개 embed 확인과 소유 계정 API 조회를 계층적으로 수행한다. 영상 분석은 명시적으로 허가된 미디어만 대상으로 하며, 결과에는 원본 URL·hash·모델 버전·실행시각을 포함한다.

## Why

검색 색인은 불완전하고 Reel의 공개 상태도 변한다. 비공식 HTML scraping은 UI 변경, rate limit, Terms of Use·개인정보 위험에 취약하다. oEmbed는 embed HTML과 provider 정보 확인에 적합하지만 범용 원본 영상 API는 아니다.

## 특징

- `instagram_oembed`: 공개 embed 가능성과 최소 provider 정보를 얻는다.
- Instagram API: 소유 Professional Account의 `media_product_type=REELS`, `permalink`, `shortcode`, `timestamp` 조회에 맞춘다.
- `media_url` 누락은 저작권 오디오·권리 플래그에 따른 정상 상태일 수 있다.
- 삭제·private 전환·rate limit·권한 부족을 별도 상태로 남긴다.
- transcript, OCR, scene tag에는 모델·언어·confidence·hash를 함께 기록한다.

```text
input URL → normalize → oEmbed probe → owned-media lookup
          → permitted analysis → immutable provenance + artifacts
```

다음: [[tech/scraping/instagram-reel-analysis/02-ecosystem|Ecosystem]]
