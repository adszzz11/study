---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive — claim matrix와 provenance

[[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/04-learning/01-getting-started|evidence packet]]이 생기면 claim마다 근거·판정·변경 이력을 연결한다.

| Claim | Evidence ID | 검증 방법 | 상태 |
| --- | --- | --- | --- |
| 도구명 | caption-001 | vendor의 공식 페이지와 대조 | pending |
| 특정 기능 | frame-003 | UI label + 문서 + 재현 | pending |
| 결과/성능 | transcript-002 | 조건이 같은 독립 실행 | pending |

## Versioning 규칙

- 원본은 overwrite하지 않고 `evidence_id`를 새로 부여한다.
- 변환(crop, OCR, transcription)은 activity로 기록한다.
- 인용은 timestamp 또는 frame ID를 포함한다.
- 캡처에 계정명·token·개인정보가 있으면 공유 전 최소화한다.

C2PA manifest가 존재하더라도 그것은 출처·이력 정보를 제공하는 보조 신호다. 화면의 주장이 사실인지, 현재 제품에도 같은 기능이 있는지는 별도 공식 문서와 실행으로 검증한다. 이 절차의 산출물 예시는 [[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/05-projects|Projects]]에서 다룬다.

## Sources

- https://www.w3.org/TR/prov-dm/
- https://spec.c2pa.org/specifications/specifications/1.4/index.html
