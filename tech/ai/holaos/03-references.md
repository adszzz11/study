---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# holaOS References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: Getting Started]]

## Research Baseline

- 조사 기준일: **2026-08-17**
- 대상: [`holaboss-ai/holaOS`](https://github.com/holaboss-ai/holaOS)
- 상태: 빠르게 변하는 초기 OSS project
- 원칙: blog나 2차 요약보다 공식 docs, repository, manifest, license를 우선한다.

## Sources

### Official Documentation

| 자료 | URL | 읽을 포인트 |
|---|---|---|
| Getting Started | https://www.holaos.ai/docs/getting-started | 제품 정의와 전체 entry point |
| Quick Start | https://www.holaos.ai/docs/getting-started/quick-start | signed Desktop, 지원 platform, 최초 실행 |
| Concepts | https://www.holaos.ai/docs/concepts/concepts | Environment Engineering의 문제 정의 |
| Workspace Model | https://www.holaos.ai/docs/concepts/workspace-model | authored contract와 runtime-managed state |
| Memory and Continuity | https://www.holaos.ai/docs/concepts/memory-and-continuity | state 계층, recall, memory proposal |
| Runtime Tools | https://www.holaos.ai/docs/concepts/agent-harness/runtime-tools | browser/runtime/MCP tool projection과 allowlist |
| Run Compilation | https://www.holaos.ai/docs/contribute/runtime/run-compilation | reduced execution package 생성 과정 |
| App Anatomy | https://www.holaos.ai/docs/build/apps/app-anatomy | manifest, lifecycle, MCP, health, integration grant |

### Repository Sources

| 자료 | URL | 확인할 것 |
|---|---|---|
| Repository | https://github.com/holaboss-ai/holaOS | release activity, source tree, issue와 변경 속도 |
| INSTALL.md | https://github.com/holaboss-ai/holaOS/blob/main/INSTALL.md | macOS, Linux, WSL, Windows build path의 최신 절차 |
| LICENSE | https://github.com/holaboss-ai/holaOS/blob/main/LICENSE | Modified Apache 2.0의 추가 상용 제한 원문 |
| Package manifests | https://github.com/holaboss-ai/holaOS | repository에서 Desktop package 위치와 version을 재확인 |

> [!warning] Manifest path
> monorepo 구조가 바뀔 수 있으므로 repository search로 실제 Desktop package와 version을 다시 찾는다.

## Recommended Reading Order

1. **Getting Started + Concepts** — 제품 정의와 Environment Engineering 문제를 이해한다.
2. **Workspace Model** — `workspace.yaml`, `AGENTS.md`, Skills, Apps의 책임을 구분한다.
3. **Run Compilation** — authored environment가 run context로 축소되는 과정을 본다.
4. **Memory and Continuity** — execution truth, resume state, durable knowledge를 나눈다.
5. **Runtime Tools** — MCP discovery, allowlist, capability exposure를 확인한다.
6. **App Anatomy** — lifecycle, health check, integration grant와 credential boundary를 읽는다.
7. **INSTALL.md + LICENSE** — 기술 적합성 뒤에 platform과 배포 조건을 검토한다.

## Verification Questions

도입 직전에는 문서만 읽지 말고 repository와 실행 환경에서 아래 질문을 확인한다.

- [ ] 최신 Desktop version과 release date는?
- [ ] signed binary가 target OS/architecture를 지원하는가?
- [ ] source install의 system dependency와 rollback 방법은?
- [ ] 현재 실제로 선택 가능한 harness는 무엇인가?
- [ ] provider별 model/reasoning option이 UI와 Runtime에서 일치하는가?
- [ ] empty MCP allowlist의 실제 semantics는?
- [ ] approval이 필요한 tool category와 우회 가능한 path는?
- [ ] memory proposal의 승인, 삭제, export 방법은?
- [ ] App이 받는 signed grant의 scope, expiry, audit log는?
- [ ] license가 예정된 배포/상용 모델을 허용하는가?

## Evidence Quality

| 주장 유형 | 현재 근거 | 신뢰 시 주의점 |
|---|---|---|
| Architecture와 기능 | 프로젝트 공식 문서 | 설계 문서와 현재 구현 사이 차이 가능 |
| Platform 지원 | Quick Start, INSTALL.md | 설치 가능과 polished UX는 다름 |
| Harness 교체 가능성 | boundary 설계와 OSS runtime | boundary 존재가 여러 harness 구현 완료를 의미하지 않음 |
| 보안·approval | 공식 architecture 설명 | custom App/MCP 구현 품질에 따라 달라짐 |
| 성능·안정성 | 공개 객관 자료 부족 | 직접 pilot와 failure test 필요 |
| License | repository LICENSE | 실제 상용 시나리오는 법률 검토 필요 |

## Source Notes

- 공식 문서의 설명은 project intent와 architecture를 이해하는 1차 자료다.
- 객관적 agent benchmark, 독립 security audit, 장기 production 사례는 dossier 기준 충분하지 않다.
- version, provider, platform, harness 목록은 변동성이 높으므로 이 vault의 숫자를 설치 근거로 고정하지 않는다.
