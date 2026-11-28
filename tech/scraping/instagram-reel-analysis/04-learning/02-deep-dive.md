---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: provenance와 멀티모달 분석

> [[tech/scraping/instagram-reel-analysis/README|목차로 돌아가기]] · [[tech/scraping/instagram-reel-analysis/04-learning/01-getting-started|이전: 시작하기]]

## 소유 계정 조회

Professional Account가 소유한 Reel만 Instagram API로 조회한다. `media_type`, `media_product_type`, `permalink`, `shortcode`, `timestamp`를 snapshot으로 적재하고, 변경 가능한 지표는 관측 시각별로 분리한다.

## 분석 레코드

허가된 `media_url` 또는 제공받은 원본만 ASR/OCR/vision에 전달한다. 원본 또는 추출물의 SHA-256 hash와 모델 정보를 묶으면 재처리 비교가 가능하다.

```json
{
  "asset_hash": "sha256:…",
  "source_url": "https://www.instagram.com/reel/<shortcode>/",
  "analysis": {
    "asr": {"model": "Whisper", "version": "pinned-version", "language": "ko", "confidence": 0.91},
    "ocr": {"model": "PaddleOCR", "version": "pinned-version"}
  },
  "ran_at": "2026-11-17T00:00:00Z"
}
```

## 상태 모델과 재시도

| 상태 | 의미 | 처리 |
|---|---|---|
| `embed_available` | embed 확인됨 | cache TTL 후 재검사 |
| `private_or_permission` | 비공개 또는 접근 권한 없음 | 우회하지 않고 종료/보류 |
| `rate_limited` | 요청 한도 초과 | `Retry-After` 또는 backoff |
| `deleted_or_unavailable` | 삭제·일시 장애 등을 포함 | 관측 사실로 저장, 재확인 |
| `analysis_not_permitted` | 분석 권한·원본 없음 | 분석 queue에 넣지 않음 |

관련 실전 과제: [[tech/scraping/instagram-reel-analysis/05-projects|Projects]]
