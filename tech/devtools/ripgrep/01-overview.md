---
date: 2026-06-10
tags:
  - tech
  - devtools
  - ripgrep
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# ripgrep - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

## 1. What - ripgrep이란?

> **한 줄 정의**: `ripgrep`(`rg`)는 Rust로 작성된 고속 line-oriented recursive search tool이다.

### 핵심 개념

- recursive code/text search를 기본 동작으로 제공한다.
- regex pattern을 받아 현재 디렉터리 tree를 검색한다.
- `.gitignore`, `.ignore`, `.rgignore` rule을 기본 적용한다.
- hidden file과 binary file은 기본 제외한다.
- POSIX 표준 `grep` 대체품이라기보다 developer search workflow에 최적화된 CLI다.

```bash
rg "struct Searcher"
rg -n --column "panic!"
rg -t rust "Regex::new"
```

## 2. Why - 왜 필요한가?

### 기존 방식의 문제

| 문제 | `grep -R` / `find \| xargs grep` | `ripgrep` |
|---|---|---|
| Noise | vendor, build output, hidden file까지 쉽게 섞임 | ignore rule과 hidden/binary skip이 기본 |
| 속도 | large repo에서 느려질 수 있음 | finite automata, SIMD, parallel walk 활용 |
| 필터 | file type/glob 조합을 직접 구성 | `-t`, `-T`, `-g` 제공 |
| 자동화 | 출력 가공이 산발적 | `--json`, `-l`, `-o`, `--stats` 지원 |
| 이식성 | Unix 기본기는 좋지만 UX 차이가 큼 | cross-platform binary 제공 |

### 2025-2026 관점

- AI coding agent는 repository context를 빠르게 찾아야 한다.
- `ripgrep` 같은 index-free lexical retrieval은 별도 index build 없이 즉시 실행된다.
- 최근 연구 흐름에서도 grep-style retrieval은 vector retrieval, graph retrieval과 비교되는 강력한 baseline이다.
- [[../../ai/codex/README|Codex]]나 [[../../ai/agent-orchestration/cli-agents|CLI agents]] 같은 agent workflow에서 `rg`는 symbol, error message, issue keyword 검색의 기본 도구가 된다.

## 3. 핵심 특징

### 기본 UX

- `rg PATTERN`: 현재 디렉터리 recursive search
- `rg PATTERN path/`: 특정 path만 검색
- `rg -uuu PATTERN`: ignore, hidden, binary 관련 자동 필터를 최대한 해제

```bash
rg "TODO|FIXME"
rg "OldComponent" src tests
rg -uuu "generated"
```

### Regex engine

- 기본 engine은 Rust `regex` crate 기반이다.
- look-around/backreference처럼 효율적 구현이 어려운 기능은 기본 engine에서 제외한다.
- 대신 worst-case `O(m * n)` 성능 보장을 제공한다.
- PCRE2가 필요하면 `-P`, `--pcre2`, `--auto-hybrid-regex`, `--engine`을 사용한다.

```bash
# 기본 regex
rg 'user_[0-9]+'

# lookbehind 등 PCRE2 feature가 필요할 때
rg -P '(?<=token=)[A-Za-z0-9._-]+'
```

### 성능 구조

- finite automata 기반 matching
- SIMD와 literal optimization
- UTF-8 DFA 통합
- mmap 또는 buffered incremental search 자동 선택
- parallel directory iterator
- `ignore` crate 기반 file walk와 filter

## 4. 15.x 변경사항

| 버전 | 날짜 | 핵심 |
|---|---:|---|
| `15.1.0` | 2025-10-22 | `--line-buffered` regression 수정, Cursor hyperlink alias 추가 |
| `15.0.0` | 2025-10-16 | parent directory gitignore 처리, large gitignore memory regression 수정, `.jj` repo 처리, `--json` + replace 개선 |

### 15.0.0에서 주목할 점

- parent directory의 `.gitignore` 적용 관련 bug fix
- 큰 `.gitignore` 파일 처리 시 memory regression 수정
- Jujutsu(`jj`) repo 일부를 Git repo처럼 처리
- nested brace glob 지원
- Windows `aarch64` artifact 추가
- LTO build 적용

## 5. 사용 사례

| 사용 사례 | 예시 |
|---|---|
| 코드 탐색 | symbol, function, class, config key 검색 |
| 마이그레이션 | deprecated API나 old package 사용처 찾기 |
| 보안 점검 | secret pattern pre-check |
| 로그 분석 | error code, stack trace keyword 검색 |
| AI agent retrieval | issue keyword와 관련 파일 후보 찾기 |

## 다음 단계

> [!tip] 다음으로
> `ripgrep`의 위치를 이해했다면 [[02-ecosystem|생태계와 대안 비교]]를 살펴보세요.

