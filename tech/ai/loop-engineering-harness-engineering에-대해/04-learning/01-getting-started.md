---
date: 2026-06-23
tags: [tech, ai, getting-started, agent-harness, agents-md]
status: learning
type: tech-tool-study
---

# 04-1. Getting Started — 작은 Repo에 Harness 만들기

## 목표

처음부터 LangGraph나 복잡한 platform을 만들 필요는 없다. 작은 repo에서는 `AGENTS.md`, 명확한 테스트 명령, 완료 보고 양식만으로도 harness의 절반은 시작된다.

## 1. 최소 Harness 구조

```text
repo/
├── AGENTS.md          # agent instruction
├── package.json       # test/build command
├── src/
└── tests/
```

`AGENTS.md`는 coding agent용 README처럼 쓴다.

```md
# AGENTS.md

## Setup
- Install dependencies with `npm install`.

## Test
- Run `npm test` before reporting completion.
- Run `npm run lint` when editing TypeScript files.

## Code Style
- Keep changes small and local.
- Follow existing file structure.

## Forbidden Actions
- Do not run production deploy commands.
- Do not rewrite lockfiles unless dependency changes are requested.
- Do not delete user data or migration files without explicit approval.

## Completion Report
- List changed files.
- Explain why each change was needed.
- Include exact verification command and result.
```

## 2. 간단한 Agent Loop를 문서화하기

```text
1. 목표를 checklist로 바꾼다.
2. 관련 파일을 찾는다.
3. 최소 변경을 만든다.
4. 테스트를 실행한다.
5. 실패하면 log를 읽고 원인을 분류한다.
6. 다시 수정한다.
7. 성공 증거와 변경 요약을 남긴다.
```

agent에게는 아래처럼 시킨다.

```text
이 작업은 아래 loop로 진행해줘.
- 먼저 요구사항을 checklist로 정리
- 관련 파일을 찾아 최소 범위로 수정
- `npm test`로 검증
- 실패하면 로그 기반으로 원인을 분류하고 재시도
- 완료 보고에는 변경 파일, 이유, 검증 명령을 포함
```

## 3. Verification Protocol 만들기

| 작업 유형 | 완료 증거 |
|-----------|-----------|
| 버그 수정 | 재현 테스트 추가/수정 + 관련 test pass |
| UI 수정 | 스크린샷 또는 Playwright 확인 |
| API 수정 | unit/integration test + 응답 예시 |
| 리팩터링 | 기존 test pass + public behavior 변화 없음 |
| 문서 작업 | 링크, frontmatter, 파일 구조 확인 |

```bash
# 검증 명령 예시
npm test
npm run lint
pytest
go test ./...
```

## 4. Failure Attribution 연습

실패를 "안 됨"으로 두지 말고 분류한다.

| 실패 유형 | 질문 | 다음 행동 |
|-----------|------|-----------|
| `context failure` | 잘못된 파일을 봤나? | search 범위 재설정 |
| `tool failure` | 명령이 없거나 환경이 다른가? | setup 확인, 대체 명령 찾기 |
| `test failure` | 코드 변경이 regression을 만들었나? | 실패 test 중심으로 patch |
| `requirement failure` | 요구사항을 잘못 해석했나? | task checklist 재작성 |
| `permission failure` | 하면 안 되는 작업이 필요한가? | 사람 승인 요청 |

## 5. 첫 실습

```text
실습: 작은 Todo 앱 repo에 harness 추가

1. AGENTS.md 작성
2. test/lint/build 명령 확인
3. "완료 보고 양식" 추가
4. agent에게 사소한 버그를 맡김
5. 변경 보고와 실제 test result가 맞는지 확인
```

## 6. 좋은 시작점 체크리스트

- [ ] `AGENTS.md`가 있다.
- [ ] setup/test/build 명령이 명시되어 있다.
- [ ] 금지 명령과 승인 필요 작업이 적혀 있다.
- [ ] 완료 조건이 "느낌"이 아니라 test/log/report로 표현된다.
- [ ] 실패 시 재시도 방식이 있다.
- [ ] 사람이 리뷰할 지점이 정해져 있다.

## 관련 노트

- [[study/tech/ai/codex]]
- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/model-context-protocol-mcp]]
