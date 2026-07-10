---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - getting-started
type: tech-tool-study
parent: "[[../README]]"
---

# GPT-5.6 in Codex - 시작하기

> [[../03-references|이전: 참고자료]] | [[02-deep-dive|다음: 심화]]

---

## 목표

이 단계의 목표는 GPT-5.6을 "새 모델 이름"으로만 외우지 않고, 실제 Codex/API 작업에서 **어떤 tier와 reasoning effort를 고를지** 판단하는 것이다.

## 1. 모델 선택

| 작업 | 추천 시작점 | 이유 |
|------|-------------|------|
| 어려운 codebase refactor | `gpt-5.6-sol` | flagship reasoning/coding 성능 |
| 일상 coding assist | `gpt-5.6-terra` | 비용/성능 균형 |
| 대량 문서/로그 triage | `gpt-5.6-luna` | high-volume low-cost |
| 모델명만 빠르게 지정 | `gpt-5.6` | dossier 기준 Sol alias |

### 선택 규칙

- 실패 비용이 큰 작업은 `sol`부터 시작한다.
- 반복량이 많고 검증이 쉬운 작업은 `terra` 또는 `luna`를 실측한다.
- 기존 GPT-5.5/5.4 사용자는 같은 effort와 한 단계 낮은 effort를 비교한다.
- latency/cost가 중요하면 "모델 tier 낮추기"와 "effort 낮추기"를 따로 실험한다.

## 2. Reasoning effort 튜닝

| effort | 시작 용도 | 체크할 것 |
|--------|-----------|-----------|
| `none` | 단순 format conversion | hallucination보다 누락/형식 |
| `low` | 빠른 요약, boilerplate | edge case 처리 |
| `medium` | 일반 default | 품질/비용 균형 |
| `high` | 설계, 디버깅, review | test와 reasoning trace 품질 |
| `xhigh` | 복잡한 실패 분석 | latency/cost 대비 개선폭 |
| `max` | release-critical task | 품질 우선, 비용 허용 여부 |

```text
실험 순서:
1. terra + medium
2. terra + low
3. sol + medium
4. sol + high
5. sol + max

측정:
- 작업 성공률
- 수정 diff 품질
- test 통과 여부
- elapsed time
- token/cost
```

## 3. Codex CLI 실습

dossier 기준 Codex CLI는 project directory에서 `codex`를 실행하고 ChatGPT sign-in 후 작업을 시작한다.

```bash
# project root에서 실행
codex

# 첫 작업 예시
# "이 repo의 test 명령을 파악하고 AGENTS.md에 개발 규칙 초안을 작성해줘"
```

### 실습 체크리스트

- [ ] project root에서 Codex CLI를 실행한다.
- [ ] 모델 선택 화면 또는 설정에서 GPT-5.6 tier가 보이는지 확인한다.
- [ ] 작은 task를 `terra/medium`으로 실행한다.
- [ ] 같은 task를 `sol/high`로 실행해 diff 품질과 시간 차이를 비교한다.
- [ ] `AGENTS.md`가 있으면 Codex가 run 시작 시 읽는지 확인한다.

## 4. Codex cloud 실습

Codex cloud는 isolated cloud environments에서 repo task를 병렬 실행하는 흐름이다.

```text
GitHub 연결
  -> environment 생성
  -> dependencies/secrets 설정
  -> task 실행
  -> diff review
  -> PR 생성
```

### 첫 cloud task 예시

```text
Task:
Find one small failing or flaky test in this repository, explain the cause,
fix it in a minimal diff, run the relevant test command, and open a PR.
```

### 확인할 것

- [ ] dependency install이 재현 가능한지
- [ ] secrets가 필요한 task와 필요 없는 task가 분리되는지
- [ ] lint/test command가 명확한지
- [ ] diff가 작은지
- [ ] PR 설명에 검증 결과가 들어가는지

## 5. AGENTS.md 구성

`AGENTS.md`는 Codex가 매 run 시작 시 읽는 repo/team convention 파일이다. GPT-5.6 자체 성능보다도, 이 파일이 실제 결과 품질에 큰 영향을 줄 수 있다.

```markdown
# AGENTS.md

## Commands
- Test: npm test
- Lint: npm run lint
- Typecheck: npm run typecheck

## Rules
- Keep diffs minimal.
- Do not change public APIs without updating tests and docs.
- Report commands run and failures honestly.
```

## 관련 노트

- [[study/tech/ai/lazy-codex]] - Codex 작업 완료 검증 루프
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent 운영 패턴
- [[study/tech/ai/model-context-protocol-mcp]] - tool integration 확장

## References

- [OpenAI latest model guide](https://developers.openai.com/api/docs/guides/latest-model)
- [Codex CLI docs](https://learn.chatgpt.com/codex/cli)
- [Codex cloud docs](https://learn.chatgpt.com/codex/cloud)
- [AGENTS.md docs](https://learn.chatgpt.com/codex/agent-configuration/agents-md)
