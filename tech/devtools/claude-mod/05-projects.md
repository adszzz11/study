---
date: 2026-10-04
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Mod Projects

## 1. PII/secret redaction gateway

prompt attachment와 tool result에서 API key·PII pattern을 탐지해 model context에 전달되기 전에 mask한다.

- 입력/출력 event의 정확한 timing을 먼저 확인한다.
- 원문을 audit log에 다시 저장하지 않는다.
- pattern matching의 false negative와 high-risk format을 별도 test fixture로 둔다.

## 2. Engineering policy gate

production branch의 destructive command, `.env` 편집, 검증 없는 deploy를 tool-call 단계에서 정책화하고 approval UI를 제공한다.

- 초기는 observe-only audit와 narrow allowlist로 시작한다.
- block 이유, 승인자, command hash를 남기되 secret argument는 redaction한다.
- emergency bypass와 incident rollback을 운영 절차에 포함한다.

## 3. Context observability panel

terminal/Desktop panel에 context/token usage, MCP 비용, active subagent, retry rate를 표시한다.

- `session.start`, `turn.complete`, `ui.render`와 `$.state`를 연결한다.
- hot reload 후에도 history를 보존한다.
- 비용 데이터가 없을 때는 추정값처럼 보이지 않게 unavailable로 표시한다.

## 4. Team workflow Mod

release command에 PR/issue ID가 없으면 진행을 막고, accepted action은 internal audit endpoint에 기록한다.

- network failure가 release를 무조건 막는지, queueing할지 명시한다.
- endpoint authentication과 event payload의 data minimization을 검토한다.
- 조직 managed policy와 ordering 충돌을 integration test한다.

## 5. Custom `/diff` replacement

domain risk, migration 영향, security-sensitive file 변경을 강조하는 review UI를 만든다.

- built-in `diff` source를 읽고 pane lifecycle을 학습한다.
- severity는 설명 가능한 rule로 산출하고, raw diff로 되돌아갈 escape hatch를 둔다.

## 공통 Definition of Done

- `claude plugin validate`와 `claude plugin test`가 통과한다.
- malicious/invalid input, network failure, hot reload, ordering을 test한다.
- source/dependency/network review와 secret data-flow review가 기록돼 있다.
- UI가 없는 환경에서도 core policy의 동작과 오류 메시지가 이해 가능하다.

## Sources

- https://claude.com/blog/claude-code-mods
- https://github.com/anthropics/claude-code/tree/main/mods
- https://claude.dev/blog/getting-started-with-claude-code-mods/
