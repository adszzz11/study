---
date: 2026-07-09
tags: [tech, ai, claude, codex, gemini, projects, workflow]
status: published
type: tech-tool-study
---

# 05. Projects — 실전 적용 아이디어

## 1. 3-agent coding pipeline

| 단계 | 담당 | 산출물 |
|------|------|--------|
| 조사 | Gemini | 공식 문서, API 변화, migration constraint |
| 설계 | Claude Fable/Sonnet | architecture plan, risk map, task breakdown |
| 구현 | Codex | scoped diff, tests, fix loop |
| 리뷰 | Gemini 또는 Claude | regression/security/test gap |
| 최종 | 사람 | merge decision |

```text
Gemini → Claude → Codex → Reviewer → Human merge
```

## 2. Legacy migration

목표: 오래된 framework/library를 새 버전으로 옮긴다.

| 역할 | 할 일 |
|------|-------|
| Claude Fable | 전체 migration strategy, risk map, 단계별 PR 계획 |
| Gemini | 최신 공식 migration guide 확인, breaking changes 조사 |
| Codex | package별 PR 구현, failing test 수정 |
| Reviewer | compatibility gap, hidden regression 점검 |

완료 조건:

- 기존 test suite PASS
- migration guide required step 반영
- rollback path 존재
- user-facing behavior 변화 문서화

## 3. Bug triage loop

```text
1. Codex: failing test 재현
2. Claude: root cause 분석과 fix plan
3. Codex: 최소 diff 구현
4. Gemini: 관련 issue/release note 검색
5. Claude/Codex: regression test 추가
```

## 4. Security-safe review

Fable safeguard 때문에 막히는 offensive 요청은 피하고, defensive workflow로 명확히 제한한다.

| 허용 중심 | 피할 것 |
|-----------|---------|
| secure coding review | exploit weaponization |
| dependency vulnerability patch | stealth/persistence 구현 |
| log analysis | credential theft 자동화 |
| configuration hardening | 공격 절차 자동화 |
| incident report 요약 | 우회/은닉 기법 개선 |

프롬프트 예:

```text
이 diff를 defensive secure coding 관점에서 리뷰해.
실행 가능한 공격 절차를 만들지 말고,
취약한 코드 위치, 영향, 안전한 patch 방향, 추가 test만 제안해.
```

## 5. Knowledge work pipeline

대규모 research나 문서 작업에도 같은 패턴을 쓴다.

```text
Gemini: 자료 수집과 긴 문서 요약
Claude Fable: thesis, outline, argument map
Codex: repo 내 markdown/사이트 반영
Reviewer: citation gap, contradiction, outdated claim 확인
```

## 6. 개인 운용 템플릿

```text
작업: <한 줄 목표>
제약: <수정 금지 영역, API compatibility, deadline>
완료 조건: <tests/docs/review 조건>

Claude:
- repo 탐색
- risk map
- plan 작성

Codex:
- Step N 구현
- test 실행
- failure fix

Gemini:
- 공식 문서 검증
- long-context review
- outdated assumption 탐지
```

## 관련 노트

- [[codex/05-projects]] · [[claude/09-agent-teams]] · [[agent-orchestration/cli-agents]] · [[lazy-codex/05-projects]]
