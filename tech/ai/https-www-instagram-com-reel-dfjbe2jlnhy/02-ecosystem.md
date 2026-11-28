---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — acquisition, archive, provenance

[[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/README|README]]의 evidence gate는 하나의 scraper가 아니라 역할이 다른 도구들의 조합이다.

| 범주 | 예시 | 강점 | 주의점 |
| --- | --- | --- | --- |
| 작성자 제공 자료 | caption, transcript, export | 의도와 문맥 보존 | 편집 여부와 시점 기록 필요 |
| browser capture | screenshot, HAR metadata | 관찰 당시 UI 보존 | 로그인 token·개인정보를 제거 |
| web archive | Wayback Machine | 변경·삭제 전 URL의 보조 기록 | crawl 제한, media 완전성 미보장 |
| provenance 표준 | W3C PROV, C2PA | 생성·변형 이력 모델링 | 진실성 자체를 자동 보장하지 않음 |

### 선택 기준

1. 먼저 작성자의 허용된 1차 자료를 요청한다.
2. 공개 URL만 archival candidate로 취급하고, archive 결과를 원문과 동등시하지 않는다.
3. 각 파일에 `source_url`, `captured_at`, `collector`, `transform`을 기록한다.

이 비교는 Reel의 실제 기술 스택을 식별한 것이 아니다. 확인된 콘텐츠가 생긴 뒤에야 해당 도구와 [[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/05-projects|project]]를 연결한다.

## Sources

- https://help.archive.org/help/save-pages-in-the-wayback-machine/
- https://www.w3.org/TR/prov-overview/
- https://spec.c2pa.org/specifications/specifications/1.4/index.html
