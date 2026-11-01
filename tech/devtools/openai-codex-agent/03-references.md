---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenAI Codex References

[[tech/devtools/openai-codex-agent/README|OpenAI Codex 학습 노트]]의 공식 source 목록이다. 기능·release·제품 범위는 빠르게 변하므로 구현 전에 문서를 다시 확인한다.

| Source | 확인할 내용 |
|---|---|
| [openai/codex repository](https://github.com/openai/codex) | 공개 구현, license, 디렉터리 구조 |
| [CLI documentation](https://learn.chatgpt.com/docs/codex/cli) | install, interactive CLI, `codex exec` |
| [SDK documentation](https://learn.chatgpt.com/docs/codex-sdk) | TypeScript·Python programmatic use |
| [GitHub Releases](https://github.com/openai/codex/releases) | version별 변경 사항 |
| [Introducing upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/) | 2025 제품 확장과 safety 설명 |
| [Codex is now generally available](https://openai.com/index/codex-now-generally-available/) | GA 맥락 |
| [Codex for (almost) everything](https://openai.com/index/codex-for-almost-everything/) | 2026 computer use·browser·memory 방향 |
| [Codex Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) | task prompt 작성 방식 |

## 조사 체크리스트

- repository README와 release note를 함께 읽어 현재 CLI behavior를 확인한다.
- product announcement는 방향성 자료로 쓰고, exact command·권한 기본값은 CLI 문서로 검증한다.
- SDK 선택 전에는 local process, API surface, credential 및 deployment boundary를 확인한다.

실습 순서는 [[tech/devtools/openai-codex-agent/04-learning/01-getting-started|시작하기]]를, 적용 아이디어는 [[tech/devtools/openai-codex-agent/05-projects|Projects]]를 참조한다.

## Sources

- https://github.com/openai/codex
- https://learn.chatgpt.com/docs/codex/cli
- https://learn.chatgpt.com/docs/codex-sdk
- https://github.com/openai/codex/releases
