---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — Ecosystem

> [[README|목차로 돌아가기]]

## Comparison

| 제품/대안 | 주된 포지션 | 강점 | 유의점 |
|---|---|---|---|
| Grammarly Humanizer | 업무용 writing surface 안의 voice refinement | custom voice, 문서 작성 흐름 통합 | 제품 내 사용 맥락 중심이며 범용 API 제품과 다름 |
| QuillBot AI Humanizer | 개인·교육·콘텐츠용 자연스러운 재작성 | basic/advanced mode와 후편집 UX | AI 결과를 자신의 작업물로 속여 제출하지 말아야 함 |
| Undetectable.AI | API·대량 처리형 humanization | purpose·readability·strength 제어, WebSocket streaming | bypass 중심 도입은 정책·평판 리스크가 큼 |
| DIY LLM pipeline | 조직별 brand voice editor | data boundary, glossary, 감사 로그를 직접 통제 | prompt·evaluation·운영 비용과 품질 검증이 필요 |
| 전통 paraphraser / grammar checker | 문장 단위 보정 | 낮은 위험, 예측 가능한 편집 | 깊은 voice transfer와 문서 단위 coherence는 제한적 |

## Selection Guide

| 상황 | 우선 검토 | 결정 기준 |
|---|---|---|
| 개인 문서의 빠른 후편집 | Grammarly 또는 QuillBot | 사용 편의성, 지원 언어, 조직의 AI 정책 |
| 대량 CMS 변환 | vendor API 또는 DIY pipeline | throughput, streaming, 비용, revision audit |
| 엄격한 terminology와 retention 요구 | DIY LLM gateway | data residency, glossary 강제, 접근 로그 |
| 규제·저작자 책임이 큰 문서 | human editor 중심 workflow | 공개 규칙, provenance, 사실 검토 책임 |

## Product Claims vs. Evaluation

제품의 mode, strength, readability 같은 제어값은 유용하지만 품질 보증이 아니다. 동일한 20개 평가 초안으로 아래를 비교한다.

- preserve list 위반률: 수치·고유명사·URL·인용이 달라진 비율
- factuality pass rate: 근거를 확인한 뒤 유지된 비율
- style acceptance rate: 편집자가 무수정 또는 경미 수정으로 승인한 비율
- latency와 문서당 비용
- reviewer가 수정에 쓴 시간

## Sources

- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://quillbot.com/ai-humanizer
- https://help.quillbot.com/hc/en-us/articles/35854318883351-What-are-modes-in-the-Quillbot-Paraphraser-and-how-do-I-use-them
- https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/
