---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — Cheatsheet

> [[README|목차로 돌아가기]]

## Snapshot

| 항목 | 내용 |
|---|---|
| Problem | LLM 초안을 voice·tone·독자·channel에 맞게 재작성 |
| Core method | style/voice conditioning + constrained rewriting |
| Essential input | 원문, audience, purpose, style guide, glossary, preserve list |
| Essential output | rewrite, diff, 변경 이유, uncertainty flag |
| Final authority | human editor 또는 문서 책임자 |

## Preserve List

```text
- proper nouns and product names
- numbers, dates, units, prices
- quotations, citations, URLs
- legal, medical, security, API terminology
- policy text, disclaimers, approved claims
```

## Safe Prompt Skeleton

```text
Rewrite for <audience> and <channel> using <voice spec>.
Preserve exactly: <preserve list>.
Do not invent facts, sources, or commitments.
Flag any sentence that cannot be rewritten safely.
Return the rewrite, a diff summary, and uncertainty flags.
```

## Release Gate

- [ ] PII·secret·retention policy를 확인했다.
- [ ] 수치, 고유명사, 인용, URL이 원문과 일치한다.
- [ ] glossary와 금지어 규칙을 통과했다.
- [ ] 사실과 정책 문구를 source로 대조했다.
- [ ] diff, model/template version, 승인자를 기록했다.
- [ ] detector score가 아닌 편집 승인과 독자 적합성으로 품질을 판단했다.

## Do / Don't

| Do | Don't |
|---|---|
| brand voice와 명확성을 개선 | detector bypass를 KPI로 설정 |
| 원문·근거·revision history 보존 | AI 사용이나 authorship를 숨김 |
| 사람의 최종 승인 유지 | high-stakes 문서를 무검토 publish |
| 실제 평가 세트로 vendor 비교 | 제품 주장만으로 도입 결정 |

## Sources

- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://quillbot.com/ai-humanizer
- https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/
- https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
