---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# ECC harness — Cheatsheet

## 설치 전

```bash
# Node.js 18+ 확인
node --version

# npm 배포 version 확인 (Releases와 반드시 대조)
npm view ecc-universal version

# Codex 대상 설치 계획만 확인
npx ecc-universal install --guided --harness codex --dry-run
```

| 확인 | 기준 |
|---|---|
| Version | GitHub Releases tag + npm registry를 대조한다. |
| Install path | plugin, guided installer, manual copy 중 **하나만** 사용한다. |
| Components | `rules/common` + 현재 stack pack 하나 + skill 하나부터 시작한다. |
| Hooks / MCP | command, permission, data flow, 제거 방법을 검토한다. |

## 권장 최소 workflow

```text
plan → test → implement → review → verify → handoff / remember
```

- test와 verification evidence를 분리해 남긴다.
- 새 session에서 handoff/search가 재작업을 줄였는지 측정한다.
- adapter support는 harness별 release 문서로 확인한다.

## Security baseline

```bash
# 결과를 검토할 JSON으로 출력
npx -y ecc-agentshield scan --path . --format json
```

- 검사 범위: instructions, permissions, hooks, MCP config, secrets
- CI: JSON/SARIF + baseline drift gate를 고려한다.
- 원칙: scanner finding은 보조 신호다. config/permission diff는 사람이 검토한다.

## 피해야 할 것

- 전체 catalog를 처음부터 전부 로드하기
- 여러 설치 경로를 중첩하기
- `CHANGELOG.md`의 main branch 항목을 이미 배포된 version으로 가정하기
- memory/hook에 민감 데이터가 남는지 확인하지 않기
- scan 통과만으로 안전하다고 결론내리기

## 빠른 링크

- [[README|스터디 시작]] · [[01-overview|Overview]] · [[04-learning/01-getting-started|Getting started]]
- https://github.com/affaan-m/ECC
- https://github.com/affaan-m/ECC/releases
- https://www.npmjs.com/package/ecc-universal
- https://github.com/affaan-m/agentshield
