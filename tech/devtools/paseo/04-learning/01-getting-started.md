---
date: 2026-08-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Paseo — Getting Started

> [[../03-references|이전: References]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: Deep Dive]]

## 목표

기존에 인증된 coding-agent CLI를 Paseo에서 실행하고, background session을 조회·attach·follow-up·wait하는 최소 workflow를 익힌다.

## 1. 사전 점검

- [ ] Git repository에서 실습한다.
- [ ] 사용할 provider CLI가 설치되어 있고 직접 실행했을 때 인증이 완료된다.
- [ ] Paseo 설치 방식과 현재 version 요구사항은 [공식 문서](https://paseo.sh/docs/why)와 [Releases](https://github.com/getpaseo/paseo/releases)에서 확인한다.
- [ ] 실습 repository에 uncommitted change가 있는지 확인한다.
- [ ] agent가 현재 사용자 권한으로 실행된다는 점을 이해한다.

```bash
git status --short
paseo --help
```

> [!warning] 설치 명령
> Paseo는 빠르게 변경 중이므로 이 노트는 dossier에 없는 설치 명령을 고정하지 않는다. 실제 설치 시점의 공식 문서를 따른다.

## 2. 첫 agent 실행

```bash
paseo run "fix the failing tests"
```

처음에는 scope가 작고 검증 조건이 분명한 prompt를 쓴다.

```text
Find the cause of the failing unit test, make the smallest fix,
run the relevant test, and summarize changed files.
```

확인할 항목:

- 어떤 provider/model이 선택됐는가?
- permission request는 어디에 표시되는가?
- agent conversation과 terminal output을 함께 볼 수 있는가?
- 변경 파일과 test result를 추적할 수 있는가?

## 3. Session 감독

```bash
# 실행 중인 agent 목록
paseo ls

# interactive session 연결
paseo attach <agent-id>

# 추가 지시
paseo send <agent-id> "also add regression tests"

# log 확인
paseo logs <agent-id>

# 완료 대기
paseo wait <agent-id>
```

`<agent-id>`에는 `paseo ls`에서 확인한 실제 ID를 넣는다.

## 4. Background와 workspace

공식 CLI reference에서 현재 flag semantics를 확인한 뒤 다음 옵션을 조합한다.

| 옵션 | 용도 |
|---|---|
| `--background` | terminal을 점유하지 않고 session 실행 |
| `--workspace` | 기존 workspace 지정 |
| `--new-workspace worktree` | 새 Git worktree에서 격리 실행 |
| `--output-schema` | machine-readable structured output 요청 |

```bash
paseo run --background "inspect the flaky test and report likely causes"
paseo run --new-workspace worktree "implement the isolated change and run tests"
```

> [!note] Worktree의 의미
> 별도 worktree는 file edit collision을 줄이지만 security sandbox가 아니다. database, cache, cloud account 같은 외부 shared resource는 별도로 격리해야 한다.

## 5. 첫 실습

### 실습 A: Read-only investigation

1. 작은 test failure 또는 TODO를 선택한다.
2. agent에게 수정 없이 원인과 관련 파일만 보고하도록 한다.
3. `paseo logs`로 조사 과정을 확인한다.
4. `paseo send`로 누락된 가설 검증을 요청한다.

### 실습 B: Isolated implementation

1. 새 worktree로 agent를 시작한다.
2. 최소 수정과 regression test를 요청한다.
3. 완료 후 diff와 test result를 검토한다.
4. branch 통합 전 사람 review를 수행한다.

## 6. 종료 전 체크

- [ ] agent가 남긴 process와 dev server 확인
- [ ] diff와 untracked file 검토
- [ ] test/lint 결과 확인
- [ ] credential 또는 sensitive log 노출 여부 확인
- [ ] 불필요한 worktree 정리 전 branch 보존 여부 확인

## Sources

- [CLI reference](https://paseo.sh/docs/cli)
- [Providers](https://paseo.sh/docs/providers)
- [Git worktrees](https://paseo.sh/docs/worktrees)
- [Security](https://paseo.sh/docs/security)
- [GitHub Releases](https://github.com/getpaseo/paseo/releases)
