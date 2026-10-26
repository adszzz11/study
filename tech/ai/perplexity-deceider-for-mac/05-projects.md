---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Private support triage

로컬 export된 고객 문의를 `billing`, `bug`, `feature_request`, `other`로 label한다. 각 message마다 `choice` request 하나를 보내고, 최고 probability가 정책 threshold 미만인 건만 human review queue에 적재한다.

**완료 기준**: labeled holdout set에서 class별 precision/recall, review rate, 잘못된 auto-route 사례를 기록한다.

## 2. Pre-commit secret guard

regex detector가 후보 줄을 찾고, `noul`이 문맥상 password/token/secret일 확률을 보조 판단한다. threshold를 넘으면 commit을 멈추거나 review를 요구한다.

**주의**: CI secret scanner의 대체물이 아니다. fail-open 동작, scanner bypass, false negative를 별도 threat로 취급한다.

## 3. Screenshot inbox organizer

image `choice`로 screenshot을 `receipt`, `error`, `chat`, `code`, `other`로 분류해 폴더 정리 후보를 만든다. confidence가 낮은 image는 자동 이동하지 않고 inbox에 남긴다.

## 4. Build/deploy monitor

주기적으로 수집한 screenshot에 “error dialog 또는 failed build가 보이는가?”라는 `noul` question을 보낸다. threshold 초과 시 알림을 만들되, alert deduplication과 사람이 확인할 원본 screenshot link를 둔다.

## 5. Human-in-the-loop compliance triage

문서의 risk 또는 approval 필요성을 `score`로 정렬하고 reviewer queue에 전달한다. model output만으로 자동 거절·해고·법적 판단을 확정하지 않는다.

## 공통 구현 checklist

- [ ] request당 한 question으로 Flash 호출을 시작했는가?
- [ ] criteria와 fallback option을 versioned configuration으로 보관했는가?
- [ ] model version·threshold·평가 date를 결과와 함께 기록했는가?
- [ ] low-confidence 및 threshold 근처 case를 human review로 보냈는가?
- [ ] local과 hosted 각각에서 labeled sample로 threshold를 검증했는가?

## Sources

- https://docs.perplexity.ai/docs/decisions/decider-for-mac
- https://docs.perplexity.ai/docs/decisions/quickstart
