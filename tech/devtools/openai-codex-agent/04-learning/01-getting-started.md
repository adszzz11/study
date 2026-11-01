---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex 시작하기

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]의 안전한 첫 실습이다. 설치 세부 사항과 최신 인증 방식은 [CLI 문서](https://learn.chatgpt.com/docs/codex/cli)를 우선한다.

## 1. 작은 Git repository 준비

처음에는 test가 빠르고 민감한 secret·production 설정이 없는 repository를 택한다. working tree를 깨끗하게 만들고, agent가 변경해도 되돌릴 Git checkpoint를 남긴다.

```bash
git status
codex
```

## 2. read-only 질문으로 시작

첫 요청은 구현이 아니라 repository 이해를 검증한다.

```text
이 project의 구조, 실행 가능한 test command, 그리고 주요 module 경계를 설명해줘.
파일을 수정하거나 network 요청을 실행하지 마.
```

답변에서 실제 file path와 command가 repository와 맞는지 확인한다. 이 단계는 prompt가 충분한 context를 주는지와 approval 경계를 점검하는 작은 probe다.

## 3. `AGENTS.md`로 작업 계약 작성

repository 가까이에 build/test/lint 명령, architecture rule, 금지 디렉터리, required verification을 적는다. rule은 짧고 검증 가능해야 한다.

```md
# AGENTS.md
- Run: `npm test` and `npm run lint` after TypeScript changes.
- Do not modify generated files under `dist/`.
- Ask for approval before network access or dependency changes.
```

## 4. 작은 bug fix와 검증

명확한 reproduction을 주고 최소 patch를 요청한다. diff와 실행한 command를 검토하고, 중요한 test는 사용자가 별도로 재실행한다.

```text
`parseDate`가 invalid month를 허용한다. 최소 수정으로 고치고,
관련 unit test를 추가해. 변경 전후 test command와 결과를 보고해줘.
```

## 5. headless task 실험

반복 task는 `codex exec` 후보가 될 수 있다. 처음에는 lint 또는 test failure 요약처럼 write가 없는 task로 scope를 제한한다.

```bash
codex exec "Run the test suite and summarize failures; do not modify files."
```

다음으로 [[tech/devtools/openai-codex-agent/04-learning/02-deep-dive|Deep Dive]]에서 permission과 SDK를 다룬다.

## Sources

- https://learn.chatgpt.com/docs/codex/cli
- https://github.com/openai/codex
- https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
