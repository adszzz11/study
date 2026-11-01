---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Instagram Reel 리서치 Cheatsheet

## 빠른 판단

| 질문 | 답변 |
|---|---|
| shortcode만으로 주제를 알 수 있는가? | 아니다. media object 식별자다. |
| public permalink이면 anonymous API 조회가 가능한가? | 아니다. Graph API는 권한·연결 계정 범위를 따른다. |
| 검색 결과가 없으면 Reel이 없는가? | 아니다. 미색인일 수 있다. |
| `obrf` parameter가 caption인가? | 아니다. 콘텐츠 근거로 사용하지 않는다. |
| 가장 강한 근거는? | creator 제공 원문 caption·영상·자막이다. |

## 조사 체크리스트

- [ ] permalink와 shortcode 기록
- [ ] 조회 시각·접근 상태 기록
- [ ] 원문 caption 또는 영상/전사본 확보 여부 표시
- [ ] OAuth·permissions·account ownership 확인
- [ ] Search snippet은 discovery 용도로만 표시
- [ ] 원문 없는 주제 추정 금지
- [ ] Terms of Use와 허용 범위 확인

## 보고 문구

> 이 링크의 실제 기술 주제 dossier를 만들려면 Reel의 caption, creator handle 또는 영상 화면/자막이 필요합니다. 현재 공개 웹에서 확인되지 않는 내용을 추정하지 않았습니다.

더 자세한 절차는 [[tech/scraping/instagram-reel-research/04-learning/01-getting-started|시작하기]], 근거는 [[tech/scraping/instagram-reel-research/03-references|References]]를 참고한다.
