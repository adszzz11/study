---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex Cheatsheet

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]의 빠른 참조다. exact option·default behavior는 실행 전 [CLI 문서](https://learn.chatgpt.com/docs/codex/cli)에서 확인한다.

## 기본 흐름

```bash
git status
codex
codex exec "Run tests and summarize failures; do not modify files."
git diff
```

## 좋은 첫 prompt

```text
이 repository의 구조와 test command를 설명해줘.
파일 수정, network 요청, dependency 변경은 하지 마.
각 결론에 근거 file path를 포함해줘.
```

## 변경 요청 template

```text
목표: <bug/feature>
범위: <허용 파일·module>
제약: <금지 변경·network/dependency policy>
검증: <test/lint command>
완료 보고: 변경 파일, 이유, 실행 명령, 남은 위험
```

## `AGENTS.md` 최소 항목

- build/test/lint command
- architecture boundary와 generated file policy
- secret·network·dependency approval rule
- required verification와 diff review rule

## 운영 체크리스트

- [ ] untrusted codebase에는 최소 filesystem 권한과 network 비활성화를 적용했는가?
- [ ] `AGENTS.md`가 실행 가능한 command와 금지 영역을 명시하는가?
- [ ] agent 변경 후 `git diff`와 test output을 사람이 검토했는가?
- [ ] MCP/plugin마다 read/write scope와 credential을 분리했는가?
- [ ] CI automation에 approval gate와 재현 가능한 artifact가 있는가?

더 넓은 비교는 [[tech/devtools/openai-codex-agent/02-ecosystem|Ecosystem]], 실습은 [[tech/devtools/openai-codex-agent/04-learning/01-getting-started|시작하기]]에서 확인한다.

## Sources

- https://learn.chatgpt.com/docs/codex/cli
- https://github.com/openai/codex
- https://openai.com/index/introducing-upgrades-to-codex/
