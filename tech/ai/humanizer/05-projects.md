---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — Projects

> [[README|목차로 돌아가기]]

## 1. Brand Voice Editor

CMS 초안을 브랜드별 tone으로 전환한다. style guide, 금지어, glossary, preserve list와 승인 workflow를 강제하고, 결과·diff·editor 결정을 version history에 남긴다.

**완료 조건**: 평가 세트에서 수치·URL·고유명사 변형이 없고, 담당 editor가 결과를 승인한다.

## 2. Bilingual Localization Reviewer

한국어↔영어 번역 뒤 어색한 직역을 다듬는다. 제품명, 수치, API 용어, code block은 고정하고 native reviewer가 locale과 존대·격식을 확인한다.

**완료 조건**: terminology 검사가 통과하고 양쪽 언어 reviewer가 의미 동등성을 승인한다.

## 3. Support Reply Copilot

티켓 답변을 따뜻하고 간결하게 편집한다. SLA, 환불, 보안 정책 문구는 LLM의 기억이 아니라 승인된 knowledge base retrieval로 검증한다.

**완료 조건**: 정책 문구가 source와 일치하며 담당자가 전송 전 승인한다.

## 4. Editorial QA Gateway

생성형 콘텐츠를 publish 전에 `rewrite → citation preservation → fact check → human approval` 순서로 통과시킨다. 어느 gate든 실패하면 publish하지 않고 원문·근거·수정 요청을 reviewer에게 돌려준다.

**완료 조건**: 모든 published version에 source, diff, reviewer decision이 연결된다.

## 5. Writing Coach

완성문만 반환하지 않고 왜 더 명확해졌는지와 수정 제안을 함께 보여 준다. 학습자의 저작물을 대체하지 않도록 원문, 제안, 채택한 수정의 경계를 명확히 표시한다.

**완료 조건**: 사용자가 수정 이유를 확인하고 자신의 문장으로 최종 선택할 수 있다.

## Sources

- https://quillbot.com/ai-humanizer
- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
