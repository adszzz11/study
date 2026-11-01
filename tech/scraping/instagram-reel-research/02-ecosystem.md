---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Instagram Reel 리서치 접근 방법 비교

| 방법 | caption/영상 확인 | 신뢰성 | 제약 |
|---|---:|---:|---|
| Search engine | 일부 | 낮음 | 색인 누락 빈번 |
| Instagram permalink/embed | 공개 시 가능 | 높음 | 로그인·접근 제한 가능 |
| Instagram Graph API | 권한 범위 내 가능 | 높음 | 임의 공개 Reel 조회용이 아님 |
| Creator가 제공한 caption/영상 | 가능 | 최고 | 원본 제공 필요 |
| 비공식 downloader/scraper | 경우에 따라 가능 | 가변적 | 약관·접근 통제·재현성 위험 |

## 선택 원칙

1. creator가 제공한 원본 caption·영상·스크린샷을 우선한다.
2. 공개 permalink 또는 embed로 원문을 직접 대조한다.
3. API는 OAuth, access token, permissions, account ownership이 충족될 때만 사용한다.
4. 검색 결과는 discovery 후보로만 사용하고 원문 근거로 승격하지 않는다.
5. 비공식 수집 도구로 접근 통제를 우회하지 않으며 Terms of Use와 대상 권한을 확인한다.

## 관련 노트

- [[tech/scraping/instagram-reel-research/01-overview|Overview]]
- [[tech/scraping/instagram-reel-research/03-references|References]]
