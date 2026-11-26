---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Exploratory / Acceptance testing

## 빠른 비교

| 항목 | Exploratory testing | Acceptance testing |
|---|---|---|
| 중심 | 발견 | 기준 충족 판단 |
| 질문 | 사용 중 어떤 버그가 보이는가? | 고객·기획 기준으로 출시 준비가 되었는가? |
| 기록 제안 | 사용 맥락·관찰 사실 | 실제 기준·출처·결과·증거 |
| 결론 한계 | 미발견 ≠ 기준 통과 | 기준 통과 ≠ 모든 상황 무결성 |

## 실행 전후 체크

- [ ] 탐색 목적과 대상 기능을 정했다.
- [ ] 실제 고객·기획 기준을 확보했다. 없으면 미확인으로 남긴다.
- [ ] 관찰과 판단을 분리했다.
- [ ] 발견 문제와 관련 기준의 영향을 연결했다.
- [ ] 확인한 범위와 남은 불확실성을 적었다.

```text
관찰 → 관련 기준에 대한 영향 ─┐
기준별 확인 결과 ────────────┴→ 출시 준비 검토
```

이 구조와 체크리스트는 학습 제안이다. 필수 순서·표준 산출물·승인 절차를 뜻하지 않는다.

## 혼동 방지

- 시나리오 없음은 목적·기록 불필요를 뜻하지 않는다.
- 고객 기준은 고객의 직접 수행을 요구한다는 뜻이 아니다.
- 속도 측정은 실제 기준과 연결해야 출시 판단 근거가 된다.
- 자료에는 도구·자동화·효율 수치·비용·시간 정보가 없다.

## 연결

[[tech/devtools/exploratory-acceptance-testing/README|학습 경로]] · [[tech/devtools/exploratory-acceptance-testing/05-projects|실전 검토표]]

## Sources

- 사용자 제공 dossier: QA 테스트 유형 설명을 정리한 자료. 원본 영상 제목·URL·게시일은 제공되지 않았다.
- 추가 용어 확인용: ISTQB Glossary — https://glossary.istqb.org/ (원자료의 출처가 아니며, 이 노트의 원자료 주장에 대한 직접 인용으로 사용하지 않음).
