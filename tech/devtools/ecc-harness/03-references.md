---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — References

## 공식 프로젝트와 배포 상태

| 자료 | 용도 |
|---|---|
| [ECC GitHub repository / README](https://github.com/affaan-m/ECC) | catalog, install route, 지원 harness의 1차 출처 |
| [ECC Releases](https://github.com/affaan-m/ECC/releases) | stable tag와 release note 확인 |
| [ECC CHANGELOG](https://github.com/affaan-m/ECC/blob/main/CHANGELOG.md) | main branch의 아직 배포되지 않았을 수 있는 변경 확인 |
| [ECC 공식 사이트](https://ecc.tools/) | 프로젝트 진입점과 문서 탐색 |
| [ecc-universal npm package](https://www.npmjs.com/package/ecc-universal) | npm registry version과 package metadata 확인 |

## Architecture / Security

- [ECC cross-harness architecture](https://github.com/affaan-m/ECC/blob/main/docs/architecture/cross-harness.md) — adapter와 portable layer의 경계를 읽는다.
- [AgentShield repository](https://github.com/affaan-m/agentshield) — scanner의 검사 범위와 사용법을 확인한다.
- [ecc-agentshield npm package](https://www.npmjs.com/package/ecc-agentshield) — CLI 배포물과 version을 확인한다.

## 읽는 순서와 검증 메모

1. README에서 목표 harness의 install route와 component model을 읽는다.
2. Releases와 npm registry를 대조해 실제 설치할 version/channel을 정한다.
3. cross-harness architecture에서 해당 adapter의 지원 범위를 확인한다.
4. AgentShield 문서로 scan output·baseline·CI integration을 검토한다.

> `CHANGELOG.md`의 main branch 항목은 release 증거가 아니다. 설치 전 release tag와 npm registry를 모두 확인한다.
