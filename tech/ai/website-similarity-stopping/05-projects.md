---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 종료 정책 적용

## 프로젝트 1: 정책 simulator

모델이나 웹사이트 생성기 없이 점수 sequence를 입력받아 종료 라운드·이유·최고 결과를 출력한다. 구현은 실습 계약을 따른다.

```python
def simulate(scores, target=0.90, cap=6):
    best = None
    for round_no, score in enumerate(scores, 1):
        if score is None or not 0 <= score <= 1:
            raise ValueError("Invalid evaluation score")
        if best is None or score > best[1]:
            best = (round_no, score)
        reason = ("target_reached" if score >= target else
                  "round_limit_reached" if round_no >= cap else None)
        if reason:
            return {"round": round_no, "reason": reason, "best": best}
    return {"round": len(scores), "reason": "input_exhausted", "best": best}
```

| 입력 (백분율 표기) | 예상 결과 |
|---|---|
| 72 → 85 → 91 | 3회, target_reached |
| 72 → 78 → 82 → 85 → 87 → 89 | 6회, round_limit_reached |
| 88 → 84 → 86 → 85 → 87 → 86 | 6회, round_limit_reached; 최고는 1회 |

입력은 `0.72`처럼 0~1로 전달한다. `input_exhausted`는 시뮬레이터 입력 부족이며 정책의 성공 종료가 아니다. None은 오류로 처리한다. 경계값 89·90·91%와 5·6회를 함께 검증한다.

## 프로젝트 2: 웹사이트 평가 기록

Reference 하나를 정하고 최대 6회 Build·Check를 기록한다. 각 라운드에 `round`, `score`, `changes`, `functional_check`, `stop_reason`과 artifact를 남긴다.

완료 기준은 최종 화면과 함께 변경·평가의 관계, 종료 이유, 기능 검사 결과, 최종·최고 결과 중 반환 정책을 설명할 수 있는 것이다. 품질 미달의 한도 종료는 추가 검토 대상으로 표시한다.

## 프로젝트 3: 반복 한도의 효과

같은 작업의 1·3·6회 중간 결과에서 외형 점수, 기능 상태, 누적 소요 시간을 비교한다. 개선 둔화와 회귀 구간을 찾고 추가 반복의 이득을 설명한다. 6회가 최적이라는 전제로 결론을 내리지 않는다.

## 연결

[[tech/ai/website-similarity-stopping/04-learning/02-deep-dive|검증 기준]] · [[tech/ai/website-similarity-stopping/README|학습 경로]]

## Sources

- 제공된 dossier: Craft Anything 소개 영상의 수집 요약. 원본 영상 URL과 공식 문서 URL은 제공되지 않았다. 따라서 기재할 수 있는 출처 URL이 없으며, 임의로 추정하지 않는다.
- 아래 정책 해석과 실습 제안은 제품 구현이나 성능을 검증한 자료가 아니다.
