---
date: 2026-06-25
tags:
  - tech
  - ai
  - agentic-browser
  - aside
type: tech-tool-study
status: learning
---

# Aside

> **한 줄 정의**: Aside는 "브라우저 자체"를 AI agent 실행환경으로 삼아, 로그인된 웹사이트, 파일, 브라우징 히스토리 위에서 장시간 업무를 수행하는 macOS용 agentic AI browser다.

## 개요

Aside는 API integration이나 별도 connector가 없어도 agent가 사용자의 실제 browser state 위에서 업무를 수행하도록 설계된 AI browser다. Gmail, CRM, payroll, dashboard, docs, spreadsheets처럼 일이 이미 웹 탭 안에서 일어나는 환경을 전제로 한다.

핵심은 세 가지다.

- **Browser-native agent**: 웹사이트, 로그인 세션, 히스토리, 파일, saved credentials를 설정에 따라 활용한다.
- **Permissioned task runtime**: task마다 mode, permission, working folder, model을 두고 browsing, file step, approval, wait/resume을 수행한다.
- **Local-first work context**: memory, privacy setting, password autofill boundary, CLI/MCP/REPL을 묶어 개인 업무 자동화와 개발자 테스트에 연결한다.

---

## 학습 경로

### 1단계: 정체와 문제의식

- [ ] [[01-overview|개요]] - Aside가 agentic browser로 해결하려는 문제
- [ ] [[02-ecosystem|생태계 비교]] - ChatGPT Atlas, Perplexity Comet, Dia, Browser Use와의 차이

### 2단계: 공식 자료 확인

- [ ] [[03-references|참고자료]] - 공식 사이트, Help Center, changelog, benchmark repo, YC profile

### 3단계: 실습

- [ ] [[04-learning/01-getting-started|시작하기]] - 설치, import, 첫 task 작성, permission mode 선택
- [ ] [[04-learning/02-deep-dive|심화]] - password policy, memory/privacy, CLI/MCP/REPL, routines, Ultrabrowse

### 4단계: 적용

- [ ] [[05-projects|프로젝트]] - QA smoke test, vendor research, back-office automation, recurring ops
- [ ] [[cheatsheet|치트시트]] - task prompt, mode, command 빠른 참조

---

## 파일 구조

```text
https-aside-com/
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

## 관련 노트

- [[../ai-ecosystem/01-overview|AI ecosystem]] - AI browser와 agent platform의 큰 흐름
- [[../model-context-protocol-mcp/README|Model Context Protocol]] - Aside MCP server와 developer integration 맥락
- [[../agent-orchestration/cli-agents|CLI agents]] - `aside` CLI를 agent workflow에 붙이는 관점

## Sources

- [Aside official](https://aside.com/)
- [Aside Help Center](https://docs.aside.com/)
- [YC profile: Aside](https://www.ycombinator.com/companies/aside)
