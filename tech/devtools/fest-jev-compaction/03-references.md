---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# fast-jev-compaction: References

## Upstream

1. [Repository — tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction)
2. [README — architecture, options, install, limitations](https://github.com/tamaratran/fast-jev-compaction/blob/main/README.md)
3. [TypeScript public API / source entry](https://github.com/tamaratran/fast-jev-compaction/blob/main/src/index.ts)
4. [Claude Code hook implementation](https://github.com/tamaratran/fast-jev-compaction/tree/main/hooks)
5. [Plugin manifest and marketplace metadata](https://github.com/tamaratran/fast-jev-compaction/tree/main/.claude-plugin)
6. [Tests](https://github.com/tamaratran/fast-jev-compaction/tree/main/tests)

## Platform guidance

7. [Claude Code environment variables](https://code.claude.com/docs/ko/env-vars)
8. [Anthropic long-horizon context / fresh-context guidance](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables)

## Community implementations

9. [pi-fast-jev-compaction](https://github.com/QuentinDanblon/pi-fast-jev-compaction)
10. [fast-dev-compaction — Codex PoC, experimental warning 확인](https://github.com/leonaaardob/fast-dev-compaction)

## 읽는 순서

`README`로 option과 limitation을 확인한 뒤, `src/index.ts`와 `tests`에서 실제 public API 및 pair-handling을 대조한다. hook은 Claude Code version/function-hook 조건을 확인할 때만 읽는다.
