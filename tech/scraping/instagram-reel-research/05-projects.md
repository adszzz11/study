---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Instagram Reel 리서치 프로젝트

## 1. Transcript 기반 주제 추출 pipeline

입력으로 creator가 제공한 caption 또는 영상/스크린샷을 받는다. 전사본을 만든 뒤 주제·주장·코드 조각을 추출하고, 각 주장을 공식 primary source로 교차 검증한다.

**산출물**: 원문 인용, timestamp, 검증 링크, 불확실성 메모가 있는 dossier.

## 2. Research provenance store

URL별로 아래 필드를 저장하는 작은 database 또는 spreadsheet를 만든다.

| 필드 | 설명 |
|---|---|
| permalink / shortcode | 대상 식별 |
| observed_at / access_status | 조사 재현성 |
| creator / published_at | 확인된 metadata만 저장 |
| caption / transcript evidence | 원문 또는 보존 위치 |
| claim / source URL | 주장과 근거 연결 |

## 3. 허용 계정 범위 Media metadata collector

권한을 받은 connected professional account에 한정해 Graph API collector를 구현한다. token과 권한 오류를 우회하지 않고, 요청·응답 시각과 API version을 log로 남긴다.

시작 전 [[tech/scraping/instagram-reel-research/04-learning/02-deep-dive|권한 경계]]와 [[tech/scraping/instagram-reel-research/cheatsheet|Cheatsheet]]를 검토한다.
