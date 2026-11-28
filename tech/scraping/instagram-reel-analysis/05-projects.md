---
date: 2026-11-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

> [[tech/scraping/instagram-reel-analysis/README|목차로 돌아가기]]

## 1. Reel research inbox

URL을 넣으면 canonicalization, embed 상태, 캡션(허용된 source에 한함), 키워드, human-review queue를 만든다. 핵심 산출물은 “수집 성공”이 아니라 오류 원인을 포함한 intake record다.

## 2. Creator-owned analytics

Professional Account Reel의 metadata와 허용된 engagement를 일별 snapshot으로 적재한다. 조회 시각·API version·권한 scope를 함께 남겨 대시보드의 수치를 설명 가능하게 만든다.

## 3. Multimodal knowledge base

허가된 Reel의 ASR·OCR·scene tag를 PostgreSQL FTS와 vector index에 저장한다. 예: “영상에서 언급한 도구”를 검색하고 원문 timestamp로 돌아간다.

## 4. Compliance-aware crawler

API 사용량, source provenance, retention policy, 삭제 요청 처리, human-review 로그를 운영 기능으로 둔다. Backend는 TypeScript/Python, 작업 큐는 Temporal/Celery, 저장소는 PostgreSQL + object storage 조합이 무난하다.

점검표: [[tech/scraping/instagram-reel-analysis/cheatsheet|Cheatsheet]]
