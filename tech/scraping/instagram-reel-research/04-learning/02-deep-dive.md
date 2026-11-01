---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: 권한 경계와 주제 검증 pipeline

## API 경계

Graph API를 사용하기 전 다음을 확인한다.

- OAuth access token의 발급 주체와 만료 정책
- 필요한 permissions와 Meta App의 승인 상태
- 대상이 연결된 Instagram professional account인지 여부
- 호출 범위가 account ownership 및 허용된 use case 안에 있는지 여부

`public URL`은 API resource 접근 권한을 뜻하지 않는다. 권한이 없거나 대상이 범위 밖이면 수집 실패를 정상 결과로 기록한다.

## 검증 pipeline

```text
permalink 발견
  -> 접근 상태 기록
  -> 원문 caption/영상/전사본 확보
  -> transcript에서 claim·키워드 추출
  -> 공식 primary source로 claim 교차 검증
  -> 인용 위치와 수집 시각을 포함해 dossier 작성
```

## 증거 등급

| 등급 | 증거 | 사용 방식 |
|---|---|---|
| A | creator 원문 caption·영상·자막 | 주제와 직접 발화 인용 |
| B | 공개 permalink/embed에서 직접 확인한 metadata | 식별·발행 맥락 보조 |
| C | 검색 snippet, 재게시물 | 후보 발견 전용 |
| D | URL parameter, 추측 | dossier 근거로 사용 금지 |

원문을 제공받았다면 [[tech/scraping/instagram-reel-research/05-projects|Projects]]의 transcript 기반 프로젝트로 진행한다.
