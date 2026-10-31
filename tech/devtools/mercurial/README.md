---
date: 2026-10-24
tags: [tech]
type: tech-tool-study
status: draft
---

# Mercurial 학습 노트

> **한 줄 정의**: Mercurial(`hg`)은 전체 이력을 로컬에 복제하는 DVCS로, `bookmark`, `named branch`, `phase`를 분리해 branching과 history rewrite를 관리한다.

## Overview

Mercury라는 이름으로 불리기도 하지만, 이 노트가 다루는 도구의 정식 명칭은 **Mercurial**이다. Git과 마찬가지로 clone마다 전체 changeset history를 보유하므로 offline에서도 log, diff, commit을 수행할 수 있다.

- 일상적인 feature line은 가변 포인터인 `bookmark`를 우선 사용한다.
- release·stable처럼 오래 남을 계통은 history에 기록되는 `named branch`가 맞다.
- `phase`는 draft/public/secret 상태로 공유와 rewrite의 경계를 표시한다.

## Learning Path

- [ ] [[01-overview|What / Why와 branch 모델]]을 읽고 bookmark와 named branch의 역할을 구분한다.
- [ ] [[04-learning/01-getting-started|시작하기]]의 hello repository 실습을 실행한다.
- [ ] `hg log -G`로 changeset DAG와 merge parent를 확인한다.
- [ ] [[04-learning/02-deep-dive|심화]]에서 phase와 draft-only rewrite를 재현한다.
- [ ] [[02-ecosystem|생태계 비교]]를 읽고 새 프로젝트에 Hg를 선택할 조건을 판단한다.
- [ ] [[05-projects|실전 적용]]의 release line 또는 patch stack 예제를 작은 사본에서 적용한다.

## When To Use

- 팀이 이미 Mercurial hosting·hooks·workflow를 운영한다.
- public history를 실수로 rewrite하지 않도록 phase 기반 안전장치가 필요하다.
- feature bookmark와 영속적인 release branch를 명시적으로 분리하고 싶다.
- Git 호환 hosting보다 분산 로컬 workflow와 Hg 생태계의 일관성이 우선이다.

## When Not To Use

- GitHub/GitLab, IDE, 채용 시장을 포함한 Git-native 통합이 최우선인 신규 프로젝트.
- Git remote와 매일 양방향 협업해야 하며 일회성 `hg convert`만으로는 부족한 경우.
- 팀이 named branch의 영속성, phase, extension 설정을 학습·운영할 여력이 없다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/git/github-repo-merge|GitHub repository merge]]
- [[01-overview]] · [[02-ecosystem]] · [[cheatsheet]]

## Sources

- https://mercurial-scm.org/
- https://www.mercurial-scm.org/help/topics/phases
- https://www.mercurial-scm.org/release/
- https://www.mercurial-scm.org/relnotes/7.2
