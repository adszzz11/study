---
date: 2026-10-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Vercel eve — References

> [[README|목차로 돌아가기]]

## Official

1. [Introducing eve — Vercel, 2026-06-17](https://vercel.com/blog/introducing-eve) — 공개 배경과 filesystem-first 모델
2. [eve official site](https://eve.dev/) — feature overview와 integration 범위
3. [vercel/eve repository](https://github.com/vercel/eve) — source, examples, issue 및 version 확인
4. [Execution model and durability](https://github.com/vercel/eve/blob/main/docs/concepts/execution-model-and-durability.mdx) — checkpoint, resume, sandbox trust boundary
5. [Deploy to Vercel](https://github.com/vercel/eve/blob/main/docs/guides/deployment/vercel.mdx) — managed deployment path
6. [Self-hosting](https://github.com/vercel/eve/blob/main/docs/guides/deployment/self-hosting.md) — Postgres durability와 Docker sandbox 구성
7. [How to use eve subagents](https://vercel.com/kb/guide/how-to-use-eve-subagents) — skill과 subagent의 역할 분리
8. [eve releases](https://github.com/vercel/eve/releases) — breaking change 및 release cadence 확인
9. [Vercel platform](https://vercel.com/platform) — agentic platform positioning

## Reading Order

발표 글로 문제와 product model을 파악한 뒤 execution model을 읽는다. 다음으로 subagent guide와 배포 문서를 보고, 실제 도입 직전에는 repository release history와 pinned version의 문서를 다시 확인한다.
