---
date: 2026-06-25
tags:
  - tech
  - ai
  - aside
  - references
type: tech-tool-study
parent: "[[README]]"
---

# Aside - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 자료

| 자료 | URL | 볼 것 |
|------|-----|-------|
| Aside official | https://aside.com/ | 제품 포지셔닝, 핵심 메시지 |
| Aside Help Center | https://docs.aside.com/ | 전체 문서 진입점 |
| Get started | https://docs.aside.com/help/get-started | 설치, import, first task |
| Run tasks | https://docs.aside.com/help/tasks | task runtime, artifact, wait/resume |
| Permissions | https://docs.aside.com/help/security | session mode, sandbox, Allow/Ask/Deny |
| Password Manager | https://docs.aside.com/help/password-manager | agent-safe credential autofill |
| Memory | https://docs.aside.com/help/memory | local memory와 retention |
| Privacy | https://docs.aside.com/help/privacy | history, cookies, analytics, Safe Browsing |
| AI providers | https://docs.aside.com/help/ai | subscription/BYOK provider layer |
| Developers | https://docs.aside.com/help/developers | CLI, MCP server, REPL |
| Automation | https://docs.aside.com/help/automation | cron/heartbeat routine |
| Ultrabrowse | https://docs.aside.com/help/ultrabrowse | citation-heavy research mode |
| Changelog | https://docs.aside.com/changelog/components | 2026년 6월 기능 변화 |
| Benchmark repo | https://github.com/at-inc/aside-benchmarks | 자체 benchmark 재현성 확인 |
| YC profile | https://www.ycombinator.com/companies/aside | company positioning |

---

## 비교 대상

| 제품 | URL | 비교 포인트 |
|------|-----|-------------|
| ChatGPT Atlas | https://openai.com/index/introducing-chatgpt-atlas/ | ChatGPT built-in browser, agent mode |
| Perplexity Comet | https://www.perplexity.ai/comet | search-first AI browser |
| Dia | https://www.diabrowser.com/ | work-context AI browser |
| Browser Use | https://browser-use.com/ | browser automation infra |
| Browser Use GitHub | https://github.com/browser-use/browser-use | open-source implementation, developer API |

---

## 읽는 순서

1. `aside.com`에서 제품의 한 줄 포지션을 잡는다.
2. `Get started`와 `Run tasks`로 user workflow를 본다.
3. `Permissions`, `Password Manager`, `Privacy`를 이어서 읽고 trust boundary를 정리한다.
4. `Developers`, `Automation`, `Ultrabrowse`로 확장 기능을 본다.
5. `Changelog`에서 최신 변화와 문서 기준 시점을 확인한다.

```text
Product positioning
  -> task lifecycle
  -> permission/security
  -> developer automation
  -> ecosystem comparison
```

---

## 검증 메모

- Aside benchmark는 공개 repo가 있으나, 자체 benchmark라는 점을 기록하고 재현 조건을 별도로 확인해야 한다.
- Platform support는 문서 기준 macOS 15.0+ 중심으로 적는다.
- Password 관련 내용은 "agent가 raw password를 본다"가 아니라 "autofill payload boundary"로 이해해야 한다.

## 관련 노트

- [[../openrouter/README|OpenRouter]] - Aside provider layer의 BYOK/model routing 맥락
- [[../codex/03-references|Codex references]] - CLI agent 문서 정리 방식 참고
- [[../model-context-protocol-mcp/03-references|MCP references]] - developer integration 참고
