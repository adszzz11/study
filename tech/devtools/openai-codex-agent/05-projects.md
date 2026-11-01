---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex Projects

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]를 적용할 수 있는 작고 검증 가능한 프로젝트들이다.

## CI failure triage bot

실패한 test log를 입력으로 받아 원인 후보, 재현 절차, 최소 patch 제안, 검증 command를 반환한다.

- input: CI log, commit SHA, 허용된 repository path
- output: evidence가 인용된 failure summary와 read-only 재현 명령
- guardrail: production credential·network write 없음, patch는 branch에서만 생성

## Legacy modernization

deprecated API 또는 dependency migration을 repository 전체에서 탐색하고 단계별 patch와 regression test를 만든다.

1. occurrences와 public API 영향을 inventory한다.
2. 작은 migration slice마다 test를 실행한다.
3. diff review 뒤 다음 slice로 진행한다.

## PR review automation

diff, 관련 test, `AGENTS.md`의 architecture rule을 읽고 bug·security·regression 가능성을 검토한다. 결과에는 심각도보다 **file/line evidence와 재현 조건**을 우선 포함해 reviewer가 판단할 수 있게 한다.

## Frontend visual loop

screenshot 또는 design spec을 입력으로 구현하고 browser에서 결과를 확인하며 반복한다. visual test 기준, allowed asset source, accessibility check를 task contract에 넣는다.

## Internal developer workflow

TypeScript/Python SDK로 issue 분류, code health 점검, 문서 동기화 같은 제한된 automation을 구축한다. persistent thread를 쓰더라도 run마다 repository revision과 permission을 다시 확인한다.

## 완료 기준 예시

```text
Done when:
- requested test/lint command succeeds;
- changed files and rationale are summarized;
- no secret, dependency, network, or production write occurred without approval;
- a human can reproduce the result from the run artifact.
```

구현 전 권한 모델은 [[tech/devtools/openai-codex-agent/04-learning/02-deep-dive|Deep Dive]]를, source는 [[tech/devtools/openai-codex-agent/03-references|References]]를 확인한다.

## Sources

- https://learn.chatgpt.com/docs/codex-sdk
- https://learn.chatgpt.com/docs/codex/cli
- https://github.com/openai/codex
