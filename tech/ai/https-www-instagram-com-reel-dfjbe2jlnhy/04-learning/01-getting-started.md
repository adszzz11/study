---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — evidence packet 만들기

[[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/README|README]]의 `insufficient evidence`를 해제하려면, 먼저 허용된 자료를 작고 검토 가능한 packet으로 정리한다.

## 1. 입력을 보존한다

- caption은 URL과 수집 시각을 함께 복사한다.
- screenshot은 원본 파일명, 표시된 timestamp, crop·blur 여부를 적는다.
- transcript는 자동 전사인지, 사람이 교정했는지와 화자 불확실성을 명시한다.

## 2. 관찰과 해석을 분리한다

```yaml
observation:
  source: creator-provided transcript
  captured_at: 2026-11-10
  quote_or_frame: "00:12에 보이는 버튼 라벨"
interpretation: "특정 AI 도구의 export 기능일 수 있음"
confidence: low
verification_needed: "공식 제품 문서 또는 전체 화면"
```

`interpretation`은 사실로 승격하지 않는다. 제품명, 버전, 가격, 성능은 공식 문서나 재현 결과로 교차검증한다.

## 3. 멈출 지점을 정한다

증거가 없으면 요약을 작성하지 않고 요청자에게 caption, screenshot, transcript 중 하나를 요청한다. 다음 단계는 [[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/04-learning/02-deep-dive|Deep Dive]]다.

## Sources

- https://www.w3.org/TR/prov-overview/
- https://www.w3.org/TR/prov-dm/
