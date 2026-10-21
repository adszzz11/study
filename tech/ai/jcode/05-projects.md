---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 프로젝트 아이디어

> [[README|목차로 돌아가기]] | [[cheatsheet|다음: 치트시트]]

## 1. Parallel Bug Triage

issue별로 reproduce, root-cause analysis, patch candidate, regression test agent를 분리한다. coordinator session은 evidence와 diff를 모아 conflict 없는 patch만 통합한다.

**완료 기준**: 재현 절차, 원인 근거, 최소 patch, regression test 결과, 미해결 risk가 issue마다 남는다.

## 2. Large Migration

package/module 단위로 agent를 나누고 typecheck·unit test 결과를 todo에 연결한다. 공용 파일 충돌이 예상되면 worktree로 격리하고 integration agent가 merge 순서와 full test를 책임진다.

## 3. Nightly Code-health Bot

SDK headless session으로 lint/test failure, dependency update 영향, flaky test를 조사해 PR 초안을 만든다. write/PR 생성은 approval 단계 뒤에만 수행하며 API key와 source code가 event log에 노출되지 않게 한다.

## 4. Remote Build Host

Linux build server에서 `jcode serve`를 유지하고 laptop은 SSH socket forwarding으로 연결한다. 무거운 build cache와 daemon session은 server에 남기되, server 계정 권한·network egress·secret 접근을 최소화한다.

## 5. Internal Developer Portal

SDK event stream을 dashboard에 연결해 session 상태, tool call, approval request, token usage를 표시한다. 사용자에게 raw prompt/secret을 노출하지 않도록 redaction, role-based access, audit retention을 함께 설계한다.

## Sources

- https://jcode.sh/docs
- https://jcode.sh/sdk
- https://jcode.sh/enterprise
