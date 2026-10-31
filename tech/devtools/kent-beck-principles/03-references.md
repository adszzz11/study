---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Kent Beck의 지론들 - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 1. 1차 자료와 공식 채널

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Kent Beck 공식 사이트 | https://kentbeck.com/ | Beck의 현재 작업, 책, 글, 강연入口 |
| Software Design: Tidy First? newsletter | https://newsletter.kentbeck.com/ | Tidy First?, Canon TDD, software design essays |
| Canon TDD by Kent Beck | https://newsletter.kentbeck.com/p/canon-tdd | TDD를 한 번에 하나의 runnable test workflow로 이해 |
| Agile Manifesto | https://agilemanifesto.org/ | Beck이 signatory인 agile values와 principles |
| Still Burning podcast | https://stillburningpodcast.com/ | 2026 AI/engineering conversations 맥락 |

---

## 2. 책과 긴 글

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| `Tidy First?` O'Reilly | https://www.oreilly.com/library/view/tidy-first/9781098151232/ | behavioral change와 structural change 분리, optionality |
| Extreme Programming overview | https://en.wikipedia.org/wiki/Extreme_programming | XP values, practices, historical context |
| Spike software development overview | https://en.wikipedia.org/wiki/Spike_%28software_development%29 | spike의 목적, prototype과 production code의 차이 |

### 읽을 때 잡을 질문

- `Tidy First?`는 "깨끗한 코드"보다 "언제 정리하는가"를 어떻게 다루는가?
- `Canon TDD`는 TDD에 대한 흔한 오해를 어떻게 줄이는가?
- `Spike`는 estimate, design decision, risk reduction 중 무엇을 산출물로 삼는가?
- XP values는 process ceremony 없이도 팀을 어떻게 조율하는가?

---

## 3. AI Coding 시대의 Beck

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Business Insider, 2025 Kent Beck on AI agents/genies | https://www.businessinsider.com/agile-manifesto-author-kent-beck-ai-coding-agents-2025-6 | AI agent를 genie/augmented coding 대상으로 보는 관점 |
| Still Burning podcast | https://stillburningpodcast.com/ | 2026 AI coding과 engineering judgment 대화 |

2025-2026 맥락에서는 AI coding agents 때문에 Beck의 지론이 다시 중요해졌다. AI가 코드를 더 많이 만들수록 필요한 능력은 문법 암기보다 `vision`, `milestone`, `task breakdown`, `feedback loop`, `design judgment`, `review`, `refactoring rhythm` 쪽으로 이동한다.

---

## 4. 학습 순서

1. **Agile Manifesto**: values와 principles를 먼저 읽는다.
2. **XP overview**: XP values와 engineering practices를 확인한다.
3. **Canon TDD**: TDD를 test-first dogma가 아니라 workflow로 이해한다.
4. **Spike overview**: timebox, prototype, decision log의 차이를 본다.
5. **Tidy First?**: behavior change와 structural change 분리 원칙을 익힌다.
6. **AI articles/podcast**: augmented coding에서 인간의 judgment가 왜 더 중요해지는지 정리한다.

---

## 5. 발췌 메모 Template

```markdown
## Source
- Title:
- URL:
- Date:

## 핵심 주장
- 

## 실무 적용
- Ticket:
- PR:
- Test:
- Review:

## 내 작업에 연결
- [[study/tech/ai/lazy-codex]]:
- [[study/tech/ai/agent-orchestration/cli-agents]]:
```

---

## 관련 노트

- [[study/tech/ai/lazy-codex]] - AI coding agent 결과를 어떻게 검증 완료 상태로 만들지 연결
- [[study/tech/ai/mitchellh-ai-adoption-study]] - AI adoption에서 개발자 업무의 재구성 비교
- [[study/tech/ai/model-context-protocol-mcp]] - 새 protocol 학습에 spike template 적용 가능
