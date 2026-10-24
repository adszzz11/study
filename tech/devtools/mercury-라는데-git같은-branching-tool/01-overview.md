---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Mercurial: What, Why, 특징

## What

Mercurial은 무료 분산형 Version Control System(DVCS)이다. repository를 clone하면 전체 changeset history가 로컬에 오며, commit은 부모 changeset을 가리키는 DAG를 이룬다. merge commit은 둘 이상의 부모를 가진다.

## Why

Git의 index/staging area, detached `HEAD`, ref와 rewrite 조합은 처음 배우는 사람에게 복잡할 수 있다. Mercurial은 `hg`라는 일관된 CLI로 기본 작업을 제공하고, **branch의 목적을 하나의 이름으로 뭉개지 않는다**.

| 개념 | 의미 | 권장 용도 |
| --- | --- | --- |
| `bookmark` | commit을 따라 움직이는 가변 포인터 | feature, hotfix, 짧은 작업 line |
| `named branch` | changeset에 영속 기록되는 branch 이름 | `stable`, `release-X` 같은 장기 계통 |
| anonymous/topological branch | DAG head에서 자연스럽게 갈라진 분기 | merge 전 DAG 상태 이해 |
| `phase` | changeset의 공유·rewrite 가능성 표지 | public history 보호 |

## 핵심 특징

### Bookmark 우선의 일상 branching

`hg book feature/login`으로 만든 bookmark는 Git branch에 가장 가깝다. 이동·삭제·rename이 가능하며 feature work에 가볍다. 반면 `hg branch stable`은 이후 commit의 metadata에 `stable`을 기록하므로, 단순 실험에 쓰기에는 무겁다.

### Phase safety model

- 새 changeset은 보통 `draft`다. local rewrite 대상이 될 수 있다.
- publishing server에 push한 changeset은 `public`이 되며 `rebase`, `histedit` 같은 rewrite가 거부된다.
- `secret` changeset은 push, pull, clone 대상이 아니다.

이는 협업자가 이미 받은 history를 실수로 바꾸는 위험을 낮춘다. 실제 server의 publishing 설정과 extension 구성은 확인해야 한다.

### Extension 기반 확장

`rebase`, `histedit`, `evolve`, `convert`, `largefiles`, `share` 등은 필요에 따라 extension으로 활성화한다. `evolve`는 obsolete/orphan/content-divergent changeset 같은 history mutation 이후의 troubled state를 추적·정리하는 workflow를 제공한다.

## 버전과 상태

2026-10 기준 공식 release index의 최신 안정 릴리스는 **7.2.4 (2026-08-11)** 이다. 7.2 release는 Python 3.14 지원을 포함한다. 배포판 package는 다른 버전을 제공할 수 있으므로 `hg version`으로 실제 설치 버전을 확인한다.

## Sources

- https://mercurial-scm.org/help/commands/branch
- https://www.mercurial-scm.org/help/commands/bookmarks
- https://www.mercurial-scm.org/help/topics/phases
- https://www.mercurial-scm.org/help/extensions
- https://www.mercurial-scm.org/release/
