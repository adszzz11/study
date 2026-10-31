---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: bookmark와 named branch 분리

## 목표

Git 명령을 일대일로 외우기보다, **짧은 작업은 bookmark, 오래 남는 product line은 named branch**라는 구분을 직접 확인한다.

## 준비

설치는 OS별 package manager 또는 [공식 다운로드](https://www.mercurial-scm.org/downloads)를 사용한다. 다음으로 설치와 identity를 확인한다.

```sh
hg version
hg config --edit  # [ui] username = Your Name <you@example.com> 설정
```

> 실습은 사본 repository에서 한다. public changeset의 rewrite를 시험하지 않는다.

## 첫 흐름

```sh
hg clone https://www.mercurial-scm.org/repo/hello
cd hello

# 가벼운 feature line
hg book feature/login
# 파일 수정
hg commit -m "Add login flow"
hg log -G

# 장기 유지 line
hg update default
hg branch stable
hg commit -m "Start stable line"

# 현재 changeset의 phase 확인
hg phase
```

## 관찰할 점

1. `hg book` 뒤 commit을 만들면 bookmark가 새 changeset으로 전진하는지 본다.
2. `hg log -G`에서 DAG와 현재 line을 확인한다.
3. `hg branch stable` 뒤 commit의 branch metadata가 `stable`인지 `hg log -v`로 확인한다.
4. `hg phase`의 결과가 기본적으로 `draft`인지 기록한다.

## 다음 실습

bookmark divergence를 만든 뒤 merge를 실행한다.

```sh
hg book feature/a
# 변경 A를 commit
hg update default
hg book feature/b
# 변경 B를 commit
hg update feature/a
hg merge feature/b
hg commit -m "Merge feature/b into feature/a"
hg log -G
```

충돌이 나면 파일을 고친 다음 `hg resolve --mark <file>`과 commit으로 마무리한다. 의도적으로 같은 줄을 수정해 conflict resolution도 경험한다.

## Sources

- https://www.mercurial-scm.org/downloads
- https://www.mercurial-scm.org/help/commands/bookmarks
- https://mercurial-scm.org/help/commands/branch
