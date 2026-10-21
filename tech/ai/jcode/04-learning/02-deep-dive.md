---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 심화

> [[../README|목차로 돌아가기]] | [[../05-projects|다음: 프로젝트]]

## Swarm Design

swarm은 속도만의 기능이 아니라 coordination 설계 문제다. coordinator는 task를 조사, 구현, test로 분해하고 각 agent에 module/file ownership과 완료 기준을 부여한다. DM/broadcast는 decision과 blocker 공유에 쓰고, sub-swarm은 독립적인 하위 문제에만 만든다.

```text
coordinator
├─ reproduce agent: failure 재현·로그
├─ analysis agent: root cause·영향 범위
├─ patch agent: 소유 module 수정
└─ test agent: regression·integration test
```

## Memory and Background Tasks

semantic memory는 embedding으로 과거 turn을 retrieval해 긴 작업의 문맥을 돕는다. 그러나 오래된 memory가 현재 code 상태를 보장하지는 않는다. retrieval 결과와 `auto-poke`가 제안하는 unfinished todo는 최신 `git diff`, source, test 결과로 다시 확인한다.

background task는 build/test처럼 오래 걸리는 process를 추적한다. task 종료·exit code·로그 위치·재시도 조건을 명시하고, 완료 선언은 test 결과를 확인한 coordinator가 한다.

## MCP and Skills

- `.jcode/mcp.json`에는 project-local, 최소 권한 MCP만 둔다.
- global 설정은 개인 편의용으로 제한하고 repository 재현성에 필요한 설정은 문서화한다.
- `SKILL.md`와 Claude Code 설정 import는 내용을 신뢰·검토한 뒤 사용한다.
- HTTP/SSE remote MCP는 endpoint 신뢰성, authentication, data egress, tool allowlist를 별도 검토한다.

## SDK Security Boundary

TypeScript SDK의 `launch()`는 private daemon instance를 만들고 `connect()`는 실행 중인 Jcode에 연결한다. 이것은 CI, dashboard, editor integration에 유용하지만 sandbox가 아니다. SDK tool은 사용자 권한으로 file·shell을 사용할 수 있다.

```ts
// 개념 예시: production에서는 approval·timeout·audit을 추가한다.
const instance = await launch({ autoApprove: false });
// approval request를 정책과 human review로 처리한다.
```

untrusted repository/code/prompt는 container 또는 VM에서 실행한다. CI에서 `autoApprove`를 무분별하게 켜지 말고 write, network, deploy 같은 action에는 명시적 approval과 audit log를 둔다.

## Sources

- https://jcode.sh/docs
- https://jcode.sh/docs/commands
- https://jcode.sh/sdk
- https://github.com/1jehuang/jcode
