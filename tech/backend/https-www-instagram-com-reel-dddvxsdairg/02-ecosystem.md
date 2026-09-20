---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 콘텐츠 식별 경로 비교

> [[01-overview|이전: 개요]] | [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

## 비교 기준

특정 tool의 ecosystem 비교는 주제 식별 후에만 가능하다. 현재는 Reel의 내용을 확보하는 경로를 비교한다.

| 경로 | 얻을 수 있는 정보 | 장점 | 한계 | 현재 결과 |
|---|---|---|---|---|
| 원본 Reel | 영상, audio, overlay text, caption | 가장 직접적인 source | 로그인·동적 렌더링·접근 제한 | 본문·캡션 미확보 |
| 화면 캡처 | UI, 코드, tool 이름 | 전달과 OCR이 쉬움 | audio·시간 흐름 누락 | 미제공 |
| 영상 파일 | 전체 프레임과 audio | 가장 완전한 offline 분석 | 파일 전달 필요 | 미제공 |
| 캡션 전문 | creator 설명, link, hashtag | text 검색과 claim 추출이 쉬움 | 화면 전용 정보 누락 | 미제공 |
| Exact-match 검색 | repost, transcript, 인용 | 공개 index 활용 | 색인되지 않은 콘텐츠에 취약 | 결과 없음 |
| embed/oEmbed | metadata, preview | 구조화된 정보 가능 | 권한·정책·삭제 상태 영향 | 복원 실패 |
| 로컬 브라우저 | 로그인 session 기반 판독 | 실제 UI 확인 가능 | runtime/session 의존 | `runtime_unavailable` |

## Source hierarchy

주제가 확인되면 다음 우선순위로 기술 내용을 검증한다.

1. Reel 자체: creator가 실제로 무엇을 주장했는지 확인
2. Vendor official docs: API, limitation, pricing, compatibility 확인
3. Official release notes 또는 repository: version과 변경 시점 확인
4. Reproducible example: 최소 예제로 claim 재현
5. Secondary source: 맥락 보충에만 사용

## 아직 작성할 수 없는 비교

다음 표는 기술명 확인 후 채운다. 빈칸을 추측으로 채우지 않는다.

| 기준 | Reel의 tool | 대안 A | 대안 B |
|---|---|---|---|
| 핵심 use case | 미확인 | 미정 | 미정 |
| Runtime/hosting | 미확인 | 미정 | 미정 |
| Integration | 미확인 | 미정 | 미정 |
| 비용·license | 미확인 | 미정 | 미정 |
| 운영 위험 | 미확인 | 미정 | 미정 |

## Sources

- [원본 Instagram Reel](https://www.instagram.com/reel/DddvxSdAIrG/)
- 사용자 제공 dossier

