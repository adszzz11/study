---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## Mental model

```text
T3 Code = provider를 대체하는 model이 아니라
          여러 coding harness를 실행·관찰·분리하는 control plane
```

## 작업 전 점검

- [ ] host machine에서 provider login과 repository access를 확인했다.
- [ ] task 하나에 thread 하나를 만들었다.
- [ ] 독립 변경이면 전용 branch/worktree를 만들었다.
- [ ] 시작 권한은 `Supervised` 또는 `Auto`로 선택했다.
- [ ] context에 credential, secret, 민감 terminal output이 없다.
- [ ] 완료 검증 command와 사람이 review할 기준을 정했다.

## 빠른 workflow

```text
작업 분해
  → thread 생성
  → permission 설정
  → branch/worktree 연결
  → provider 실행
  → diff + test 검토
  → commit / push / PR
```

## 권한 선택

| 모드 | 적합한 경우 |
|---|---|
| Supervised | 처음 보는 repo, 민감 작업, 명령별 확인 필요 |
| Auto-accept edits | edit은 반복적이지만 command는 검토할 때 |
| Auto | 검증된 routine task와 격리된 worktree |
| Full access | disposable sandbox 또는 명확한 allowlist가 있을 때만 |

## Context 명령·재료

| 항목 | 용도 |
|---|---|
| `/goal` | 현재 task의 성공 기준 갱신 |
| `/compact` | 긴 대화 압축 |
| `/clear` | 더 이상 유효하지 않은 context 분리 |
| file / image / terminal excerpt | 재현·판단에 필요한 증거 제공 |
| PR / 다른 thread reference | 구현과 review의 연결 |

## 원격 운영 원칙

- `t3 up`/T3 Connect는 remote client와 host를 연결한다.
- agent와 Git credential은 host에서 실행·보관된다는 점을 잊지 않는다.
- long-running task에는 stop 기준, 관찰자, 검증 단계를 둔다.

## 관련 학습

- [[tech/devtools/t3-code-control-plane/README|T3 Code]]
- [[tech/devtools/t3-code-control-plane/04-learning/01-getting-started|시작하기]]
- [[tech/devtools/t3-code-control-plane/04-learning/02-deep-dive|심화]]

## Sources

- https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/composer.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md
