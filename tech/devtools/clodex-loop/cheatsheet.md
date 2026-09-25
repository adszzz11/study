---
date: 2026-09-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Clodex loop — Cheatsheet

## 핵심 흐름

```text
plan → accepted plan → isolated build → dual audit
     → agreement(final diff hash) → manual apply
```

## 사전 점검과 dry-run

```bash
# 요구사항·CLI readiness 확인
python --version
git --version
clodex doctor
clodex native doctor

# 파일에 적용하기 전 예정 변경 확인
clodex init --dry-run

# 계획과 full workflow를 분리해 관찰
clodex plan "Add a small, testable feature"
clodex build --dry-run "Add a small, testable feature"
```

| 항목 | 기본/확인 기준 |
|---|---|
| 격리 | `.clodex/workspaces/<run-id>/` Git worktree |
| 상태 | `.clodex/state.sqlite3` |
| loop cap | default `max_fix_loops: 2`; 첫 실습은 `1` 권장 |
| approval | `05-agreement.json`의 `approved: true`와 final diff hash 일치 |
| 적용 | `clodex apply <run-id>`는 사람이 diff를 확인한 뒤 실행 |

## run artifact 빠른 확인

```text
.clodex/runs/<run-id>/
├── 01-claude-plan.json
├── 02-codex-implementation.md
├── 03-claude-audit.json
├── 04-codex-audit.json
├── 05-agreement.json
├── changes.diff / apply.patch
├── trace.jsonl
└── workspace.json
```

## apply 전 checklist

- [ ] `changes.diff`가 요청 scope와 일치한다.
- [ ] 실행한 test와 결과가 implementation report에 남아 있다.
- [ ] unresolved finding과 waived risk를 사람이 검토했다.
- [ ] 양쪽 audit이 동일한 final diff hash를 가리킨다.
- [ ] `05-agreement.json`이 `approved: true`다.
- [ ] migration, secret, destructive operation, production deployment는 별도 승인받았다.

## 피해야 할 것

- 동명 `clodex` 프로젝트를 같은 workflow로 가정하기
- contract의 기본 model string을 현재 CLI의 가용 모델로 단정하기
- audit agreement만으로 CI test/lint/SAST와 release approval을 생략하기
- loop cap 뒤에도 자동으로 계속 수정하거나 apply하기
- `--workspace local`을 기본 격리와 같은 안전성으로 오해하기

## 빠른 링크

- [[README|스터디 시작]] · [[01-overview|Overview]] · [[04-learning/01-getting-started|Getting started]]
- https://github.com/9thLevelSoftware/Clodex/blob/main/README.md
- https://github.com/9thLevelSoftware/Clodex/blob/main/CLODEX.md
