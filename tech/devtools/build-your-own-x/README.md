---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X

> **한 줄 정의**: `Build Your Own X`는 database, Git, Docker, compiler, operating system 같은 기술을 축소해 직접 구현하며 내부 원리를 배우는 외부 tutorial을 주제별로 모은 community-curated GitHub index다.

## Overview

- [공식 repository](https://github.com/codecrafters-io/build-your-own-x)의 Markdown README가 catalog 역할을 한다.
- 약 30개 technology category에서 여러 programming language로 작성된 guide를 찾을 수 있다.
- course, package, executable framework가 아니며 공통 runtime, test suite, grading도 제공하지 않는다.
- 실제 tutorial과 source code는 외부 사이트에 분산되어 있으므로 시작 전에 link, dependency, API의 유효성을 확인해야 한다.
- 2026-07-17 GitHub API 기준 약 526,000 stars, 49,800 forks, 6,800 subscribers를 가진 대규모 community resource다. 수치는 계속 변할 수 있다.

```text
Build Your Own X README
  → technology category 선택
  → language와 tutorial 선택
  → 외부 guide에서 축소판 구현
  → 자체 test·benchmark·회고 추가
```

## Learning Path

- [ ] [[01-overview|Overview]] — What/Why, content architecture, 강점과 한계 이해
- [ ] [[02-ecosystem|Ecosystem]] — CodeCrafters, Coding Challenges, Nand2Tetris 등과 비교
- [ ] [[03-references|References]] — 공식 자료와 tutorial 검증 출처 확인
- [ ] [[04-learning/01-getting-started|Getting Started]] — category 선택부터 첫 milestone까지 진행
- [ ] [[04-learning/02-deep-dive|Deep Dive]] — black-box test, benchmark, failure analysis로 학습 확장
- [ ] [[05-projects|Projects]] — 난이도별 재구현 project 수행
- [ ] [[cheatsheet|Cheatsheet]] — 선택 기준과 실습 checklist 빠르게 참조

## When To Use

- abstraction 아래의 storage, parser, protocol, runtime 동작을 손으로 확인하고 싶을 때
- 새 programming language를 익히면서 의미 있는 systems project를 만들고 싶을 때
- database, container, Git, compiler 같은 기술의 작은 working model이 필요할 때
- tutorial을 출발점으로 삼아 자체 test, benchmark, design note를 만드는 self-directed learning에 익숙할 때
- portfolio보다 구현 원리와 trade-off 설명 능력을 우선할 때

## When Not To Use

- 표준화된 curriculum, mentor feedback, automated grading이 반드시 필요할 때
- 구현물을 바로 production에 배포하려는 경우
- prerequisite와 학습 순서가 정해진 입문 course가 필요한 경우
- 보안, 장애복구, data migration, compatibility까지 검증된 reference implementation이 필요한 경우
- 외부 link와 오래된 dependency를 직접 점검할 시간이 없을 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/ripgrep/README|ripgrep]] — repository와 tutorial source를 탐색할 때 유용한 code search tool
- [[tech/devtools/git/github-repo-merge|GitHub Repository Merge]] — GitHub 기반 협업 흐름과 함께 읽기

## Sources

- [Build Your Own X 공식 repository](https://github.com/codecrafters-io/build-your-own-x)
- [GitHub REST API repository metadata](https://api.github.com/repos/codecrafters-io/build-your-own-x)
- [Build Your Own X submission template](https://github.com/codecrafters-io/build-your-own-x/blob/master/ISSUE_TEMPLATE.md)
- [Build Your Own X issues](https://github.com/codecrafters-io/build-your-own-x/issues)
- [CodeCrafters challenge overview](https://app.codecrafters.io/concepts/overview)
- [CodeCrafters: Pausing New Challenges](https://codecrafters.io/blog/pausing-new-challenges)

