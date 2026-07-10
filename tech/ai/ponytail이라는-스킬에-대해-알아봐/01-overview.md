---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - claude-skills
  - overview
  - ponytail
type: tech-tool-study
parent: "[[README]]"
---

# ponytail skill - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - ponytail skill이란?

> **한 줄 정의**: `ponytail`이라는 공개 표준/공식 Skill은 확인되지 않았고, Agent Skills/Claude Skills 포맷으로 만들 수 있는 custom skill 이름으로 해석하는 것이 안전하다.

### 현재 확인된 상태

| 항목 | 판단 |
|------|------|
| 공개 표준 | `ponytail`이라는 공식 skill 표준은 확인되지 않음 |
| marketplace skill | 널리 쓰이는 공개 marketplace skill로 확인되지 않음 |
| package ecosystem | Python/npm/crates의 대표 package로 보기 어려움 |
| built-in skill | Codex/Claude built-in skill로 확인되지 않음 |
| 가장 타당한 해석 | 특정 조직/사용자의 private custom Agent Skill |

따라서 `ponytail skill`을 학습할 때의 핵심은 “ponytail이 무엇을 한다”가 아니라, **알 수 없는 skill 이름을 만났을 때 공개 근거를 검증하고 custom skill로 설계하는 방법**이다.

## 2. Why - 왜 Skill 포맷인가?

LLM agent에게 반복 업무를 시킬 때 단순 prompt만으로는 다음 문제가 생긴다.

- 긴 절차와 예외가 매번 context에 들어가 token cost가 커진다.
- 도메인 지식, template, script, sample output이 흩어져 재사용성이 낮다.
- agent가 언제 어떤 지침을 써야 하는지 activation 기준이 불명확하다.
- deterministic processing이 필요한 작업까지 자연어 추론에 맡기게 된다.

Agent Skills는 이 문제를 폴더 단위 package로 푼다.

```text
ponytail/
├── SKILL.md          # 필수: metadata + activation + 절차
├── scripts/          # 선택: deterministic processing
├── references/       # 선택: 긴 정책/도메인 문서
└── assets/           # 선택: templates, examples, media
```

## 3. 핵심 특징

### SKILL.md 중심 구조

`SKILL.md`는 skill의 entry point다. Agent Skills spec에서는 YAML frontmatter의 `name`, `description`을 필수로 보고, `name`은 폴더명과 일치해야 한다.

```markdown
---
name: ponytail
description: Use this skill when ...
---

# Ponytail Skill

## Procedure

1. ...
2. ...
3. ...
```

### Progressive Disclosure

처음부터 skill 전체를 context에 넣지 않는다.

| 단계 | 로드되는 정보 | 목적 |
|------|---------------|------|
| 시작 | `name`, `description` | 어떤 skill이 있는지 가볍게 인식 |
| 활성화 | 전체 `SKILL.md` | 절차와 판단 기준 확인 |
| 필요 시 | `scripts/`, `references/`, `assets/` | 긴 자료와 실행 파일을 선택적으로 사용 |

이 구조는 [[study/tech/ai/model-context-protocol-mcp]]의 tool/resource discovery와 비슷한 문제의식이 있지만, Skill은 protocol server가 아니라 **agent instruction package**에 가깝다.

### 실행성과 이식성

Skill은 prompt bundle만이 아니다. Python, Bash, JavaScript script를 포함해 반복 변환, 검증, formatting 같은 deterministic step을 agent가 실행하게 만들 수 있다.

| 특징 | 의미 |
|------|------|
| Instruction | agent가 따라야 할 업무 절차 |
| Script | 계산/변환/검증을 재현 가능하게 처리 |
| Reference | 긴 정책, schema, domain knowledge 보관 |
| Asset | template, sample, 이미지 등 작업 재료 |
| Portability | Claude apps, Claude Code, API, compatible agent에서 재사용 가능하도록 설계 |

## 4. 보안 관점

Skill은 code execution을 포함할 수 있다. 특히 third-party skill은 자연어 지침만이 아니라 실행 가능한 script와 template까지 포함하므로 review가 필요하다.

| 위험 | 대응 |
|------|------|
| 악성 script | trusted source 사용, code review, checksum 확인 |
| 과도한 권한 | sandbox, least privilege, workspace boundary |
| prompt injection | external content를 untrusted data로 취급 |
| secret leakage | env var 접근 제한, redaction, logging review |
| false activation | `description`을 구체화하고 negative cases 추가 |

## 5. ponytail에 적용하는 결론

- `ponytail`이라는 이름만으로 공개 표준/공식 skill이라고 보기는 어렵다.
- 실제 사용하려면 먼저 목적을 정의해야 한다. 예: research workflow, PR review checklist, document formatter.
- `description`에는 “언제 활성화해야 하는지”와 “언제 쓰면 안 되는지”를 함께 넣는 것이 좋다.
- 반복 로직이 있다면 `scripts/`에 두고, 긴 배경 지식은 `references/`로 옮긴다.
- [[study/tech/ai/claude/05-skills]]와 [[study/tech/ai/thin-harness-fat-skills]]를 함께 보면 skill 중심 설계의 장단점이 명확해진다.

---

## 참고

- [Anthropic, Introducing Agent Skills](https://claude.com/blog/skills)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Code Docs, Extend Claude with skills](https://code.claude.com/docs/en/skills)

