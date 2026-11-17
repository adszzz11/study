---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: URL과 oEmbed 상태 기록

> [[tech/scraping/instagram-reel-analysis/README|목차로 돌아가기]] · [[tech/scraping/instagram-reel-analysis/04-learning/02-deep-dive|다음: 심화]]

## 목표

Reel URL을 안전하게 정규화하고, 공개 embed 확인 결과를 콘텐츠 사실과 구별해 저장한다.

## 1. 입력 정규화

입력 `https://www.instagram.com/reel/DfyffnnlfXC/?xtok=NnoxMmJkbHZtd3Y4`에서 query string은 별도 원문 필드에 보존하되 canonical URL은 다음처럼 만든다.

```text
canonical_url = https://www.instagram.com/reel/DfyffnnlfXC/
shortcode     = DfyffnnlfXC
```

## 2. oEmbed probe 기록

공식 `instagram_oembed`를 호출할 수 있는 승인 환경에서 URL, 요청 시각, API 버전, HTTP 상태와 오류 분류를 저장한다. embed HTML이 반환되어도 영상 파일 또는 전체 metadata를 받았다는 뜻은 아니다.

```json
{
  "canonical_url": "https://www.instagram.com/reel/DfyffnnlfXC/",
  "shortcode": "DfyffnnlfXC",
  "probe_status": "embed_available",
  "checked_at": "2026-11-17T00:00:00Z",
  "source": "instagram_oembed"
}
```

## 체크리스트

- [ ] 원 입력 URL과 canonical URL을 분리해 저장했다.
- [ ] shortcode를 deduplication key 후보로 기록했다.
- [ ] 응답·오류에 request timestamp와 API version을 붙였다.
- [ ] `not_found`, `private_or_permission`, `rate_limited`를 구별했다.

다음: [[tech/scraping/instagram-reel-analysis/04-learning/02-deep-dive|심화 설계]]
