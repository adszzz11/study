---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude-Mem References

> [[02-ecosystem|이전: Ecosystem]] | [[README|목차]] | [[04-learning/01-getting-started|다음: Getting Started]]

## Primary Sources

| 자료 | URL | 읽을 포인트 |
|---|---|---|
| Repository README | https://github.com/thedotmack/claude-mem | project positioning, host 지원, 설치 진입점 |
| `package.json` | https://github.com/thedotmack/claude-mem/blob/main/package.json | manifest version, scripts, dependency |
| Releases | https://github.com/thedotmack/claude-mem/releases | 배포된 release와 changelog |
| Installation | https://github.com/thedotmack/claude-mem/blob/main/docs/public/installation.mdx | installer, requirement, verification |
| Configuration | https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx | provider, model, port, context settings |
| Security Policy | https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md | 지원 version과 vulnerability reporting |
| Issues | https://github.com/thedotmack/claude-mem/issues | 현재 failure mode와 regression 징후 |
| Claude Code memory | https://code.claude.com/docs/en/memory | built-in auto memory와 `CLAUDE.md` 비교 기준 |

## Architecture Sources

| 자료 | URL | 질문 |
|---|---|---|
| Hook architecture | https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/hooks.mdx | 어느 event에서 무엇을 capture하는가? |
| Worker service | https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/worker-service.mdx | queue, API, viewer, lifecycle은 어떻게 연결되는가? |
| Database | https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/database.mdx | source of truth와 relation은 무엇인가? |
| Search architecture | https://github.com/thedotmack/claude-mem/blob/main/docs/public/architecture/search-architecture.mdx | FTS5와 Chroma의 fallback은 어떻게 동작하는가? |
| Memory Search | https://github.com/thedotmack/claude-mem/blob/main/docs/public/usage/search-tools.mdx | `search → timeline → details` 흐름은 무엇인가? |

## Reading Order

1. README에서 해결하려는 문제와 설치 경로를 파악한다.
2. Hook architecture와 Worker service를 읽어 capture path를 그린다.
3. Database와 Search architecture에서 저장·검색 fallback을 확인한다.
4. Configuration에서 provider별 data flow와 기본 network bind를 검토한다.
5. Security Policy와 Issues에서 운영 위험을 확인한다.
6. `package.json`과 Releases를 대조해 실제로 설치할 version을 결정한다.

## Source Evaluation Notes

- 조사 기준일: **2026-09-20**
- `main` manifest v13.25.2와 Releases 최신 노출 v13.24.23 사이에 시차가 있다.
- “약 10x token savings”는 project 문서의 estimate이며 독립 benchmark가 아니다.
- 기능 설명과 security claim은 공식 문서 기준이다. 실제 배포 전에는 설치할 exact version의 source/config를 다시 확인한다.
- 현재 license는 `Apache-2.0`으로 확인하되, 불완전한 과거 자료를 근거로 license history를 단정하지 않는다.

## Sources

- https://github.com/thedotmack/claude-mem
- https://github.com/thedotmack/claude-mem/blob/main/package.json
- https://github.com/thedotmack/claude-mem/releases
- https://github.com/thedotmack/claude-mem/issues
- https://github.com/thedotmack/claude-mem/blob/main/SECURITY.md
- https://code.claude.com/docs/en/memory
