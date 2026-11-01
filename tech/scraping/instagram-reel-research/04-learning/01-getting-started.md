---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 관찰 가능한 사실 기록하기

## 목표

Reel URL의 식별 정보와 실제 콘텐츠 근거를 분리하고, 나중에 같은 판단을 재현할 수 있는 provenance record를 만든다.

## 절차

1. permalink에서 shortcode를 기록한다. 예: `DfLt9CrCLxN`.
2. 조회 시각(UTC 또는 시간대 포함), 요청 URL, 접근 결과를 기록한다.
3. 직접 확인한 creator handle·caption·발행일·영상·자막만 원문 그대로 보존한다.
4. 검색엔진 결과는 발견 경로로 기록하되, 색인 부재를 콘텐츠 부재로 해석하지 않는다.
5. 영상 또는 caption이 없으면 결과를 `unverified`로 종료하고 원본 제공을 요청한다.

## 최소 record 예시

```yaml
permalink: https://www.instagram.com/reel/DfLt9CrCLxN/
shortcode: DfLt9CrCLxN
observed_at: 2026-11-01T00:00:00+09:00
access_status: unverified
creator_handle: null
caption_verbatim: null
video_or_transcript_evidence: null
claim: "실제 주제는 공개 웹 관찰만으로 확인되지 않음"
```

## 완료 기준

- 추론과 관찰 사실이 분리되어 있다.
- `obrf` 같은 query parameter를 콘텐츠 근거로 쓰지 않았다.
- [[tech/scraping/instagram-reel-research/03-references|References]]의 정책·API 범위를 확인했다.

다음: [[tech/scraping/instagram-reel-research/04-learning/02-deep-dive|심화]]
