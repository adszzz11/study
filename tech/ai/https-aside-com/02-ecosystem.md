---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - ecosystem
type: tech-tool-study
parent: "[[README]]"
---

# Aside - 생태계 비교

> [[01-overview|이전: 개요]] | [[README|목차로 돌아가기]] | [[03-references|다음: 참고자료]]

---

## 1. 포지셔닝

Aside는 **local-first agentic browser**에 가깝다. 검색 assistant나 일반 browser에 AI sidebar를 붙인 제품보다, "로그인된 웹 업무를 agent가 직접 수행한다"는 점에 초점이 있다.

```text
AI browser spectrum

Search assistant browser
  -> work-context browser
  -> browser-native agent runtime
  -> developer browser automation infra
```

---

## 2. 경쟁/대안 비교

| 제품 | 포지션 | 강점 | 제약/차이 |
|---|---|---|---|
| **Aside** | Local-first agentic browser | 로그인된 웹, 파일, credential, memory, permission을 통합. CLI/MCP/REPL 제공 | 현재 문서 기준 macOS 15.0+ 중심. 벤치마크는 자체 공개 repo 기반이라 재현성 확인 필요 |
| **ChatGPT Atlas** | ChatGPT built-in browser | ChatGPT memory, sidebar, agent mode, macOS 출시 | Agent mode는 Plus/Pro/Business preview. 출시 당시 Windows/iOS/Android는 예정 |
| **Perplexity Comet** | Search-first AI browser | Perplexity search와 assistant 중심. Mac/Windows/iOS/Android 제공 | 검색과 개인 assistant 성격이 강함 |
| **Dia** | Work-context AI browser | GSuite, Slack, tabs, reports, meeting/workflow context | macOS 14+ Apple silicon 중심. 업무 productivity browser 성격 |
| **Browser Use** | Browser automation infra / library | Open-source + cloud. Python/Rust core, headless/stealth/proxy/skill API | 사용자용 브라우저보다 developer automation platform에 가까움 |

---

## 3. 선택 기준

| 질문 | Aside가 유리한 경우 | 다른 선택지가 유리한 경우 |
|------|--------------------|---------------------------|
| 로그인된 웹 업무를 직접 처리해야 하는가? | Payroll, CRM, vendor portal, dashboard처럼 UI workflow가 핵심 | API가 안정적이고 backend automation으로 충분 |
| 사용자가 실제로 쓰는 browser state가 중요한가? | Cookie, history, files, saved credentials가 task context | 검색 중심 research나 public web 탐색 |
| 권한/승인 경계가 필요한가? | `Read only`/`Guard`/`Full access`, Ask/Deny rule이 중요 | 단순 script automation |
| 개발자 자동화가 필요한가? | `aside` CLI, MCP server, REPL로 smoke test와 browser automation 연결 | Headless browser infra, Playwright, Browser Use가 더 적합 |
| 플랫폼 범위가 중요한가? | macOS 중심 사용 | Windows/mobile까지 당장 필요 |

---

## 4. Aside vs Browser Use

Aside와 Browser Use는 모두 browser automation과 agent를 다루지만, 출발점이 다르다.

| 항목 | Aside | Browser Use |
|------|-------|-------------|
| 주 사용자 | 지식노동자, operator, developer | developer, automation team |
| 실행 환경 | 사용자용 browser | library/cloud/headless infra |
| 인증/세션 | 사용자의 browser session과 password manager 중심 | automation profile, proxy, stealth, API 중심 |
| 권한 UX | session mode, approval, local file root | code/API policy와 infra config |
| 적합 작업 | 로그인된 웹 업무, local artifact, 반복 ops | 대량 browser automation, scraping-like workflow, test infra |

---

## 5. Aside vs Atlas/Comet/Dia

| 제품군 | 중심 질문 |
|--------|-----------|
| Aside | "agent가 내 browser에서 실제 업무를 끝낼 수 있는가?" |
| ChatGPT Atlas | "ChatGPT를 browser context 안에서 자연스럽게 쓸 수 있는가?" |
| Perplexity Comet | "검색과 답변을 browser workflow의 중심에 둘 수 있는가?" |
| Dia | "업무 context와 tabs를 이해하는 productivity browser가 될 수 있는가?" |

Aside의 차별점은 password manager boundary, permission model, task runtime, routine, developer interface를 한 제품 안에서 엮는다는 점이다.

---

## 관련 노트

- [[../agent-orchestration/README|Agent orchestration]] - 여러 agent runtime을 운영하는 관점
- [[../model-context-protocol-mcp/README|Model Context Protocol]] - MCP server를 통한 도구 연결
- [[../../scraping/playwright/README|Playwright]] - browser automation infra 비교 축

## References

- [Aside](https://aside.com/)
- [ChatGPT Atlas](https://openai.com/index/introducing-chatgpt-atlas/)
- [Perplexity Comet](https://www.perplexity.ai/comet)
- [Dia](https://www.diabrowser.com/)
- [Browser Use](https://browser-use.com/)
- [GitHub: browser-use/browser-use](https://github.com/browser-use/browser-use)
