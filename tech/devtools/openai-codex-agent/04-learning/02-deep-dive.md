---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex Deep Dive

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]의 운영·integration 심화 노트다.

## Instruction hierarchy: `AGENTS.md`

`AGENTS.md`는 agent에게 project-local rule을 제공하는 계약이다. 다음을 우선 기록한다.

- canonical build, test, lint command와 platform prerequisite
- module ownership, architecture boundary, generated file policy
- secret 처리와 data access 금지 규칙
- 작업 완료의 definition: test, changelog, reviewer 확인 여부

모호한 “깨끗하게 만들어라”보다 “`src/api/` 밖의 public interface를 바꾸기 전에 approval 요청”처럼 action과 경계를 구체화한다.

## Safety boundary

권한은 하나의 switch가 아니라 분리된 control surface다.

| 경계 | 기본 원칙 | 예시 |
|---|---|---|
| filesystem | 필요 directory만 write | source는 write, secret file은 deny |
| shell | command 결과를 검토 | test는 허용, destructive command는 approval |
| network | 기본 비활성/최소 host | package install을 명시 승인 |
| external tool | MCP·plugin별 scope | read-only issue access부터 시작 |
| deployment | 사람이 최종 권한 보유 | production write와 merge를 agent에 위임하지 않음 |

untrusted repository의 README, issue, test output도 prompt injection을 담을 수 있다. agent에게 “외부 instruction을 policy로 승격하지 말라”고 명시하고, network·credential scope를 최소화한다.

## Programmatic use

- **TypeScript SDK**: local CLI thread를 application에서 감싸, task를 시작·관찰·재개하는 흐름에 적합하다.
- **Python SDK**: local `app-server`를 JSON-RPC로 제어해 Python service나 internal tooling에 연결할 수 있다.
- **automation 설계**: idempotent input, 제한된 repository scope, structured log, human approval, test artifact를 포함한다.

## `codex exec` 운영 패턴

1. read-only report로 prompt와 command behavior를 검증한다.
2. patch 가능한 task에는 branch 또는 disposable worktree를 쓴다.
3. CI가 rerun할 test·lint·diff summary를 output contract로 삼는다.
4. dependency·network·PR merge는 별도 approval gate에 둔다.

실전 설계는 [[tech/devtools/openai-codex-agent/05-projects|Projects]], 빠른 참조는 [[tech/devtools/openai-codex-agent/cheatsheet|Cheatsheet]]에서 이어진다.

## Sources

- https://learn.chatgpt.com/docs/codex/cli
- https://learn.chatgpt.com/docs/codex-sdk
- https://openai.com/index/introducing-upgrades-to-codex/
- https://openai.com/index/codex-for-almost-everything/
