---
date: 2026-06-18
tags:
  - tech
  - devtools
  - kent-beck
  - xp
  - tdd
  - spike
status: learning
type: tech-tool-study
---

# Kent Beck의 지론들

> **한 줄 정의**: Kent Beck의 지론은 `short feedback loop`, `working software`, `human relationships`, `simple design`, `TDD`, `XP`, `spike`, `tidying`, `optionality`를 통해 불확실한 software work를 작게 배우고 안전하게 바꾸는 실천 체계다.

## 개요

Kent Beck은 `Extreme Programming(XP)`, `Test-Driven Development(TDD)`, `JUnit/xUnit`, `Agile Manifesto`, `Tidy First?`, `Augmented Coding` 논의로 이어지는 소프트웨어 엔지니어링 실천가다.

핵심 문제의식은 "소프트웨어 개발은 기술 문제가 아니라 사람, 피드백, 경제성, 불확실성 관리의 문제"라는 쪽에 가깝다. `spike`는 그중에서도 모르는 기술, 설계, 요구사항을 바로 production implementation으로 밀어붙이지 않고 짧은 `timebox` 안에서 가장 작은 실험으로 학습하는 방식이다.

---

## 학습 경로

### 1단계: 큰 그림 이해

- [ ] [[01-overview|개요]] 읽기 - XP, TDD, spike, Tidy First?, 3X의 공통 문제의식 파악
- [ ] `short feedback loop`와 `working software`가 왜 반복해서 등장하는지 정리
- [ ] 기술 지식보다 `judgment`, `communication`, `design option`이 중요한 이유 적기

### 2단계: 생태계 비교

- [ ] [[02-ecosystem|생태계]] 읽기 - XP, Scrum, Kanban, Lean Startup, AI coding agents 비교
- [ ] `spike ticket`과 일반 feature ticket의 차이 정리
- [ ] [[study/tech/ai/agent-orchestration/cli-agents]]와 연결해 AI agent 작업 단위 비교

### 3단계: 원문과 참고자료

- [ ] [[03-references|참고자료]]에서 Kent Beck 공식 사이트, newsletter, Canon TDD, Agile Manifesto 확인
- [ ] `Tidy First?`가 Clean Code류와 다른 지점을 메모
- [ ] 2025-2026 AI coding agents 맥락에서 Beck의 `augmented coding` 관점 정리

### 4단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - TDD kata, spike log, tidy commit 분리 실습
- [ ] [[04-learning/02-deep-dive|심화]] - 3X, optionality, AI-assisted spike 운영 방식 학습

### 5단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]] - spike log template, TDD refactor kata, Tidy First bot rule 만들기
- [ ] [[cheatsheet|치트시트]] - 팀 ticket, PR, AI coding agent 운영 시 빠르게 참조

---

## 파일 구조

```text
켄트백이-가지고-있는-지론들에-대해-공부하고싶어-spike라던가-이런-소/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | What/Why, 핵심 특징, 개념 지도 |
| 생태계 | [[02-ecosystem]] | XP, Scrum, Kanban, Lean Startup, AI agents 비교 |
| 참고자료 | [[03-references]] | 공식 사이트, newsletter, 책, article |
| 시작하기 | [[04-learning/01-getting-started]] | TDD kata, spike ticket, tidy commit 실습 |
| 심화 | [[04-learning/02-deep-dive]] | 3X, optionality, augmented coding, Thinkies |
| 프로젝트 | [[05-projects]] | 실무 적용 프로젝트와 template |
| 치트시트 | [[cheatsheet]] | 핵심 문장, 체크리스트, ticket/PR template |

---

## 관련 노트

- [[study/tech/ai/agent-orchestration/cli-agents]] - AI coding agent와 작은 task breakdown 연결
- [[study/tech/ai/lazy-codex]] - agent에게 일을 맡길 때 feedback loop와 verified completion 적용
- [[study/tech/ai/mitchellh-ai-adoption-study]] - AI adoption에서 인간의 judgment와 workflow 변화 비교
- [[study/tech/ai/model-context-protocol-mcp]] - agent tool integration을 실험할 때 spike 대상으로 삼기 좋음

---

**생성일**: 2026-06-18  
**상태**: 학습 중
