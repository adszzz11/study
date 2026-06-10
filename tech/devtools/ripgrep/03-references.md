---
date: 2026-06-10
tags:
  - tech
  - devtools
  - ripgrep
  - references
type: tech-tool-study
parent: "[[README]]"
---

# ripgrep - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

## 공식 자료

- [ripgrep GitHub README](https://github.com/BurntSushi/ripgrep)
- [ripgrep Releases](https://github.com/BurntSushi/ripgrep/releases)
- [ripgrep User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
- [ripgrep FAQ](https://github.com/BurntSushi/ripgrep/blob/master/FAQ.md)

## Rust crate 문서

- [Rust `regex` crate docs](https://docs.rs/regex/latest/regex/)
- [Rust `ignore` crate docs](https://docs.rs/ignore/latest/ignore/)
- [Rust `grep` crate docs](https://docs.rs/grep/latest/grep/)

## 비교 자료

- [Beyond Grep feature comparison](https://beyondgrep.com/feature-comparison/)
- [ugrep GitHub](https://github.com/Genivia/ugrep)

## AI/RAG 관련 논문

- [GrepRAG: Fast Retrieval-Augmented Generation by Grep, 2026](https://arxiv.org/abs/2601.23254)
- [Is Grep All You Need?, 2026](https://arxiv.org/abs/2605.15184)

## 릴리스 체크 포인트

| 항목 | 확인할 곳 | 메모 |
|---|---|---|
| 최신 버전 | GitHub Releases | 2025-10-22 기준 `15.1.0` |
| breaking/major changes | Release note | `15.0.0`은 major release |
| engine 옵션 | User Guide / FAQ | `-P`, `--auto-hybrid-regex`, `--engine` |
| ignore 동작 | User Guide / `ignore` crate | `.gitignore`, `.ignore`, `.rgignore` |
| library API | `grep` crate docs | `grep-cli`, `grep-matcher`, `grep-printer`, `grep-regex`, `grep-searcher` |

## 핵심 권장 학습 순서

1. **GitHub README** - 도구 정체와 기본 특징 파악
2. **User Guide** - 실제 command pattern 학습
3. **FAQ** - 성능, regex, encoding, ignore 관련 의문 정리
4. **`regex` crate docs** - 기본 engine의 trade-off 이해
5. **`ignore` crate docs** - file walk와 filtering 구조 이해
6. **2026 retrieval 논문** - AI agent/RAG 맥락에서 `rg`의 위치 이해

## 관련 노트

- [[README]]
- [[01-overview]]
- [[02-ecosystem]]
- [[../../ai/codex/README|Codex tool-study]]
- [[../../ai/agent-orchestration/cli-agents|CLI agents]]

