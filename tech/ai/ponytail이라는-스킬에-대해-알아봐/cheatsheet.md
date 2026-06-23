---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - cheatsheet
  - ponytail
type: tech-tool-study
parent: "[[README]]"
---

# ponytail skill - 치트시트

> [[README|목차로 돌아가기]]

---

## 핵심 판단

| 질문 | 답 |
|------|----|
| `ponytail`은 공식 공개 skill인가? | 2026-06-24 기준 확인되지 않음 |
| 가장 타당한 해석은? | Agent Skills/Claude Skills 기반 custom skill 이름 |
| 필수 파일은? | `ponytail/SKILL.md` |
| 필수 metadata는? | `name`, `description` |
| 핵심 설계 원리 | progressive disclosure |

## 기본 구조

```text
ponytail/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## 최소 SKILL.md

```markdown
---
name: ponytail
description: Use this skill when the user asks to run the Ponytail workflow. Do not use it for unrelated hairstyle, fashion, or generic summarization tasks.
---

# Ponytail Skill

## Procedure

1. Confirm the workflow goal.
2. Check required inputs.
3. Run the documented steps.
4. Validate the result.
5. Report assumptions, output, and open issues.
```

## Description 작성법

| 포함할 것 | 이유 |
|-----------|------|
| 사용 조건 | activation 정확도 향상 |
| 제외 조건 | false positive 감소 |
| 입력/출력 힌트 | agent가 준비물을 판단 |
| 위험 작업 여부 | permission/confirmation 판단 |

## 파일 분리 기준

| 내용 | 위치 |
|------|------|
| 짧은 절차 | `SKILL.md` |
| 긴 정책/도메인 지식 | `references/` |
| 계산/검증/변환 | `scripts/` |
| template/sample | `assets/` |

## 비교 한 줄

| 기술 | 기억할 문장 |
|------|-------------|
| Agent Skill | agent가 특정 업무를 수행하는 방법을 package로 제공 |
| MCP | agent가 외부 tool/data를 발견하고 호출하는 protocol |
| Custom instructions | 항상 적용되는 짧은 규칙 |
| Plugin | skills/hooks/MCP 등을 묶는 배포 단위 |
| Prompt template | 재사용 가능한 prompt 조각 |

## 평가 체크

| 체크 | 기준 |
|------|------|
| True positive | 써야 할 task에서 skill이 켜짐 |
| False positive | 무관한 task에서 skill이 꺼짐 |
| Completeness | 절차, 입력, 출력, 검증이 있음 |
| Script safety | 실행 파일이 안전하고 권한이 제한됨 |
| Context cost | 긴 내용이 references로 분리됨 |

## 보안 검색

```bash
rg -n "curl|wget|rm -rf|ssh|eval|TOKEN|SECRET|HOME|\\.ssh" ponytail/
```

## 관련 노트

- [[study/tech/ai/claude/05-skills]]
- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/thin-harness-fat-skills]]
- [[study/tech/ai/codex]]

