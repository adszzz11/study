---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화

## 1. Thread와 worktree를 함께 설계하기

독립 변경마다 thread와 worktree를 나눈다. 예를 들어 feature, test, documentation을 각 thread에 배치하면 동일 파일을 건드릴 가능성과 merge 부담을 사전에 줄일 수 있다. 반대로 서로 강하게 의존하는 변경은 무리하게 분리하지 말고 하나의 thread에서 순서를 명확히 한다.

```text
feature thread  → feature/my-change worktree → implementation diff
test thread     → test/my-change worktree    → regression diff
docs thread     → docs/my-change worktree    → documentation diff
```

## 2. Context orchestration

message context에는 file, image, terminal excerpt, PR, 다른 thread를 넣을 수 있다. 긴 thread 전체를 반복 복사하지 말고 reference로 연결해 agent가 필요할 때 읽게 한다.

- `/goal`: 현재 작업 목표를 명시·갱신한다.
- `/compact`: 긴 대화를 압축해 context 부담을 낮춘다.
- `/clear`: 더 이상 유효하지 않은 대화 상태를 분리한다.
- attachment: 판단 근거가 되는 diff, error output, screenshot을 직접 첨부한다.

context는 많이 넣는 것보다 task 결정에 필요한 근거를 선별하는 것이 중요하다. credential, customer data, private key가 포함된 terminal output은 첨부하지 않는다.

## 3. 권한과 운영 경계

권한은 task 위험도에 비례해 설정한다. 일반 개발은 `Supervised`에서 시작하고, 검증된 반복 작업만 `Auto-accept edits` 또는 `Auto`로 넓힌다. `Full access`는 disposable sandbox나 명확한 allowlist가 있는 host에서만 고려한다.

| 위험 신호 | 권장 대응 |
|---|---|
| production credential 또는 고객 데이터 | context에서 제외하고 Supervised 유지 |
| broad file delete 또는 migration | 별도 승인과 backup, 수동 review |
| 장시간 unattended run | worktree 격리, status 관찰, stop 기준 문서화 |
| remote client 노출 | T3 Connect 접근 범위와 host login을 점검 |

## 4. Remote access와 queueing

`t3 up` 또는 T3 Connect는 router port-forwarding 없이 다른 device에서 host machine에 접근하는 경로를 제공한다. 이는 개발 환경을 cloud로 옮기는 기능이 아니라, agent가 실제로 실행되는 host를 remote client가 제어·관찰하는 방식이다.

긴 thread는 mobile/web에서 progress를 확인하고, 다음 task를 queue하거나 추가 지시를 보낼 수 있다. 다만 network 경로가 생겨도 provider credential과 repository 권한은 여전히 host의 보안 경계에 남는다.

## 관련 학습

- [[tech/devtools/t3-code-control-plane/04-learning/01-getting-started|시작하기]]
- [[tech/devtools/t3-code-control-plane/05-projects|Projects]]
- [[tech/devtools/t3-code-control-plane/03-references|References]]

## Sources

- https://github.com/pingdotgg/t3code/blob/main/docs/user/composer.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md
