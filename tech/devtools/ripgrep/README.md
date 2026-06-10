---
date: 2026-06-10
tags:
  - tech
  - devtools
  - ripgrep
  - search
type: tech-tool-study
status: learning
---

# ripgrep (`rg`)

> **한 줄 정의**: `ripgrep`(`rg`)는 Rust로 작성된 고속 line-oriented recursive search tool로, regex 검색을 수행하면서 기본적으로 `.gitignore`, hidden file, binary file을 자동으로 제외하는 개발자용 코드/텍스트 검색 CLI다.

## 개요

- `grep -R`보다 개발자 workflow에 맞춘 기본값을 제공한다.
- `rg PATTERN`만으로 현재 디렉터리 아래를 recursive search한다.
- `.gitignore`, `.ignore`, `.rgignore`를 존중하고 hidden/binary file을 기본 skip한다.
- Rust `regex` crate 기반 engine으로 빠른 검색과 worst-case `O(m * n)` 보장을 우선한다.
- look-around/backreference가 필요하면 PCRE2 engine을 `-P`로 opt-in한다.
- AI coding agent와 RAG context retrieval에서도 index-free lexical retrieval baseline으로 중요하다.

## Quick Start

```bash
# 설치
brew install ripgrep
cargo install ripgrep

# 기본 검색
rg "TODO|FIXME"
rg -n "functionName"
rg -i "error"

# 파일 타입 필터
rg -tpy "import requests"
rg -Tjs "console.log"
rg --type-list

# ignore/hidden/binary 제어
rg --hidden "dotenv"
rg -a "binary-ish text"
rg -uuu "really search everything"
```

## 학습 경로

### 1단계: 도구의 기본값 이해

- [ ] [[01-overview|개요]] - What/Why, `rg`가 `grep -R`과 다른 지점
- [ ] [[04-learning/01-getting-started|시작하기]] - 설치, 기본 검색, file type filter

### 2단계: 생태계와 비교

- [ ] [[02-ecosystem|생태계]] - GNU `grep`, `git grep`, `ack`, `ag`, `ugrep` 비교
- [ ] [[03-references|참고자료]] - 공식 README, User Guide, FAQ, Rust crate docs

### 3단계: 내부 동작과 자동화

- [ ] [[04-learning/02-deep-dive|Deep Dive]] - regex engine, ignore walker, PCRE2, JSON output
- [ ] [[cheatsheet|치트시트]] - 자주 쓰는 플래그와 패턴

### 4단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]] - monorepo audit, secret pre-check, AI agent retrieval

## 파일 구조

```text
ripgrep/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|---|---|---|
| 개요 | [[01-overview]] | 정의, 배경, 핵심 특징 |
| 생태계 | [[02-ecosystem]] | 대안 도구와 비교 |
| 참고자료 | [[03-references]] | 공식 문서와 논문 |
| 시작하기 | [[04-learning/01-getting-started]] | 설치와 기본 명령 |
| 심화 | [[04-learning/02-deep-dive]] | engine, ignore, automation |
| 프로젝트 | [[05-projects]] | 실전 적용 아이디어 |
| 치트시트 | [[cheatsheet]] | 명령 빠른 참조 |

## 관련 노트

- [[../../ai/codex/README|Codex tool-study]] - agent가 repo context를 찾을 때 `rg`를 함께 사용
- [[../../ai/agent-orchestration/cli-agents|CLI agents]] - CLI tool 기반 agent workflow
- [[../../ai/llm-wiki-study/README|LLM Wiki study]] - lexical retrieval과 지식 베이스 운영 맥락

