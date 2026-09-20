---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 참고자료와 provenance

> [[02-ecosystem|이전: 비교]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

## Source register

| ID | Source | 종류 | 확인 결과 | 신뢰도/용도 |
|---|---|---|---|---|
| S1 | https://www.instagram.com/reel/DddvxSdAIrG/ | 원본 URL | 비로그인 요청에서 본문·캡션 미반환 | 대상 식별자만 확정 |
| S2 | shortcode `DddvxSdAIrG` exact-match 검색 | 검색 기록 | 색인 결과 없음 | 부재는 내용의 증거가 아님 |
| S3 | 공유 token exact-match 검색 | 검색 기록 | 색인 결과 없음 | 부재는 내용의 증거가 아님 |
| S4 | 공개 embed/oEmbed 경로 | 대체 접근 | 콘텐츠 복원 실패 | 기술 주제 확인 불가 |
| S5 | Orca local browser | 로컬 판독 | `runtime_unavailable` | 실행 환경 장애 기록 |

## 식별자

```yaml
canonical_url: https://www.instagram.com/reel/DddvxSdAIrG/
shortcode: DddvxSdAIrG
shared_url: https://www.instagram.com/reel/DddvxSdAIrG/?stkn=MTA2cWltdXN0bmkyOQ==
observed_at: 2026-09-20
content_status: unavailable
topic_status: unknown
```

공유 token은 접근 맥락을 보존하기 위해 기록하지만, 공개 노트에서 인증 정보나 비공개 session으로 간주하지 않는다. 기술 주제를 검증할 때는 query를 제거한 canonical URL을 기본 식별자로 쓴다.

## 추가로 필요한 자료

다음 중 하나만 있어도 1차 식별을 재개할 수 있다.

- tool 이름이나 logo가 보이는 화면 캡처
- Reel 영상 파일
- caption 전문과 hashtags
- 영상에서 언급된 기술명

## 후속 source 기준

기술명이 확인되면 최소 다섯 개의 관련 URL을 수집한다.

- 공식 product/docs landing page
- 공식 getting started 또는 API reference
- 공식 release notes/changelog
- 공식 GitHub repository 또는 package registry
- 공식 limitation, security, pricing 중 주제와 관련된 문서

## Sources

- [원본 Instagram Reel](https://www.instagram.com/reel/DddvxSdAIrG/)
- [공유 URL](https://www.instagram.com/reel/DddvxSdAIrG/?stkn=MTA2cWltdXN0bmkyOQ==)
- 사용자 제공 dossier

