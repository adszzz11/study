---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기

## 목표

작은 disposable repository에서 provider 하나를 연결하고, `Supervised` mode의 thread 하나를 worktree와 함께 실행해 diff를 검토·commit한다.

## 준비

- Codex 또는 Claude Code를 host machine에 설치하고 login을 완료한다.
- 기존 변경이 없는 작은 Git repository를 선택한다.
- `npx t3@latest`로 일회 실행하거나 T3 CLI/desktop app을 설치한다.
- 첫 실습에 production credential이나 민감한 source를 넣지 않는다.

정확한 설치 옵션은 [공식 설치 가이드](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md)를 따른다.

## 첫 실습

1. 새 project를 열고 provider가 login을 인식하는지 확인한다.
2. 새 thread를 만들고 작은 task를 입력한다. 예: test 하나 추가, README typo 수정, lint 오류 하나 수정.
3. thread의 permission mode를 `Supervised`로 설정한다.
4. 이 thread 전용 branch와 worktree를 만든다.
5. agent의 제안과 command를 승인하며 실행한다.
6. diff와 test 결과를 검토한다.
7. 의도가 맞을 때만 commit하고 필요하면 push/PR을 만든다.

## provider 비교 실험

동일 task를 별도 thread/worktree에서 Codex와 Claude Code에 각각 맡긴다. 다음을 기록하면 tool 선택보다 운영 판단에 도움이 된다.

| 관찰 항목 | 기록 예 |
|---|---|
| 계획 품질 | 요구사항을 먼저 확인했는가 |
| tool behavior | test, search, edit의 순서가 적절했는가 |
| 변경 범위 | 필요한 파일만 고쳤는가 |
| 검증 | 어떤 test/command를 수행했는가 |
| review 용이성 | diff가 작고 설명 가능한가 |

## 완료 기준

- [ ] thread와 worktree가 1:1로 연결되어 있다.
- [ ] `Supervised`에서 실행·승인 흐름을 경험했다.
- [ ] diff와 test 결과를 사람이 검토했다.
- [ ] provider별 실행 결과를 짧게 비교 기록했다.

## 다음 단계

- [[tech/devtools/t3-code-control-plane/04-learning/02-deep-dive|심화]] — context와 remote operation을 다룬다.
- [[tech/devtools/t3-code-control-plane/cheatsheet|Cheatsheet]] — 실행 전 점검 항목을 확인한다.

## Sources

- https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/thread-sidebar.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md
