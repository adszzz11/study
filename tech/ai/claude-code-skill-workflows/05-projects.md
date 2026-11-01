---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 적용 패턴

## Evidence-backed market scout

세 worker가 고객 고충, 경쟁, 가격 근거를 각각 수집한다. judge는 중복을 제거하고 source별 신뢰도를 표시해 MVP 가설과 인터뷰 질문을 만든다. 시장 규모를 추정으로 채우지 말고, 모르는 부분은 interview backlog로 남긴다.

## PR quality gate

구현 agent와 security reviewer, test reviewer, API contract reviewer를 분리한다. CI 결과가 없거나 acceptance criterion을 충족하지 못한 변경은 merge 후보에서 제외한다.

## Large-repo context optimizer

`CODEMAP.md`, API contract 요약, 실패 테스트 추출, session handoff template을 만든다. 작업 전후 token/시간, 재시도 횟수, regression을 기록해 context 절약이 품질 저하로 이어지지 않는지 확인한다.

## Brand-aware frontend audit

현재 design token, 접근성 기준, 반응형 요구, 브랜드 reference를 입력으로 준다. “보라색 gradient·Inter·범용 카드 UI 금지” 같은 규칙은 출발점일 뿐이다. checklist와 screenshot review로 콘텐츠 hierarchy 및 브랜드 적합성을 검증한다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/cheatsheet|Cheatsheet]]

## Sources

- https://github.com/ANVEAI/idea-hunt-skill
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables

## 추가 조사: Evidence-First Business Idea Discovery

릴스의 “business idea 발굴”은 모델에게 아이디어 목록을 많이 생성시키는 작업이 아니라, **반복되는 고충(problem)과 지불 의사(willingness to pay)를 반증 가능하게 확인**하는 조사다. AI는 source clustering과 interview preparation에는 유용하지만, 시장 수요를 증명하지는 않는다.

| 단계 | agent가 할 일 | 사람/외부 검증 |
|---|---|---|
| Problem signal | 리뷰·forum·support ticket에서 반복 고충을 분류 | 원문 URL과 인용 맥락 확인 |
| Segment | 누가 얼마나 자주 겪는지 가설화 | 잠재 고객 interview |
| Existing alternative | 경쟁사·수작업·내부 workaround 정리 | 가격·약관·현재 기능 직접 확인 |
| WTP | 시간·매출·위험 비용으로 가설 작성 | pre-order, paid pilot, LOI 등 실제 행동 |
| MVP decision | 가장 작은 test를 제안 | 성공/중단 기준을 사전에 합의 |

```text
Claim: <누가>가 <상황>에서 <고충>을 겪는다.
Evidence: <원문 URL, 날짜, 직접 인용/요약>
Counter-evidence: <이미 해결됨 / 빈도 낮음 / 무료 대안>
Next test: <5명 interview 또는 paid pilot>
Kill criterion: <어떤 결과면 가설을 중단할지>
```

- 같은 Reddit thread를 여러 agent가 반복 요약한 것은 독립 증거가 아니다. source diversity와 날짜 범위를 표에 명시한다.
- agent output의 TAM·가격·수요 수치는 가설로 라벨링하고, 검증 전에는 투자·채용·출시 결정을 정당화하는 숫자로 쓰지 않는다.

## 추가 조사: AI 티 없는 UI는 Design System과 검증의 문제

“AI 티 없는 UI”는 특정 font나 gradient 금지 목록이 아니라 product context에 맞는 **의도된 visual system**과 반복적인 시각 검증이다. 최신 prompting guidance도 CSS variable로 일관성을 유지하고, 맥락 없는 cookie-cutter layout·보라색 gradient·과용된 font에 수렴하지 말 것을 권한다.

| 입력 | 구현 규칙 | 검증 방법 |
|---|---|---|
| 브랜드 자산·콘텐츠 우선순위 | token(색·type·spacing)과 hierarchy를 먼저 정의 | reference와 side-by-side review |
| 사용자·기기·접근성 요구 | responsive states, keyboard, contrast를 명세 | viewport별 screenshot + manual keyboard test |
| 기존 제품 패턴 | 재사용 가능한 component boundary 설정 | visual regression + design review |
| 금지할 generic pattern | 이유와 대체 방향을 기록 | “금지”가 아니라 task fit으로 판정 |

```text
UI audit prompt:
"아래 screenshot을 기준 reference와 비교하라. 색상만 평하지 말고
정보 hierarchy, 읽기 흐름, responsive overflow, keyboard focus,
contrast, 빈 상태와 오류 상태를 각각 PASS/FAIL과 근거로 기록하라."
```

- screenshot review는 기능 test를 대체하지 않고, 기능 test는 hierarchy·밀도·브랜드 적합성 판단을 대체하지 않는다.
- reference asset의 license와 실제 브랜드 가이드를 먼저 확인한다. 임의로 인기 UI를 복제하는 것은 품질 기준이 될 수 없다.

출처: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
