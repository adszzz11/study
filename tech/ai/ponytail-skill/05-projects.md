---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - projects
  - ponytail
type: tech-tool-study
parent: "[[README]]"
---

# ponytail skill - 실전 프로젝트

> [[04-learning/02-deep-dive|이전: 심화]] | [[README|목차]] | [[cheatsheet|다음: 치트시트]]

---

## 1. 사내 workflow skill

목표: 반복되는 PR review, release note, incident report를 `ponytail` workflow로 표준화한다.

| 구성 | 내용 |
|------|------|
| `SKILL.md` | 작업 순서, 입력/출력, 검증 기준 |
| `references/checklist.md` | 팀별 review checklist |
| `assets/report-template.md` | 결과 보고 template |
| `scripts/lint_report.py` | 필수 section 누락 검사 |

예시 activation:

```text
Use the ponytail workflow to review this PR and produce a risk-focused checklist.
```

## 2. Data skill

목표: CSV/Excel 변환, validation, chart generation 절차를 skill로 묶는다.

| 작업 | skill화 포인트 |
|------|----------------|
| CSV schema 검사 | script로 column/type/null 검증 |
| Excel cleanup | 절차와 edge case를 `SKILL.md`에 기록 |
| chart generation | template과 style guide를 `assets/`에 저장 |
| report 작성 | output format을 reference로 고정 |

관련: [[study/tech/data/dolt]]처럼 data 변경 이력을 다루는 도구와 함께 쓰면 검증 흐름을 더 명확히 만들 수 있다.

## 3. Scraping/Research skill

목표: source ranking, query expansion, citation formatting 규칙을 package로 만든다.

| 구성 | 설명 |
|------|------|
| query expansion | 한국어/영어 keyword 생성 규칙 |
| source ranking | official docs, source repo, paper 우선순위 |
| citation formatting | Markdown reference table format |
| quality gate | 날짜, 출처, 불확실성 표시 |

이 프로젝트는 [[study/tech/ai/autoresearch-study]]와 잘 연결된다.

## 4. Devtools skill

목표: repo별 build/run/test recipe, debugging playbook, migration checklist를 skill로 묶는다.

```text
devtools-ponytail/
├── SKILL.md
├── scripts/
│   ├── run_checks.sh
│   └── summarize_failures.py
└── references/
    ├── build-matrix.md
    └── migration-checklist.md
```

| 기대 효과 | 설명 |
|-----------|------|
| onboarding | 새 agent가 repo 규칙을 빠르게 이해 |
| reproducibility | test/build 명령이 문서화됨 |
| quality | 완료 전 검증 루프를 강제 |

## 5. 문서 skill

목표: brand guideline, proposal template, compliance wording을 references/assets로 묶는다.

| 파일 | 내용 |
|------|------|
| `references/voice-and-tone.md` | 문체와 금지 표현 |
| `references/compliance.md` | 법무/보안 문구 |
| `assets/proposal-template.md` | 제안서 template |
| `scripts/check_terms.py` | 금지어/필수어 검사 |

## 우선순위

| 우선순위 | 프로젝트 | 이유 |
|----------|----------|------|
| 1 | 사내 workflow skill | Skill의 장점인 절차+검증을 바로 확인 가능 |
| 2 | Research skill | source ranking과 citation format처럼 반복 규칙이 많음 |
| 3 | Devtools skill | repo-specific workflow를 agent에게 안정적으로 전달 |
| 4 | Data skill | script 분리의 효과가 큼 |
| 5 | 문서 skill | references/assets 구조 연습에 좋음 |

## 관련 노트

- [[study/tech/ai/lazy-codex]] - 완료 검증 루프 설계
- [[study/tech/ai/model-context-protocol-mcp]] - 외부 tool/data 연동
- [[study/tech/ai/autoresearch-study]] - research workflow 자동화
- [[study/tech/ai/llm-wiki-study]] - 지식 노트와 agent workflow 연결

