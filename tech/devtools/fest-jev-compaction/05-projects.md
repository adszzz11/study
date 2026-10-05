---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# fast-jev-compaction: Projects

## 1. Debugging agent

오래된 build/test output은 줄이되, 현재 failing test의 stack trace·관련 source read·실행 command는 남긴다.

- fixture: 반복 CI failure가 있는 debugging transcript
- 비교: native summary vs extractive pruning
- 성공: task completion과 rerun 수가 baseline보다 나빠지지 않음

## 2. CI triage assistant

반복 lint/test output을 call 단위로 정리하고 최종 failure evidence와 관련 command만 보존한다.

- 같은 job의 이전 성공 log는 drop 후보로 둔다.
- result 앞부분 truncate가 failure summary를 잘라내지 않는지 확인한다.
- raw log artifact의 위치를 별도로 유지한다.

## 3. IDE / agent harness library

`JevAsker` transport를 자체 gateway에 연결하고 tenant별 redaction·audit log·fallback policy를 둔다.

- API 호출 전 secret scanner/redaction을 적용한다.
- malformed response는 fail-open이 아니라 안전한 native fallback으로 처리한다.
- tenant 경계를 넘는 transcript 보관을 금지한다.

## 4. Benchmark harness

동일한 SWE-bench 또는 내부 bug-fix trajectory를 native summary, fresh context, extractive pruning으로 비교한다.

```text
trajectory fixture → strategy별 replay → task 결과 / token / latency / rerun 기록
```

원본 session과 strategy별 산출물을 분리 보관하고, private output은 측정 전에 redaction한다.
