---
date: 2026-08-12
tags: [tech]
type: tech-tool-study
status: draft
---

# Diagram Design — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차로 돌아가기]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 우선 읽을 자료

1. [README](https://github.com/cathrynlavery/diagram-design/blob/main/README.md) — 정체, 지원 type, 설치 방향, architecture
2. [SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/SKILL.md) — 실제 agent workflow와 quality contract
3. [Style guide](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/style-guide.md) — semantic token과 typography의 source of truth
4. [Onboarding spec](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/onboarding.md) — website-to-brand mapping과 first-use gate
5. [Commit history](https://github.com/cathrynlavery/diagram-design/commits/main/) — 빠르게 변하는 기능과 문서 불일치 확인

## Repository 탐색 지도

| 경로 | 확인할 내용 |
|---|---|
| `skills/diagram-design/SKILL.md` | type selection, connector rule, pre-output checklist |
| `skills/diagram-design/references/type-*.md` | 선택한 diagram의 semantic/layout 규칙 |
| `skills/diagram-design/references/style-guide.md` | token, font, spacing, visual constraints |
| `skills/diagram-design/references/onboarding.md` | website signal을 token으로 mapping하는 절차 |
| `skills/diagram-design/assets/template*.html` | HTML + inline SVG scaffold |
| `skills/diagram-design/assets/example-*.html` | type/variant별 실제 구조 |
| `skills/diagram-design/scripts/*_extract.py` | Mermaid·draw.io bounded parser |
| `.codex-plugin/`, `.claude-plugin/` | agent integration metadata |

## 도입 전 검증표

| 항목 | 이유 | 확인 위치 |
|---|---|---|
| type 수와 파일 목록 | 설명 29, README 27 불일치 | repository tree와 README |
| 설치 방식 | agent별 discovery 방식 차이 | README와 plugin metadata |
| pinning 대상 SHA | versioned release 부재 | commit history |
| security update 방식 | 최신 `main`만 지원 | Security Policy |
| license | 재배포·수정 조건 | LICENSE |
| font/network dependency | offline 및 brand rendering 영향 | style guide, onboarding |
| accessibility output | SVG마다 고유 label 필요 | SKILL.md와 생성 결과 |

## 상태 자료

- [Repository](https://github.com/cathrynlavery/diagram-design)
- [Commit history](https://github.com/cathrynlavery/diagram-design/commits/main/)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)
- [MIT License](https://github.com/cathrynlavery/diagram-design/blob/main/LICENSE)

> [!note] 조사 기준
> 이 노트의 숫자와 기능 상태는 2026-08-12 dossier를 기준으로 한다. 저장소 설명, README, gallery, reference tree가 서로 다른 시점에 갱신될 수 있으므로 숫자 자체보다 pin한 commit의 실제 파일을 신뢰한다.

## Sources

- [GitHub repository](https://github.com/cathrynlavery/diagram-design)
- [README — Architecture](https://github.com/cathrynlavery/diagram-design/blob/main/README.md#architecture)
- [Onboarding spec](https://github.com/cathrynlavery/diagram-design/blob/main/skills/diagram-design/references/onboarding.md)
- [Security Policy](https://github.com/cathrynlavery/diagram-design/blob/main/SECURITY.md)

