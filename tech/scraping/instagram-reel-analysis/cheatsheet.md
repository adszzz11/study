---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

> [[tech/scraping/instagram-reel-analysis/README|목차로 돌아가기]]

## 최소 저장 필드

| 그룹 | 필드 |
|---|---|
| 입력 | `input_url`, `canonical_url`, `shortcode`, `received_at` |
| 수집 | `source`, `api_version`, `checked_at`, `http_status`, `probe_status` |
| 소유 미디어 | `media_type`, `media_product_type`, `permalink`, `timestamp` |
| 분석 | `asset_hash`, `model`, `model_version`, `language`, `confidence`, `ran_at` |

## 운영 규칙

- query string을 제거한 canonical URL로 deduplicate한다.
- oEmbed는 embed 확인용이며 원본 media API로 오해하지 않는다.
- `media_url` 누락은 권리·오디오·정책 조건의 정상 결과일 수 있다.
- 삭제·비공개·rate limit은 서로 다른 상태로 기록한다.
- 원본, 파생 transcript, OCR, scene tag의 retention policy를 분리한다.

## 빠른 결정

```text
공개 URL인가? → canonicalize / oEmbed probe
소유 Professional Account인가? → Instagram API 조회
분석 권한과 원본이 있는가? → ASR/OCR/vision queue
아니오 → 상태와 provenance만 저장, 우회 수집하지 않음
```

상세 근거: [[tech/scraping/instagram-reel-analysis/03-references|References]]
