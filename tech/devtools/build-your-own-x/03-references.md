---
date: 2026-07-17
tags: [tech]
type: tech-tool-study
status: draft
---

# Build Your Own X — References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 자료

1. [Build Your Own X 공식 repository](https://github.com/codecrafters-io/build-your-own-x) — catalog, license/waiver, contribution 안내
2. [Tutorials section](https://github.com/codecrafters-io/build-your-own-x#tutorials) — category와 외부 tutorial 목록
3. [GitHub REST API metadata](https://api.github.com/repos/codecrafters-io/build-your-own-x) — stars, forks, activity, default branch 등 live metadata
4. [Submission template](https://github.com/codecrafters-io/build-your-own-x/blob/master/ISSUE_TEMPLATE.md) — language, title, URL, category 제출 형식
5. [Issues](https://github.com/codecrafters-io/build-your-own-x/issues) — 신규 제안, broken link, maintenance backlog 확인
6. [Pull requests](https://github.com/codecrafters-io/build-your-own-x/pulls) — 추가·수정 제안과 review 맥락 확인
7. [Commit history](https://github.com/codecrafters-io/build-your-own-x/commits/master/) — catalog 변경 시점 확인

## 대안과 보완 자료

- [CodeCrafters Concepts Overview](https://app.codecrafters.io/concepts/overview) — staged challenge와 `git push` feedback model
- [CodeCrafters: Pausing New Challenges](https://codecrafters.io/blog/pausing-new-challenges) — 2026년 platform 운영 상태
- [Coding Challenges](https://codingchallenges.fyi/) — 작은 language-agnostic specification
- [Project Based Learning](https://github.com/practical-tutorials/project-based-learning) — language 중심 project index
- [Nand2Tetris](https://www.nand2tetris.org/) — hardware부터 OS까지 이어지는 fixed curriculum
- [Teach Yourself CS](https://teachyourselfcs.com/) — theory와 systems foundation 보완

## Tutorial 검증 checklist

외부 tutorial을 선택할 때 repository에 올라와 있다는 사실만으로 품질을 가정하지 않는다.

| 확인 항목 | 확인 방법 |
|---|---|
| Link health | URL이 열리고 redirect target이 의도한 문서인지 확인 |
| 최신성 | 게시/수정일, dependency version, deprecated API 확인 |
| 완결성 | 마지막 chapter, source code, expected output 존재 여부 확인 |
| 재현성 | clean environment에서 setup부터 실행 가능한지 확인 |
| License | tutorial text와 sample code의 license를 각각 확인 |
| Scope | toy implementation에서 의도적으로 빠진 기능 확인 |
| Feedback | test, fixture, expected behavior가 있는지 확인 |
| Security | unsafe default를 production pattern으로 소개하지 않는지 확인 |

## 출처 기록 template

```markdown
### Tutorial title

- URL:
- 확인일: 2026-07-17
- Language / version:
- 예상 소요 시간:
- Prerequisite:
- 제공 test:
- 누락된 production concern:
- License:
```

## Snapshot 읽는 법

이 노트의 526,000 stars, 49,800 forks 같은 값은 2026-07-17 snapshot이다. 인기도·활동성 수치가 필요하면 REST API를 다시 조회하고 날짜와 함께 기록한다. 외부 tutorial 목록도 변하므로 특정 항목을 인용할 때 permalink 또는 확인일을 남긴다.

## Sources

- [Build Your Own X repository](https://github.com/codecrafters-io/build-your-own-x)
- [GitHub REST API metadata](https://api.github.com/repos/codecrafters-io/build-your-own-x)
- [Build Your Own X issues](https://github.com/codecrafters-io/build-your-own-x/issues)
- [Build Your Own X pull requests](https://github.com/codecrafters-io/build-your-own-x/pulls)

