---
date: 2026-06-09
tags:
  - tech
  - devtools
  - claude
  - dynamic-workflows
  - cheatsheet
status: learning
type: tech-tool-study
parent: "[[README]]"
---

# Claude Dynamic Workflows - Cheatsheet

> [[05-projects|이전: 프로젝트]] | [[README|목차로 돌아가기]]

---

## Trigger

| 방법 | 예시 |
|------|------|
| prompt phrase | `use a workflow: audit src/auth for permission checks` |
| high effort keyword | `ultracode: migrate deprecated API callsites` |
| effort setting | `/effort ultracode` |
| built-in workflow | `/deep-research <question>` |
| workflow UI | `/workflows` |

---

## Limits

| 항목 | 값/주의 |
|------|---------|
| 상태 | research preview |
| version | Claude Code v2.1.154+ 확인 |
| concurrent agents | 한 run 최대 16 |
| total agents | 한 run 최대 1,000 |
| 비용 | 일반 session보다 token 사용량이 훨씬 클 수 있음 |
| 저장 위치 | `.claude/workflows/`, `~/.claude/workflows/` |

---

## Prompt Template

```text
ultracode: <goal>

Scope:
- <target directories/files>
- <explicit exclusions>

Split:
- <split by package/route/module/file group/source type>

Verification:
- <verifier agent role>
- <evidence requirement>
- <false positive handling>

Output:
- <schema: file, line, risk, evidence, fix, verifier status>

Budget:
- <token/agent/time constraints>
- <smaller model routing if appropriate>

Stop:
- <clear completion condition>

Safety:
- <do not edit / ask before patch / avoid destructive commands>
```

---

## Pattern 선택

| 하고 싶은 일 | Pattern |
|--------------|---------|
| repo 전체를 넓게 훑기 | fan-out-and-synthesize |
| finding 품질 높이기 | adversarial verification |
| test/refactor 후보 많이 만들기 | generate-and-filter |
| 여러 해결책 비교 | tournament |
| migration 완료까지 반복 | loop-until-done |

---

## 좋은 요청 vs 위험한 요청

| 구분 | 예시 |
|------|------|
| 좋은 요청 | `ultracode: audit src/auth only, split by route, verifier-confirm findings, do not edit files` |
| 위험한 요청 | `ultracode: fix all security issues in this repo` |
| 좋은 요청 | `use a workflow: discover deprecated API callsites and report a migration plan` |
| 위험한 요청 | `migrate everything and run all possible tests until done` |

---

## 운영 체크리스트

- [ ] `/config`에서 Dynamic workflows 활성화 확인
- [ ] 작은 directory로 첫 실행
- [ ] `/workflows`에서 phase/token/agent count 확인
- [ ] verifier phase 포함
- [ ] stop condition 명시
- [ ] patch 전 report-only 실행
- [ ] 성공한 workflow만 저장
- [ ] 저장 전 path, permissions, budget 검토

---

## 관련 노트

- [[study/tech/ai/claude/03-claude-code]]
- [[study/tech/ai/claude/08-subagents]]
- [[study/tech/ai/thin-harness-fat-skills]]
- [[study/tech/ai/codex]]
