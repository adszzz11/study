---
date: 2026-11-06
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Parallel feature delivery

feature 구현, test, documentation을 각 worktree/thread로 분리한다. Codex와 Claude Code는 task 성격에 맞춰 배치하고, 각 결과를 PR 단위로 review·통합한다.

**성공 기준**: 작업마다 owner, branch, 검증 command, merge 순서가 기록되어 있고 변경이 서로 덮어쓰지 않는다.

## 2. Cross-agent code review

한 provider thread가 변경을 구현한 뒤, 다른 provider thread에 diff 또는 PR을 context로 전달한다. review thread에는 변경 목적, 검증 결과, 의심되는 regression 영역을 제공해 독립적인 failure hypothesis를 만든다.

**주의**: 두 agent의 동의는 correctness의 증명이 아니다. 사람이 test 결과와 domain requirement를 최종 확인한다.

## 3. Remote homelab/VM development

Linux VM에서 T3 Code server와 agent를 실행하고 T3 Connect로 노트북·mobile에서 승인, progress 확인, PR 생성을 한다. host에는 최소 권한 Git credential을 두고, remote access와 provider login의 scope를 정기 점검한다.

## 4. Mobile app verification loop

agent가 app을 수정하는 동안 iOS Simulator 또는 Android Emulator panel을 관찰하고 `device_*` 도구 기반 검증을 요청한다. 구현 thread와 verification thread를 분리하면 결과와 재현 절차를 review하기 쉽다.

## 5. Internal custom control plane

MIT source를 fork해 사내 provider adapter, policy, design system, audit integration을 더한 self-hosted build를 운영한다. 이 경우 가장 먼저 정할 것은 UI가 아니라 credential 저장, permission default, audit log retention, update 책임이다.

## 프로젝트 회고 템플릿

```markdown
- Task / thread:
- Provider / model:
- Permission mode:
- Worktree / branch:
- 검증 command와 결과:
- 사람이 수정하거나 되돌린 부분:
- 다음 반복에서 바꿀 policy/context:
```

## 관련 학습

- [[tech/devtools/t3-code-control-plane/04-learning/02-deep-dive|심화]]
- [[tech/devtools/t3-code-control-plane/02-ecosystem|Ecosystem]]
- [[tech/devtools/t3-code-control-plane/cheatsheet|Cheatsheet]]

## Sources

- https://github.com/pingdotgg/t3code/blob/main/docs/user/source-control.md
- https://github.com/pingdotgg/t3code/blob/main/docs/user/devices.md
- https://github.com/pingdotgg/t3code
