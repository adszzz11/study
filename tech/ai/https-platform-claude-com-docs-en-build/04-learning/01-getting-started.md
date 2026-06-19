---
date: 2026-06-20
tags:
  - tech
  - ai
  - claude
  - prompt-engineering
  - getting-started
type: tech-tool-study
parent: "[[../README]]"
---

# Claude Prompting Best Practices - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 목표

이 단계의 목표는 Claude prompt를 "요청문"이 아니라 재사용 가능한 task spec으로 작성하는 것이다. 작은 classification/extraction 작업부터 시작해 XML structure, examples, output format을 체감한다.

---

## 1. 기본 prompt skeleton

```xml
<role>
You are a careful Korean technical study-note writer.
</role>

<task>
Summarize the input into a concise Korean study note.
</task>

<context>
Audience: software engineers studying AI tools.
Style: Korean explanation with English technical terms preserved.
</context>

<instructions>
- Use bullets and a small comparison table when useful.
- Do not invent facts not present in the input.
- If information is missing, write "확인 필요".
</instructions>

<input>
{{source_text}}
</input>

<output_format>
## 요약
- ...

## 핵심 용어
| 용어 | 설명 |
|------|------|
</output_format>
```

### 체크포인트

| 항목 | 확인 질문 |
|------|-----------|
| Role | 모델이 어떤 관점으로 답해야 하는가? |
| Task | 수행할 동사가 명확한가? |
| Context | audience, domain, business rule이 있는가? |
| Instructions | 제약과 성공 기준이 검증 가능한가? |
| Input | 처리 대상과 instruction이 분리되어 있는가? |
| Output | 결과 format이 충분히 구체적인가? |

---

## 2. Vague prompt 개선

### Before

```text
이 티켓 분류해줘.
```

### After

```xml
<role>
You are a B2B SaaS support triage agent.
</role>

<task>
Classify the ticket and assign priority.
</task>

<priority_rules>
- Security incident, leaked secret, or account takeover: P0
- Production outage or data loss: P1
- Billing issue or degraded feature: P2
- General question or feature request: P3
</priority_rules>

<ticket>
{{ticket_text}}
</ticket>

<output_format>
Return only JSON:
{
  "category": "security|outage|billing|bug|feature_request|question|other",
  "priority": "P0|P1|P2|P3",
  "rationale": "one short Korean sentence"
}
</output_format>
```

---

## 3. Few-shot examples 추가

예시는 모델에게 format과 판단 기준을 동시에 보여준다. 관련성, 다양성, edge case가 중요하다.

```xml
<examples>
  <example>
    <ticket>We found an exposed production API key in a public repo.</ticket>
    <answer>{"category":"security","priority":"P0","rationale":"노출된 production secret은 즉시 대응이 필요합니다."}</answer>
  </example>
  <example>
    <ticket>Can you add dark mode to the billing page?</ticket>
    <answer>{"category":"feature_request","priority":"P3","rationale":"기능 요청이며 긴급 장애가 아닙니다."}</answer>
  </example>
  <example>
    <ticket>Invoices are not loading for all admins.</ticket>
    <answer>{"category":"billing","priority":"P2","rationale":"billing workflow 장애지만 보안 사고는 아닙니다."}</answer>
  </example>
</examples>
```

---

## 4. Grounded answer template

문서 기반 답변에서는 모르는 것을 만들지 않게 해야 한다.

```xml
<instructions>
- Answer only from <documents>.
- Include citations as [doc_id].
- If the documents do not contain the answer, say "문서에서 확인할 수 없습니다."
- Do not use outside knowledge.
</instructions>

<documents>
  <document id="doc1">
  {{retrieved_context_1}}
  </document>
  <document id="doc2">
  {{retrieved_context_2}}
  </document>
</documents>

<question>
{{user_question}}
</question>
```

---

## 5. 실습 과제

| 과제 | 요구사항 |
|------|----------|
| Ticket classifier | category/priority JSON schema, 3 examples 작성 |
| 문서 요약 | `<documents>`와 citation rule 사용 |
| 데이터 추출 | missing value를 `null`로 반환하는 JSON template 작성 |
| 코드 리뷰 | severity 기준, patch scope, test expectation 명시 |

### 결과 검증

```text
Prompt review checklist:
- [ ] instruction과 input이 tag로 분리되어 있는가?
- [ ] output format이 machine-checkable 한가?
- [ ] 예시가 최소 3개 있고 edge case를 포함하는가?
- [ ] "모르면 모른다고 말하기" 규칙이 있는가?
- [ ] security/tool 관련 작업이면 trust boundary가 있는가?
```

---

## 관련 노트

- [[study/tech/ai/claude]] - Claude API에서 system/user message 구성
- [[study/tech/ai/llm-wiki-study]] - 문서 기반 답변과 wiki workflow
- [[study/tech/ai/codex]] - coding agent task brief 작성 방식
