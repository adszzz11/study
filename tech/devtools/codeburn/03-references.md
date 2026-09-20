---
date: 2026-08-17
tags: [tech]
type: tech-tool-study
status: draft
---

# CodeBurn — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 공식 진입점

| 자료 | 용도 |
|---|---|
| [GitHub repository](https://github.com/getagentseal/codeburn) | source, README, issue, release 확인 |
| [Official docs](https://codeburn.app/docs) | 개념, feature, 사용법 |
| [npm package](https://www.npmjs.com/package/codeburn) | stable version과 package metadata 확인 |
| [CHANGELOG](https://github.com/getagentseal/codeburn/blob/main/CHANGELOG.md) | version별 command와 behavior 변화 확인 |
| [GitHub Issues](https://github.com/getagentseal/codeburn/issues) | provider parsing과 정확도 문제 확인 |

## 주제별 문서

| 질문 | 먼저 읽을 문서 |
|---|---|
| 어디서 데이터를 읽는가? | [Data Locations](https://codeburn.app/docs/data-locations) |
| provider별 추정과 제약은? | [Provider Notes](https://codeburn.app/docs/provider-notes) |
| model별 비용은 어떻게 계산하는가? | [Models](https://codeburn.app/docs/models) |
| 낭비 탐지는 무엇을 보는가? | [Optimize](https://codeburn.app/docs/optimize) |
| model 효율을 어떻게 비교하는가? | [Compare](https://codeburn.app/docs/compare) |
| Git delivery와 어떻게 연결하는가? | [Yield](https://codeburn.app/docs/yield) |
| export와 status output은? | [Status & Export](https://codeburn.app/docs/status-export) |
| 설치 방식과 요구사항은? | [Installation](https://codeburn.app/docs/installation) |

## 버전 확인 체크리스트

- [ ] `codeburn --version`과 npm stable version 비교
- [ ] repository README, docs, npm의 integration 수가 같은지 확인
- [ ] `package.json`의 `engines.node` 확인
- [ ] 사용하려는 subcommand의 `--help` 확인
- [ ] provider 관련 open issue와 최근 changelog 확인
- [ ] cache schema 변경이나 historical recomputation 여부 확인

> [!note] 2026-08-17 snapshot
> dossier 기준 npm stable은 `v0.9.19`·36 integrations, 현재 `main`/문서는 40 integrations다. 공식 설치 페이지는 Node.js 20+라고 설명하지만 현재 package metadata는 `>=22.13.0`을 요구한다. 실사용 baseline은 Node.js 22.13+로 잡는다.

## 검증 질문

새 version을 도입할 때 다음 질문을 원본 log sample과 함께 확인한다.

1. session 수와 provider 자체 history가 대략 일치하는가?
2. timezone과 날짜 경계가 기대한 reporting period와 맞는가?
3. cumulative token이 message별 token과 중복 합산되지 않았는가?
4. unknown/Auto model의 가격 가정이 화면에 명확히 표시되는가?
5. subscription-covered cost와 실제 out-of-pocket이 분리되는가?
6. pseudonymization과 export가 project name을 의도대로 다루는가?

## Sources

- https://codeburn.app/docs
- https://github.com/getagentseal/codeburn
- https://www.npmjs.com/package/codeburn
- https://github.com/getagentseal/codeburn/blob/main/package.json
- https://github.com/getagentseal/codeburn/blob/main/CHANGELOG.md
- https://github.com/getagentseal/codeburn/issues

