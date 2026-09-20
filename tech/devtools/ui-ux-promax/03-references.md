---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# UI UX Pro Max — References

[[tech/devtools/ui-ux-promax/README|학습 진입점]]

## Official sources

1. [Official GitHub repository / README](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — 설치 방법, 사용 흐름, 프로젝트 개요.
2. [Latest releases](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases) — 도입 전 실제 최신 version과 release note 확인.
3. [Architecture and sync model](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/CLAUDE.md) — `src/ui-ux-pro-max/{data,scripts,templates}`를 source-of-truth로 보는 구조.
4. [Search CLI](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/search.py) — 검색 domain, argument, stack 지원 범위 확인.
5. [Search core](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/src/ui-ux-pro-max/scripts/core.py) — BM25·regex hybrid, reliability 구현 확인.
6. [CLI package](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/cli) — Node.js package 구성 확인.
7. [MIT License](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE) — 재사용 조건 확인.
8. [Issue #362](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/362) — 과거 CLI packaging 문제와 설치 후 검증 필요성.

## Source-of-truth와 검증

repository의 `src/ui-ux-pro-max/{data,scripts,templates}`가 공식 data·script·template의 기준이다. CLI asset과 assistant별 skill file은 동기화 검증 대상이므로, 설치 명령의 성공 메시지만으로 준비 완료를 판단하지 않는다.

```bash
find .agents/skills/ui-ux-pro-max -maxdepth 3 -type f | sort
python3 .agents/skills/ui-ux-pro-max/scripts/search.py --help
```

Issue #362는 특정 과거 bundle이 orchestrator skill만 설치하는 재현 사례다. 현재 version에서도 필요한 sub-skill, script, data가 실제 생성됐는지 검사한다. 이는 issue를 현재 결함으로 단정하는 것이 아니라 안전한 설치 acceptance check다.

## Sources

- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/362
