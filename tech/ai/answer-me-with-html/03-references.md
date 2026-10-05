---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Answer me with HTML — References

> [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

## Primary Sources

| 자료 | 확인할 내용 |
|---|---|
| [GitHub README](https://github.com/QingYunA/answer-me-with-html) | 설치, 기능, example, 지원 template/component |
| [SKILL.md](https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/skills/answer-me-with-html/SKILL.md) | agent에게 전달되는 authoring workflow와 format |
| [CLI source](https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/src/cli.js) | command surface와 실제 구현 근거 |
| [package.json](https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/package.json) | Node version, dependency, package metadata |
| [benchmark README](https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/bench/README.md) | 측정 조건, 수치, 재현 절차와 한계 |
| [CONTRIBUTING.md](https://raw.githubusercontent.com/QingYunA/answer-me-with-html/main/CONTRIBUTING.md) | build/test·기여 규약 |
| [skills.sh listing](https://www.skills.sh/qingyuna/answer-me-with-html/answer-me-with-html) | skill 배포 경로 |

## Adjacent Documentation

- [Mermaid introduction](https://mermaid.js.org/intro/) — Markdown-inspired diagram authoring의 기준점
- [Mermaid usage](https://mermaid.js.org/config/usage) — docs/site embedding 시의 설정
- [Quarto text-editor workflow](https://quarto.org/docs/get-started/hello/text-editor.html) — executable publishing workflow 비교
- [Marp GitHub repository](https://github.com/marp-team/marp) — Markdown presentation 대안

## Reading Order

1. README로 output과 기본 command를 파악한다.
2. SKILL.md로 agent가 생성해야 할 Markdown contract를 읽는다.
3. `am help` 및 CLI source로 실제 설치 버전의 syntax를 확인한다.
4. benchmark는 결론이 아니라 가설로 보고, 동일한 task set에서 직접 측정한다.

## Source Hygiene

- versioned tool의 command와 option은 노트 작성 시점이 아니라 실행 시점의 `am help`로 재확인한다.
- benchmark 수치는 provider/프로젝트 자기 보고와 독립 평가를 구분해 인용한다.
- HTML artifact의 주장·수치·인용은 renderer가 검증하지 않으므로 source draft 단계에서 검증한다.
