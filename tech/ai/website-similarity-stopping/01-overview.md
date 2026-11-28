---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

영상 요약에는 `Browse → Build → Check → Complete`와 `Build ↔ Check` 반복, 웹사이트 유사도 90% 및 최대 6라운드가 함께 등장한다. 개념적으로 결과를 평가해 다시 제작하는 **feedback loop**로 읽을 수 있다.

## Why

- 품질 기준은 “언제 충분히 가까운가”에 답한다.
- 반복 한도는 “목표에 미달해도 언제 멈출 것인가”에 답한다.
- 품질 기준만으로는 반복이 끝나지 않을 수 있고, 횟수만으로는 품질과 무관하게 종료된다.

## 관찰된 구조와 미확인 사항

| 단계 | 확인된 내용 | 확인되지 않은 내용 |
|---|---|---|
| Browse | 제작 흐름의 단계 | 탐색 대상·수집 방식·reference 선정 |
| Build | Check와 반복 | 모델·언어·framework·실행 환경 |
| Check | 제작 결과 검사 | 검사 도구·평가 항목·점수 계산 |
| Complete | 완료 단계 | 목표 달성과 한도 도달의 표시 차이 |

Check 결과가 어떤 형식으로 Build에 전달되는지, 수정 항목을 자동 결정하는지는 확인되지 않았다.

## 종료 조건의 개념적 해석

```text
종료 = similarity >= 0.90 OR completed_rounds >= 6
```

실제 구현 코드가 아니다. 90% 이상을 통과로 보는지, 최초 Build를 라운드로 세는지, 한 라운드가 Build·Check 한 쌍인지, 6번째 검사에서 미달하면 어떤 상태가 되는지는 확인이 필요하다.

실전에서는 `target_reached`와 `round_limit_reached`를 구분해 기록할 수 있다. Craft Anything에 이 상태 구분이 구현되어 있다는 근거는 없다.

## 점수의 한계

Similarity가 screenshot, layout, 색상·typography·이미지, 텍스트, 상호작용 중 무엇을 측정하는지 알 수 없다. 화면이 비슷한 것과 기능이 올바른 것은 별개의 평가 대상이다.

영상의 Snake 요청에는 방향키 조작, 먹이 섭취 후 성장, 속도 증가가 포함된다. 이는 요구가 외형을 넘어설 수 있음을 보여주지만, 유사도 검사가 기능을 평가한다는 증거는 아니다.

반복 자체도 점수 상승을 보장하지 않는다. 한 요소의 수정이 다른 요소의 회귀를 만들 수 있다. 평가 환경 고정, 라운드 기록, 최고 결과 보관, 반환 정책 명시는 적용 제안이다.

## 다음 학습

[[tech/ai/website-similarity-stopping/02-ecosystem|종료 정책 비교]] · [[tech/ai/website-similarity-stopping/README|학습 경로]]

## Sources

- 제공된 dossier: Craft Anything 소개 영상의 수집 요약. 원본 영상 URL과 공식 문서 URL은 제공되지 않았다. 따라서 기재할 수 있는 출처 URL이 없으며, 임의로 추정하지 않는다.
- 아래 정책 해석과 실습 제안은 제품 구현이나 성능을 검증한 자료가 아니다.
