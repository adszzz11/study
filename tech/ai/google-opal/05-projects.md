---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Google Opal Projects

> [[README|목차로 돌아가기]]

| 프로젝트 | Workflow | 검증 기준 |
|---|---|---|
| 시장 리서치 brief generator | 회사명 → Search/Maps → 경쟁사·최근 뉴스 → citation webpage/Sheet | 각 claim에 URL이 있고 날짜가 표시된다. |
| 콘텐츠 repurposing studio | topic·brand guide → outline/social copy/image prompt/storyboard 병렬 생성 | 브랜드 제약을 지키고 채널별 결과가 중복되지 않는다. |
| study-pack builder | lecture note 업로드 → 요약·quiz·이미지 설명·TTS podcast | 답이 원문에서 추적 가능하고 quiz에 정답·근거가 있다. |
| plant-care assistant | 사진 → 식물 식별 → Memory 관리 기록 → care card | 식별 confidence와 불확실성을 표시하며 위험 조언은 단정하지 않는다. |
| 여행 planner | destination·기간 → Search/Maps → itinerary → Memory 선호 반영 | 운영 시간·장소 정보를 출처와 함께 검증한다. |

## 권장 진행 순서

1. 시장 리서치 brief로 `User Input → Generate → Output`과 citation을 익힌다.
2. study-pack builder로 uploaded asset과 output format constraint를 추가한다.
3. 여행 planner로 Agent Mode, Search/Maps, Memory, `@Go to` fallback을 연습한다.

## 공통 acceptance checklist

- [ ] input이 비어 있거나 모호할 때 재질문 또는 제한을 보여 준다.
- [ ] 외부 조사 claim에는 source URL과 조사 시점이 있다.
- [ ] asset 원문 밖의 사실은 추정으로 표시한다.
- [ ] memory에 민감 정보나 확인되지 않은 사실을 저장하지 않는다.
- [ ] publish 전 Drive/Opal 공유 권한과 prompt graph 노출을 검토한다.

## Sources

- https://developers.google.com/opal/overview
- https://developers.google.com/opal/Agent_Mode
- https://developers.google.com/opal/faq
