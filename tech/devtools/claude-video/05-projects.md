---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Bug Reproduction Triage

사용자가 올린 screen recording에서 오류 timestamp, 재현 단계, 의심 UI state를 issue template으로 만든다.

```markdown
## Observed evidence
- Timestamp: 02:21
- Visible state: Save button disabled after selecting an item
- Transcript: "I clicked save, but nothing happened"

## Reproduction candidate
1. Open Settings
2. Select an item
3. Click Save
```

완료 기준은 영상 요약이 아니라 각 claim이 timestamped evidence에 연결되는 것이다. 자동 생성된 재현 절차는 QA가 재실행해 검증한다.

## 2. Video QA/RAG

강의·웨비나를 chapter 단위의 transcript, scene thumbnail, timestamp citation으로 색인한다. 질의가 들어오면 전체 영상 대신 관련 chapter와 좁은 window를 재분석한다.

- ingestion: 권한 확인 → caption/transcript → chapter 후보 생성
- retrieval: 질문의 topic·timestamp 후보 선택
- answer: transcript와 frame evidence를 함께 인용
- evaluation: timestamp 정확도, citation coverage, 놓친 장면 비율

## 3. Competitive Creative Analysis

광고 또는 product launch 영상에서 hook, CTA, 화면 구성, 핵심 메시지를 비교한다. 한 영상의 절대적 "좋음"을 판정하기보다 일관된 rubric과 timestamp 증거를 사용한다.

| Dimension | 질문 |
|---|---|
| Hook | 첫 5초에 무엇이 주의를 끄는가? |
| Message | 핵심 value proposition은 언제·어떻게 전달되는가? |
| CTA | 행동 요청이 화면·음성에서 일치하는가? |
| Visual rhythm | scene 변화와 copy 지속시간은 충분한가? |

## 4. Design-to-Implementation Review

Figma prototype 또는 product demo를 분석해 화면 흐름, copy, interaction regression 후보를 PR checklist로 변환한다. video만으로 interaction semantics를 확정하지 말고 design source와 implementation을 함께 대조한다.

## 5. Accessibility Audit Assist

자막 존재 여부, 화면 텍스트의 지속시간, 안내 음성과 시각 정보의 불일치를 후보로 추출한다. contrast ratio, WCAG 준수 여부, 실제 사용성은 사람이 최종 판정한다.

## Sources

- https://github.com/bradautomates/claude-video
- https://platform.claude.com/docs/en/build-with-claude/vision
