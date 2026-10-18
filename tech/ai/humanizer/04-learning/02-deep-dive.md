---
date: 2026-10-18
tags: [tech]
type: tech-tool-study
status: draft
---

# Humanizer — 심화

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]]

## Constrained Rewriting Pipeline

```text
draft + context
  → PII redaction / policy check
  → voice conditioning + preserve list
  → LLM rewrite
  → diff + semantic/factual/citation/glossary QA
  → human approval + version history
```

이 흐름에서 model output은 항상 검토 대상이다. 특히 원문에 URL, 인용, 수치, SLA, 환불·보안 정책 문구가 있으면 retrieval 또는 원문 대조로 근거를 확인한다.

## Voice Modeling

voice spec은 모델의 막연한 "human-like" 지시보다 검증 가능해야 한다.

| 속성 | 예시 | 평가 방법 |
|---|---|---|
| 문장 길이 | 짧고 직접적 / 설명형 | 문장 길이 분포 비교 |
| 격식 | 존댓말, 공식적, conversational | editor rubric |
| 어휘 | 제품 고유 용어, 쉬운 단어 | glossary 준수율 |
| 직접성 | 능동태, 명확한 CTA | 독자 task completion |
| locale | 한국어 존대, US English 등 | native reviewer 검토 |

Grammarly의 custom voice처럼 writing sample을 활용할 수 있지만, sample이 실제 승인 문서를 대표하는지와 외부 처리 권한을 별도로 확인한다.

## Quality Gates

```text
release = preserve-list pass
       AND citation/URL pass
       AND factuality review pass
       AND glossary pass
       AND human approval
```

- **Semantic similarity**: 의도와 핵심 주장 변경 여부를 찾아내는 보조 신호다.
- **Factual consistency**: source 또는 retrieval 결과와 대조한다. similarity만으로 대체할 수 없다.
- **Citation preservation**: 인용문, URL, 출처 label의 누락·변형을 검사한다.
- **Provenance**: 입력 version, prompt/template version, model, diff, reviewer 결정을 보관한다.

## Metrics and Failure Modes

| 지표 | 바람직한 방향 | 흔한 실패 |
|---|---|---|
| preserve-list violation | 0에 가깝게 | 수치·고유명사·URL 변형 |
| factuality pass rate | 높게 | 그럴듯한 설명을 새로 추가 |
| editor acceptance rate | 높게 | tone은 맞지만 의미가 약화 |
| reviewer time | 낮게 | 자동화가 오히려 수정량 증가 |
| detector score | 품질 KPI로 사용하지 않음 | 우회 경쟁이 목표를 왜곡 |

2025년 DAMAGE 연구는 기존 detector 다수가 humanized text에 취약함을 보였고 augmentation 기반 접근의 가능성도 제시했다. 이는 안정적으로 "우회"할 수 있다는 뜻이 아니라, 계속 변하는 공격-방어 환경임을 뜻한다.

## Sources

- https://help.undetectable.ai/en/article/humanization-api-v2-p28b2n/
- https://support.grammarly.com/hc/en-us/articles/38552339652109-Humanizer-user-guide
- https://arxiv.org/abs/2501.03437
- https://doi.org/10.1016/j.nlp.2025.100151
