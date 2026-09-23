---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — Getting started

## 목표: 최소 profile을 안전하게 평가하기

처음부터 전체 catalog, hooks, memory를 켜지 않는다. 현재 사용하는 언어/framework rule pack 하나와 `rules/common`, `tdd-workflow` 같은 skill 하나만 선택해 작은 feature에서 효과를 검증한다.

## 1. 사전 확인

```bash
# Node.js 18+인지 확인
node --version

# 실제 배포 version은 GitHub release와 npm registry에서 함께 확인한다.
npm view ecc-universal version
```

`npm view`의 값만으로 channel을 결정하지 않는다. [GitHub Releases](https://github.com/affaan-m/ECC/releases) tag와 release note도 대조한다.

## 2. Codex 설치 계획을 dry-run으로 보기

```bash
npx ecc-universal install --guided --harness codex --dry-run
```

확인할 항목:

- 생성·수정 예정 파일과 target channel
- 선택 가능한 profile, rules, skills
- hook 또는 MCP config의 추가 여부와 실행 권한
- 이미 존재하는 plugin, manual copy, 다른 installer의 흔적

> 한 harness에는 하나의 설치 경로만 선택한다. plugin, guided installer, manual copy를 섞으면 중복 hook·command와 config 충돌이 생길 수 있다.

## 3. 최소 component 선택

| 우선순위 | 선택 | 이유 |
|---|---|---|
| 1 | `rules/common` | 공통 작업 규칙의 기준점을 만든다. |
| 2 | 현재 언어/framework pack 하나 | 현재 repo에만 관련된 guidance를 추가한다. |
| 3 | TDD skill 하나 | test-first 흐름을 작은 단위로 검증한다. |
| 나중 | hooks, memory, broad catalog | side effect·context·data flow를 평가한 뒤 도입한다. |

## 4. Security baseline 검토

```bash
# 결과를 파일에 적용하지 않는 scan이다. JSON finding을 사람이 검토한다.
npx -y ecc-agentshield scan --path . --format json
```

CI에는 JSON/SARIF 결과와 baseline drift gate를 고려할 수 있다. 다만 finding의 severity만 보지 말고 permission, hook command, secret exposure, MCP endpoint를 diff와 함께 검토한다.

## 5. 첫 평가 과제

작은 feature 하나를 아래 순서로 끝낸다.

```text
plan → test → implement → review → verify → handoff
```

새 session에서 handoff/search를 사용해 재탐색 시간, test failure 수, review finding, token cost를 이전 방식과 비교한다. 결과가 없다면 hooks/memory 확대보다 minimal configuration을 유지한다.

## Sources

- https://github.com/affaan-m/ECC
- https://www.npmjs.com/package/ecc-universal
- https://github.com/affaan-m/agentshield
- https://www.npmjs.com/package/ecc-agentshield
