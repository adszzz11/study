---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Image to Code — Deep Dive

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. 문제를 역문제로 보기

하나의 rendered image를 만드는 code는 여러 개다.

```text
render(code, data, viewport, browser, state) = image
```

Image to code는 `image → code`의 유일한 inverse를 찾는 문제가 아니다. 관찰되지 않은 변수에 constraint를 추가해 좋은 해를 선택하는 문제다.

```text
best implementation
  = visual fidelity
  + executable behavior
  + semantic structure
  + repository conventions
  + maintainability
  + accessibility
  + security
```

## 2. Observation과 inference 분리

| 종류 | 예시 | 처리 |
|---|---|---|
| 관찰 가능 | text, color, visible spacing, element position | 이미지/OCR에서 추출 |
| 부분 관찰 | component hierarchy, layout rule, breakpoint | 여러 viewport로 constraint 강화 |
| 관찰 불가 | click result, validation, API, auth | requirement나 기존 code에서 확인 |
| 외부 자산 | font file, source image, icon set | 원본 제공·검색·placeholder 정책 필요 |

Pipeline은 inference를 사실처럼 숨기지 말고 assumption log로 남겨야 한다.

## 3. Intermediate Representation 설계

IR은 vision 결과와 framework code를 분리한다.

```json
{
  "node": "Hero",
  "bounds": [96, 144, 1248, 520],
  "layout": {"type": "grid", "columns": [0.55, 0.45], "gap": 48},
  "children": [
    {"node": "Heading", "text": "...", "token": "display-lg"},
    {"node": "Image", "asset": "hero-product", "fit": "contain"}
  ],
  "confidence": {"hierarchy": 0.88, "asset": 0.97}
}
```

좋은 IR은 다음을 지원한다.

- Coordinate가 아니라 relation과 constraint 표현
- Repeated pattern을 component candidate로 표시
- Color·spacing·typography를 token으로 정규화
- Asset provenance와 placeholder 상태 기록
- 각 추론의 confidence와 unresolved question 기록
- React, Vue, HTML 같은 여러 target으로 변환 가능

## 4. Visual grounding 개선

Text OCR와 bounding box를 vision prompt에 추가하면 작은 text의 누락을 줄일 수 있다. 그러나 OCR 결과도 오류가 있으므로 원본 이미지와 상호 검증한다.

```yaml
ocr:
  - text: "Start building"
    box: [104, 422, 238, 462]
    confidence: 0.98
layout:
  - role: primary-action
    box: [96, 408, 254, 476]
```

여러 screenshot을 사용할 때는 viewport와 state를 명확히 label한다. 그렇지 않으면 agent가 mobile 요소를 desktop variation으로 오해할 수 있다.

## 5. Render–Compare–Repair loop

```text
1. Generate or patch code
2. Build in sandbox
3. Render at controlled viewport
4. Measure global and region-level differences
5. Map mismatched region to DOM/component
6. Form one causal hypothesis
7. Apply localized patch
8. Re-render and keep only verified improvement
```

종료 조건을 먼저 정한다.

```yaml
stop_conditions:
  max_rounds: 8
  no_improvement_rounds: 2
  build_must_pass: true
  critical_a11y_violations: 0
  human_review_required: true
```

전체 파일 재생성은 이미 맞은 부분을 깨뜨릴 수 있다. Diff region을 DOM node와 source component로 연결하고 최소 patch를 만드는 편이 regression을 줄인다.

## 6. Metric의 함정

| Metric | 잘 보는 것 | 놓치기 쉬운 것 |
|---|---|---|
| Pixel diff | 정확한 위치·색 차이 | anti-aliasing, browser/font 차이에 민감 |
| SSIM/LPIPS | 지각적 유사성 | text 정확성, semantics |
| CLIP/DINO similarity | 전체 의미·구도 | 작은 요소 누락, 정확한 text |
| Block recall | element 누락 | code structure와 interaction |
| DOM/style comparison | 구조·style 차이 | 실제 시각 인상 |
| Human review | 종합 품질 | 비용, 일관성, 재현성 |

Metric 하나를 목표로 최적화하지 말고 실행 가능성, element recall, visual fidelity, code quality, responsive, interaction, accessibility를 함께 본다.

## 7. Accessibility와 semantics

Screenshot은 접근성 tree를 보여주지 않는다. 별도 검사가 필요한 항목:

- Landmark와 heading hierarchy
- Form label, error association, validation message
- Image `alt`와 decorative image 처리
- Native control 및 keyboard operation
- Focus order와 visible focus
- Color contrast와 color-only meaning
- Accessible name, role, value

## 8. Security와 권리

- Generated dependency를 allowlist/review한다.
- User-controlled HTML을 무검증 `innerHTML`로 넣지 않는다.
- 외부 image/font URL과 tracking resource를 확인한다.
- Screenshot에 포함된 secret·personal data를 제거한다.
- UI, logo, font, image의 사용·복제·게시 권한을 확인한다.
- Hosted service에 올릴 때 data retention과 model training policy를 확인한다.

## Sources

- https://aclanthology.org/2025.naacl-long.199/
- https://github.com/Djanghao/widget2code
- https://arxiv.org/abs/2506.06251
- https://arxiv.org/abs/2602.18548
- https://arxiv.org/abs/2602.05998
- https://arxiv.org/abs/2607.06306
- https://www.w3.org/TR/WCAG22/

