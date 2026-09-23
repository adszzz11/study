---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 실전 적용

## 1. Product launch / social video factory

CMS의 product copy, 가격, image를 composition data로 주입하고 9:16/16:9 variant를 일괄 render한다.

- 입력: validated product JSON과 versioned asset URL
- composition: aspect ratio별 layout token과 scene template
- 출력: social channel별 MP4/WebM, manifest
- 검증: SKU별 keyframe snapshot과 brand font 검사

## 2. Data storytelling

주간 KPI JSON을 animated chart, count-up, map, UI panel로 변환해 보고용 clip을 만든다.

- 데이터 집계는 render 이전에 완료한다.
- 숫자 animation은 timestamp에서 계산 가능해야 한다.
- chart scale, locale, 기준일을 composition input에 명시한다.

## 3. Release-note-to-video pipeline

```text
GitHub release / PR summary
  → LLM script + approved assets
  → HyperFrames composition
  → preview approval
  → lint / render
  → MP4 + Shorts export
```

LLM output은 바로 render하지 말고 schema validation과 preview approval을 통과시킨다. 외부 release data와 image URL은 render 시점이 아니라 job 생성 시 snapshot으로 고정한다.

## 4. Personalized lifecycle video

사용자명, 상품, 추천 결과만 parameter로 바꿔 template 영상의 variant를 만든다. 개인화 input에는 PII 최소화, tenant isolation, request rate limit, retention policy를 둔다. queue에는 idempotency key를 사용해 같은 job의 중복 render를 막는다.

## 5. Interactive preview + render API

Vercel/Cloudflare template을 기반으로 preview와 `/api/render`를 분리한다.

| 계층 | 책임 |
| --- | --- |
| Preview | `<hyperframes-player>`로 편집 전 결과 확인 |
| API | auth, input schema, job 생성 |
| Queue | concurrency, retry, deduplication |
| Worker | 고정된 Chrome/FFmpeg environment에서 render |
| Storage | Blob/R2 저장, lifecycle, signed URL |

## Sources

- https://hyperframes.heygen.com/guides/deploy
- https://hyperframes.heygen.com/packages/cli
- https://hyperframes.heygen.com/introduction
