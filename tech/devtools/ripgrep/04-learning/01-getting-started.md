---
date: 2026-06-10
tags:
  - tech
  - devtools
  - ripgrep
  - learning
type: tech-tool-study
parent: "[[../README]]"
---

# ripgrep - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep Dive]]

## 1. 설치

### macOS

```bash
brew install ripgrep
rg --version
```

### Rust/Cargo

```bash
cargo install ripgrep
rg --version
```

### Linux

```bash
# Debian/Ubuntu 계열
sudo apt install ripgrep

# Fedora
sudo dnf install ripgrep

# Arch
sudo pacman -S ripgrep
```

> 배포판 package가 오래된 경우 GitHub release binary를 확인한다.

## 2. 기본 검색

| 명령 | 의미 |
|---|---|
| `rg "TODO"` | 현재 디렉터리 아래에서 `TODO` 검색 |
| `rg -n "TODO"` | line number 출력 |
| `rg -i "error"` | case-insensitive search |
| `rg "TODO\|FIXME"` | 여러 keyword regex 검색 |
| `rg "functionName" src tests` | 특정 path만 검색 |

```bash
rg "TODO|FIXME"
rg -n "functionName"
rg -i "error"
rg "DATABASE_URL" config src
```

## 3. File Type Filter

### 포함

```bash
rg -tpy "import requests"
rg -tjs "console.log"
rg -trs "Regex::new"
```

### 제외

```bash
rg -Tjs "console.log"
rg -Tmd "TODO"
```

### type 확인

```bash
rg --type-list
rg --type-list | rg "python|rust|javascript"
```

## 4. Glob Filter

```bash
rg "password" -g '*.env'
rg "password" -g '!node_modules'
rg "OldComponent" -g 'src/**/*.{ts,tsx}'
```

| 패턴 | 의미 |
|---|---|
| `-g '*.md'` | Markdown file만 검색 |
| `-g '!dist'` | `dist` 제외 |
| `-g 'src/**/*.{js,ts}'` | `src` 아래 JS/TS 검색 |

## 5. Ignore Rule 이해

기본적으로 `rg`는 다음을 자동 적용한다.

- `.gitignore`
- `.ignore`
- `.rgignore`
- hidden file/directory skip
- binary file skip

```bash
# hidden file 포함
rg --hidden "TOKEN"

# binary를 text처럼 검색
rg -a "needle"

# 자동 필터를 강하게 해제
rg -uuu "needle"
```

## 6. 실습 과제

### 과제 1: TODO 찾기

```bash
rg -n "TODO|FIXME|HACK"
```

- 어떤 directory가 자동 제외되는지 확인한다.
- `rg --debug "TODO"`로 skip reason을 살펴본다.

### 과제 2: Python dependency 사용처 찾기

```bash
rg -tpy "import requests|from requests"
```

- `-tpy`가 어떤 확장자를 포함하는지 `rg --type-list`로 확인한다.

### 과제 3: migration 후보 찾기

```bash
rg -n --context 2 "OldComponent"
```

- 바로 replace하지 말고 주변 context를 먼저 읽는다.
- 후보가 맞으면 [[../05-projects|실전 프로젝트]]의 migration workflow로 확장한다.

## 관련 노트

- [[../../../../tech/ai/codex/README|Codex tool-study]]
- [[../../../../tech/ai/agent-orchestration/cli-agents|CLI agents]]

