---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem과 대안 비교

## 비교

| 도구 | 저장소 / 호환성 | Branching·rewrite 관점 | 적합한 경우 |
| --- | --- | --- | --- |
| **Mercurial** | 독자 Hg repository, DVCS | bookmark + named branch + phase, extension 기반 `evolve` | Hg ecosystem, 명시적 공유 상태와 안전한 rewrite policy가 중요한 팀 |
| **Git** | 사실상 표준, GitHub/GitLab/IDE 생태계 최대 | ref 기반 branch, index/staging, rebase/reflog | 외부 협업·채용·SaaS 통합이 중요한 대부분의 신규 프로젝트 |
| **Sapling** | Git `.git` mode 또는 Sapling mode, GitHub 연동 | stack 중심 UX, large monorepo 지향 | Meta 스타일 monorepo 또는 Git 위 stacked workflow |
| **Jujutsu (`jj`)** | production-ready Git backend, 기존 Git remote 사용 | working copy를 자동 commit으로 취급, rewrite/stack을 단순화 | Git hosting은 유지하며 개인 workflow를 현대화할 때 |
| **Pijul** | 독자 patch-theory DVCS | patch commutation, first-class conflict | merge correctness 연구·실험, Git 모델을 벗어난 프로젝트 |

## 선택 기준

Mercurial의 강점은 Git을 대체하는 보편적 network effect가 아니라, history 상태를 드러내는 모델이다. `bookmark`는 가볍게 움직이고, named branch는 의도적으로 history에 남고, phase는 public rewrite를 막는다.

반대로 Git-native hosting과 PR automation이 협업의 중심이면 Git 또는 Git backend를 쓰는 `jj`가 마찰이 적다. Sapling은 Git 연동을 제공하지만, 공식 문서상 corporate·always-online·single-master·rebase 중심 환경에 특히 최적화돼 있다. `jj`는 Git remote와 공존할 수 있어도 공식 project가 experimental VCS로 표기하는 제약을 검토한다.

## Hosting과 migration

- **Heptapod**: Git과 Mercurial repository를 함께 hosting하는 선택지다.
- **TortoiseHg**: Mercurial GUI client의 릴리스 아카이브를 제공한다.
- **`hg convert`**: Git repository의 reachable branch와 remote ref를 가져오며 Git branch는 Mercurial bookmark로 변환한다. 주 용도는 일회성 변환이다.

`convert`를 Git-native hosting과의 상시 양방향 bridge로 가정하지 말고, production repository 대신 사본에서 author/committer metadata와 branch→bookmark 매핑을 검증한다.

## Sources

- https://sapling-scm.com/docs/introduction/
- https://github.com/jj-vcs/jj/blob/main/docs/git-compatibility.md
- https://pijul.org/
- https://www.mercurial-scm.org/help/commands/convert
- https://heptapod.net/heptapod/
- https://www.mercurial-scm.org/release/tortoisehg/
