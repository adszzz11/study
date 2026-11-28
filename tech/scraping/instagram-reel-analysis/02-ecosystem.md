---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem 비교

> [[tech/scraping/instagram-reel-analysis/README|목차로 돌아가기]]

| 방식 | 적합한 범위 | 장점 | 제약 |
|---|---|---|---|
| Meta `instagram_oembed` | 공개 Reel embed 확인 | 공식·가벼운 URL 처리 | 제한된 필드, 분석용 원본 데이터 부족 |
| Instagram API | 내가 관리하는 Professional Account | 구조화된 media/engagement 데이터 | 개인 계정·임의 타인 콘텐츠 수집용이 아님 |
| Meta Content Library/API | 자격 있는 연구 | 공익·연구 목적의 대규모 분석 | 접근 자격과 데이터 범위 제약 |
| 비공식 scraper/SaaS | 제한적인 공개 리서치 | 캡션·댓글·transcript 편의성 | 약관, 품질, UI 변경, 법적 검토 위험 |
| 수동 검증 + 자체 분석 | 소수의 특정 Reel | 맥락·영상 내용 정확도 | 자동화·확장성 낮음 |

1. 공개 embed를 먼저 확인한다.
2. 소유 Professional Account에는 Instagram API를 primary source로 쓴다.
3. 연구 목적 대량 분석은 Content Library/API의 자격 요건을 검토한다.
4. 비공식 도구는 정책·계약·개인정보 검토 후 보조 수단으로만 둔다.

관련: [[tech/scraping/instagram-reel-analysis/03-references|References]]
