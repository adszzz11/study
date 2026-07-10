---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# GPT-5.6 in Codex - cheatsheet

> [[README|시리즈 처음]]

## 이름 정리

| 말 | 정확한 의미 |
|----|-------------|
| Codex 5.6 | 비공식/사용자식 표현 |
| GPT-5.6 | 공식 model family |
| GPT-5.6 in Codex | GPT-5.6이 Codex surface에 통합된 것 |

## Model tier

| 모델 | 용도 |
|------|------|
| `gpt-5.6-sol` | flagship, 어려운 coding/research |
| `gpt-5.6-terra` | cost/performance balance |
| `gpt-5.6-luna` | high-volume/low-cost |
| `gpt-5.6` | dossier 기준 Sol alias |

## Reasoning effort

| effort | 빠른 기준 |
|--------|-----------|
| `none` | 단순 추출/변환 |
| `low` | 빠른 일반 작업 |
| `medium` | 기본 시작점 |
| `high` | 복잡한 설계/디버깅/review |
| `xhigh` | 난제 분석 |
| `max` | 품질 우선, 비용 허용 |

## Codex surface

| Surface | 쓰임 |
|---------|------|
| ChatGPT desktop/web | 대화형 work/coding |
| Codex CLI | local repo 작업 |
| IDE extension | editor 안의 수정/review |
| Codex cloud | isolated cloud env, 병렬 task, PR workflow |

## `max` vs `ultra`

| 기능 | 한 줄 |
|------|-------|
| `max` | 한 task에 더 깊은 reasoning effort |
| `ultra` | Codex에서 여러 agent를 병렬 조율 |

## 시작 실험

```text
1. terra + medium으로 baseline 측정
2. terra + low로 비용/속도 개선 확인
3. sol + medium으로 품질 차이 확인
4. sol + high로 어려운 task 확인
5. sol + max는 release-critical task에만 사용
```

## Codex CLI

```bash
codex
```

```text
첫 요청 예시:
이 repo의 test/lint 명령을 파악하고, AGENTS.md 초안을 작성한 뒤,
작은 문서 수정 하나를 수행하고 검증 결과를 보고해줘.
```

## Codex cloud workflow

```text
GitHub 연결
  -> environment 생성
  -> dependencies/secrets 설정
  -> task 실행
  -> diff review
  -> PR 생성
```

## Programmatic Tool Calling

```javascript
const docs = await tools.search({ query: "GPT-5.6 Codex Programmatic Tool Calling" });
const official = docs.filter((doc) =>
  doc.url.includes("openai.com") || doc.url.includes("developers.openai.com")
);
return official.slice(0, 5);
```

## 도입 체크리스트

- [ ] "Codex 5.6"이라는 이름을 공식 제품명으로 쓰지 않는다.
- [ ] tier와 effort를 따로 실험한다.
- [ ] `AGENTS.md`에 test/lint/approval convention을 적는다.
- [ ] Codex cloud task는 PR과 CI로 닫는다.
- [ ] `max/ultra`는 비용과 review 부담을 고려해 제한적으로 쓴다.
- [ ] security/cyber task는 defensive workflow와 access boundary를 둔다.

## 링크

- [[README|시리즈 처음]]
- [[01-overview|개요]]
- [[02-ecosystem|생태계]]
- [[04-learning/01-getting-started|시작하기]]
- [[04-learning/02-deep-dive|심화]]
- [[05-projects|프로젝트]]
- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/model-context-protocol-mcp]]
