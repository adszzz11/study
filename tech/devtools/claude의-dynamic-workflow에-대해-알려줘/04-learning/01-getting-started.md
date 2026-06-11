---
date: 2026-06-09
tags:
  - tech
  - devtools
  - claude
  - dynamic-workflows
  - learning
status: learning
type: tech-tool-study
parent: "[[../README]]"
---

# Claude Dynamic Workflows - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 딥다이브]]

---

## 1. 사전 확인

| 항목 | 확인 방법 | 기준 |
|------|-----------|------|
| Claude Code version | `claude --version` | v2.1.154+ |
| 기능 활성화 | `/config` | Dynamic workflows enabled |
| 조직 정책 | admin settings | disabled 여부 확인 |
| 비용 한도 | team/admin settings 또는 개인 budget | token cap 필요 |

```bash
claude --version

# Claude Code session 안에서
/config
```

---

## 2. 첫 실습: 작은 directory audit

처음부터 repo-wide audit을 실행하지 말고, 디렉터리와 검증 기준을 좁힌다.

```text
ultracode: audit src/auth for missing permission checks.

Split by route/module.
For each finding, include file path, risk, evidence, and suggested fix.
Use verifier agents to remove false positives.
Stop when all files under src/auth are checked once and every finding has verifier confirmation.
Keep the workflow under a conservative token budget.
```

좋은 첫 workflow의 조건:

- scope가 작다: `src/auth`, `packages/api/routes`처럼 directory를 지정
- split 기준이 명확하다: route, module, package, file group
- verification 기준이 있다: false positive 제거, evidence 요구
- stop condition이 있다: 모든 파일 1회 확인, verifier confirmation 완료
- budget 언급이 있다: token cap, smaller model routing, 단계별 중단

---

## 3. 실행 중 관찰

`/workflows` UI에서 다음을 본다.

| 지표 | 의미 | 체크 포인트 |
|------|------|-------------|
| phase | 현재 단계 | discovery, analysis, verification, synthesis 구분 |
| agent count | 실행된 subagent 수 | 불필요한 fan-out 폭주 여부 |
| token usage | token 사용량 | 예상 budget 초과 여부 |
| elapsed time | 경과 시간 | stop condition이 작동하는지 |
| controls | pause/resume/stop/restart/save | runaway workflow 중단 |

```text
/workflows
```

실행 중 판단:

- token usage가 빠르게 증가하면 pause 후 scope를 줄인다.
- phase가 오래 멈춰 있으면 stop condition이 모호했는지 확인한다.
- findings가 많으면 verifier를 추가 요청한다.
- 결과가 좋으면 `s`로 저장해 project workflow로 재사용한다.

---

## 4. Built-in `/deep-research` 체험

research workflow는 Dynamic Workflows의 구조를 이해하기 좋다.

```text
/deep-research Compare Claude Dynamic Workflows, OpenAI Codex, and LangGraph for repo-wide security audits.
```

관찰할 점:

- source search fan-out이 어떻게 나뉘는가
- claim extraction과 source verification이 분리되는가
- cited report synthesis가 어떤 구조로 정리되는가
- contradiction이나 약한 근거를 어떻게 처리하는가

이 흐름은 [[study/tech/ai/llm-wiki-study]]의 raw source ingest나 [[study/tech/ai/autoresearch-study]]의 research loop와 연결해서 볼 수 있다.

---

## 5. 저장과 재사용

성공한 workflow는 저장해서 slash command처럼 재실행한다.

| 저장 위치 | 용도 |
|----------|------|
| `.claude/workflows/` | project-local workflow |
| `~/.claude/workflows/` | user-global workflow |

```text
# /workflows UI에서
s

# 이후 project workflow command처럼 재사용
/workflow-name
```

저장 전에 확인할 것:

- repository-specific path가 너무 하드코딩되어 있지 않은가
- 권한이 강한 command가 포함되어 있지 않은가
- token budget과 stop condition이 포함되어 있는가
- verifier agent가 false positive를 제거하는가

---

## 관련 노트

- [[study/tech/ai/claude/03-claude-code]]
- [[study/tech/ai/claude/08-subagents]]
- [[study/tech/ai/codex]]
