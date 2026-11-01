---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# ego(lite) Ecosystem

[[tech/scraping/egolite-agent-browser/README|README]] · [[tech/scraping/egolite-agent-browser/01-overview|Overview]]

## 비교

| 도구 | 중심 모델 | 강점 | ego(lite)보다 적합한 경우 |
|---|---|---|---|
| ego(lite) | Local full Chromium + shared authenticated state | 실제 로그인 상태, 병렬 Space, human takeover, audit 탭 | workstation의 logged-in workflow |
| Playwright | Code-first browser automation | 성숙한 test ecosystem, CI, deterministic E2E | 앱 테스트와 CI 중심 automation |
| Browser Use | LLM agent loop | agent reasoning과 browser control의 결합, 오픈 생태계 | 범용 agent workflow를 직접 조합할 때 |
| Browserbase | Hosted browser infrastructure | remote execution, managed concurrency, observability | cloud scale·운영형 browser workload |
| OpenAI/Codex 내장 browser | product-scoped agent browser | 설치 부담이 작고 Codex 흐름에 통합 | 기존 profile·extension과 분리된 작업 |

## 선택 기준

핵심 경계는 **local authenticated session**이 필요한지, **CI/cloud scale**이 필요한지다. Browserbase는 hosted capacity와 운영성을, ego(lite)는 로컬 browser state·가시성·즉시 takeover를 우선한다. 동일 account에서 write 작업을 여러 Space로 병렬화하면 충돌할 수 있으므로 write는 직렬화한다.

## 플랫폼과 성숙도

공개 repository는 MIT 라이선스의 `ego-browser` SDK/Skill을 제공한다. 반면 수정 Chromium과 native binding을 포함하는 desktop app은 closed-source다. README는 macOS·Windows 지원과 Linux roadmap을 명시하며, 2026-10 changelog에는 Chromium 156 및 Windows installer/import 개선이 기록되어 있다.

## Sources

- https://www.egolite.app/compare/ego-lite-vs-browserbase
- https://www.egolite.app/article/browser-use-vs-browserbase
- https://github.com/citrolabs/ego-lite/blob/main/README.md
- https://www.egolite.app/changelog

