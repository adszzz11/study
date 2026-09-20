---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — Getting Started

> [[../03-references|이전: References]] · [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 1. 사전 점검

CodeBurn은 local session transcript를 읽는다. 설치 전 다음을 확인한다.

```bash
node --version
npm --version
```

- 공식 설치 문서는 Node.js 20+라고 쓰지만 package metadata는 `>=22.13.0`을 요구한다.
- 호환성 충돌을 피하려면 **Node.js 22.13+**를 사용한다.
- Claude Code, Codex, Cursor 등 지원 tool의 local session data가 최소 하나 있어야 한다.
- Cursor와 OpenCode용 `better-sqlite3`는 optional dependency로 자동 설치된다.

## 2. 실행 또는 설치

먼저 one-off로 실행해도 된다.

```bash
npx codeburn
```

지속적으로 사용할 때:

```bash
npm install -g codeburn
codeburn --version
codeburn status
```

macOS의 Homebrew 방식:

```bash
brew tap getagentseal/codeburn
brew install codeburn
```

> [!warning] Version drift
> 빠르게 개발 중이므로 예제보다 현재 설치본의 `codeburn --help`와 `codeburn <command> --help`를 우선한다.

## 3. 첫 dashboard 읽기

```bash
codeburn
```

처음에는 다음 순서로 본다.

1. 감지된 provider와 예상한 provider가 같은지 확인한다.
2. today/7 days/30 days 같은 period를 바꾸며 날짜 경계를 확인한다.
3. 총 cost보다 provider → model → project → activity 순서로 drill-down한다.
4. 가장 비싼 session을 원본 작업 기억과 대조한다.
5. unknown model이나 estimated label을 기록한다.

## 4. Baseline export

```bash
# 오늘과 이번 달의 compact status
codeburn status

# machine-readable status
codeburn status --format json

# CSV export
codeburn export

# JSON export
codeburn export -f json

# model별 최근 30일
codeburn models

# 붙여넣기 쉬운 Markdown
codeburn models --format markdown
```

민감한 project name과 usage 정보가 포함될 수 있으므로 export 파일을 public repository에 commit하지 않는다.

## 5. 첫 분석

```bash
# model 효율 비교
codeburn compare -p week

# 지난 30일 waste 후보
codeburn optimize

# Git repository 안에서 최근 7일 delivery proxy
codeburn yield
```

| 결과 | 첫 질문 | 피해야 할 결론 |
|---|---|---|
| high cost session | task가 어려웠나, context가 컸나? | “model이 나쁘다” |
| low one-shot | retry가 실제 실패였나, iterative design이었나? | “개발자가 비효율적이다” |
| Abandoned Yield | commit이 다른 branch/repo에 있었나? | “성과가 없다” |
| unused MCP | 관찰 기간이 충분한가? | 즉시 설정 삭제 |

## 6. 7일 학습 실습

- [ ] 설치 직후 version과 Node.js 요구사항 기록
- [ ] provider별 하루 usage를 원본 tool과 대조
- [ ] JSON export를 private location에 보관
- [ ] 가장 비싼 session 3개에 작업 유형 메모
- [ ] `compare`의 cost per edit와 one-shot rate 비교
- [ ] `optimize` finding을 자동 적용하지 말고 원인만 검토
- [ ] Git repo에서 `yield`의 commit 연결을 sample 검증

## Sources

- https://codeburn.app/docs/installation
- https://codeburn.app/docs
- https://codeburn.app/docs/status-export
- https://codeburn.app/docs/models
- https://codeburn.app/docs/compare
- https://codeburn.app/docs/yield

