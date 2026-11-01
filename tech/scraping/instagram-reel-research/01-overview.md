---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Instagram Reel 리서치 개요

## What

Instagram Reel 리서치는 permalink가 가리키는 media object의 내용을, 출처와 접근 상태를 남기며 검증하는 작업이다. `DfLt9CrCLxN`의 경우 공개 웹에서 caption·영상·전사본을 확인하지 못했으므로 실제 주제를 분류하지 않는다.

## Why

URL 존재와 콘텐츠 접근 가능성은 다르다. 미색인, 비공개 전환, 삭제·보관, 로그인 요구, 지역·연령 제한은 외부 웹 조사 결과를 불완전하게 만든다. 확인되지 않은 내용을 기술 dossier로 작성하면 허위 분류가 된다.

## 정보 계층

| 계층 | 예시 | 이것만으로 알 수 없는 것 |
|---|---|---|
| 식별자 | `DfLt9CrCLxN` shortcode | 주제, 발화, creator |
| 링크 | permalink, `obrf` query | caption, 영상 내용 |
| metadata | creator, publish time, caption | 화면 속 코드·맥락 |
| 원본 | 영상, 자막, caption | 별도 검증이 필요한 외부 주장 |

## 핵심 특징

- Search engine은 일부 public professional account 게시물만 색인하므로 완전한 Reel 검색 수단이 아니다.
- Instagram permalink/embed는 공개 상태이면 강한 직접 근거가 될 수 있지만, 로그인 또는 접근 제한의 영향을 받는다.
- Graph API는 권한을 받은 연결 professional account 범위의 API이며, 임의 Reel 익명 조회 API가 아니다.
- 재현 가능한 결과는 permalink뿐 아니라 조회 시각, 접근 상태, 원문, 보존한 증거를 함께 기록한다.

## 다음 노트

- [[tech/scraping/instagram-reel-research/02-ecosystem|Ecosystem]]
- [[tech/scraping/instagram-reel-research/04-learning/01-getting-started|시작하기]]
