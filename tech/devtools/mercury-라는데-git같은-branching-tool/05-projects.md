---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# 실전 적용 패턴

## 장기 지원 제품

`default`에서는 feature bookmark를 운용하고, `stable`과 `release-X`는 named branch로 둔다. hotfix는 stable에서 bookmark로 만들고 검토·테스트 후 stable line으로 merge한다.

| 목적 | 추천 모델 | 이유 |
| --- | --- | --- |
| 로그인 기능 개발 | `feature/login` bookmark | 짧고 이동 가능한 feature line |
| 2.x 유지보수 | `release-2.x` named branch | history에 제품 계통을 영속 기록 |
| 긴급 수정 | stable에서 만든 bookmark | 격리·검토 후 안정 line에 통합 |

운영 규칙은 단순하다. public changeset은 rewrite하지 않고, release branch 생성 권한과 merge 검토 기준을 문서화한다.

## 개인·소규모 팀 patch stack

작은 `draft` commit을 bookmark 위에 쌓고 review 전 `histedit` 또는 `rebase`로 정리한다. publish 전에는 `hg log -G`, `hg diff`, test를 실행해 DAG와 내용을 확인한다. publish 뒤에는 phase policy를 존중한다.

## Git에서 일회성 migration

1. production Git repository를 읽기 전용 사본으로 만든다.
2. `convert` extension으로 Hg destination에 변환한다.
3. branch→bookmark, reachable ref, author/committer metadata를 검증한다.
4. sample build·test와 `hg log -G`를 비교한다.
5. hosting과 CI를 Hg workflow로 전환할 수 있을 때만 cutover를 결정한다.

Git remote와 지속적으로 동기화해야 한다면 convert-only 접근은 적합하지 않다.

## Sources

- https://mercurial-scm.org/help/commands/branch
- https://www.mercurial-scm.org/help/commands/bookmarks
- https://www.mercurial-scm.org/help/topics/phases
- https://www.mercurial-scm.org/help/commands/convert
